import { useState } from "react";

const sections = [
  {
    id: "scope",
    num: "01",
    title: "Project Scope",
    titleAr: "نطاق المشروع",
    icon: "◈",
    content: [
      {
        type: "paragraph",
        text: "Building an AI Agent system operating via MCP (Model Context Protocol). The system bridges the Claude Desktop user interface with the Beam.cloud serverless computing platform. The goal is to automate file and data processing workflows, enabling the AI to dispatch heavy processing tasks to Beam and manage results seamlessly.",
      },
    ],
  },
  {
    id: "architecture",
    num: "02",
    title: "Architecture & Tech Stack",
    titleAr: "البنية التقنية",
    icon: "◎",
    content: [
      {
        type: "stack",
        items: [
          { label: "Core Language", value: "Python 3.10+", tag: "RUNTIME" },
          { label: "Connection Protocol", value: "FastMCP Library", tag: "PROTOCOL" },
          { label: "Cloud Infrastructure", value: "Beam SDK", tag: "CLOUD" },
          { label: "Environment Management", value: ".env / BEAM_API_KEY / BEAM_CLIENT_ID", tag: "CONFIG" },
          { label: "Containerization", value: "Docker — Full Containerized Deployment", tag: "DEPLOY" },
        ],
      },
    ],
  },
  {
    id: "functional",
    num: "03",
    title: "Functional Requirements",
    titleAr: "المواصفات الوظيفية",
    icon: "◉",
    content: [
      {
        type: "tools",
        items: [
          {
            name: "process_file(file_path)",
            desc: "Accept local file path → validate existence → upload to Beam workspace → launch cloud task.",
            badge: "TOOL",
          },
          {
            name: "get_task_result(task_id)",
            desc: "Query task status [Pending / Running / Completed / Failed] and retrieve final output upon completion.",
            badge: "TOOL",
          },
          {
            name: "list_recent_tasks()",
            desc: "Display a log of the last 5 executed operations and their current status.",
            badge: "TOOL",
          },
        ],
      },
    ],
  },
  {
    id: "workflow",
    num: "04",
    title: "Workflow Logic",
    titleAr: "سير العمل التقني",
    icon: "⬡",
    content: [
      {
        type: "workflow",
        steps: [
          {
            step: "AUTH",
            title: "Authentication",
            desc: "API keys are validated at server startup before any task execution.",
          },
          {
            step: "DISPATCH",
            title: "Async Execution",
            desc: "System dispatches task to Beam and immediately returns task_id to the user, then monitors status in background to prevent chat interface timeout.",
          },
          {
            step: "FORMAT",
            title: "Output Formatting",
            desc: "Beam outputs (JSON or plain text) are transformed into clean, readable Markdown in the user interface.",
          },
        ],
      },
    ],
  },
  {
    id: "nonfunctional",
    num: "05",
    title: "Non-Functional Requirements",
    titleAr: "متطلبات الجودة",
    icon: "◫",
    content: [
      {
        type: "nfr",
        items: [
          {
            category: "SECURITY",
            points: [
              "Block execution of unauthorized code outside the defined workspace.",
              "Encrypted handling of directory access.",
            ],
          },
          {
            category: "ERROR HANDLING",
            points: [
              "Automatic Retry Mechanism on temporary API connection failures.",
              "Clear error codes on failure: BEAM_CONN_ERR, FILE_NOT_FOUND.",
            ],
          },
          {
            category: "DOCUMENTATION",
            points: [
              "README.md: dependencies installation (requirements.txt).",
              "Environment variable configuration guide.",
              "Server startup & Claude Desktop connection steps.",
            ],
          },
          {
            category: "TESTING",
            points: [
              "Attach test_mcp.py script to verify Beam connection integrity.",
            ],
          },
        ],
      },
    ],
  },
  {
    id: "deliverables",
    num: "06",
    title: "Deliverables",
    titleAr: "مخرجات التسليم",
    icon: "◰",
    content: [
      {
        type: "deliverables",
        items: [
          { icon: "⟨/⟩", label: "Source Code", desc: "Clean, fully documented codebase with inline comments." },
          { icon: "◻", label: "Dockerfile", desc: "Containerized deployment ensuring cross-environment compatibility." },
          { icon: "⊞", label: "Operation Guide", desc: "Step-by-step setup, configuration, and connection instructions." },
          { icon: "◷", label: "14-Day Support", desc: "Programmer commits to fixing any bugs within 14 days of final delivery." },
        ],
      },
    ],
  },
];

