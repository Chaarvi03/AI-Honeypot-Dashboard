import json
from collections import Counter

LOG_FILE = "docker/cowrie/var/log/cowrie/cowrie.json"

commands = []
ips = []

with open(LOG_FILE, "r") as file:
    for line in file:
        event = json.loads(line)

        if event.get("eventid") == "cowrie.command.input":
            commands.append(event["input"])
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

for cmd, count in counter.items():
    print(f"{cmd:<25} {count}")
