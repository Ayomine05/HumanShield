import os
import sys
from datetime import datetime, timezone

# Make sibling modules (database.py, scenarios.py) importable no matter how
# this file is loaded: `python app.py`, gunicorn, or a host that imports it
# as `backend.app`.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request, send_from_directory

import database
import scenarios

# Static files (the web page, CSS, JS) live in public/. Vercel serves that
# folder from its CDN; locally and on other hosts, Flask serves it itself.
FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
)

# The frontend is served by this same app, so the page and the API share
# one address and no cross-origin (CORS) setup is needed.
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

database.init_db()

SKILLS = {
    "verification": "Verification",
    "credential": "Credential protection",
    "manipulation": "Manipulation detection",
    "pressure": "Pressure resistance",
    "redflag": "Red-flag recognition",
    "decision": "Safe decision-making",
    "reasoning": "Reasoning"
}

RECOMMENDATIONS = {
    "verification": (
        "Before acting on any unexpected message, verify through a "
        "channel you already trust \u2014 the bank's app, a number on "
        "your card, or a website you typed yourself."
    ),
    "credential": (
        "Never enter passwords, OTPs, or card details through a link "
        "someone sent you. Type the official website address yourself "
        "instead."
    ),
    "manipulation": (
        "Watch for scarcity, authority, and urgency language stacked "
        "together \u2014 that combination is a strong signal of "
        "manipulation, even if the sender looks legitimate."
    ),
    "pressure": (
        "When a message pushes you to act immediately, that urgency "
        "is the attack. Slow down and give yourself time before "
        "responding."
    ),
    "redflag": (
        "Practice pausing on small inconsistencies \u2014 shortened "
        "links, slightly-off sender names, unexpected requests \u2014 "
        "rather than dismissing them."
    ),
    "decision": (
        "After identifying a suspicious message, follow through: "
        "report it and delete it, rather than just ignoring it."
    ),
    "reasoning": (
        "Before replying to anything suspicious, ask what the sender "
        "gains from your response \u2014 even a simple reply can "
        "confirm your number or account is active."
    )
}


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "storage": "temporary" if database.is_temporary() else "persistent"
    })


@app.route("/api/summary")
def summary():
    conn = database.get_connection()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    tests_completed = conn.execute("SELECT COUNT(*) FROM test_results").fetchone()[0]
    conn.close()

    scored = [c for c in categories if c["last_score"] is not None]

    if scored:
        readiness_score = round(sum(c["last_score"] for c in scored) / len(scored))
        weakest = min(scored, key=lambda c: c["last_score"])
        weak_skill = weakest["name"]
        _, next_difficulty = scenarios.pick_scenario_for_category(
            weakest["id"], weakest["last_score"]
        )
        next_test = f'{weakest["name"]} \u00b7 {next_difficulty or weakest["difficulty"]}'

        if readiness_score < 40:
            level = "Vulnerable"
        elif readiness_score < 60:
            level = "Needs Training"
        elif readiness_score < 75:
            level = "Developing"
        elif readiness_score < 90:
            level = "Strong"
        else:
            level = "HumanShield Expert"
    else:
        readiness_score = None
        weak_skill = "Not enough data"
        next_test = "Take your first test"
        level = "Not assessed yet"

    return jsonify({
        "readinessScore": readiness_score,
        "readinessLevel": level,
        "weakSkill": weak_skill,
        "testsCompleted": tests_completed,
        "nextTest": next_test
    })


@app.route("/api/categories")
def categories():
    conn = database.get_connection()
    rows = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()

    data = []
    for row in rows:
        scenario_id, adaptive_difficulty = scenarios.pick_scenario_for_category(row["id"], row["last_score"])
        data.append({
            "id": row["id"],
            "name": row["name"],
            "sub": row["sub"],
            "difficulty": adaptive_difficulty if adaptive_difficulty else row["difficulty"],
            "lastScore": row["last_score"],
            "scenarioId": scenario_id
        })

    return jsonify(data)


