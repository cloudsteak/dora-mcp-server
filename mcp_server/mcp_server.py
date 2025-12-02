from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

app = FastAPI(
    title="DORA MCP Server",
    version="0.1.0",
    description="Minimal, resource-efficient MCP server for DORA agents."
)


# ---------------------------------------------------
# MCP MODELS
# ---------------------------------------------------

class CapabilityResponse(BaseModel):
    resources: bool
    tools: bool


class Resource(BaseModel):
    id: str
    name: str
    description: str
    mime_type: str = "application/json"


class Tool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]


class ToolCallResponse(BaseModel):
    success: bool
    result: Any
    error: Optional[str] = None


# ---------------------------------------------------
# STATIC MCP DATA (POC)
# ---------------------------------------------------

RESOURCES: List[Resource] = [
    Resource(
        id="dora.status",
        name="DORA status",
        description="Basic status information about the DORA system."
    ),
    Resource(
        id="dora.config",
        name="DORA configuration",
        description="Static configuration describing available DORA agents."
    ),
]

TOOLS: List[Tool] = [
    Tool(
        name="get_status",
        description="Returns a short status summary of DORA.",
        input_schema={"type": "object", "properties": {}},
    ),
    Tool(
        name="ping_agent",
        description="Ping a DORA agent by its ID.",
        input_schema={
            "type": "object",
            "properties": {
                "agent_id": {"type": "string"}
            },
            "required": ["agent_id"],
        },
    ),
]


# ---------------------------------------------------
# MCP ENDPOINTS
# ---------------------------------------------------

@app.get("/mcp/capabilities", response_model=CapabilityResponse)
async def get_capabilities():
    """
    Lists the server's capabilities according to the MCP protocol.
    """
    return CapabilityResponse(resources=True, tools=True)


@app.get("/mcp/resources", response_model=List[Resource])
async def list_resources():
    """
    Lists available resources.
    """
    return RESOURCES


@app.get("/mcp/resources/{resource_id}")
async def get_resource(resource_id: str):
    """
    Returns a specific resource.
    """
    if resource_id == "dora.status":
        return {
            "status": "ok",
            "version": "0.1.0",
            "description": "Minimal MCP server is running."
        }

    if resource_id == "dora.config":
        return {
            "agents_supported": ["doc-analyzer", "diagram-builder"],
            "environment": "local",
            "note": "Static config for POC."
        }

    return {"error": "resource_not_found"}


@app.get("/mcp/tools", response_model=List[Tool])
async def list_tools():
    """
    Lists available MCP tools.
    """
    return TOOLS


@app.post("/mcp/tool-call", response_model=ToolCallResponse)
async def call_tool(req: ToolCallRequest):
    """
    Executes a specific tool call.
    """
    if req.tool_name == "get_status":
        return ToolCallResponse(
            success=True,
            result={"status": "ok", "message": "DORA MCP server is operational."},
        )

    if req.tool_name == "ping_agent":
        agent_id = req.arguments.get("agent_id", "unknown")
        # Dummy backend logic – later this will be real DORA logic
        return ToolCallResponse(
            success=True,
            result={
                "agent_id": agent_id,
                "reachable": True,
                "latency_ms": 12,
            },
        )

    return ToolCallResponse(
        success=False,
        result=None,
        error=f"Unknown tool: {req.tool_name}"
    )


@app.get("/health")
async def health():
    """
    Simple healthcheck endpoint.
    """
    return {"status": "ok"}
