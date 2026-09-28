import json
import sqlite3
import os

LOG_FILE = "docker/cowrie/var/log/cowrie/cowrie.json"
DB_FILE = "data/attacks.db"

# -------------------------------
# Threat Classification
# -------------------------------

HIGH = [
    "wget",
    "curl",
    "chmod",
    "sudo",
    "rm",
    "rm -rf",
    "nc",
    "python",
    "bash",
    "perl"
]

MEDIUM = [
    "cat",
    "uname",
    "ifconfig",
    "netstat",
    "ps",
    "scp"
]

LOW = [
    "pwd",
    "ls",
    "whoami",
    "exit"
]


def classify_risk(cmd):
    """Return the risk level of a command."""

    cmd = cmd.lower()

    for word in HIGH:
        if word in cmd:
            return "HIGH"

    for word in MEDIUM:
        if word in cmd:
            return "MEDIUM"

    return "LOW"


def update_database():

    if not os.path.exists(LOG_FILE):
        print("Cowrie log file not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attacks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            command TEXT,
            risk TEXT
        )
    """)

    with open(LOG_FILE, "r") as file:

        for line in file:

            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            if event.get("eventid") != "cowrie.command.input":
                continue

            cmd = event.get("input", "").strip()

            # Skip blank commands
            if not cmd:
                continue

            ip = event.get("src_ip", "")
            timestamp = event.get("timestamp", "")

            risk = classify_risk(cmd)

            # Prevent duplicate entries
            cursor.execute("""
                SELECT id
                FROM attacks
                WHERE timestamp=? AND ip=? AND command=?
            """, (timestamp, ip, cmd))

            if cursor.fetchone():
                continue

            cursor.execute("""
                INSERT INTO attacks(timestamp, ip, command, risk)
                VALUES (?, ?, ?, ?)
            """, (timestamp, ip, cmd, risk))

    conn.commit()
    conn.close()

    print("Database updated successfully!")


if __name__ == "__main__":
    update_database()
