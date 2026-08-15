from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .agent import MODEL, agent_stages, root_agent
from .engine import FleetEngine
from .live import live_credentials_available, run_live_agent
from .models import AgentRunRequest, ApprovalResult, CampaignResult, ChangeRequest
from .scenario import load_scenario


app = FastAPI(
    title="ChangeFleet",
    version="0.1.0",
    description="Policy-gated agent fleet for enterprise data-contract changes.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

engine = FleetEngine()


@app.get("/api/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "mode": "live" if live_credentials_available() else "fixture",
        "model": MODEL,
        "agent_count": len(agent_stages),
    }


@app.get("/api/scenario")
def scenario() -> dict[str, object]:
    change, assets = load_scenario()
    return {
        "change": change.model_dump(),
        "assets": [asset.model_dump() for asset in assets],
    }


@app.get("/api/architecture")
def architecture() -> dict[str, object]:
    return {
        "root": root_agent.name,
        "model": MODEL,
        "stages": [
            {
                "name": agent.name,
                "description": agent.description,
                "tools": [tool.__name__ for tool in getattr(agent, "tools", [])],
            }
            for agent in agent_stages
        ],
        "cloud_service": "Cloud Run",
        "mutation_boundary": "explicit approval",
    }


@app.post("/api/campaigns", response_model=CampaignResult)
def run_campaign(change: ChangeRequest) -> CampaignResult:
    try:
        return engine.run(change)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/campaigns/{campaign_id}/approve", response_model=ApprovalResult)
def approve_campaign(campaign_id: str) -> ApprovalResult:
    try:
        return engine.approve(campaign_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Campaign not found") from exc


@app.post("/api/adk/run")
async def run_adk(request: AgentRunRequest) -> dict[str, str]:
    try:
        response = await run_live_agent(request.prompt, request.user_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"mode": "live", "response": response}


FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{path:path}")
    def frontend(path: str) -> FileResponse:
        candidate = FRONTEND_DIST / path
        if path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")
else:

    @app.get("/")
    def root() -> dict[str, object]:
        return {"name": "ChangeFleet API", "ui_built": False, "docs": "/docs"}
