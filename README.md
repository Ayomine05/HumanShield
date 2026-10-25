# HumanShield

A behavioral cybersecurity training platform. Instead of just asking
"is this a scam?", HumanShield puts you inside realistic social
engineering scenarios, tracks *how* you actually respond under
pressure, and adapts future tests to your weak spots.

Core loop: **STOP → THINK → VERIFY → ACT**

**Live demo:** https://human-shield-vert.vercel.app

The demo uses temporary storage, so progress can reset between visits.

## What it does

- **27 scripted scenarios across 9 categories:** Education, Finance,
  Work, Economy, Social Media, Shopping & E-commerce, Personal &
  Relationships, Government & Public Services, and Gaming &
  Entertainment
- **Adaptive difficulty:** each category has three tiers. The next
  test you get depends on your last score there, and 90%+ unlocks an
  Expert-tier adaptive attacker
- **Adaptive attacker:** a branching phone-call simulation where the
  caller changes tactics based on your first reaction. Show alarm and
  they escalate urgency. Show skepticism and they pivot to false
  authority
- **Voice mode:** phone-call scenarios can be played aloud using the
  browser's built-in text-to-speech
- **Seven tracked skills:** Verification, Credential Protection,
  Manipulation Detection, Pressure Resistance, Red-Flag Recognition,
  Safe Decision-Making, and Reasoning
- **Behavioral profile:** per-skill percentages built from your real
  answers over time
- **Recommendation engine:** after every test, it names your weakest
  skill and gives concrete advice
- **Test history:** every completed session is recorded

## Tech stack

| Layer      | Technology                              |
|------------|------------------------------------------|
| Frontend   | HTML, CSS, vanilla JavaScript            |
| Backend    | Python + Flask                           |
| Database   | SQLite                                   |
| Hosting    | Vercel                                   |

No frontend frameworks or build tools required.

## Project structure

```
HumanShield/
├── public/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/
│   ├── app.py            (API routes, serves the frontend)
│   ├── scenarios.py      (all scenario content + difficulty logic)
│   ├── database.py       (SQLite setup)
│   └── requirements.txt
├── database/
│   └── humanshield.db    (created automatically, not tracked in git)
├── pyproject.toml        (tells Vercel where the app lives)
├── .gitignore
└── README.md
```

## Running it locally

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser. Flask serves both
the page and the API, so there is nothing else to start. The database
is created automatically on first run.

## Deployment

The app is deployed on Vercel as a single Flask project:

- Root Directory: the repository root
- Application Preset: Flask
- `pyproject.toml` points Vercel at `backend.app:app`
- Static files are served from `public/`

Vercel's filesystem is read-only except for a temporary folder, so on
that host the app automatically keeps its database in temporary
storage. To use a persistent location on another host, set the
`DATABASE_PATH` environment variable.

## Safety and privacy

All scenarios are fictional training simulations. No real
organizations are impersonated beyond generic references, and the app
never asks for or stores real passwords, OTPs, banking details, or
other sensitive information. Everything you enter is a button choice.

## Roadmap

- [x] Dashboard and navigation
- [x] Nine training categories, 27 scenarios
- [x] Scoring, behavioral skill profile, and recommendations
- [x] Adaptive difficulty and adaptive attacker
- [x] Voice mode (spoken scenarios)
- [x] Public demo deployment
- [ ] User accounts and a persistent hosted database
- [ ] Server-side grading of answers
- [ ] Privacy policy and terms
- [ ] Spoken responses (speech recognition)
- [ ] AI-powered attacker