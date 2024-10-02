import psycopg2
import os
import sys

sys.path.append(os.path.abspath("../"))
import config

connection = psycopg2.connect(
    database=config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_IP,
    port=5432,
)

cursor = connection.cursor()


def check_leetcode_user(leetcode_username):
    cursor.execute(
        "SELECT * from account_owner WHERE LOWER(leetcode_username) = LOWER(%s);",
        (leetcode_username,),
    )
    record = cursor.fetchall()

    return record


def check_discord_user(discord_id):
    cursor.execute(
        "SELECT * from account_owner WHERE LOWER(discord_username) = LOWER(%s);",
        (discord_id,),
    )
    record = cursor.fetchall()

    return record


def get_leetcode_from_discord(discord_username):
    cursor.execute(
        "SELECT leetcode_username from account_owner WHERE LOWER(discord_username) = LOWER(%s);",
        (discord_username,),
    )
    record = cursor.fetchall()
    if len(record) == 0:
        return False
    return record[0][0]


def get_discord_from_leetcode(leetcode_username):
    cursor.execute(
        "SELECT discord_username from account_owner WHERE LOWER(leetcode_username) = LOWER(%s);",
        (leetcode_username,),
    )
    record = cursor.fetchall()
    if len(record) == 0:
        return False
    return record[0][0]


def add_user(discord_id, leetcode_username):
    try:
        cursor.execute(
            "INSERT INTO account_owner (discord_username, leetcode_username) VALUES (%s, %s);",
            (discord_id, leetcode_username),
        )
        cursor.execute(
            "INSERT INTO users (username) VALUES (LOWER(%s));", (leetcode_username,)
        )
        cursor.execute(
            "SELECT id from users WHERE LOWER(username) = LOWER(%s);",
            (leetcode_username,),
        )
        user_id = cursor.fetchall()[0][0]
        cursor.execute(
            "INSERT INTO points (user_id, points, wins) VALUES (%s, 0, 0);", (user_id,)
        )
        connection.commit()
        return (True, "")
    except Exception as e:
        print(e)
        return (False, e)


def remove_user(discord_id):
    try:
        cursor.execute(
            "SELECT leetcode_username FROM account_owner WHERE LOWER(discord_username) = LOWER(%s);",
            (discord_id,),
        )
        leetcode_username = cursor.fetchall()[0][0]
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
        connection.commit()
        return (True, "")
    except Exception as e:
        print(e)
        return (False, e)


def add_points(discord_user, leetcode_user, points):
    try:
        if discord_user:
            result = get_leetcode_from_discord(discord_user)
            if result:
                leetcode_username = result
        else:
            leetcode_username = leetcode_user
        statement = f"UPDATE points SET points = points + {points} WHERE user_id = (SELECT id FROM users WHERE LOWER(username) = LOWER(%s));"
        cursor.execute(statement, (leetcode_username,))
        connection.commit()
        return (True, "")
    except Exception as e:
        print(e)
        return (False, e)


def add_admin(discord_id):
    try:
        cursor.execute(
            "INSERT INTO admins (discord_id) VALUES (%s);",
            (discord_id,),
        )
        connection.commit()
        return True
    except Exception as e:
        print(e)
        return False

def get_user_points(discord_user):
    try:
        result = get_leetcode_from_discord(discord_user)
        if result:
            leetcode_username = result
        cursor.execute(
            "SELECT points FROM points WHERE user_id = (SELECT id FROM users WHERE LOWER(username) = LOWER(%s));",
            (leetcode_username,),
        )
        record = cursor.fetchall()
        return record[0][0]
    except Exception as e:
        print(e)
        return False
    