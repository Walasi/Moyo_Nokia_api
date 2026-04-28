import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from backend.decision_engine import evaluate_claim
from backend.stellar_service import submit_voucher_issuance
from backend.user_store import verify_secret_word
from backend.mock_nokia import recovered_numbers

load_dotenv()

app = FastAPI(title="Moyo Token Prototype")

# Allow frontend to call API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClaimRequest(BaseModel):
    phone_number: str
    location: str

class RecoveryRequest(BaseModel):
    phone_number: str
    secret_word: str

@app.post("/api/claim")
async def claim_token(request: ClaimRequest):
    # 1. Evaluate network checks
    decision = evaluate_claim(request.phone_number, request.location)

    if not decision["approved"]:
        return {
            "status": "blocked",
            "reason": decision["reason"],
            "checks": decision["checks"],
            "tx_id": None
        }

    # 2. Submit Stellar transaction (mock token issuance)
    try:
        tx_hash = submit_voucher_issuance(request.phone_number)
        return {
            "status": "approved",
            "reason": decision["reason"],
            "checks": decision["checks"],
            "tx_id": tx_hash
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")

@app.post("/api/recover")
async def recover_account(request: RecoveryRequest):
    if verify_secret_word(request.phone_number, request.secret_word):
        recovered_numbers.add(request.phone_number)
        return {"status": "verified", "message": "Account recovered. You may now claim your tokens."}
    else:
        raise HTTPException(status_code=403, detail="Secret word incorrect. Recovery failed.")

@app.get("/")
def root():
    return {"message": "Moyo Token API is running"}