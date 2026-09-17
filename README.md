# 🛡️ SecOps-AI Sentinel v2.0 — Autonomous Cyber Threat Copilot

<div align="center">

[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Single File](https://img.shields.io/badge/Single--File-HTML-46E3B7?style=for-the-badge&logo=html5&logoColor=white)]()
[![Zero Backend](https://img.shields.io/badge/Backend-None_(100%25_Client--Side)-purple?style=for-the-badge)]()
[![Multi AI](https://img.shields.io/badge/AI_Providers-8_Supported-8E75B2?style=for-the-badge)]()
[![MITRE ATT&CK](https://img.shields.io/badge/Taxonomy-MITRE_v14-red?style=for-the-badge)](https://attack.mitre.org/)

**A single-file, zero-dependency, enterprise-grade SOC Copilot that runs entirely in your browser.**
Ingests raw telemetry, maps to **MITRE ATT&CK**, extracts IoCs, generates containment rules
(`iptables` / `ufw` / `Snort` / `Suricata` / Windows Firewall), and exports **STIX 2.1** bundles.

**No backend. No install. No build step. Just open `index.html`.**

</div>

---

## 🖥️ Mission Control Dashboard

<div align="center">
  <img src="interface.png" alt="SecOps-AI Sentinel Mission Control Dashboard" width="100%" style="border-radius: 12px; border: 1px solid #1e293b;" />
</div>

---

## ⚡ Why This Exists

Traditional SOC tooling requires: a Python backend, a cloud VM, an LLM API proxy, an IaC pipeline, and 4 different dashboards glued together.  
**SecOps-AI Sentinel collapses all of that into a single HTML file** you can drop on any static host (or even open from your filesystem) and start triaging.

- ✅ **Zero Backend** — 100% client-side, no server, no data leaves your browser (unless you opt in to a cloud AI provider).
- ✅ **BYOK Model** — Bring Your Own Key. Keys are stored **only** in your browser's `localStorage`.
- ✅ **Deterministic Fallback** — If no API key is set, a built-in heuristic engine still performs full triage. **Never fails, never returns empty.**
- ✅ **Air-Gap Friendly** — Works offline for heuristic analysis. Only the CDN assets need internet on first load.

---

## 🧠 Dual-Engine Threat Analysis

| Engine | Purpose | Requires Key? |
|---|---|---|
| **Local Heuristic Engine v2.0** | Regex + rule-based TTP detection, IoC extraction, MITRE mapping. Always available. | ❌ No |
| **Google Gemini 1.5 Flash** | Deep narrative threat synthesis. | ✅ Yes (Free tier) |
| **Groq (Llama 3.1)** | Ultra-fast inference. | ✅ Yes (Free tier) |
| **OpenRouter** | Access to free Llama models. | ✅ Yes (Free tier) |
| **Mistral Small** | EU-hosted inference. | ✅ Yes (Free tier) |
| **Cohere Command-R** | Enterprise RAG-friendly. | ✅ Yes (Free tier) |
| **OpenAI GPT-4o-mini** | Paid high-accuracy. | ✅ Yes (Paid) |
| **Anthropic Claude 3.5 Haiku** | Paid high-accuracy. | ✅ Yes (Paid) |

> If a cloud provider fails (rate limit, invalid key, network error), the platform **automatically falls back** to the local heuristic engine and continues triage — no crash, no data loss.

---

## 🧰 Feature Matrix

| Module | Capability |
|---|---|
| **Mission Control** | Real-time animated radar, live telemetry feed, 1-click scenario tests |
| **Terminal Shell** | 20+ commands (`scan`, `hash`, `encode`, `ioc add`, `setkey`, `goto`, etc.) with history |
| **Log Analyzer** | Paste logs OR drag-and-drop files (`.log`, `.txt`, `.json`, `.csv`), CTRL+ENTER to run |
| **Recon Scanner** | Simulated port sweep (labeled clearly — no real network calls) |
| **Payload Builder** | Red-team vectors: Bash, Python, PowerShell, PHP, Netcat, SQLi |
| **Encoder Lab** | Base64, Hex, URL, ROT13 — encode & decode |
| **Hash Generator** | SHA-256 via Web Crypto API |
| **MITRE ATT&CK Matrix** | Auto-highlights detected techniques across tactics |
| **IoC Vault** | Manual + auto-extracted indicators, CSV export, localStorage persistence |
| **Containment Synthesis** | Auto-generates rules for **iptables, UFW, Snort, Suricata, Windows Firewall** |
| **Incident Report** | Severity badge, kill-chain chart (Chart.js), targets, mitigations |
| **STIX 2.1 Export** | Standardized JSON bundle download for SIEM/TIP ingestion |
| **Settings** | Manage all provider keys, toggle Matrix rain, reset to factory |

---

## 📊 Technical Specifications

| Metric | Value |
|---|---|
| **Footprint** | Single `index.html` (~90 KB uncompressed) |
| **Runtime Dependencies** | Tailwind CSS CDN, Chart.js CDN (only external assets) |
| **Analysis Latency** | `< 380 ms` (local heuristic) · `< 3 s` (cloud AI) |
| **Storage** | `localStorage` for API keys, IoC vault, provider preference |
| **Supported Telemetry** | Linux `auth.log`, Nginx/Apache access logs, Syslog, Windows Event Log exports, raw text |
| **Taxonomy** | MITRE ATT&CK Enterprise v14 |
| **Containment Targets** | iptables · UFW · Snort · Suricata · Windows Advanced Firewall |
| **Export Format** | STIX 2.1 JSON bundle |
| **Browser Support** | Chrome / Edge / Firefox / Safari (modern, ES2020+) |

---

## 🚀 Quickstart

### Option 1: Just Open It
```bash
git clone https://github.com/umairs759/secops-ai-cloudrun.git
cd secops-ai-cloudrun
# Open index.html in your browser. Done.
```
## Option 2: Serve Locally (recommended)
```
python3 -m http.server 8080
# Visit http://localhost:8080
```
### Option 3: Deploy to Static Host (Free)

    GitHub Pages: Push to main, enable Pages in repo settings.

    Netlify: Drag-and-drop index.html at https://app.netlify.com/drop

    Vercel: vercel --prod

    Cloudflare Pages: Connect repo, zero config.

## 🕹️ 1-Click Attack Scenarios

Click any card on Mission Control to load & auto-analyze real-world traces:

    SSH Brute Force → T1110.001 (Password Guessing) · HIGH

    SQL Injection → T1190 (Exploit Public-Facing App) · CRITICAL

    Webshell Execution → T1059.004 (Unix Shell) · HIGH

    Ransomware (VSSAdmin) → T1490 (Inhibit System Recovery) · CRITICAL
  
## 🔐 Security & Privacy

    API keys never leave your device. They're stored in localStorage and sent directly from your browser to the provider you chose.

    No telemetry, no analytics, no tracking.

    CORS note: Some providers (like Anthropic) require the anthropic-dangerous-direct-browser-access header, which is already wired up. For production use, consider routing through your own proxy.

    Air-gap mode: Leave all keys blank → heuristic engine runs entirely offline.

## 📂 Project Structure
secops-ai-cloudrun/
│
├── index.html              # 🧠 The entire application (single-file, zero-backend)
├── interface.png           # 🖼️ Mission Control UI preview (README banner)
├── LICENSE                 # 📜 MIT License
├── README.md               # 📖 Project documentation
│
├── samples/                # 📁 Sample telemetry for demo
│   ├── auth_sample.log     #    SSH brute-force attack trace
│   └── web_sample.log      #    Web SQL injection trace
│
├── docs/                   # 📁 Extended documentation
│   ├── SETUP.md            #    Provider key setup guide
│   └── ARCHITECTURE.md     #    Deep-dive on heuristic engine
│
├── .gitignore              # 🚫 Ignore OS/editor junk
└── .nojekyll               # ⚙️ (Only if deploying to GitHub Pages)

That's it. No requirements.txt, no Dockerfile, no app/ folder, no venv. If you want to add a backend later (e.g., to proxy Anthropic calls), the code is modular enough to extract AI_CALLERS into a small FastAPI service.

## 🛠️ Extending

Add a new AI provider:

    Add an entry to AI_PROVIDERS in the <script> block.

    Add a caller function to AI_CALLERS.

    Done — it will auto-appear in the dropdown and Settings.

Add a new containment format:

    Add a <button class="tab-btn" data-ctab="myfw"> in the Containment view.

    Add a rule-template branch in updateContainmentOutput().

## 📜 License & Acknowledgments

MIT License — see LICENSE.
Built for blue teams, red teams, incident responders, and anyone tired of 12-tab triage workflows.

Iconography hand-rolled as inline SVG (no Lucide CDN dependency).
UI inspired by Black Hat / DEF CON terminal aesthetics.
</div> ```
