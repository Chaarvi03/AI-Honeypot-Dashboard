import sqlite3
from collections import Counter
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder="../templates")

DATABASE = "data/attacks.db"


@app.route("/")
def home():

    search = request.args.get("search", "")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT timestamp, ip, command, risk
            FROM attacks
            WHERE ip LIKE ?
               OR command LIKE ?
               OR risk LIKE ?
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("""
            SELECT timestamp, ip, command, risk
            FROM attacks
        """)

    rows = cursor.fetchall()
    conn.close()

    # Dashboard Statistics
    total = len(rows)
    unique_ips = len(set(row[1] for row in rows))

    low = sum(1 for row in rows if row[3] == "LOW")
    medium = sum(1 for row in rows if row[3] == "MEDIUM")
    high = sum(1 for row in rows if row[3] == "HIGH")

    # Command Frequency
    commands = [row[2] for row in rows]
    command_counts = Counter(commands)

    # Sort commands by frequency (highest first)
    sorted_commands = command_counts.most_common()

    labels = [cmd for cmd, count in sorted_commands]
    values = [count for cmd, count in sorted_commands]

    return render_template(
        "index.html",
        attacks=rows,
        total=total,
        unique_ips=unique_ips,
        low=low,
        medium=medium,
        high=high,
        search=search,
        labels=labels,
        values=values
    )


@app.route("/attacks")
def attacks():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, ip, command, risk
        FROM attacks
    """)

    rows = cursor.fetchall()
    conn.close()

    results = []

    for row in rows:
        results.append({
            "timestamp": row[0],
            "ip": row[1],
            "command": row[2],
            "risk": row[3]
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)