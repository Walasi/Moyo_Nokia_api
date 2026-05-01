# backend/decision_engine.py
import os
from backend.mock_nokia import mock_sim_swap_check, mock_location_verify, mock_number_verify

# Try importing the real Nokia API module; if not available, we stay with mock
try:
    from backend.nokia_api import real_sim_swap_check
    REAL_API_AVAILABLE = True
except ImportError:
    REAL_API_AVAILABLE = False

# Set this to True to use the live Nokia API (requires valid key in .env)
USE_REAL_NOKIA_API = os.getenv("USE_REAL_NOKIA_API", "False").lower() == "true"

def evaluate_claim(phone_number: str, registered_location: str) -> dict:
    checks = {}

    # Decide whether to use real or mock functions
    if USE_REAL_NOKIA_API and REAL_API_AVAILABLE:
        from backend.nokia_api import real_sim_swap_check, real_location_verify, real_number_verify
        sim_func = real_sim_swap_check
        loc_func = real_location_verify
        num_func = real_number_verify
    else:
        sim_func = mock_sim_swap_check
        loc_func = mock_location_verify
        num_func = mock_number_verify

    # 1. Number verification
    num_check = num_func(phone_number)
    checks["number_verify"] = num_check
    if not num_check["verified"]:
        return {"approved": False, "reason": "Number verification failed", "checks": checks}

    # 2. SIM Swap check
    sim_check = sim_func(phone_number)
    checks["sim_swap"] = sim_check
    if sim_check["recent_swap"]:
        return {"approved": False, "reason": "SIM recently swapped. Transaction blocked.", "checks": checks}

    # 3. Location verification
    loc_check = loc_func(phone_number, registered_location)
    checks["location"] = loc_check
    if not loc_check["match"]:
        return {"approved": False, "reason": "Location mismatch. Verification failed.", "checks": checks}

    return {"approved": True, "reason": "All checks passed", "checks": checks}