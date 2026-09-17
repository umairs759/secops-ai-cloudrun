# 🛡️ SecOps-AI Sentinel — Autonomous Cloud-Native Threat Copilot

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/AI_Engine-Gemini_1.5_Flash-8E75B2?logo=googlebard&logoColor=white)](https://aistudio.google.com/)
[![Google Cloud Run](https://img.shields.io/badge/Serverless-Cloud_Run-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![MITRE ATT&CK](https://img.shields.io/badge/Taxonomy-MITRE_v14-red)](https://attack.mitre.org/)

**SecOps-AI Sentinel** is an enterprise-grade, serverless SOC analyst assistant built to eliminate manual log triage fatigue. It accepts raw Linux, Web Server, and Firewall security telemetry, parses Indicators of Compromise (IoCs), classifies adversaries against the **MITRE ATT&CK Framework**, and creates immediate copy-paste host firewall containment commands (`iptables` / `ufw`).

Built specifically for high availability on the **Google Cloud Run $0 Free Tier** with zero standby costs.

---

## ⚡ Key Architecture & Features

- **Hybrid Intelligence Core:** Uses Google Gemini 1.5 Flash structured outputs with a deterministic heuristic fallback engine ensuring 100% uptime without failure.
- **MITRE ATT&CK v14 Taxonomy:** Maps attacks to explicit technique IDs (e.g. `T1110.001 Brute Force`, `T1190 Exploit Public-Facing App`).
- **Autonomous Remediation:** Produces executable bash commands (`iptables`, `ufw`) to block discovered attack origins instantly.
- **Interactive SOC UI:** Dark Obsidian Cyber interface designed with Tailwind CSS, Lucide security icons, and real-time Chart.js attack severity progression.
- **1-Click Test Scenarios:** Built-in samples for SSH brute-force and Web SQL Injection for instant demonstration.

---

## 🖥️ Local Quickstart

### 1. Install & Run
```bash
# Clone the repository
git clone https://github.com/umairs759/secops-ai-cloudrun.git
cd secops-ai-cloudrun

# Install dependencies
pip install -r requirements.txt

# Start the local server
uvicorn app.main:app --reload --port 8080

Open http://localhost:8080 in your browser.
```

## ☁️ Deploy to Google Cloud Run (100% Free Tier)

Ensure you have the Google Cloud CLI authenticated:

# Deploy with one single command:
gcloud run deploy secops-ai-sentinel \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 2 \
  --memory 512Mi \
  --cpu 1

Once deployment completes, Cloud Run will output a live HTTPS URL.
## 📄 License

This project is open-source under the MIT License.



---

## How to Run Locally (Testing)

After saving all files, execute the following commands in your terminal:

# 1. Install required dependencies
pip install -r requirements.txt

# 2. Launch the application server
python -m uvicorn app.main:app --reload --port 8080

Open your browser and navigate to: http://localhost:8080

    Click either "SSH Brute-Force" or "Web SQL Injection" under the 1-Click test scenarios.

    Click the "Execute AI Triage" button.

    The interactive cyber telemetry dashboard will render immediately—displaying threat severity levels, MITRE ATT&CK mappings, extracted IoCs, kill chain charts, and host firewall mitigation rules.

## How to Push to GitHub

Run the following commands in your terminal to push the project to your GitHub repository:

git add .
git commit -m "feat: complete enterprise SecOps-AI Sentinel dashboard with zero-cost cloud architecture"
git push origin main