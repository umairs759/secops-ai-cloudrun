import os
import base64
from pathlib import Path
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.analyzer import SecOpsAnalyzer

app = FastAPI(
    title="SecOps-AI Sentinel",
    description="Autonomous Cloud-Native SOC Assistant for Rapid Threat Triage",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

analyzer = SecOpsAnalyzer()

SAMPLES = {
    "ssh": (
        "Sep 17 04:12:01 edge-srv01 sshd[2841]: Failed password for invalid user admin from 185.220.101.5 port 41202 ssh2\n"
        "Sep 17 04:12:03 edge-srv01 sshd[2843]: Failed password for root from 185.220.101.5 port 41208 ssh2\n"
        "Sep 17 04:12:06 edge-srv01 sshd[2847]: Failed password for root from 185.220.101.5 port 41214 ssh2\n"
        "Sep 17 04:12:09 edge-srv01 sshd[2850]: Failed password for invalid user test from 185.220.101.5 port 41220 ssh2\n"
        "Sep 17 04:12:12 edge-srv01 sshd[2855]: Failed password for invalid user oracle from 185.220.101.5 port 41228 ssh2\n"
        "Sep 17 04:12:15 edge-srv01 sshd[2860]: Failed password for root from 185.220.101.5 port 41235 ssh2\n"
        "Sep 17 04:12:22 edge-srv01 sshd[2870]: Maximum authentication attempts exceeded for root from 185.220.101.5 port 41240 ssh2 [preauth]"
    ),
    "sqli": (
        '194.26.29.112 - - [17/Sep/2026:08:15:20 +0000] "GET /api/v1/products?cat=1 HTTP/1.1" 200 4520 "-" "Mozilla/5.0"\n'
        '194.26.29.112 - - [17/Sep/2026:08:15:22 +0000] "GET /api/v1/products?cat=1%27%20UNION%20SELECT%20null,username,password%20FROM%20users-- HTTP/1.1" 200 4520 "-" "sqlmap/1.6#stable"\n'
        '194.26.29.112 - - [17/Sep/2026:08:15:25 +0000] "GET /admin/login.php?user=admin%27%20OR%201=1-- HTTP/1.1" 302 512 "-" "sqlmap/1.6#stable"\n'
        '194.26.29.112 - - [17/Sep/2026:08:15:30 +0000] "GET /../../../../etc/passwd HTTP/1.1" 403 162 "-" "curl/7.88.1"\n'
        '194.26.29.112 - - [17/Sep/2026:08:15:35 +0000] "POST /api/v1/checkout HTTP/1.1" 500 891 "XSS_SECURITY_PROBE" "Mozilla/5.0"'
    )
}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "secops-ai-sentinel", "version": "1.0.0"}

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    index_file = TEMPLATES_DIR / "index.html"
    return FileResponse(index_file)

@app.get("/api/sample/{sample_type}")
async def fetch_sample_log(sample_type: str):
    log_content = SAMPLES.get(sample_type, SAMPLES["ssh"])
    return {"log_content": log_content}

@app.post("/api/analyze")
async def execute_analysis(
    raw_logs: str = Form(""),
    raw_logs_b64: str = Form(""),
    api_key: str = Form(""),
    file: UploadFile = File(None)
):
    content = raw_logs
    if raw_logs_b64:
        try:
            content = base64.b64decode(raw_logs_b64).decode("utf-8", errors="ignore")
        except Exception:
            content = raw_logs

    if file and file.filename:
        file_bytes = await file.read()
        content = file_bytes.decode("utf-8", errors="ignore")

    if not content.strip():
        return JSONResponse(status_code=400, content={"error": "Telemetry stream is empty."})

    result = analyzer.analyze_logs(content, user_api_key=api_key)
    return JSONResponse(content=result)
