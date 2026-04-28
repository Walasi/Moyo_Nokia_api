# backend/decision_engine.py
from backend.mock_nokia import mock_sim_swap_check, mock_location_verify, mock_number_verify

def evaluate_claim(phone_number: str, registered_location: str) -> dict:
    """
    Returns a decision dict: 
    {
        "approved": bool,
        "reason": str,
        "checks": {
            "sim_swap": {...},
            "location": {...},
            "number_verify": {...}
        }
    }
    """
    checks = {}

    # 1. Number verification
    num_check = mock_number_verify(phone_number)
    checks["number_verify"] = num_check
    if not num_check["verified"]:
        return {"approved": False, "reason": "Number verification failed", "checks": checks}

    # 2. SIM Swap check
    sim_check = mock_sim_swap_check(phone_number)
    checks["sim_swap"] = sim_check
    if sim_check["recent_swap"]:
        return {"approved": False, "reason": "SIM recently swapped. Transaction blocked.", "checks": checks}

    # 3. Location verification
    loc_check = mock_location_verify(phone_number, registered_location)
    checks["location"] = loc_check
    if not loc_check["match"]:
        return {"approved": False, "reason": "Location mismatch. Verification failed.", "checks": checks}

    # All passed
    return {"approved": True, "reason": "All checks passed", "checks": checks}