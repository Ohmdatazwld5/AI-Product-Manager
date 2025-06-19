from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Body, Query
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
from app.agent_orchestration import (
    prioritize_features, groom_backlog, suggest_tasks, team_insights
)
from app.rag import add_context
from app.utils import init_cache
import os

app = FastAPI(
    title="AI Product Manager Agent",
    description="AI-powered PM agent with LangChain, FastAPI, and RAG.",
    version="0.1"
)

init_cache()

class FeatureList(BaseModel):
    features: List[str]

class BacklogItem(BaseModel):
    id: str
    title: str
    desc: str

class BacklogList(BaseModel):
    backlog: List[BacklogItem]

class ActivityLog(BaseModel):
    activity_log: str

# --- Favicon route ---
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    # Make sure you have a favicon.ico at the specified path, e.g., app/static/favicon.ico
    favicon_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
    return FileResponse(favicon_path)

# --- Optional: Root route redirects to docs ---
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.post("/context/add")
def add_project_context(texts: List[str] = Body(...)):
    add_context(texts)
    return {"status": "ok", "count": len(texts)}

@app.post("/prioritize-features")
def api_prioritize_features(payload: FeatureList):
    return prioritize_features(payload.features)

@app.get("/prioritize-features")
def get_prioritize_features(
    features: List[str] = Query(..., description="List of features to prioritize, e.g. features=Login&features=Signup")
):
    """
    GET endpoint for feature prioritization.
    Example: /prioritize-features?features=Login&features=SSO&features=Dark Mode
    """
    return prioritize_features(features)

@app.post("/groom-backlog")
def api_groom_backlog(payload: BacklogList):
    return groom_backlog([item.dict() for item in payload.backlog])

@app.get("/groom-backlog")
def get_groom_backlog(
    ids: List[str] = Query(..., description="List of ticket IDs"),
    titles: List[str] = Query(..., description="List of ticket titles"),
    descs: List[str] = Query(..., description="List of ticket descriptions"),
):
    """
    GET endpoint for backlog grooming.
    Example: /groom-backlog?ids=T1,T2&titles=Bug1,Bug2&descs=Fix+error,Update+UI
    The lists must be the same length and aligned by index.
    """
    if not (len(ids) == len(titles) == len(descs)):
        return {"error": "ids, titles, and descs must have the same length."}
    backlog = [{"id": i, "title": t, "desc": d} for i, t, d in zip(ids, titles, descs)]
    return groom_backlog(backlog)

@app.post("/suggest-tasks")
def api_suggest_tasks(payload: BacklogList):
    return suggest_tasks([item.dict() for item in payload.backlog])

@app.get("/suggest-tasks")
def get_suggest_tasks(
    ids: List[str] = Query(..., description="List of ticket IDs"),
    titles: List[str] = Query(..., description="List of ticket titles"),
    descs: List[str] = Query(..., description="List of ticket descriptions"),
):
    """
    GET endpoint for task suggestion.
    The lists must be the same length and aligned by index.
    """
    if not (len(ids) == len(titles) == len(descs)):
        return {"error": "ids, titles, and descs must have the same length."}
    backlog = [{"id": i, "title": t, "desc": d} for i, t, d in zip(ids, titles, descs)]
    return suggest_tasks(backlog)

@app.post("/team-insights")
def api_team_insights(payload: ActivityLog):
    return team_insights(payload.activity_log)

@app.get("/team-insights")
def get_team_insights(
    activity_log: str = Query(..., description="Activity log string")
):
    """
    GET endpoint for team insights.
    Example: /team-insights?activity_log=User+X+closed+ticket+T1
    """
    return team_insights(activity_log)