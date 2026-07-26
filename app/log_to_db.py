import json
import sqlite3

LOG_FILE = "docker/cowrie/var/log/cowrie/cowrie.json"
DB_FILE = "data/attacks.db"

LOW = ["whoami", "pwd", "ls", "cat", "exit", "uname"]
MEDIUM = ["wget", "curl", "chmod", "scp"]
HIGH = ["bash", "python", "nc", "rm", "perl"]

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

            first = cmd.split()[0]

            if first in HIGH:
                risk = "HIGH"
            elif first in MEDIUM:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            cursor.execute(
                "INSERT INTO attacks(timestamp, ip, command, risk) VALUES (?, ?, ?, ?)",
                (timestamp, ip, cmd, risk)
            )

conn.commit()
conn.close()

print("Attack data stored successfully!")
