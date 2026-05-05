# Moyo Token – Network-Verified Identity Layer for Financial Inclusion

Moyo Token prevents SIM swap fraud in humanitarian aid and UBI programs by using **Nokia's CAMARA APIs** (SIM Swap Detection, Location Verification, Number Verification) to approve transactions, combined with a transparent blockchain ledger.

## Problem
Across Sub-Saharan Africa, mobile money fraud—especially SIM swap scams—causes billions in losses. Beneficiaries of social programs often lose their monthly stipends when fraudsters intercept OTPs. 
**Real story:** A nurse in Malawi found her salary gone because a criminal swapped her SIM card. Or a government payroll that pays a 'ghost worker' three times because no one verifies identity. Moyo Token stops both. By coupling Nokia's SIM Swap and Location APIs with a blockchain ledger, we ensure every token reaches a real, verified person—once, and only once."
It’s a network‑verified identity layer for financial inclusion in Africa and worldwide.”

"Beyond individual fraud, this also solves the ghost beneficiary problem. Because the blockchain records every claim against a verified SIM, the same number can't claim twice. Governments lose billions to these phantom payments every year."

Why Ghost Payments Matter?
In many government aid and payroll systems across Africa, "ghost workers" or "ghost beneficiaries" are people who don't exist—or who exist but are registered multiple times under different names. They drain public funds meant for the vulnerable. Because Moyo Token ties each claim to a unique, verified SIM card and a registered location, and records every disbursement on an immutable blockchain, the same phone number can't claim twice in the same payment cycle. This single feature eliminates double‑dipping.


## Solution
Moyo Token acts as a **network‑aware smart contract**. Before releasing funds on the blockchain, the backend calls Nokia's network APIs to:
- Verify the SIM card hasn't been recently swapped
- Confirm the user is at their registered location
- Silently authenticate the phone number without any SMS OTP

- **ECOWAS ID → SIM linkage:** During onboarding, the user's national ID number is bound to their phone number via Nokia’s Number Verification, creating a trusted digital identity.
- **One ID, one claim:** Before each disbursement, the backend checks whether that ID has already received a payment in the current cycle. If yes, the transaction is blocked—making double‑dipping impossible.

Only if all checks pass is a token issued.


How It Works (new section, optional):

1. **Onboarding:** User provides ECOWAS ID number + phone number. Nokia Number Verification confirms the SIM belongs to that device. The ID‑SIM pair is stored.
2. **Monthly Claim:** SIM Swap check → Location Verification → Duplicate claim check → Blockchain payment.
3. **Recovery:** If SIM is swapped legitimately, secret word verification restores access without losing the ID linkage.

Government identity (ECOWAS) + network identity (Nokia) + transparent ledger (blockchain).

## User Stories

### Abena – Smooth Claim
Abena has never changed her SIM. She enters her phone number, confirms her location, and instantly receives her token.

### Grandma Efua – SIM Swap Recovery
Efua's son helped her replace an old SIM. When she tries to claim, the system detects the recent swap and blocks the transaction. But Efua knows her secret word. She recovers her account and receives her funds.

### Kwame – Location Mismatch Block
A thief steals Kwame's phone and attempts a claim from a different city. Moyo Token detects the location mismatch and freezes the transaction.

## Tech Stack
- **Backend:** Python (FastAPI)
- **APIs:** Nokia Network as Code (SIM Swap, Location, Number Verification)
- **Blockchain:** Stellar testnet (or mock for demo reliability)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** Supabase (planned)

## Demo Video
🎥 [Watch the silent 2‑minute demo](https://www.youtube.com/watch?v=0iM8c0x-Y5g)

## Real API Integration
- Subscribed to Nokia SIMULATOR plan (30 April 2026)
- Tested SIM Swap, Location Verification, Number Verification endpoints
- Integration code is ready; mock fallback ensures flawless demo

## How to Run Locally
```bash
# Backend (from project root)
cd moyo-token-prototype
uvicorn backend.main:app --reload

# Frontend (inside frontend folder)
cd frontend
python -m http.server 5500


Test Cases
Phone	        Location	Story	        Result
+233500000001	Accra	    Abena	        ✅ Approved
+233500000002	(any)	    Grandma Efua	❌ Blocked → Recover with moyo123 → ✅ Approved
+233500000003	Accra	    Kwame	        ❌ Location block
