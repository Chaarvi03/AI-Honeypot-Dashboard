# 🛡️ AI Honeypot Dashboard

A Flask-based cybersecurity dashboard that visualizes attack data collected from a Cowrie SSH Honeypot. The project parses honeypot logs, stores attack information in SQLite, classifies threats based on executed commands, and presents real-time insights through an interactive dashboard.

---

## 📌 Project Overview

Cyber attackers often scan and interact with exposed SSH servers. This project simulates a vulnerable SSH server using the **Cowrie Honeypot** to capture attacker activity.

The captured logs are processed using Python, stored in an SQLite database, and displayed through a Flask web application with an interactive dashboard.

---

## 🚀 Features

- 📡 Collects attack logs from Cowrie Honeypot
- 🗄 Stores attack data in SQLite database
- ⚠️ Command-based risk classification
  - 🟢 Low Risk
  - 🟡 Medium Risk
  - 🔴 High Risk
- 📊 Dashboard statistics
  - Total Attacks
  - Unique IP Addresses
  - Risk Summary
- 🥧 Risk Distribution Pie Chart
- 📈 Most Executed Commands Bar Chart
- 🔍 Search attacks by:
  - IP Address
  - Command
  - Risk Level
- ⚡ Quick Filter Table
- 🔄 Auto-refresh Dashboard (every 5 seconds)
- 🌙 Modern Dark Theme UI

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Flask | Web Framework |
| SQLite | Database |
| HTML | Frontend |
| CSS | Styling |
| JavaScript | Client-side Logic |
| Chart.js | Dashboard Charts |
| Cowrie Honeypot | Attack Collection |
| Docker | Honeypot Deployment |

---

## 📂 Project Structure

```
AI-HONEYPOT-LAB
│
├── app/
│   ├── api.py
│   ├── log_parser.py
│   └── log_to_db.py
│
├── templates/
│   └── index.html
│
├── data/
│   └── attacks.db
│
├── docker/
│   └── cowrie/
│
├── docs/
│   └── screenshots/
│
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 🏗️ System Architecture

```
                Internet

                    │

                    ▼

          Cowrie SSH Honeypot
                    │
                    ▼
          Honeypot JSON Logs
                    │
                    ▼
          Python Log Parser
                    │
                    ▼
            SQLite Database
                    │
                    ▼
             Flask Backend API
                    │
                    ▼
         AI Honeypot Dashboard
```

---

## 📸 Screenshots

### Dashboard

> Add your dashboard screenshot here.

Example:

```
docs/dashboard.png
```

---

### Risk Distribution

> Add pie chart screenshot.

---

### Search Functionality

> Add search feature screenshot.

---

## ⚠️ Threat Classification

### 🟢 Low Risk

- whoami
- pwd
- ls
- exit

---

### 🟡 Medium Risk

- uname
- cat
- wget
- curl
- chmod

---

### 🔴 High Risk

- bash
- python
- nc
- rm
- perl

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/AI-Honeypot-Dashboard.git

cd AI-Honeypot-Dashboard
```

---

### Create Virtual Environment

```bash
python3 -m venv .venv
```

Activate

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Run the Flask Application

```bash
python app/api.py
```

---

Open your browser

```
http://127.0.0.1:5000
```

---

## 📊 Dashboard Statistics

The dashboard displays:

- Total Attacks
- Unique Source IPs
- Low Risk Attacks
- Medium Risk Attacks
- High Risk Attacks
- Risk Distribution
- Most Executed Commands

---

## 🔍 Search

Users can search attacks by:

- IP Address
- Command
- Risk Level

The dashboard updates instantly with matching results.

---

## 🔄 Auto Refresh

The dashboard refreshes every **5 seconds** to display newly captured attacks.

---

## 🎯 Future Improvements

- Machine Learning based attack detection
- Live WebSocket updates
- Geographic attack map
- User authentication
- Email alerts
- PDF report generation
- Elasticsearch integration
- Threat intelligence feeds

---

## 👨‍💻 Author

**Chaarvi**

Artificial Intelligence & Data Science Student

CMR Institute of Technology

---

## 📜 License

This project is developed for educational and cybersecurity learning purposes.