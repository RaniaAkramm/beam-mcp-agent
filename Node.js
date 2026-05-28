import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
app.use(express.json());

// ضروري لتعريف المسارات
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/* =========================
   📁 FRONTEND (الموقع)
========================= */

// لازم يكون عندك مجلد اسمه public وفيه index.html
app.use(express.static(path.join(__dirname, "public")));

// الصفحة الرئيسية (إجباري)
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});


/* =========================
   ⚙️ MCP API
========================= */

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

app.post("/mcp", (req, res) => {
  const { method, params, id } = req.body;

  // Initialize
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

  // List tools
  if (method === "tools/list") {
    return res.json({
      jsonrpc: "2.0",
      id,
      result: { tools }
    });
  }

  // Call tool
  if (method === "tools/call") {
    const { name, arguments: args } = params;

    if (name === "searchDomain") {
      return res.json({
        jsonrpc: "2.0",
        id,
        result: {
          available: true,
          domain: args.domain
        }
      });
    }
  }

  return res.status(404).json({
    error: "Unknown method"
  });
});


/* =========================
   🚀 تشغيل السيرفر
========================= */

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`BeamMCP running on port ${PORT}`);
});
