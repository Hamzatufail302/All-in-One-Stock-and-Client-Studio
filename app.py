"""
StockPulse AI - Keywords & Trends Crawler for Stock & Digital Asset Creators
FastAPI Backend Application
"""

import os
import uvicorn
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from database.db import (
    init_db, save_keyword, get_saved_items, update_saved_item,
    delete_saved_item, add_search_history, get_search_history, clear_search_history,
    get_or_create_daily_goal, update_daily_goal_targets, log_daily_asset,
    update_logged_asset, delete_logged_asset, get_progress_streak_and_history,
    save_outreach_lead, get_outreach_leads, update_outreach_lead, delete_outreach_lead
)
from crawler.engine import search_keywords, run_alphabet_soup_crawl
from crawler.seasonal_trends import get_current_seasonal_intel, MONTH_DATA
from crawler.daily_calendar import get_upcoming_ranked_events
from crawler.marketplace_data import PLATFORMS_INFO
from crawler.ai_prompt_engine import (
    generate_ai_prompts, generate_stock_tags,
    generate_daily_quota_batch, PLATFORM_AI_POLICIES,
    CURATED_STYLE_REFERENCES, generate_cross_marketplace_kit
)
from crawler.android_playstore_engine import get_android_studio_data, audit_app_permissions
from crawler.client_acquisition import (
    get_client_acquisition_overview, generate_custom_pitch
)

# Initialize Database
init_db()

app = FastAPI(
    title="StockPulse AI - Stock Keywords & Trends Crawler",
    description="Local web intelligence platform for Adobe Stock, Shutterstock, Etsy, IconScout, and GraphicRiver creators.",
    version="2.0.0"
)

# Enable CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Helper for Pydantic v1 / v2 compatibility
def dump_model(model: BaseModel) -> dict:
    return model.model_dump() if hasattr(model, "model_dump") else model.dict()

# Pydantic Models
class SaveItemRequest(BaseModel):
    keyword: str
    platform: Optional[str] = "Multi"
    asset_type: Optional[str] = "All"
    demand_score: Optional[float] = 0
    competition: Optional[str] = "Medium"
    tags: Optional[str] = ""
    title_suggestion: Optional[str] = ""
    notes: Optional[str] = ""
    status: Optional[str] = "Idea"

