import os
import sqlite3
import tempfile


def _resolve_db_path():
    # 1. An explicit location always wins (e.g. a persistent disk).
    explicit = os.environ.get("DATABASE_PATH")
    if explicit:
        return explicit

    # 2. Normal case: database/humanshield.db next to the backend folder.
    default = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database", "humanshield.db")
    )
    try:
        os.makedirs(os.path.dirname(default), exist_ok=True)
        if os.access(os.path.dirname(default), os.W_OK):
            return default
    except OSError:
        pass

    # 3. Read-only filesystem (serverless hosts such as Vercel only allow
    #    writing to a temp folder). Data stored there is NOT permanent.
    return os.path.join(tempfile.gettempdir(), "humanshield.db")


DB_PATH = _resolve_db_path()


def is_temporary():
    """True when the database lives in a temp folder that can be wiped."""
    if os.environ.get("DATABASE_PATH"):
        return False
    return os.path.abspath(DB_PATH).startswith(os.path.abspath(tempfile.gettempdir()))


def get_connection():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            sub TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            last_score INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id TEXT NOT NULL,
            scenario_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            completed_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_id TEXT NOT NULL,
            safe INTEGER NOT NULL,
            completed_at TEXT NOT NULL
        )
    """)

    existing = cursor.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    if existing == 0:
        seed_categories(cursor)

    conn.commit()
    conn.close()


def seed_categories(cursor):
    # Every category starts untested (no score), so a new user sees their
    # own real progress rather than made-up numbers.
    starter_data = [
        ("education", "Education", "Fake scholarships, admissions, exam results", "Beginner", None),
        ("finance", "Finance", "Fake bank reps, OTP requests, loans, investments", "Beginner", None),
        ("work", "Work", "Fake managers, HR, IT support, BEC", "Intermediate", None),
        ("economy", "Economy", "Fake grants, relief funds, job offers", "Beginner", None),
        ("social", "Social Media", "Fake support, verification requests, giveaways", "Intermediate", None),
        ("shopping", "Shopping & E-commerce", "Fake stores, deliveries, refunds", "Beginner", None),
        ("personal", "Personal & Relationships", "Romance scams, fake emergencies", "Beginner", None),
        ("government", "Government & Public Services", "Fake officials, tax, immigration", "Intermediate", None),
        ("gaming", "Gaming & Entertainment", "Fake rewards, account recovery, currency", "Beginner", None),
    ]

    cursor.executemany(
        "INSERT INTO categories (id, name, sub, difficulty, last_score) VALUES (?, ?, ?, ?, ?)",
        starter_data
    )
