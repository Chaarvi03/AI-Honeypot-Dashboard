import json
from collections import Counter

LOG_FILE = "docker/cowrie/var/log/cowrie/cowrie.json"

LOW = ["whoami", "pwd", "ls", "cat", "exit", "uname"]
MEDIUM = ["wget", "curl", "chmod", "scp"]
HIGH = ["bash", "python", "nc", "rm", "perl"]

commands = []
ips = []

with open(LOG_FILE, "r") as file:
    for line in file:
        event = json.loads(line)

        if event.get("eventid") == "cowrie.command.input":
            cmd = event["input"]
            commands.append(cmd)
            ips.append(event["src_ip"])

print("=" * 50)
print("Cowrie Attack Summary")
print("=" * 50)

print(f"\nTotal Commands : {len(commands)}")

print("\nUnique IPs:")
for ip in set(ips):
    print(f" - {ip}")

print("\nCommands Executed:")

counter = Counter(commands)

highest_risk = "LOW"

for cmd, count in counter.items():
    print(f"{cmd:<25} {count}")

    first_word = cmd.split()[0]

    if first_word in HIGH:
        highest_risk = "HIGH"
    elif first_word in MEDIUM and highest_risk != "HIGH":
        highest_risk = "MEDIUM"

print("\n" + "=" * 50)

if highest_risk == "HIGH":
    print("Overall Threat Level : 🔴 HIGH")
elif highest_risk == "MEDIUM":
    print("Overall Threat Level : 🟡 MEDIUM")
else:
    print("Overall Threat Level : 🟢 LOW")
