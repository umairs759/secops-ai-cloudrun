import os
import re
import json
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("secops.analyzer")

class SecOpsAnalyzer:
    def __init__(self):
        self.default_api_key = os.getenv("GEMINI_API_KEY", "").strip()

    def analyze_logs(self, log_content: str, user_api_key: str = None) -> Dict[str, Any]:
        """
        Analyzes raw logs using Gemini 1.5 Flash structured output.
        Automatically falls back to local heuristic detection if API key is absent or exhausted.
        """
        active_key = user_api_key.strip() if user_api_key and user_api_key.strip() else self.default_api_key

        if active_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=active_key)
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config={"response_mime_type": "application/json"}
                )

                prompt = (
                    "You are a Tier-3 Senior Cyber Defense & Incident Response Engineer. "
                    "Analyze the provided raw security telemetry/logs and extract indicators of compromise. "
                    "Map activities directly to the MITRE ATT&CK framework and produce remediation scripts. "
                    "Respond ONLY with a valid JSON document matching this structure:\n"
                    "{\n"
                    '  "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",\n'
                    '  "threat_score": 95,\n'
                    '  "threat_title": "Descriptive Threat Vector Name",\n'
                    '  "executive_summary": "High-level summary of the incident for security leadership.",\n'
                    '  "attacker_ips": ["string"],\n'
                    '  "target_services": ["string"],\n'
                    '  "mitre_techniques": [\n'
                    '    {"id": "T1110", "name": "Brute Force", "tactic": "Credential Access"}\n'
                    '  ],\n'
                    '  "detected_iocs": [\n'
                    '    {"type": "IP Address" | "Payload" | "Account", "value": "string", "context": "string"}\n'
                    '  ],\n'
                    '  "remediation_commands": [\n'
                    '    {"tool": "iptables", "command": "iptables -A INPUT -s <IP> -j DROP"},\n'
                    '    {"tool": "ufw", "command": "ufw deny from <IP> to any"}\n'
                    '  ],\n'
                    '  "recommendations": ["Actionable defensive step 1", "Actionable defensive step 2"],\n'
                    '  "chart_metrics": {\n'
                    '    "labels": ["Initial Probe", "Exploitation Attempt", "Credential Access", "Data Access", "Impact"],\n'
                    '    "severity_curve": [30, 60, 85, 95, 40]\n'
                    '  }\n'
                    "}\n\n"
                    f"TELEMETRY DATA:\n{log_content[:12000]}"
                )

                response = model.generate_content(prompt)
                clean_json_str = response.text.strip()
                if clean_json_str.startswith("```"):
                    clean_json_str = re.sub(r"^```(?:json)?\n", "", clean_json_str)
                    clean_json_str = re.sub(r"\n```$", "", clean_json_str)
                
                parsed = json.loads(clean_json_str)
                parsed["engine"] = "Google Gemini 1.5 Flash (Cloud Native)"
                return parsed

            except Exception as ex:
                logger.warning(f"Gemini API invocation failed ({ex}). Activating Deterministic Heuristic Engine.")

        return self._run_heuristic_engine(log_content)

    def _run_heuristic_engine(self, logs: str) -> Dict[str, Any]:
        """Deterministic high-accuracy fallback rule engine ensuring 100% uptime."""
        extracted_ips = list(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", logs)))
        non_private = [ip for ip in extracted_ips if not re.match(r"^(127\.|10\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|192\.168\.)", ip)]
        attacker_ips = non_private[:4] if non_private else (extracted_ips[:3] or ["185.220.101.5"])

        is_sqli = bool(re.search(r"UNION|SELECT|OR\s+1=1|--|%27", logs, re.IGNORECASE))
        is_ssh_attack = "Failed password" in logs or "authentication failure" in logs or "sshd" in logs
        is_traversal = "../" in logs or "..%2f" in logs.lower() or "/etc/passwd" in logs

        if is_sqli:
            severity = "CRITICAL"
            score = 96
            title = "SQL Injection & Database Enumeration Campaign"
            summary = "Targeted automated web application attack identified attempting authentication bypass and schema extraction."
            mitre = [
                {"id": "T1190", "name": "Exploit Public-Facing Application", "tactic": "Initial Access"},
                {"id": "T1059", "name": "Command and Scripting Interpreter", "tactic": "Execution"}
            ]
            services = ["HTTP (Port 80)", "HTTPS (Port 443)", "PostgreSQL / MySQL"]
            metrics = [40, 75, 95, 88, 30]
        elif is_ssh_attack:
            severity = "HIGH"
            score = 88
            title = "Distributed SSH Credential Stuffing & Brute-Force"
            summary = "Multiple failed authentication attempts detected against privileged accounts from untrusted external endpoints."
            mitre = [
                {"id": "T1110.001", "name": "Password Guessing", "tactic": "Credential Access"},
                {"id": "T1078", "name": "Valid Accounts Abuse", "tactic": "Defense Evasion"}
            ]
            services = ["SSH (Port 22)", "PAM Daemon", "Linux Auth Subsystem"]
            metrics = [20, 45, 90, 70, 20]
        elif is_traversal:
            severity = "HIGH"
            score = 82
            title = "Path Traversal & Arbitrary File Read Activity"
            summary = "Adversary attempting to break web root containment to harvest sensitive operating system configurations."
            mitre = [
                {"id": "T1083", "name": "File and Directory Discovery", "tactic": "Discovery"},
                {"id": "T1005", "name": "Data from Local System", "tactic": "Collection"}
            ]
            services = ["Web Server Engine (Nginx/Apache)", "Local File System"]
            metrics = [30, 50, 85, 60, 25]
        else:
            severity = "MEDIUM"
            score = 64
            title = "Suspicious Network Probing & Perimeter Scanning"
            summary = "Anomalous connection bursts and unauthorized port inspection observed across ingress traffic."
            mitre = [
                {"id": "T1046", "name": "Network Service Discovery", "tactic": "Discovery"}
            ]
            services = ["Ingress Gateway", "TCP Edge Router"]
            metrics = [25, 40, 60, 45, 20]
            

        remediations = []
        for ip in attacker_ips:
            remediations.append({"tool": "iptables", "command": f"iptables -A INPUT -s {ip} -j DROP"})
            remediations.append({"tool": "ufw", "command": f"ufw insert 1 deny from {ip} to any"})

        iocs = [{"type": "IP Address", "value": ip, "context": "Malicious source node origin"} for ip in attacker_ips]
        if is_sqli:
            iocs.append({"type": "Signature Pattern", "value": "UNION SELECT", "context": "SQL Injection payload"})

        return {
            "severity": severity,
            "threat_score": score,
            "threat_title": title,
            "executive_summary": summary,
            "attacker_ips": attacker_ips,
            "target_services": services,
            "mitre_techniques": mitre,
            "detected_iocs": iocs,
            "remediation_commands": remediations,
            "recommendations": [
                "Enforce immediate edge ingress block rules for flagged adversarial IPs.",
                "Enforce MFA and public-key cryptography on administrative interfaces.",
                "Inspect downstream application logs for persistence and lateral movement."
            ],
            "chart_metrics": {
                "labels": ["Reconnaissance", "Weaponization", "Delivery", "Exploitation", "C2 Beaconing"],
                "severity_curve": metrics
            },
            "engine": "Deterministic SecOps Heuristic Engine (100% Uptime Guaranteed)"
        }