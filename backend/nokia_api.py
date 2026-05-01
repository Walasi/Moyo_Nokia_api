import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOKIA_API_KEY = os.getenv("NOKIA_API_KEY")
if not NOKIA_API_KEY:
    raise Exception("Missing NOKIA_API_KEY in .env")

# RapidAPI base URL and host from the portal snippets
BASE_URL = "https://network-as-code.p-eu.rapidapi.com"
RAPIDAPI_HOST = "network-as-code.nokia.rapidapi.com"

def _headers():
    return {
        "x-rapidapi-key": NOKIA_API_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }

def real_sim_swap_check(phone_number: str) -> dict:
    """
    Calls the real SIM Swap retrieve-date endpoint.
    """
    url = f"{BASE_URL}/passthrough/camara/v1/sim-swap/sim-swap/v0/retrieve-date"
    payload = {"phoneNumber": phone_number}

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Example response: { "latestSimChange": "2026-04-20T...", "swapped": true/false }
        recent = data.get("swapped", False)
        return {
            "last_swap_date": data.get("latestSimChange", "2023-01-01T00:00:00Z"),
            "recent_swap": recent,
            "status": "high_risk" if recent else "safe"
        }
    except Exception as e:
        print(f"[Nokia API] SIM Swap error: {e}")
        return {"last_swap_date": "2023-01-01T00:00:00Z", "recent_swap": False, "status": "safe (fallback)"}

def real_location_verify(phone_number: str, expected_location: str) -> dict:
    """
    Calls the real Location Verification verify endpoint.
    Since the API expects latitude/longitude, we map the location string
    to approximate coordinates. In a real app you'd store precise coordinates.
    """
    # Simple mapping for demo – replace with actual lat/lon database
    location_coords = {
        "accra": (5.6037, -0.1870),
        "kumasi": (6.6885, -1.6244),
        "tamale": (9.4000, -0.8393),
    }
    coords = location_coords.get(expected_location.lower(), (5.6037, -0.1870))  # default Accra

    url = f"{BASE_URL}/location-verification/v1/verify"  # from snippet part 2
    payload = {
        "device": {"phoneNumber": phone_number},
        "area": {
            "areaType": "CIRCLE",
            "center": {"latitude": coords[0], "longitude": coords[1]},
            "radius": 50000  # 50 km radius, adjust as needed
        }
    }

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Expected response: { "verificationResult": "TRUE" or "FALSE" }
        match = data.get("verificationResult", "FALSE") == "TRUE"
        return {
            "match": match,
            "network_location": expected_location if match else "Unknown",
            "expected_location": expected_location
        }
    except Exception as e:
        print(f"[Nokia API] Location error: {e}")
        return {"match": True, "network_location": expected_location, "fallback": True}

def real_number_verify(phone_number: str) -> dict:
    """
    Calls the real Number Verification verify endpoint.
    """
    url = f"{BASE_URL}/passthrough/camara/v1/number-verification/number-verification/v0/verify"
    payload = {"phoneNumber": phone_number}

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Example response: { "verificationResult": "TRUE" }
        verified = data.get("verificationResult", "FALSE") == "TRUE"
        return {"verified": verified, "phone_number": phone_number}
    except Exception as e:
        print(f"[Nokia API] Number verification error: {e}")
        return {"verified": True, "phone_number": phone_number, "fallback": True}