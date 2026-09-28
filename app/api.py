import sqlite3
from collections import Counter
from flask import Flask, jsonify, render_template, request

# Import database updater
from log_to_db import update_database

app = Flask(__name__, template_folder="../templates")

DATABASE = "data/attacks.db"


@app.route("/")
def home():

    # Update database from latest Cowrie logs
    update_database()

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
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("""
            SELECT timestamp, ip, command, risk
            FROM attacks
            ORDER BY id DESC
        """)

    rows = cursor.fetchall()
    conn.close()

    # ---------------- Dashboard Statistics ----------------

    total = len(rows)
    unique_ips = len(set(row[1] for row in rows))

    low = sum(1 for row in rows if row[3] == "LOW")
    medium = sum(1 for row in rows if row[3] == "MEDIUM")
    high = sum(1 for row in rows if row[3] == "HIGH")

    # ---------------- Latest Attack ----------------

    latest_attack = rows[0][0] if rows else "No attacks"
    # ---------------- Top Attacking IP ----------------

    ip_counts = Counter(row[1] for row in rows)
    top_ip = ip_counts.most_common(1)[0][0] if ip_counts else "N/A"

    # Data for Top Attacking IP chart
    sorted_ips = ip_counts.most_common()
    ip_labels = [ip for ip, count in sorted_ips]
    ip_values = [count for ip, count in sorted_ips]

    # ---------------- Command Frequency ----------------

    commands = [row[2] for row in rows]
    command_counts = Counter(commands)

    sorted_commands = command_counts.most_common()

    labels = [cmd for cmd, count in sorted_commands]
    values = [count for cmd, count in sorted_commands]

    # ---------------- Most Executed Command ----------------

    top_command = (
        command_counts.most_common(1)[0][0]
        if command_counts else "N/A"
    )

    # ---------------- Attacks Over Time ----------------

    time_counter = Counter()

    for row in rows:
        # Group attacks by minute
        minute = row[0][:16]
        time_counter[minute] += 1

    sorted_time = sorted(time_counter.items())

    time_labels = [item[0] for item in sorted_time]
    time_values = [item[1] for item in sorted_time]
    return render_template(
        "index.html",
        attacks=rows,
        total=total,
        unique_ips=unique_ips,
        low=low,
        medium=medium,
        high=high,
        latest_attack=latest_attack,
        top_ip=top_ip,
        top_command=top_command,
        search=search,

        # Command chart
        labels=labels,
        values=values,

        # Top Attacking IP chart
        ip_labels=ip_labels,
        ip_values=ip_values,

        # Timeline chart
        time_labels=time_labels,
        time_values=time_values
    )


@app.route("/attacks")
def attacks():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, ip, command, risk
        FROM attacks
        ORDER BY id DESC
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