class UpdateItemRequest(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None
    title_suggestion: Optional[str] = None

class CustomAIBriefRequest(BaseModel):
    topic: str
    style: Optional[str] = "commercial_stock"
    reference_url: Optional[str] = None

class DailyGoalUpdateRequest(BaseModel):
    target_vectors: Optional[int] = None
    target_images: Optional[int] = None
    target_videos: Optional[int] = None
    target_templates: Optional[int] = None
    notes: Optional[str] = None

class LogAssetRequest(BaseModel):
    title: str
    asset_type: str
    platform: str
    prompt_or_tags: Optional[str] = ""
    status: Optional[str] = "Created"
    date: Optional[str] = None

class UpdateLoggedAssetRequest(BaseModel):
    title: Optional[str] = None
    asset_type: Optional[str] = None
    platform: Optional[str] = None
    status: Optional[str] = None
    prompt_or_tags: Optional[str] = None

class PermissionAuditRequest(BaseModel):
    permissions: List[str]

class SaveLeadRequest(BaseModel):
    client_name: str
    channel_or_website: Optional[str] = ""
    client_niche: Optional[str] = "YouTube"
    outreach_channel: Optional[str] = "Email"
    pitch_content: Optional[str] = ""
    status: Optional[str] = "Targeted"
    followup_date: Optional[str] = ""
    notes: Optional[str] = ""

class UpdateLeadRequest(BaseModel):
    client_name: Optional[str] = None
    channel_or_website: Optional[str] = None
    client_niche: Optional[str] = None
    outreach_channel: Optional[str] = None
    pitch_content: Optional[str] = None
    status: Optional[str] = None
    followup_date: Optional[str] = None
    notes: Optional[str] = None

class GeneratePitchRequest(BaseModel):
    client_name: str
    channel_or_niche: str
    pitch_type: Optional[str] = "youtube_sample"
    custom_link: Optional[str] = None

# Routes
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    index_file = os.path.join(TEMPLATES_DIR, "index.html")
    with open(index_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api/trends/overview")
async def get_overview():
    """Returns real-time seasonal intelligence and platform highlights."""
    seasonal = get_current_seasonal_intel()
    daily_goal = get_or_create_daily_goal()
    return {
        "seasonal": seasonal,
        "platforms": PLATFORMS_INFO,
        "daily_goal": daily_goal
    }

@app.get("/api/platforms/{platform_id}")
async def get_platform_details(platform_id: str, q: Optional[str] = Query(None, description="Optional search term to dynamically change platform intelligence")):
    """Returns platform specific guidelines, isolated requirements, and curated trends or dynamic search intelligence with full score systems."""
    p_id = platform_id.lower()
    if p_id not in PLATFORMS_INFO:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    import copy
    from crawler.score_engine import enrich_concepts_with_scores, generate_dynamic_platform_concepts
    from crawler.ai_prompt_engine import generate_cross_marketplace_kit
    
    platform_data = copy.deepcopy(PLATFORMS_INFO[p_id])
    
    clean_q = q.strip() if isinstance(q, str) and q.strip() else None
    if clean_q:
        dynamic_concepts = generate_dynamic_platform_concepts(clean_q, p_id)
        platform_data["what_to_create"] = dynamic_concepts
        platform_data["active_search"] = clean_q
        platform_data["search_mode"] = True
        platform_data["cross_marketplace_kit"] = generate_cross_marketplace_kit(clean_q)
    else:
        platform_data["what_to_create"] = enrich_concepts_with_scores(platform_data.get("what_to_create", []), p_id)
        platform_data["active_search"] = None
        platform_data["search_mode"] = False
        
    return platform_data

@app.get("/api/search")
async def live_search(
    q: str = Query(..., min_length=2, description="Search term or niche"),
    platform: Optional[str] = Query("all", description="Filter by platform"),
    limit: Optional[int] = Query(50, ge=10, le=100)
):
    """Executes live multi-engine stock search crawl."""
    res = search_keywords(q, platform_filter=platform, limit=limit)
    add_search_history(q, platform, res.get("total", 0))
    return res

@app.get("/api/alphabet-soup")
async def alphabet_soup(
    base_kw: str = Query(..., min_length=2, description="Base seed keyword"),
    platform: Optional[str] = Query("all")
):
    """Executes deep 26-letter alphabet crawl."""
    res = run_alphabet_soup_crawl(base_kw, platform=platform)
    return res

@app.get("/api/seasonal")
async def seasonal_calendar():
    """Returns full 12-month stock demand radar."""
    current_intel = get_current_seasonal_intel()
    return {
        "current": current_intel,
        "all_months": MONTH_DATA
    }

@app.get("/api/daily-events")
async def get_daily_ranked_events(days: Optional[int] = Query(120, ge=30, le=365)):
    """Returns upcoming events ranked by commercial demand & optimal production lead times."""
    events = get_upcoming_ranked_events(days_ahead=days)
    return {
        "total": len(events),
        "events": events
    }

@app.get("/api/ai-daily-quota")
async def get_ai_daily_quota(
    topic: Optional[str] = Query(None, description="Theme or seed topic"),
    count: Optional[int] = Query(20, ge=10, le=30),
    ref_url: Optional[str] = Query(None, description="Custom style reference image URL")
):
    """Generates a full daily quota of 15-20 ready AI image and video prompts."""
    if not topic:
        # Default to current seasonal high-demand topic
        seasonal = get_current_seasonal_intel()
        topic = seasonal["priority_niches"][0]["theme"] if seasonal.get("priority_niches") else "future technology"
    
    prompts = generate_daily_quota_batch(seed_topic=topic, total_count=count, reference_url=ref_url)
    return {
        "topic": topic,
        "total": len(prompts),
        "prompts": prompts,
        "ai_policies": PLATFORM_AI_POLICIES,
        "presets": CURATED_STYLE_REFERENCES
    }

@app.get("/api/ai-policies")
async def get_ai_policies():
    """Returns acceptance policies for Adobe Stock, Shutterstock, Etsy, IconScout, and GraphicRiver."""
    return PLATFORM_AI_POLICIES

@app.post("/api/generate-ai-brief")
async def generate_brief(req: CustomAIBriefRequest):
    """Generates AI prompts and tool production specs for any keyword."""
    brief = generate_ai_prompts(req.topic, req.style, reference_url=req.reference_url)
    tags_adobe = generate_stock_tags(req.topic, [], "adobe_stock")
    tags_etsy = generate_stock_tags(req.topic, [], "etsy")
    return {
        "brief": brief,
        "tags_adobe": tags_adobe,
        "tags_etsy": tags_etsy,
        "presets": CURATED_STYLE_REFERENCES
    }

@app.get("/api/adobe-stock/ai-studio")
async def adobe_stock_ai_studio(
    topic: Optional[str] = Query("abstract 3d liquid waves", description="Topic or niche for Adobe Stock"),
    ref_url: Optional[str] = Query(None, description="Custom style reference image URL")
):
    """Generates precise commercial AI prompts, camera parameters, and visual style references for Adobe Stock."""
    clean_top = topic.strip() if isinstance(topic, str) and topic.strip() else "abstract 3d liquid waves"
    clean_ref = ref_url.strip() if isinstance(ref_url, str) and ref_url.strip() else None
    brief = generate_ai_prompts(clean_top, reference_url=clean_ref)
    tags_adobe = generate_stock_tags(clean_top, [], "adobe_stock")
    return {
        "topic": clean_top,
        "brief": brief,
        "tags_adobe": tags_adobe,
        "presets": CURATED_STYLE_REFERENCES
    }

@app.get("/api/marketplace-kit")
async def get_marketplace_kit(
    keyword: str = Query(..., description="Target keyword or concept"),
    ref_url: Optional[str] = Query(None, description="Optional style reference URL")
):
    """Returns the complete Version 2 Cross-Marketplace Upload Kit across all 5 platforms."""
    clean_kw = keyword.strip() if isinstance(keyword, str) else str(keyword).strip()
    clean_ref = ref_url.strip() if isinstance(ref_url, str) and ref_url.strip() else None
    kit = generate_cross_marketplace_kit(clean_kw, reference_url=clean_ref)
    brief = generate_ai_prompts(clean_kw, reference_url=clean_ref)
    return {
        "keyword": clean_kw,
        "kit": kit,
        "brief": brief,
        "policies": PLATFORM_AI_POLICIES
    }

# --- DAILY GOAL & PROGRESS TRACKER ENDPOINTS ---

@app.get("/api/daily-goals/today")
async def get_today_goal(date: Optional[str] = Query(None)):
    """Gets daily goals and completed asset progress for a given date or today."""
    d_val = date if isinstance(date, str) else None
    goal = get_or_create_daily_goal(d_val)
    return goal

@app.post("/api/daily-goals/today")
async def set_today_targets(req: DailyGoalUpdateRequest, date: Optional[str] = Query(None)):
    """Sets or updates quota targets for today."""
    d_val = date if isinstance(date, str) else None
    goal = get_or_create_daily_goal(d_val)
    updates = {k: v for k, v in dump_model(req).items() if v is not None}
    update_daily_goal_targets(goal['date'], updates)
    return get_or_create_daily_goal(goal['date'])

@app.post("/api/daily-goals/log-asset")
async def log_asset(req: LogAssetRequest):
    """Logs an asset created or uploaded towards the daily goal."""
    asset_id = log_daily_asset(dump_model(req))
    return {"success": True, "id": asset_id}

@app.put("/api/daily-goals/asset/{asset_id}")
async def update_asset_log(asset_id: int, req: UpdateLoggedAssetRequest):
    """Updates status or details of a logged asset."""
    updates = {k: v for k, v in dump_model(req).items() if v is not None}
    success = update_logged_asset(asset_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Asset log not found")
    return {"success": True}

@app.delete("/api/daily-goals/asset/{asset_id}")
async def remove_asset_log(asset_id: int):
    """Deletes an asset from the daily log."""
    delete_logged_asset(asset_id)
    return {"success": True}

@app.get("/api/daily-goals/streak")
async def get_streak_and_history(days: Optional[int] = Query(14, ge=7, le=60)):
    """Returns historical completion streak."""
    return get_progress_streak_and_history(days)

# --- PRODUCTION QUEUE ENDPOINTS ---

@app.post("/api/saved-keywords")
async def create_saved_item(item: SaveItemRequest):
    """Saves a keyword to the user's production queue."""
    item_id = save_keyword(dump_model(item))
    return {"success": True, "id": item_id}

@app.get("/api/saved-keywords")
async def list_saved_items(
    status: Optional[str] = Query(None),
    platform: Optional[str] = Query(None)
):
    """Retrieves all saved items in the production queue."""
    s_val = status if isinstance(status, str) else None
    p_val = platform if isinstance(platform, str) else None
    items = get_saved_items(status=s_val, platform=p_val)
    return {"total": len(items), "items": items}

@app.put("/api/saved-keywords/{item_id}")
async def update_item(item_id: int, req: UpdateItemRequest):
    """Updates status or notes of an item in the queue."""
    updates = {k: v for k, v in dump_model(req).items() if v is not None}
    success = update_saved_item(item_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found or no changes")
    return {"success": True}

@app.delete("/api/saved-keywords/{item_id}")
async def delete_item(item_id: int):
    """Deletes an item from the production queue."""
    delete_saved_item(item_id)
    return {"success": True}

@app.get("/api/search-history")
async def list_history():
    """Returns recent search queries."""
    history = get_search_history(25)
    return {"history": history}

@app.delete("/api/search-history")
async def delete_history():
    """Clears search history."""
    clear_search_history()
    return {"success": True}

# --- ANDROID PLAY STORE STUDIO ENDPOINTS ---

@app.get("/api/android/studio")
async def get_android_studio(q: Optional[str] = Query(None)):
    """Returns trending Android app blueprints, store asset specs, and policy guidelines."""
    clean_q = q.strip() if isinstance(q, str) and q.strip() else None
    return get_android_studio_data(clean_q)

@app.post("/api/android/audit-permissions")
async def audit_permissions_endpoint(req: PermissionAuditRequest):
    """Audits requested permissions against Google Play Developer Policies."""
    return audit_app_permissions(req.permissions)

# --- VIDEO CLIENT ACQUISITION & OUTREACH ENDPOINTS ---

@app.get("/api/client-acquisition/overview")
async def get_client_acquisition_data():
    """Returns complete video editing client acquisition playbooks, market demands, scripts, and retainer guides."""
    return get_client_acquisition_overview()

@app.post("/api/client-acquisition/generate-pitch")
async def generate_pitch_endpoint(req: GeneratePitchRequest):
    """Generates personalized high-conversion pitch scripts tailored for video editing outreach."""
    pitch = generate_custom_pitch(
        client_name=req.client_name,
        channel_or_niche=req.channel_or_niche,
        pitch_type=req.pitch_type or "youtube_sample",
        custom_link=req.custom_link
    )
    return pitch

@app.get("/api/client-acquisition/leads")
async def list_outreach_leads(status: Optional[str] = Query(None)):
    """Returns all tracked video editing outreach leads in the CRM pipeline."""
    s_val = status.strip() if isinstance(status, str) and status.strip() and status != "All" else None
    leads = get_outreach_leads(status=s_val)
    return {"total": len(leads), "leads": leads}

@app.post("/api/client-acquisition/leads")
async def add_outreach_lead(req: SaveLeadRequest):
    """Saves a new prospective client lead into the video outreach pipeline."""
    lead_id = save_outreach_lead(dump_model(req))
    return {"success": True, "lead_id": lead_id}

@app.put("/api/client-acquisition/leads/{lead_id}")
async def update_outreach_lead_endpoint(lead_id: int, req: UpdateLeadRequest):
    """Updates status, followup date, pitch or notes for a lead."""
    updates = {k: v for k, v in dump_model(req).items() if v is not None}
    success = update_outreach_lead(lead_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Lead not found or no changes made")
    return {"success": True}

@app.delete("/api/client-acquisition/leads/{lead_id}")
async def remove_outreach_lead(lead_id: int):
    """Deletes a lead from the outreach CRM pipeline."""
    success = delete_outreach_lead(lead_id)
    return {"success": success}

if __name__ == "__main__":
    print("=" * 60)
    print(">> StockPulse AI - Keywords & Trends Crawler Starting...")
    print(">> Local Server: http://localhost:8000")
    print("=" * 60)
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
