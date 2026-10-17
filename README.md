# HumanShield

A behavioral cybersecurity training platform. Instead of just asking
"is this a scam?", HumanShield puts you inside realistic social
engineering scenarios, tracks *how* you actually respond under
pressure, and adapts future tests to your weak spots.

Core loop: **STOP → THINK → VERIFY → ACT**

## What it does

- **27 scripted scenarios across 9 categories:** Education, Finance,
  Work, Economy, Social Media, Shopping & E-commerce, Personal &
  Relationships, Government & Public Services, and Gaming &
  Entertainment
- **Three difficulty tiers per category.** The tier you get next
  depends on your last score in that category: below 50 stays at the
  lowest tier, 50+ moves to Intermediate, 75+ to Advanced, and 90+
  unlocks Expert
- **Adaptive attacker (Expert tier):** a branching phone-call
  simulation where the caller changes tactics based on your first
  reaction. Show alarm and they escalate urgency. Show skepticism and
  they pivot to false authority
- **Voice mode:** phone-call scenarios can be played aloud using the
  browser's built-in text-to-speech
- **Seven tracked skills:** Verification, Credential Protection,
  Manipulation Detection, Pressure Resistance, Red-Flag Recognition,
  Safe Decision-Making, and Reasoning
- **Behavioral profile:** per-skill percentages built from your real
  answers over time
- **Recommendation engine:** after every test, it names your weakest
  skill and gives concrete advice
- **Test history:** every completed session, saved to a local
  database

## Tech stack

| Layer     | Technology                     |
|-----------|---------------------------------|
| Frontend  | HTML, CSS, vanilla JavaScript  |
| Backend   | Python + Flask                 |
| Database  | SQLite                         |

No frontend frameworks or build tools required.

## Project structure

```
HumanShield/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/
│   ├── app.py            (API routes)
│   ├── scenarios.py      (all scenario content + difficulty logic)
│   ├── database.py       (SQLite setup)
│   └── requirements.txt
├── database/
│   └── humanshield.db    (created automatically, not tracked in git)
├── .gitignore
└── README.md
```

## Running it locally

**1. Backend**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

This starts the API at `http://127.0.0.1:5000` and creates the SQLite
database automatically on first run.

**2. Frontend**

With the backend still running, open `frontend/index.html` in a
browser (or use VS Code's Live Server extension).

## Safety and privacy

All scenarios are fictional training simulations. No real
organizations are impersonated beyond generic references, and the app
never asks for or stores real passwords, OTPs, banking details, or
other sensitive information. Everything you enter is a button choice.

## Roadmap

- [x] Dashboard and navigation
- [x] Nine training categories
- [x] Text-based tests with real scoring
- [x] SQLite persistence
- [x] Behavioral skill profile
- [x] Personalized recommendations
- [x] Adaptive difficulty across all categories
- [x] Voice mode (spoken scenarios)
- [x] Adaptive simulated attacker (scripted branching)
- [ ] Spoken responses (speech recognition)
- [ ] AI-powered attacker
- [ ] Deployment