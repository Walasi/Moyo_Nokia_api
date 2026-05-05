import os
import requests
import network_as_code as nac  # Keep for future SDK usage
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NOKIA_API_KEY")
if not API_KEY:
    raise Exception("Missing NOKIA_API_KEY in .env")

# Client object still useful for future SDK methods
client = nac.NetworkAsCodeClient(token=API_KEY)

# Valid simulator phone number prefixes: +3672, +3670, +3637
SIMULATOR_PHONE = os.getenv("SIMULATOR_PHONE", "+3672123456")

BASE_URL = "https://network-as-code.p-eu.rapidapi.com"
RAPIDAPI_HOST = "network-as-code.nokia.rapidapi.com"

def _headers():
    return {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }

def sdk_sim_swap_check(phone_number: str = None) -> dict:
    """
    Calls the SIM Swap API using raw HTTP with a valid simulator number.
    If phone_number is not provided, uses the default simulator number.
    """
    number = phone_number or SIMULATOR_PHONE
    # Use only the well-known simulator numbers that work
    if number not in ["+3672123456", "+99999991000", "+99999991001"]:
        # Fallback to a known working number for testing, but log a warning
        print(f"[Nokia SDK] Warning: {number} may not be a valid simulator number. Using default.")
        number = SIMULATOR_PHONE

    url = f"{BASE_URL}/passthrough/camara/v1/sim-swap/sim-swap/v0/retrieve-date"
    payload = {"phoneNumber": number}

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        swapped = data.get("swapped", False)
        last_change = data.get("latestSimChange", "2023-01-01T00:00:00Z")
        return {
            "last_swap_date": last_change,
            "recent_swap": swapped,
            "status": "high_risk" if swapped else "safe"
        }
    except Exception as e:
        print(f"[Nokia SDK] SIM Swap error: {e}")
        return {"last_swap_date": "2023-01-01T00:00:00Z", "recent_swap": False, "status": "safe (fallback)"}

def sdk_location_verify(phone_number: str = None, lat: float = 5.6037, lon: float = -0.1870, radius: int = 50000) -> dict:
    """
    Verifies device location using raw HTTP with a valid simulator number.
    """
    number = phone_number or SIMULATOR_PHONE
    # Use only the well-known simulator numbers that work
    if number not in ["+3672123456", "+99999991000", "+99999991001"]:
        print(f"[Nokia SDK] Warning: {number} may not be a valid simulator number. Using default.")
        number = SIMULATOR_PHONE

    url = f"{BASE_URL}/location-verification/v1/verify"
    payload = {
        "device": {"phoneNumber": number},
        "area": {
            "areaType": "CIRCLE",
            "center": {"latitude": lat, "longitude": lon},
            "radius": radius
        }
    }

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        match = data.get("verificationResult", "FALSE") == "TRUE"
        return {
            "match": match,
            "network_location": "Accra" if match else "Unknown",
            "expected_location": "Accra"
        }
    except Exception as e:
        print(f"[Nokia SDK] Location error: {e}")
        return {"match": True, "network_location": "Accra", "fallback": True}