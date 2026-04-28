# backend/mock_nokia.py
from datetime import datetime, timedelta, timezone

recovered_numbers = set()

def mock_sim_swap_check(phone_number: str):
    """
    Returns sim swap data. Use specific phone numbers to simulate recent swap.
    """
     # For demo: +233500000001 is "safe", +233500000002 is "recent swap"
    if phone_number in recovered_numbers:
        # Bypass swap check for recovered users
        return {
            "last_swap_date": "2023-01-01T00:00:00Z",
            "recent_swap": False,
            "status": "safe"
        }
    if phone_number == "+233500000002":
        recent_swap_date = datetime.now(timezone.utc) - timedelta(days=1)
        return {
            "last_swap_date": recent_swap_date.isoformat(),
            "recent_swap": True,
            "status": "high_risk"
        }
    else:
        old_swap_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        return {
            "last_swap_date": old_swap_date.isoformat(),
            "recent_swap": False,
            "status": "safe"
        }

def mock_location_verify(phone_number: str, expected_location: str):
    """
    Compares expected location with mock network location.
    """
    # For demo: +233500000003 fails location
    if phone_number == "+233500000003":
        return {
            "match": False,
            "network_location": "Kumasi",
            "expected_location": expected_location
        }
    else:
        return {
            "match": True,
            "network_location": expected_location,  # assume match
            "expected_location": expected_location
        }

def mock_number_verify(phone_number: str):
    """All numbers pass verification for now."""
    return {"verified": True, "phone_number": phone_number}