export default function BeamMCPSpec() {
  const [active, setActive] = useState("scope");

  const activeSection = sections.find((s) => s.id === active);

  return (
    <div style={{
      fontFamily: "'Courier New', 'Lucida Console', monospace",
      background: "#0a0a0f",
      minHeight: "100vh",
      color: "#c8d0e0",
      display: "flex",
      flexDirection: "column",
    }}>
      {/* Header */}
      <header style={{
        borderBottom: "1px solid #1e2535",
        padding: "24px 40px 20px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        background: "linear-gradient(180deg, #0d0f1a 0%, #0a0a0f 100%)",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <div style={{
            width: 44, height: 44,
            border: "1px solid #2a3550",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 20, color: "#4a90d9",
            background: "rgba(74,144,217,0.06)",
            letterSpacing: "-1px",
          }}>⬡</div>
          <div>
            <div style={{ fontSize: 18, fontWeight: "bold", letterSpacing: "4px", color: "#e8edf5", textTransform: "uppercase" }}>
              BeamMCP
            </div>
            <div style={{ fontSize: 10, color: "#3d5080", letterSpacing: "3px", marginTop: 2 }}>
              DATA WORKFLOW AUTOMATION AGENT
            </div>
          </div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: 10, color: "#3d5080", letterSpacing: "2px" }}>TECHNICAL SPECIFICATION</div>
          <div style={{ fontSize: 10, color: "#2a3d60", marginTop: 2, letterSpacing: "1px" }}>REV 1.0 · MCP-BEAM PROTOCOL</div>
        </div>
      </header>

      <div style={{ display: "flex", flex: 1 }}>
        {/* Sidebar */}
        <nav style={{
          width: 220,
          borderRight: "1px solid #141926",
          padding: "24px 0",
          flexShrink: 0,
          background: "rgba(10,12,22,0.8)",
        }}>
          {sections.map((s) => (
            <button
              key={s.id}
              onClick={() => setActive(s.id)}
              style={{
                width: "100%", textAlign: "left",
                background: active === s.id ? "rgba(74,144,217,0.08)" : "transparent",
                border: "none",
                borderLeft: active === s.id ? "2px solid #4a90d9" : "2px solid transparent",
                padding: "12px 20px",
                cursor: "pointer",
                color: active === s.id ? "#7ab8f5" : "#3d5080",
                display: "flex", alignItems: "center", gap: 12,
                transition: "all 0.15s",
                fontSize: 11,
                letterSpacing: "1px",
              }}
            >
              <span style={{ color: active === s.id ? "#4a90d9" : "#253045", fontSize: 13 }}>{s.icon}</span>
              <div>
                <div style={{ fontWeight: active === s.id ? "bold" : "normal" }}>{s.num}</div>
                <div style={{ fontSize: 10, marginTop: 2, lineHeight: 1.4, color: active === s.id ? "#7ab8f5" : "#2d3e5a" }}>
                  {s.title.toUpperCase()}
                </div>
              </div>
            </button>
          ))}

          <div style={{ margin: "32px 20px 0", borderTop: "1px solid #141926", paddingTop: 20 }}>
            <div style={{ fontSize: 9, color: "#1e2a40", letterSpacing: "2px", marginBottom: 8 }}>COMPONENTS</div>
            {["Claude Desktop", "MCP Server", "Beam.cloud", "Docker Container"].map((c) => (
              <div key={c} style={{
                fontSize: 10, color: "#253045", padding: "4px 0",
                display: "flex", alignItems: "center", gap: 6,
              }}>
                <span style={{ color: "#1e3060" }}>▸</span> {c}
              </div>
            ))}
          </div>
        </nav>

        {/* Main Content */}
        <main style={{ flex: 1, padding: "36px 48px", overflowY: "auto" }}>
          {activeSection && (
            <div>
              {/* Section Header */}
              <div style={{ marginBottom: 36 }}>
                <div style={{ fontSize: 10, color: "#2a3d60", letterSpacing: "4px", marginBottom: 8 }}>
                  SECTION {activeSection.num}
                </div>
                <div style={{ display: "flex", alignItems: "baseline", gap: 16 }}>
                  <h1 style={{
                    fontSize: 28, fontWeight: "bold", color: "#d0daea",
                    letterSpacing: "2px", margin: 0, textTransform: "uppercase",
                  }}>
                    {activeSection.title}
                  </h1>
                  <span style={{ fontSize: 13, color: "#2a3d60", letterSpacing: "2px" }}>
                    [{activeSection.titleAr}]
                  </span>
                </div>
                <div style={{ width: 60, height: 1, background: "#4a90d9", marginTop: 12, opacity: 0.5 }} />
              </div>

              {/* Content */}
              {activeSection.content.map((block, i) => (
                <div key={i}>
                  {block.type === "paragraph" && (
                    <p style={{
                      fontSize: 13, lineHeight: 1.9, color: "#8090a8",
                      maxWidth: 680, margin: 0,
                      borderLeft: "2px solid #1a2540",
                      paddingLeft: 20,
                    }}>{block.text}</p>
                  )}

                  {block.type === "stack" && (
                    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                      {block.items.map((item, j) => (
                        <div key={j} style={{
                          display: "flex", alignItems: "center",
                          border: "1px solid #141926",
                          background: "rgba(20,25,45,0.5)",
                          padding: "14px 20px",
                          gap: 20,
                        }}>
                          <span style={{
                            fontSize: 9, letterSpacing: "2px", color: "#2a4070",
                            background: "rgba(42,64,112,0.2)",
                            border: "1px solid #1a3060",
                            padding: "3px 8px",
                            whiteSpace: "nowrap",
                            minWidth: 80, textAlign: "center",
                          }}>{item.tag}</span>
                          <div style={{ fontSize: 11, color: "#4a6090", minWidth: 160 }}>{item.label}</div>
                          <div style={{ fontSize: 12, color: "#90aad0", fontWeight: "bold", letterSpacing: "1px" }}>{item.value}</div>
                        </div>
                      ))}
                    </div>
                  )}

                  {block.type === "tools" && (
                    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                      {block.items.map((tool, j) => (
                        <div key={j} style={{
                          border: "1px solid #141926",
                          background: "rgba(16,22,40,0.6)",
                          padding: "20px 24px",
                          position: "relative",
                        }}>
                          <div style={{
                            position: "absolute", top: -1, right: 20,
                            fontSize: 9, letterSpacing: "2px",
                            background: "#4a90d9", color: "#0a0a0f",
                            padding: "2px 10px",
                          }}>{tool.badge}</div>
                          <div style={{
                            fontSize: 13, color: "#7ab8f5", fontWeight: "bold",
                            marginBottom: 10, letterSpacing: "1px",
                          }}>{tool.name}</div>
                          <div style={{ fontSize: 12, color: "#5a7090", lineHeight: 1.7 }}>{tool.desc}</div>
                        </div>
                      ))}
                    </div>
                  )}

                  {block.type === "workflow" && (
                    <div style={{ display: "flex", gap: 0, flexWrap: "wrap" }}>
                      {block.steps.map((step, j) => (
                        <div key={j} style={{ display: "flex", alignItems: "stretch" }}>
                          <div style={{
                            border: "1px solid #141926",
                            background: "rgba(16,22,40,0.6)",
                            padding: "24px 28px",
                            width: 200,
                          }}>
                            <div style={{
                              fontSize: 9, letterSpacing: "3px", color: "#4a90d9",
                              marginBottom: 10,
                            }}>{step.step}</div>
                            <div style={{ fontSize: 13, color: "#c0d0e8", fontWeight: "bold", marginBottom: 8 }}>
                              {step.title}
                            </div>
                            <div style={{ fontSize: 11, color: "#4a6080", lineHeight: 1.7 }}>{step.desc}</div>
                          </div>
                          {j < block.steps.length - 1 && (
                            <div style={{
                              display: "flex", alignItems: "center",
                              padding: "0 8px", color: "#1e3060", fontSize: 18,
                            }}>→</div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}

                  {block.type === "nfr" && (
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                      {block.items.map((item, j) => (
                        <div key={j} style={{
                          border: "1px solid #141926",
                          background: "rgba(16,22,40,0.6)",
                          padding: "20px 24px",
                        }}>
                          <div style={{
                            fontSize: 9, letterSpacing: "3px", color: "#4a90d9",
                            marginBottom: 14, paddingBottom: 8,
                            borderBottom: "1px solid #141926",
                          }}>{item.category}</div>
                          {item.points.map((p, k) => (
                            <div key={k} style={{
                              fontSize: 11, color: "#5a7090", lineHeight: 1.7,
                              display: "flex", gap: 8, marginBottom: 6,
                            }}>
                              <span style={{ color: "#2a4070", flexShrink: 0 }}>▸</span>
                              <span>{p}</span>
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  )}

                  {block.type === "deliverables" && (
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                      {block.items.map((item, j) => (
                        <div key={j} style={{
                          border: "1px solid #141926",
                          background: "rgba(16,22,40,0.6)",
                          padding: "22px 24px",
                          display: "flex", gap: 16, alignItems: "flex-start",
                        }}>
                          <div style={{
                            fontSize: 20, color: "#2a4070", flexShrink: 0, marginTop: 2,
                          }}>{item.icon}</div>
                          <div>
                            <div style={{ fontSize: 12, color: "#90aad0", fontWeight: "bold", marginBottom: 6, letterSpacing: "1px" }}>
                              {item.label.toUpperCase()}
                            </div>
                            <div style={{ fontSize: 11, color: "#4a6080", lineHeight: 1.7 }}>{item.desc}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </main>
      </div>

      {/* Footer */}
      <footer style={{
        borderTop: "1px solid #0f1520",
        padding: "12px 40px",
        display: "flex", justifyContent: "space-between", alignItems: "center",
        background: "#080b14",
      }}>
        <div style={{ fontSize: 9, color: "#1a2540", letterSpacing: "3px" }}>
          BEAMMCP · MCP-BEAM PROTOCOL · DATA WORKFLOW AUTOMATION
        </div>
        <div style={{ display: "flex", gap: 24 }}>
          {["Python 3.10+", "FastMCP", "Beam SDK", "Docker"].map((t) => (
            <span key={t} style={{ fontSize: 9, color: "#1e3050", letterSpacing: "2px" }}>{t}</span>
          ))}
        </div>
      </footer>
    </div>
  );
}
