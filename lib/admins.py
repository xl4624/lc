import psycopg2
import sys

sys.path.append("..")
import config


def getAdmins(DB_IP, DB_NAME, DB_USER, DB_PASS):
    conn = psycopg2.connect(
        host=DB_IP, database=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute("SELECT discord_id FROM admins")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [int(row[0]) for row in rows]


# ADMINS = getAdmins(config.DB_IP, config.DB_NAME, config.DB_USER, config.DB_PASS)
# print(ADMINS)
