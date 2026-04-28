
Place your architecture diagram (even a simple hand‑drawn photo) in `docs/architecture.png` and the GSMA test screenshot in `docs/gsma-test.png`. Update the README accordingly.

---

## 5. 📄 Final Continuation Markdown

Save this as `MOYO_PROJECT.md` for your next session. It includes all progress and the remaining tasks.

```markdown
# Moyo Token – Africa Ignite Hackathon Prototype

## Status (27 April)
- ✅ Backend stable: mock APIs, mock blockchain, secret‑word recovery.
- ✅ Frontend fully functional with recovery UI.
- ✅ Mentor meeting confirmed: **5 May, 10:00 AM GMT**, Zoom sent.
- ✅ All test flows verified.
- ⬜ Record demo video.
- ⬜ Test GSMA Open Gateway sandbox and capture screenshot.
- ⬜ Update README with video link, GSMA test, and architecture.
- ⬜ Practice pitch.

## How to Run
```powershell
# Backend (project root)
cd "C:\Users\Waldis\Desktop\project mdfiles\africa\moyo-token-prototype"
uvicorn backend.main:app --reload

# Frontend (inside frontend folder)
cd frontend
python -m http.server 5500