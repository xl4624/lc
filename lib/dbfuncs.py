import psycopg2
from functools import wraps
import os
import time
import sys
import traceback
sys.path.append(os.path.abspath("../"))
import config


class DBConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_IP,
            port=5432,
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()


def with_db(func):
    """Decorator to handle database connection and cursor."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = DBConnection()
        try:
            result = func(conn.cursor, *args, **kwargs)
            conn.connection.commit()
            return result
        except Exception as e:
            print(traceback.format_exc())
            conn.connection.rollback()
            raise e
        finally:
            conn.close()
    return wrapper

@with_db
def check_leetcode_user(cursor, leetcode_username):
    cursor.execute(
        "SELECT * FROM account_owner WHERE LOWER(leetcode_username) = LOWER(%s);",
        (leetcode_username,),
    )
    return cursor.fetchall()


@with_db
def check_discord_user(cursor, discord_id):
    cursor.execute(
        "SELECT * FROM account_owner WHERE LOWER(discord_username) = LOWER(%s);",
        (discord_id,),
    )
    return cursor.fetchall()


@with_db
def get_leetcode_from_discord(cursor, discord_username):
    cursor.execute(
        "SELECT leetcode_username FROM account_owner WHERE LOWER(discord_username) = LOWER(%s);",
        (discord_username,),
    )
    record = cursor.fetchall()
    return record[0][0] if record else None

@with_db
def get_discord_from_leetcode(cursor, leetcode_username):
    cursor.execute(
        "SELECT discord_username FROM account_owner WHERE LOWER(leetcode_username) = LOWER(%s);",
        (leetcode_username,),
    )
    record = cursor.fetchall()
    return record[0][0] if record else None


@with_db
def add_user(cursor, discord_id, leetcode_username):
    try:
        cursor.execute(
            "INSERT INTO account_owner (discord_username, leetcode_username) VALUES (%s, %s);",
            (discord_id, leetcode_username),
        )
        cursor.execute(
            "INSERT INTO users (username) VALUES (LOWER(%s));", (leetcode_username,)
        )
        cursor.execute(
            "SELECT id FROM users WHERE LOWER(username) = LOWER(%s);",
            (leetcode_username,),
        )
        user_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO points (user_id, points, wins) VALUES (%s, 0, 0);", (user_id,)
        )
        cursor.execute(
            """
            INSERT INTO last_completed (user_id, problem_name, completed_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP);
            """,
            (user_id, "PLACEHOLDERPROBLEMNAMEFORINITIALREGISTRATION"),
        )
        return True, ""
    except Exception as e:
        return False, str(e)


@with_db
def remove_user(cursor, discord_id):
    try:
        cursor.execute(
            "SELECT leetcode_username FROM account_owner WHERE LOWER(discord_username) = LOWER(%s);",
            (discord_id,),
        )
        leetcode_username = cursor.fetchone()[0]
        cursor.execute(
            "DELETE FROM last_completed WHERE user_id = (SELECT id FROM users WHERE LOWER(username) = LOWER(%s));",
            (leetcode_username,),
        )
        cursor.execute(
            "DELETE FROM user_submissions WHERE user_id = (SELECT id FROM users WHERE LOWER(username) = LOWER(%s));",
            (leetcode_username,),
        )
        cursor.execute(
            "DELETE FROM points WHERE user_id = (SELECT id FROM users WHERE LOWER(username) = LOWER(%s));",
            (leetcode_username,),
        )
        cursor.execute(
            "DELETE FROM users WHERE LOWER(username) = LOWER(%s);",
            (leetcode_username,),
        )
        cursor.execute(
            "DELETE FROM account_owner WHERE LOWER(discord_username) = LOWER(%s);",
            (discord_id,),
        )
        return True, ""
    except Exception as e:
        return False, str(e)


@with_db
def add_points(cursor, discord_user, leetcode_user, points):
    try:
        leetcode_username = (
            get_leetcode_from_discord(discord_user) if discord_user else leetcode_user
        )
        cursor.execute(
            "UPDATE points SET points = points + %s WHERE user_id = (SELECT id FROM users WHERE LOWER(username) = LOWER(%s));",
            (points, leetcode_username),
        )
        return True, ""
    except Exception as e:
        return False, str(e)


@with_db
def get_user_points(cursor, discord_user):
    try:
        leetcode_username = get_leetcode_from_discord(discord_user)
        cursor.execute(
            "SELECT points FROM points WHERE user_id = (SELECT id FROM users WHERE LOWER(username) = LOWER(%s));",
            (leetcode_username,),
        )
        return cursor.fetchone()[0]
    except Exception as e:
        return None


@with_db
def get_win_history(cursor, original_rows=False):
    cursor.execute(
        "SELECT username, timestamp FROM win_history JOIN users ON win_history.user_id = users.id ORDER BY timestamp DESC LIMIT 10;"
    )
    result = cursor.fetchall()
    if len(result) == 0:
        return None
    if original_rows:
        return result
    data = [list(row) for row in result]
    for row in data:
        row[1] = time.mktime(row[1].timetuple())
        row.append(get_discord_from_leetcode(row[0]))
        row[0],row[1],row[2] = row[2],row[0],row[1]
    return data

@with_db
def get_points(cursor, problem_slug=None):
    if not problem_slug:
        return -1
    cursor.execute(
        "SELECT points FROM difficulty WHERE titleslug = %s;",
        (problem_slug,),
    )
    result = cursor.fetchall()
    return result[0][0] if result else None


@with_db
def get_last_reset(cursor):
    cursor.execute("SELECT last_reset, reset_interval FROM reset;")
    result = cursor.fetchall()
    return result if result else None


@with_db
def get_admins(cursor):
    cursor.execute("SELECT discord_id FROM admins;")
    result = cursor.fetchall()
    return result if result else []


@with_db
def add_admin(cursor, discord_id):
    try:
        cursor.execute(
            "INSERT INTO admins (discord_id) VALUES (%s);",
            (discord_id,),
        )
        return True
    except Exception as e:
        return False, str(e)
