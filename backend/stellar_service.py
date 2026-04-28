import os
from dotenv import load_dotenv
import uuid

load_dotenv()

# Try to import real Stellar SDK, but fallback to mock if something fails
try:
    from stellar_sdk import Server, Keypair, TransactionBuilder, Network
    STELLAR_AVAILABLE = True
except ImportError:
    STELLAR_AVAILABLE = False

# Use environment variable or hardcode for demo
MOCK_BLOCKCHAIN = os.getenv("MOCK_BLOCKCHAIN", "True").lower() == "true"
# Hardcoded keys only used if STELLAR_AVAILABLE and not MOCK_BLOCKCHAIN
STELLAR_SECRET_SEED = "SB34UXQCWK7HK5LGY75A5OS723V6BXH3CK2QQSXT4IGXZDND44JZJA5"
BENEFICIARY_PUBLIC_KEY = "GANYZROMOADGGAVF5JN4HZAHDWZWO25GVCNL66LGIL6UE6TG7DJL3A"

def submit_voucher_issuance(user_phone: str, amount: str = "1") -> str:
    """Return a transaction hash. Uses real Stellar if available, else mock."""
    
    if MOCK_BLOCKCHAIN or not STELLAR_AVAILABLE:
        # Generate a realistic-looking mock transaction hash
        mock_hash = f"mock-{uuid.uuid4().hex[:40]}"
        print(f"[MOCK] Claim for {user_phone}: {mock_hash}")
        return mock_hash

    # Real Stellar transaction (only if not mocking and SDK works)
    server = Server(horizon_url="https://horizon-testnet.stellar.org")
    issuer_kp = Keypair.from_secret(STELLAR_SECRET_SEED)
    source_account = server.load_account(issuer_kp.public_key)
    base_fee = server.fetch_base_fee()

    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .append_payment_op(
            destination=BENEFICIARY_PUBLIC_KEY,
            asset_code="XLM",
            asset_issuer=None,
            amount=amount,
        )
        .add_text_memo(f"Moyo UBI for {user_phone}")
        .set_timeout(30)
        .build()
    )
    transaction.sign(issuer_kp)
    response = server.submit_transaction(transaction)
    return response["hash"]