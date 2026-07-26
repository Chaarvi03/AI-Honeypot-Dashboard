import json
import sqlite3

LOG_FILE = "docker/cowrie/var/log/cowrie/cowrie.json"
DB_FILE = "data/attacks.db"

# Threat Classification
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

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    ip TEXT,
    command TEXT,
    risk TEXT
)
""")

with open(LOG_FILE, "r") as file:
    for line in file:
        event = json.loads(line)

        if event.get("eventid") == "cowrie.command.input":
            cmd = event["input"]
            ip = event["src_ip"]
            timestamp = event["timestamp"]

            # Default Risk
            risk = "LOW"

            # Check High Risk Commands
            for word in HIGH:
                if word in cmd:
                    risk = "HIGH"
                    break

            # Check Medium Risk Commands
            if risk == "LOW":
                for word in MEDIUM:
                    if word in cmd:
                        risk = "MEDIUM"
                        break

            cursor.execute(
                """
                INSERT INTO attacks(timestamp, ip, command, risk)
                VALUES (?, ?, ?, ?)
                """,
                (timestamp, ip, cmd, risk)
            )

conn.commit()
conn.close()

print("Attack data stored successfully!")
