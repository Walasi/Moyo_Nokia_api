# backend/user_store.py
# Hardcoded demo user database (in production, use a real DB)
users = {
    "+233500000001": {
        "secret_word": "moyo123",
        "registered_location": "Accra"
    },
    "+233500000002": {
        "secret_word": "moyo123",
        "registered_location": "Kumasi"
    },
    "+233500000003": {
        "secret_word": "moyo123",
        "registered_location": "Accra"
    }
}

def verify_secret_word(phone_number: str, secret_word: str) -> bool:
    user = users.get(phone_number)
    if not user:
        return False
    return user["secret_word"] == secret_word