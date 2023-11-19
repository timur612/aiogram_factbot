import sqlite3 as sq


async def db_start():
    global db, cur
    db = sq.connect("facts.db")
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS facts(id INTEGER PRIMARY KEY "
                "AUTOINCREMENT, text TEXT, type TEXT, subtype TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS offer_facts(id INTEGER PRIMARY KEY "
                "AUTOINCREMENT, text TEXT, type TEXT, subtype TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY,"
                "is_admin INTEGER)")
    db.commit()


async def create_fact(fact_type: str, fact_subtype: str, fact_text: str):
    fact = (fact_text, fact_type, fact_subtype)
    cur.execute(
        f"INSERT INTO facts (text, type, subtype) VALUES (?, ? , ?)", fact)
    db.commit()


async def create_offer_fact(fact_type: str, fact_subtype: str, fact_text: str):
    fact = (fact_text, fact_type, fact_subtype)
    cur.execute(
        f"INSERT INTO offer_facts (text, type, subtype) VALUES (?, ? , ?)", fact)
    db.commit()


async def get_facts(fact_subtype: str):
    result = cur.execute(
        f"SELECT text FROM facts WHERE subtype='{fact_subtype}'").fetchall()
    facts = []
    for fact in result:
        facts.append(fact)
    return facts


async def get_offer_facts():
    result = cur.execute(
        f"SELECT * FROM offer_facts").fetchall()
    facts = []
    for fact in result:
        facts.append(fact)
    return facts


async def get_all_facts():
    result = cur.execute(
        f"SELECT text FROM facts").fetchall()
    facts = []
    for fact in result:
        facts.append(fact)
    return facts


async def delete_offer_fact(fact_id: int):
    cur.execute(f"DELETE FROM offer_facts WHERE id={fact_id}")
    db.commit()


async def create_user(user_id: str, is_admin: int):
    user = cur.execute(f"SELECT 1 FROM users WHERE user_id={user_id}").fetchone()
    if not user:
        cur.execute(f"INSERT INTO users(user_id, is_admin) VALUES(?, ?)",
                    (user_id, is_admin))
        db.commit()


async def is_user_admin(user_id: str) -> bool:
    user = cur.execute(f"SELECT is_admin FROM users WHERE user_id={user_id}").fetchone()
    if user[0] == 1:
        return True
    return False
