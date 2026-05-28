import express from "express";

const app = express();
app.use(express.json());

// MCP tools
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

// 1) MCP endpoint (INIT + messages)
app.post("/mcp", async (req, res) => {
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

  res.status(404).json({ error: "Unknown method" });
});

app.listen(3000, () => {
  console.log("BeamMCP running on port 3000");
});
