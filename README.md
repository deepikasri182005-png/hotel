# AI Hotel Voice Assistant (Maya)

A production-grade voice assistant for hotel bookings, powered by Groq (LLM), ElevenLabs (TTS), Deepgram (STT), and Twilio (VOIP).

## 🚀 Project Structure

```text
├── app/                # Main application source code
│   ├── api/            # FastAPI routers (Voice, UI, Auth)
│   ├── core/           # Configuration and prompt settings
│   ├── db/             # MongoDB connection logic
│   ├── models/         # Pydantic/Database models
│   ├── schemas/        # API request/response schemas
│   └── services/       # Core business logic (AI, TTS, STT, Twilio)
├── data/               # Persistent data (fallback JSON storage)
├── scripts/            # Utility scripts for DB seeding and verification
├── index.html          # Web-based Monitoring Dashboard
├── run.py              # Main entry point to start the server
├── requirements.txt    # Python dependencies
└── .env                # Environment variables (API Keys)
```

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.9+
- MongoDB (Running locally on :27017 or via URI)

### 2. Setup Environment
Create a `.env` file in the root directory (refer to `.env.example` if available) with your keys:
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`
- `GROQ_API_KEY`
- `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`
- `DEEPGRAM_API_KEY`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed the Database
```bash
python scripts/seed_db.py
```

### 5. Run the Server
```bash
python run.py
```
The server will start on port `8000`. Access the dashboard at `http://localhost:8000`.

## 🖥️ Dashboard Features
- **Real-time Live Transcript**: Watch conversations as they happen.
- **Service Health Monitoring**: Track connectivity to Cloud APIs.
- **Session History**: Review previous guest interactions.
- **Phone/Web Integration**: Handles both Twilio calls and direct browser interactions.

---
**Maya** is designed to be crisp, professional, and efficient. Happy Booking!
