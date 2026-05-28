import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
app.use(express.json());

// =========================
// Fix __dirname (ESM)
// =========================
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// =========================
// FRONTEND (STATIC SITE)
// =========================
const publicPath = path.join(__dirname, "public");

// لازم هذا أولاً
app.use(express.static(publicPath));

// =========================
// HOME PAGE (IMPORTANT FIX)
// =========================
app.get("/", (req, res) => {
  res.sendFile(path.join(publicPath, "index.html"));
});

// =========================
// MCP TOOLS
// =========================
const tools = [
  {
    name: "searchDomain",
    description: "Search for domain availability",
    inputSchema: {
      type: "object",
      properties: {
        domain: { type: "string" }
      },
      required: ["domain"]
    }
  }
];

// =========================
// MCP API
// =========================
app.post("/mcp", (req, res) => {
  const { method, params, id } = req.body;

  // INIT
  if (method === "initialize") {
    return res.json({
      jsonrpc: "2.0",
      id,
      result: {
        serverName: "BeamMCP-Agent",
        version: "1.0.0"
      }
    });
  }

  // LIST TOOLS
  if (method === "tools/list") {
    return res.json({
      jsonrpc: "2.0",
      id,
      result: { tools }
    });
  }

  // CALL TOOL
  if (method === "tools/call") {
    const { name, arguments: args } = params;

    if (name === "searchDomain") {
      return res.json({
        jsonrpc: "2.0",
        id,
        result: {
          domain: args.domain,
          available: true
        }
      });
    }
  }

  return res.status(404).json({
    error: "Unknown method"
  });
});

// =========================
// HEALTH CHECK (OPTIONAL)
// =========================
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    service: "BeamMCP"
  });
});

// =========================
// START SERVER
// =========================
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 BeamMCP running on port ${PORT}`);
});
