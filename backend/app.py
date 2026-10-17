from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timezone

import database
import scenarios

app = Flask(__name__)
CORS(app)

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
    return "HumanShield backend is running"


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
        next_test = f'{weakest["name"]} \u00b7 {weakest["difficulty"]}'
    else:
        readiness_score = 0
        weak_skill = "Not enough data"
        next_test = "Take your first test"

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


@app.route("/api/scenario/<scenario_id>/score", methods=["POST"])
def score_scenario(scenario_id):
    answers = request.get_json()

    safe_count = sum(1 for a in answers if a.get("safe"))
    total = len(answers)
    score = round((safe_count / total) * 100) if total > 0 else 0

    all_scenarios = scenarios.get_scenarios()
    matching_scenario = all_scenarios.get(scenario_id)
    category_id = matching_scenario["category"] if matching_scenario else None

    if category_id:
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
            if skill_id:
                conn.execute(
                    "INSERT INTO skill_results (skill_id, safe, completed_at) VALUES (?, ?, ?)",
                    (skill_id, 1 if answer.get("safe") else 0, now)
                )

        conn.commit()
        conn.close()

    return jsonify({
        "score": score,
        "safeCount": safe_count,
        "total": total
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
