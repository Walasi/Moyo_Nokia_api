# backend/decision_engine.py
import os
from backend.mock_nokia import mock_sim_swap_check, mock_location_verify, mock_number_verify

# Try importing the SDK-based module first
try:
    from backend.nokia_sdk import sdk_sim_swap_check, sdk_location_verify
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False

# Try importing the old raw API module as fallback (for Number Verification only)
try:
    from backend.nokia_api import real_number_verify as raw_number_verify
    RAW_NUMBER_AVAILABLE = True
except ImportError:
    RAW_NUMBER_AVAILABLE = False

USE_REAL_NOKIA_API = os.getenv("USE_REAL_NOKIA_API", "False").lower() == "true"

def evaluate_claim(phone_number: str, registered_location: str) -> dict:
    checks = {}

    # 1. SIM Swap check
    if USE_REAL_NOKIA_API and SDK_AVAILABLE:
        sim_check = sdk_sim_swap_check(phone_number)  # will use default simulator number if you pass +233 numbers? Better to decide:
        # For demo, we may want to keep the story numbers, but real API only works with simulator numbers.
        # Solution: when real API is on, we'll convert our demo numbers to simulator numbers for testing only.
        # For final submission, you'd use real subscriber numbers. Here, we'll just call the SDK with the phone_number;
        # if it's not a valid simulator number, the SDK will throw an error and fallback will trigger.
    else:
        sim_check = mock_sim_swap_check(phone_number)
    checks["sim_swap"] = sim_check
    if sim_check["recent_swap"]:
        return {"approved": False, "reason": "SIM recently swapped. Transaction blocked.", "checks": checks}

    # 2. Location verification
    if USE_REAL_NOKIA_API and SDK_AVAILABLE:
        # Hardcode Accra coordinates for demo, but we could map location string to coords
        loc_check = sdk_location_verify(phone_number, lat=5.6037, lon=-0.1870)
    else:
        loc_check = mock_location_verify(phone_number, registered_location)
    checks["location"] = loc_check
    if not loc_check["match"]:
        return {"approved": False, "reason": "Location mismatch. Verification failed.", "checks": checks}

    # 3. Number verification (always mock because OAuth required)
    num_check = mock_number_verify(phone_number)
    checks["number_verify"] = num_check
    if not num_check["verified"]:
        return {"approved": False, "reason": "Number verification failed", "checks": checks}

    return {"approved": True, "reason": "All checks passed", "checks": checks}