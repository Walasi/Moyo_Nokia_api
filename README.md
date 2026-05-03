Problem

**Ghost beneficiaries** in government payrolls and aid programs cost African nations billions each year. Without a verified identity anchor, the same person can be registered multiple times and collect payments under different names. In West Africa, the ECOWAS ID card provides a ready‑made biometric identity base that is underutilised in payment systems.

Solution
- **ECOWAS ID → SIM linkage:** During onboarding, the user's national ID number is bound to their phone number via Nokia’s Number Verification, creating a trusted digital identity.
- **One ID, one claim:** Before each disbursement, the backend checks whether that ID has already received a payment in the current cycle. If yes, the transaction is blocked—making double‑dipping impossible.

How it works
1. **Onboarding:** User provides ECOWAS ID number + phone number. Nokia Number Verification confirms the SIM belongs to that device. The ID‑SIM pair is stored.
2. **Monthly Claim:** SIM Swap check → Location Verification → Duplicate claim check → Blockchain payment.
3. **Recovery:** If SIM is swapped legitimately, secret word verification restores access without losing the ID linkage.

## User Stories

### Abena – A Smooth Claim
Abena, a trader in Accra, has never changed her SIM card. Each month, she enters her phone number (`+233500000001`) and confirms her location. The Nokia APIs instantly verify her identity and location. Within seconds, a Moyo Token is issued to her digital wallet. No OTP, no delay, no fear.

**Result:** ✅ Claim approved, token sent.

---

### Grandma Efua – SIM Swap Recovery
Efua’s son in the city recently helped her replace an old SIM. When she tries to claim her monthly stipend from her village, Moyo Token detects the recent SIM change and blocks the transaction—protecting her funds from a potential SIM swap fraud. But Efua knows her secret word. She taps **“Recover My Account”**, enters her secret `moyo123`, and the system instantly verifies her identity. The block is lifted, and her claim is auto-approved.(`+233500000002`)

**Result:** ❌ Blocked → Recovery with secret word → ✅ Approved.

---

### Kwame – Location Mismatch Block
A thief steals Kwame’s phone and attempts to claim money from a different city. Moyo Token checks the network location and sees it doesn’t match Kwame’s registered home area (`+233500000003` → Accra vs. actual Kumasi). The transaction is frozen, and Kwame’s funds remain safe.

**Result:** ❌ Location mismatch. Transaction blocked.

Video URL: https://www.youtube.com/watch?v=0iM8c0x-Y5g
