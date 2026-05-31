import os
import uuid
import httpx
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastmcp import FastMCP
from dotenv import load_dotenv

# =========================
# ENV
# =========================
load_dotenv()
API_KEY = os.getenv("API_KEY", "beam-123456")
MODAL_TOKEN_ID = os.getenv("MODAL_TOKEN_ID")
MODAL_TOKEN_SECRET = os.getenv("MODAL_TOKEN_SECRET")

# Simple in-memory task store
tasks = {}

# =========================
# MODAL HELPER
# =========================
async def run_modal_function(fn_name: str, payload: dict) -> dict:
    """Call a Modal deployed function via REST API"""
    if not MODAL_TOKEN_ID or not MODAL_TOKEN_SECRET:
        return {"error": "MODAL_TOKEN_MISSING"}

    url = f"https://api.modal.com/v1/functions/{fn_name}/calls"
    headers = {
        "Authorization": f"Token {MODAL_TOKEN_ID}:{MODAL_TOKEN_SECRET}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"MODAL_ERR_{response.status_code}", "detail": response.text}
    except Exception as e:
        return {"error": "MODAL_CONN_ERR", "detail": str(e)}

# =========================
# MCP SERVER
# =========================
mcp = FastMCP("BeamMCP-Agent")

@mcp.tool()
async def process_file(file_path: str) -> dict:
    """Process a file using Modal cloud compute"""
    if not os.path.exists(file_path):
        return {"error": "FILE_NOT_FOUND", "path": file_path}

    task_id = f"task_{uuid.uuid4().hex[:8]}"
    tasks[task_id] = {"status": "pending", "file": file_path}

    result = await run_modal_function("process-file", {
        "file_path": file_path,
        "task_id": task_id
    })

    if "error" in result:
        tasks[task_id] = {"status": "failed", "error": result["error"]}
        return {"task_id": task_id, "status": "failed", "error": result["error"]}

    tasks[task_id] = {"status": "completed", "result": result}
    return {
        "task_id": task_id,
        "status": "dispatched",
        "message": "Task sent to Modal cloud",
        "result": result
    }

@mcp.tool()
async def get_task_result(task_id: str) -> dict:
    """Get the result of a task by ID"""
    if task_id not in tasks:
        return {"error": "TASK_NOT_FOUND", "task_id": task_id}

    task = tasks[task_id]
    return {
        "task_id": task_id,
        "status": task.get("status", "unknown"),
        "result": task.get("result"),
        "error": task.get("error")
    }

@mcp.tool()
async def list_recent_tasks() -> dict:
    """List the last 5 tasks"""
    recent = list(tasks.items())[-5:]
    return {
        "total": len(tasks),
        "tasks": [
            {"task_id": tid, "status": t.get("status")}
            for tid, t in reversed(recent)
        ]
    }

# =========================
# LIFESPAN
# =========================
mcp_app = mcp.http_app()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_app.router.lifespan_context(app):
        yield

# =========================
# FASTAPI APP
# =========================
app = FastAPI(title="BeamMCP SaaS", lifespan=lifespan)

# =========================
# API KEY MIDDLEWARE
# =========================
@app.middleware("http")
async def check_api_key(request: Request, call_next):
    path = request.url.path
    if path.startswith("/mcp") and path != "/mcp/health":
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return await call_next(request)

# =========================
# MCP MOUNT
# =========================
app.mount("/mcp", mcp_app)

# =========================
# DASHBOARD
# =========================
@app.get("/dashboard")
async def dashboard():
    modal_status = "connected" if MODAL_TOKEN_ID else "not configured"
    return {
        "name": "BeamMCP SaaS",
        "status": "running",
        "modal": modal_status,
        "tools": ["process_file", "get_task_result", "list_recent_tasks"],
        "total_tasks": len(tasks)
    }

# =========================
# HOME PAGE
# =========================
@app.get("/", response_class=HTMLResponse)
async def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BeamMCP — The MCP Agent That Gets Things Done</title>
<meta name="description" content="BeamMCP is a Model Context Protocol server that lets AI agents run Python tasks, process files, and execute workflows in the cloud — instantly.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #03060d;
  --bg2: #070d1a;
  --card: #0a1222;
  --border: #112240;
  --accent: #00ff88;
  --accent2: #00c2ff;
  --warn: #ff6b35;
  --text: #ccd6f6;
  --muted: #4a6280;
  --white: #e8f0fe;
}
* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; }
body {
  font-family: 'Outfit', sans-serif;
  background: var(--bg);
  color: var(--text);
  overflow-x: hidden;
  cursor: none;
}
.cursor {
  width: 12px; height: 12px;
  background: var(--accent);
  border-radius: 50%;
  position: fixed; pointer-events: none;
  z-index: 99999;
  transition: transform 0.1s;
  mix-blend-mode: difference;
}
.cursor-ring {
  width: 36px; height: 36px;
  border: 1px solid rgba(0,255,136,0.4);
  border-radius: 50%;
  position: fixed; pointer-events: none;
  z-index: 99998;
  transition: all 0.15s ease;
}
nav {
  position: fixed; top:0; left:0; right:0; z-index:1000;
  padding: 20px 40px;
  display: flex; justify-content:space-between; align-items:center;
  background: rgba(3,6,13,0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(17,34,64,0.5);
}
.nav-logo { font-family: 'Space Mono', monospace; font-size: 1.2rem; font-weight: 700; color: var(--accent); letter-spacing: -1px; }
.nav-logo span { color: var(--accent2); }
.nav-links { display:flex; gap:32px; align-items:center; }
.nav-links a { color: var(--muted); text-decoration:none; font-size: 0.85rem; font-weight: 500; transition: color 0.2s; }
.nav-links a:hover { color: var(--accent); }
.nav-cta { background: transparent; border: 1px solid var(--accent); color: var(--accent) !important; padding: 8px 20px; border-radius: 6px; transition: all 0.2s !important; }
.nav-cta:hover { background: rgba(0,255,136,0.1) !important; }
.hero { min-height: 100vh; display: flex; align-items:center; justify-content:center; text-align: center; padding: 100px 24px 60px; position: relative; overflow:hidden; }
.hero-bg { position: absolute; inset:0; background: radial-gradient(ellipse 80% 50% at 50% 0%, rgba(0,255,136,0.06) 0%, transparent 60%), radial-gradient(ellipse 60% 40% at 80% 100%, rgba(0,194,255,0.05) 0%, transparent 50%); }
.grid-lines { position: absolute; inset:0; background-image: linear-gradient(rgba(0,255,136,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,136,0.03) 1px, transparent 1px); background-size: 60px 60px; animation: gridMove 20s linear infinite; }
@keyframes gridMove { 0%{transform:translateY(0)} 100%{transform:translateY(60px)} }
.hero-content { position:relative; z-index:1; max-width: 900px; }
.hero-badge { display: inline-flex; align-items:center; gap:8px; background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.2); padding: 8px 18px; border-radius:4px; font-family: 'Space Mono', monospace; font-size: 0.75rem; color: var(--accent); letter-spacing: 2px; margin-bottom: 32px; animation: fadeUp 0.6s ease both; }
.dot { width:6px; height:6px; background:var(--accent); border-radius:50%; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
@keyframes fadeUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
.hero h1 { font-size: clamp(3rem, 8vw, 6rem); font-weight: 900; line-height: 0.95; letter-spacing: -3px; margin-bottom: 24px; animation: fadeUp 0.6s 0.1s ease both; }
.hero h1 .line1 { display:block; color: var(--white); }
.hero h1 .line2 { display:block; background: linear-gradient(90deg, var(--accent), var(--accent2)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero-sub { font-size: 1.15rem; color: var(--muted); max-width: 600px; margin: 0 auto 48px; line-height: 1.8; animation: fadeUp 0.6s 0.2s ease both; }
.hero-btns { display:flex; gap:16px; justify-content:center; flex-wrap:wrap; animation: fadeUp 0.6s 0.3s ease both; }
.btn-primary { background: var(--accent); color: #000; padding: 16px 36px; border-radius: 6px; font-weight: 700; font-size: 0.95rem; text-decoration:none; transition: all 0.2s; font-family: 'Space Mono', monospace; }
.btn-primary:hover { transform:translateY(-3px); box-shadow: 0 12px 40px rgba(0,255,136,0.3); }
.btn-secondary { background: transparent; border: 1px solid var(--border); color: var(--text); padding: 16px 36px; border-radius: 6px; font-weight: 500; text-decoration:none; transition: all 0.2s; }
.btn-secondary:hover { border-color: var(--accent2); color: var(--accent2); }
.terminal-section { padding: 80px 24px; max-width: 900px; margin: 0 auto; }
.terminal { background: #0d1117; border: 1px solid var(--border); border-radius: 12px; overflow:hidden; box-shadow: 0 40px 80px rgba(0,0,0,0.6); }
.terminal-header { background: #161b22; padding: 14px 20px; display:flex; align-items:center; gap:8px; border-bottom: 1px solid var(--border); }
.t-dot { width:12px; height:12px; border-radius:50%; }
.t-red{background:#ff5f57} .t-yellow{background:#febc2e} .t-green{background:#28c840}
.t-title { font-family:'Space Mono',monospace; font-size:0.75rem; color:var(--muted); margin-left:8px; }
.terminal-body { padding:28px; font-family:'Space Mono',monospace; font-size:0.82rem; line-height:2; }
.t-comment{color:#444c56} .t-cmd{color:var(--accent2)} .t-string{color:var(--accent)} .t-output{color:var(--muted)} .t-success{color:var(--accent)}
.t-line{display:block}
.typing::after{content:'▋';animation:blink 1s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
.section { padding: 100px 24px; max-width: 1100px; margin: 0 auto; }
.section-label { font-family:'Space Mono',monospace; font-size:0.7rem; color:var(--accent); letter-spacing:3px; text-transform:uppercase; margin-bottom:12px; }
.section-title { font-size: clamp(2rem, 4vw, 3rem); font-weight: 800; letter-spacing:-1.5px; margin-bottom: 60px; color: var(--white); }
.steps { display:grid; gap:2px; }
.step { display:grid; grid-template-columns: 80px 1fr; gap:24px; padding: 32px 0; border-bottom: 1px solid rgba(17,34,64,0.5); transition: all 0.3s; }
.step:hover { background: rgba(0,255,136,0.02); padding-left:12px; }
.step-num { font-family:'Space Mono',monospace; font-size:2.5rem; font-weight:700; color: rgba(0,255,136,0.15); line-height:1; }
.step-content h3 { font-size:1.2rem; font-weight:700; color:var(--white); margin-bottom:8px; }
.step-content p { color:var(--muted); line-height:1.7; font-size:0.95rem; }
.step-tag { display:inline-block; margin-top:10px; background: rgba(0,194,255,0.1); border: 1px solid rgba(0,194,255,0.2); color: var(--accent2); padding:4px 12px; border-radius:4px; font-size:0.75rem; font-family:'Space Mono',monospace; }
.tools-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap:1px; background: var(--border); border: 1px solid var(--border); border-radius: 12px; overflow:hidden; }
.tool-item { background: var(--card); padding:32px; transition: all 0.3s; }
.tool-item:hover { background: rgba(0,255,136,0.03); }
.tool-icon { font-size:2rem; margin-bottom:16px; }
.tool-name { font-family:'Space Mono',monospace; font-size:0.85rem; color:var(--accent); margin-bottom:8px; }
.tool-desc { color:var(--muted); font-size:0.9rem; line-height:1.6; }
.tool-badge { display:inline-block; margin-top:12px; background: rgba(0,255,136,0.1); border: 1px solid rgba(0,255,136,0.2); color: var(--accent); padding:3px 10px; border-radius:4px; font-size:0.7rem; font-family:'Space Mono',monospace; }
.domain-section { padding: 100px 24px; background: linear-gradient(180deg, transparent, rgba(0,255,136,0.03), transparent); }
.domain-inner { max-width: 800px; margin: 0 auto; text-align:center; }
.domain-card-big { background: var(--card); border: 1px solid rgba(0,255,136,0.2); border-radius: 16px; padding: 60px 40px; position:relative; overflow:hidden; margin-top: 48px; }
.domain-card-big::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background: linear-gradient(90deg, transparent, var(--accent), transparent); }
.domain-card-big::after { content:'FOR SALE'; position:absolute; top:20px; right:-30px; background: var(--warn); color:#fff; padding:6px 50px; font-size:0.7rem; font-family:'Space Mono',monospace; font-weight:700; transform:rotate(45deg); letter-spacing:2px; }
.domain-name-big { font-family:'Space Mono',monospace; font-size: clamp(2.5rem, 6vw, 4.5rem); font-weight:700; letter-spacing:-2px; color: var(--white); margin-bottom:16px; }
.domain-name-big span { color:var(--accent); }
.domain-tagline { color:var(--muted); font-size:1rem; margin-bottom:40px; }
.domain-features { display:flex; justify-content:center; gap:32px; flex-wrap:wrap; margin-bottom:48px; }
.domain-feat { text-align:center; }
.feat-val { font-family:'Space Mono',monospace; font-size:1.5rem; color:var(--accent); font-weight:700; }
.feat-label { font-size:0.75rem; color:var(--muted); margin-top:4px; }
.domain-btns { display:flex; gap:16px; justify-content:center; flex-wrap:wrap; }
.btn-buy { background: var(--accent); color:#000; padding: 16px 40px; border-radius:8px; font-weight:700; font-size:1rem; text-decoration:none; transition:all 0.2s; font-family:'Space Mono',monospace; display:inline-flex; align-items:center; gap:8px; }
.btn-buy:hover { transform:translateY(-3px); box-shadow:0 16px 48px rgba(0,255,136,0.3); }
.btn-offer { background: transparent; border: 1px solid var(--muted); color: var(--text); padding: 16px 40px; border-radius:8px; font-weight:500; font-size:1rem; text-decoration:none; transition:all 0.2s; display:inline-flex; align-items:center; gap:8px; cursor:pointer; }
.btn-offer:hover { border-color:var(--accent2); color:var(--accent2); }
.modal-overlay { position:fixed; inset:0; background:rgba(0,0,0,0.8); backdrop-filter:blur(8px); z-index:9000; display:none; align-items:center; justify-content:center; }
.modal-overlay.open { display:flex; }
.modal { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:48px; max-width:500px; width:90%; position:relative; }
.modal h3 { font-size:1.5rem; font-weight:800; color:var(--white); margin-bottom:8px; }
.modal p { color:var(--muted); margin-bottom:28px; font-size:0.9rem; }
.modal-input { width:100%; background:var(--bg2); border:1px solid var(--border); color:var(--text); padding:14px 18px; border-radius:8px; font-size:0.95rem; margin-bottom:14px; font-family:'Outfit',sans-serif; transition:all 0.2s; }
.modal-input:focus { outline:none; border-color:var(--accent); }
.modal-submit { width:100%; background:var(--accent); color:#000; border:none; padding:16px; border-radius:8px; font-weight:700; font-size:1rem; cursor:pointer; font-family:'Space Mono',monospace; transition:all 0.2s; }
.modal-submit:hover { transform:translateY(-2px); }
.modal-close { position:absolute; top:16px; right:20px; background:none; border:none; color:var(--muted); font-size:1.5rem; cursor:pointer; }
footer { border-top:1px solid var(--border); padding:40px 24px; text-align:center; color:var(--muted); font-size:0.85rem; }
footer strong { color:var(--accent); font-family:'Space Mono',monospace; }
@media(max-width:600px){ nav{padding:16px 20px;} .nav-links{display:none;} .step{grid-template-columns:1fr;} }
</style>
</head>
<body>
<div class="cursor" id="cursor"></div>
<div class="cursor-ring" id="cursorRing"></div>
<nav>
  <div class="nav-logo">Beam<span>MCP</span></div>
  <div class="nav-links">
    <a href="#how">How It Works</a>
    <a href="#tools">Tools</a>
    <a href="#domain">Domain</a>
    <a href="/dashboard">Dashboard</a>
    <a href="#domain" class="nav-cta">Buy Domain →</a>
  </div>
</nav>
<section class="hero">
  <div class="hero-bg"></div>
  <div class="grid-lines"></div>
  <div class="hero-content">
    <div class="hero-badge"><div class="dot"></div>MCP SERVER · POWERED BY MODAL</div>
    <h1><span class="line1">The MCP Agent</span><span class="line2">That Gets Things Done</span></h1>
    <p class="hero-sub">BeamMCP connects your AI agent to real Modal cloud compute. Send tasks, process files, run Python — all through the Model Context Protocol standard.</p>
    <div class="hero-btns">
      <a href="#how" class="btn-primary">→ See How It Works</a>
      <a href="#tools" class="btn-secondary">View MCP Tools</a>
    </div>
  </div>
</section>
<div class="terminal-section">
  <div class="terminal">
    <div class="terminal-header">
      <div class="t-dot t-red"></div><div class="t-dot t-yellow"></div><div class="t-dot t-green"></div>
      <span class="t-title">beammcp-agent · Modal connected</span>
    </div>
    <div class="terminal-body">
      <span class="t-line t-comment"># AI Agent calls BeamMCP tool</span>
      <span class="t-line">result = mcp.process_file(<span class="t-string">"data.csv"</span>)</span>
      <span class="t-line"> </span>
      <span class="t-line t-success">✓ File validated locally</span>
      <span class="t-line t-success">✓ Task dispatched to Modal cloud</span>
      <span class="t-line t-success">✓ Processing complete in 1.2s</span>
      <span class="t-line t-output">→ task_id: task_a3f9c2b1</span>
      <span class="t-line t-output">→ status: completed</span>
      <span class="t-line typing"> </span>
    </div>
  </div>
</div>
<section class="section" id="how">
  <div class="section-label">// HOW IT WORKS</div>
  <div class="section-title">Three steps.<br>Real cloud power.</div>
  <div class="steps">
    <div class="step">
      <div class="step-num">01</div>
      <div class="step-content">
        <h3>Connect Your AI Agent</h3>
        <p>Point Claude Desktop or any MCP client to BeamMCP. Add your API key and you're live in seconds.</p>
        <span class="step-tag">streamable-http · MCP protocol</span>
      </div>
    </div>
    <div class="step">
      <div class="step-num">02</div>
      <div class="step-content">
        <h3>Call Tools Naturally</h3>
        <p>Your AI agent discovers all tools automatically and calls them through natural language — no manual API calls needed.</p>
        <span class="step-tag">tools/list · tools/call</span>
      </div>
    </div>
    <div class="step">
      <div class="step-num">03</div>
      <div class="step-content">
        <h3>Modal Executes in the Cloud</h3>
        <p>Heavy compute runs on Modal's serverless infrastructure. Results returned instantly without timeouts or scaling issues.</p>
        <span class="step-tag">Modal · serverless · auto-scaling</span>
      </div>
    </div>
  </div>
</section>
<section class="section" id="tools">
  <div class="section-label">// MCP TOOLS</div>
  <div class="section-title">Real tools.<br>Real cloud execution.</div>
  <div class="tools-grid">
    <div class="tool-item">
      <div class="tool-icon">📁</div>
      <div class="tool-name">process_file()</div>
      <div class="tool-desc">Send any file to Modal for real cloud processing. Returns task ID immediately while Modal handles the heavy work.</div>
      <span class="tool-badge">MODAL POWERED</span>
    </div>
    <div class="tool-item">
      <div class="tool-icon">🔍</div>
      <div class="tool-name">get_task_result()</div>
      <div class="tool-desc">Query status and output of any running or completed Modal task by its unique ID.</div>
      <span class="tool-badge">REAL-TIME</span>
    </div>
    <div class="tool-item">
      <div class="tool-icon">📋</div>
      <div class="tool-name">list_recent_tasks()</div>
      <div class="tool-desc">Get the last 5 executed tasks with live status updates. Perfect for monitoring cloud jobs.</div>
      <span class="tool-badge">LIVE STATUS</span>
    </div>
  </div>
</section>
<section class="domain-section" id="domain">
  <div class="domain-inner">
    <div class="section-label" style="text-align:center">// PREMIUM DOMAIN FOR SALE</div>
    <div class="section-title" style="text-align:center">Own the brand.<br>Own the future.</div>
    <div class="domain-card-big">
      <div class="domain-name-big">Beam<span>MCP</span>.com</div>
      <div class="domain-tagline">The definitive domain for MCP infrastructure — before someone else takes it.</div>
      <div class="domain-features">
        <div class="domain-feat"><div class="feat-val">.com</div><div class="feat-label">Extension</div></div>
        <div class="domain-feat"><div class="feat-val">7</div><div class="feat-label">Characters</div></div>
        <div class="domain-feat"><div class="feat-val">MCP</div><div class="feat-label">Trending Keyword</div></div>
        <div class="domain-feat"><div class="feat-val">2025</div><div class="feat-label">Registered</div></div>
      </div>
      <div class="domain-btns">
        <a href="https://www.godaddy.com/domainsearch/find?checkAvail=1&domainToCheck=BeamMCP.com" target="_blank" class="btn-buy">🛒 Buy on GoDaddy</a>
        <button class="btn-offer" onclick="openModal()">✉️ Make an Offer</button>
      </div>
    </div>
  </div>
</section>
<div class="modal-overlay" id="modalOverlay">
  <div class="modal">
    <button class="modal-close" onclick="closeModal()">×</button>
    <h3>Make an Offer</h3>
    <p>Send your offer for BeamMCP.com and we'll get back to you within 24 hours.</p>
    <input type="text" class="modal-input" placeholder="Your Name" id="offerName">
    <input type="email" class="modal-input" placeholder="Your Email" id="offerEmail">
    <input type="text" class="modal-input" placeholder="Your Offer (e.g. $500)" id="offerPrice">
    <textarea class="modal-input" rows="3" placeholder="Message (optional)" id="offerMsg" style="resize:none"></textarea>
    <button class="modal-submit" onclick="sendOffer()">Send Offer →</button>
  </div>
</div>
<footer>
  <p>© 2026 <strong>BeamMCP</strong> · MCP Server + Modal Cloud · Domain: <a href="mailto:cccvcccv3@gmail.com" style="color:var(--accent2)">cccvcccv3@gmail.com</a></p>
</footer>
<script>
const cursor = document.getElementById('cursor');
const ring = document.getElementById('cursorRing');
document.addEventListener('mousemove', e => {
  cursor.style.left = e.clientX - 6 + 'px';
  cursor.style.top = e.clientY - 6 + 'px';
  ring.style.left = e.clientX - 18 + 'px';
  ring.style.top = e.clientY - 18 + 'px';
});
document.querySelectorAll('a,button').forEach(el => {
  el.addEventListener('mouseenter', () => { cursor.style.transform='scale(2)'; ring.style.transform='scale(1.5)'; });
  el.addEventListener('mouseleave', () => { cursor.style.transform='scale(1)'; ring.style.transform='scale(1)'; });
});
function openModal() { document.getElementById('modalOverlay').classList.add('open'); }
function closeModal() { document.getElementById('modalOverlay').classList.remove('open'); }
function sendOffer() {
  const name = document.getElementById('offerName').value;
  const email = document.getElementById('offerEmail').value;
  const price = document.getElementById('offerPrice').value;
  const msg = document.getElementById('offerMsg').value;
  if(!name||!email||!price){ alert('Please fill all required fields'); return; }
  const subject = encodeURIComponent('Offer for BeamMCP.com - ' + price);
  const body = encodeURIComponent('Name: ' + name + '\\nEmail: ' + email + '\\nOffer: ' + price + '\\nMessage: ' + msg);
  window.location.href = 'mailto:cccvcccv3@gmail.com?subject=' + subject + '&body=' + body;
  closeModal();
}
document.getElementById('modalOverlay').addEventListener('click', e => {
  if(e.target===document.getElementById('modalOverlay')) closeModal();
});
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if(e.isIntersecting) e.target.style.opacity='1'; });
}, {threshold:0.1});
document.querySelectorAll('.step,.tool-item').forEach(el => {
  el.style.opacity='0';
  el.style.transition='opacity 0.6s ease';
  observer.observe(el);
});
</script>
</body>
</html>"""

# =========================
# START
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