@app.route("/api/history")
def history():
    conn = database.get_connection()
    rows = conn.execute("""
        SELECT test_results.completed_at, test_results.score,
               categories.name AS category_name, categories.difficulty
        FROM test_results
        JOIN categories ON test_results.category_id = categories.id
        ORDER BY test_results.completed_at DESC
    """).fetchall()
    conn.close()

    data = [
        {
            "date": row["completed_at"][:10],
            "category": row["category_name"],
            "mode": "Text",
            "difficulty": row["difficulty"],
            "score": row["score"]
        }
        for row in rows
    ]
    return jsonify(data)


@app.route("/api/profile")
def profile():
    conn = database.get_connection()
    rows = conn.execute("""
        SELECT skill_id, AVG(safe) * 100 AS pct
        FROM skill_results
        GROUP BY skill_id
    """).fetchall()
    conn.close()

    scores_by_skill = {row["skill_id"]: round(row["pct"]) for row in rows}

    data = [
        {
            "id": skill_id,
            "name": skill_name,
            "score": scores_by_skill.get(skill_id)
        }
        for skill_id, skill_name in SKILLS.items()
    ]
    return jsonify(data)


@app.route("/api/recommendation")
def recommendation():
    conn = database.get_connection()
    rows = conn.execute("""
        SELECT skill_id, AVG(safe) * 100 AS pct, COUNT(*) AS attempts
        FROM skill_results
        GROUP BY skill_id
    """).fetchall()
    conn.close()

    if not rows:
        return jsonify({
            "skill": None,
            "skillName": None,
            "action": "Complete a test to get a personalized recommendation."
        })

    weakest = min(rows, key=lambda r: r["pct"])
    skill_id = weakest["skill_id"]

    return jsonify({
        "skill": skill_id,
        "skillName": SKILLS.get(skill_id, skill_id),
        "action": RECOMMENDATIONS.get(skill_id, "Keep practicing this category.")
    })


@app.route("/api/scenario/<scenario_id>")
def scenario(scenario_id):
    all_scenarios = scenarios.get_scenarios()
    result = all_scenarios.get(scenario_id)

    if result is None:
        return jsonify({"error": "Scenario not found"}), 404

    return jsonify(result)


MAX_ANSWERS = 10


@app.route("/api/scenario/<scenario_id>/score", methods=["POST"])
def score_scenario(scenario_id):
    all_scenarios = scenarios.get_scenarios()
    matching_scenario = all_scenarios.get(scenario_id)
    if matching_scenario is None:
        return jsonify({"error": "Scenario not found"}), 404

    answers = request.get_json(silent=True)
    if (
        not isinstance(answers, list)
        or not 0 < len(answers) <= MAX_ANSWERS
        or not all(isinstance(a, dict) for a in answers)
    ):
        return jsonify({"error": "Expected a non-empty list of answers"}), 400

    safe_count = sum(1 for a in answers if a.get("safe") is True)
    total = len(answers)
    score = round((safe_count / total) * 100)

    category_id = matching_scenario["category"]
    now = datetime.now(timezone.utc).isoformat()
    conn = database.get_connection()

    conn.execute(
        "INSERT INTO test_results (category_id, scenario_id, score, completed_at) VALUES (?, ?, ?, ?)",
        (category_id, scenario_id, score, now)
    )
    conn.execute(
        "UPDATE categories SET last_score = ? WHERE id = ?",
        (score, category_id)
    )

    for answer in answers:
        skill_id = answer.get("skill")
        if skill_id in SKILLS:
            conn.execute(
                "INSERT INTO skill_results (skill_id, safe, completed_at) VALUES (?, ?, ?)",
                (skill_id, 1 if answer.get("safe") is True else 0, now)
            )

    conn.commit()
    conn.close()

    return jsonify({
        "score": score,
        "safeCount": safe_count,
        "total": total
    })


if __name__ == "__main__":
    # Local development only. In production, gunicorn serves `app`.
    app.run(debug=True, host="127.0.0.1", port=5000)