# ⚡ BeamMCP

> The MCP Agent That Gets Things Done

**BeamMCP** is a production-ready MCP (Model Context Protocol) server that connects AI agents like Claude to real cloud compute. Process files, analyze text, and generate reports — all through natural language.

🌐 **Live:** [beammcp.com](https://beammcp.com)

---

## 🚀 Features

- ✅ **MCP Server** — Built with FastMCP + FastAPI
- ✅ **3 AI Tools** — Ready to use instantly
- ✅ **API Key Protection** — Secure `/mcp` endpoint
- ✅ **Docker Ready** — Deploy anywhere
- ✅ **Railway Compatible** — One-click deploy

---

## 🛠️ MCP Tools

| Tool | Description |
|------|-------------|
| `process_file(file_path)` | Upload and process any file in the cloud |
| `get_task_result(task_id)` | Check status and get result of a task |
| `list_recent_tasks()` | View last 5 executed tasks |

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/RaniaAkramm/beam-mcp-agent
cd beam-mcp-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp env.example .env
```

Edit `.env`:

```env
API_KEY=your-secret-key
PORT=8080
```

### 4. Run locally

```bash
python main.py
```

Server runs at: `http://localhost:8080`

---

## 🔌 Connect to Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "beammcp": {
      "url": "https://beammcp.com/mcp",
      "headers": {
        "x-api-key": "your-secret-key"
      }
    }
  }
}
```

---

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Landing page |
| `GET /dashboard` | Server status + tools list |
| `POST /mcp` | MCP protocol endpoint |

---

## 🐳 Docker

```bash
docker build -t beammcp .
docker run -p 8080:8080 --env-file .env beammcp
```

---

## 🚂 Deploy on Railway

1. Connect GitHub repo to Railway
2. Add environment variables: `API_KEY`, `PORT`
3. Set start command: `python main.py`
4. Deploy ✅

---

## 📁 Project Structure

```
beammcp/
├── main.py          # FastAPI + MCP server + Landing page
├── requirements.txt # Python dependencies
├── Procfile         # Railway start command
├── env.example      # Environment variables template
└── README.md        # This file
```

---

## 🌐 Domain For Sale

**BeamMCP.com** is available for purchase.

📧 Contact: [cccvcccv3@gmail.com](mailto:cccvcccv3@gmail.com)

---

## 📄 License

MIT © 2026 BeamMCP
