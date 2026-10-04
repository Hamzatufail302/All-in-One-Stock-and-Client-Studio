"""
Stock Intelligence Crawler Engine
Concurrent multi-platform crawler querying live buyer search intents,
Adobe Stock direct autocomplete weights, and deep alphabet-soup expansions.
Supports both Combined Search and Platform-Specific Isolated Search.
"""

import concurrent.futures
import requests
import json
import re
import string
from urllib.parse import quote
from .marketplace_data import PLATFORMS_INFO
from .ai_prompt_engine import generate_ai_prompts, generate_stock_tags, generate_cross_marketplace_kit
from .deadline_engine import get_keyword_deadline

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

SESSION = requests.Session()
_adapter = requests.adapters.HTTPAdapter(pool_connections=25, pool_maxsize=35, max_retries=1)
SESSION.mount('https://', _adapter)
SESSION.mount('http://', _adapter)

def fetch_adobe_stock_direct(term: str) -> list:
    """Queries Adobe Stock's Fotolia autocomplete backend for exact search weights."""
    results = []
    words = term.strip().split()
    query_terms = [term]
    if len(words) > 1:
        query_terms.append(words[0])
        query_terms.append(f"{words[0]} {words[1]}")

    for q in query_terms:
        try:
            url = f"https://autocomplete.fotolia.com?query={quote(q)}&languageTag=en-US&callback=cb"
            r = SESSION.get(url, headers=HEADERS, timeout=3.5)
            m = re.search(r'cb\((.*)\)', r.text, re.DOTALL)
            if m:
                data = json.loads(m.group(1))
                for h in data.get('hits', []):
                    weight = float(h.get('weight', 0))
                    norm_score = min(max(int(weight * 100), 30), 99)
                    results.append({
                        "keyword": h['term'].strip().lower(),
                        "source": "Adobe Stock Direct",
                        "score": norm_score,
                        "raw_weight": weight
                    })
        except Exception:
            pass
    return results

def fetch_google_suggest(query: str, label: str) -> list:
    """Queries Google Suggest engine for live human search autocomplete."""
    results = []
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={quote(query)}"
        r = SESSION.get(url, headers=HEADERS, timeout=3.5)
        if r.status_code == 200:
            data = r.json()
            suggestions = data[1] if len(data) > 1 else []
            for idx, s in enumerate(suggestions):
                clean = s.strip().lower()
                score = max(96 - idx * 4, 35)
                results.append({
                    "keyword": clean,
                    "source": label,
                    "score": score
                })
    except Exception:
        pass
    return results

def fetch_bing_suggest(query: str, label: str) -> list:
    """Queries Bing open suggestion API."""
    results = []
    try:
        url = f"https://api.bing.com/osjson.aspx?query={quote(query)}"
        r = SESSION.get(url, headers=HEADERS, timeout=3.5)
        if r.status_code == 200:
            data = r.json()
            suggestions = data[1] if len(data) > 1 else []
            for idx, s in enumerate(suggestions):
                clean = s.strip().lower()
                score = max(92 - idx * 4, 30)
                results.append({
                    "keyword": clean,
                    "source": label,
                    "score": score
                })
    except Exception:
        pass
    return results

def estimate_competition_and_opportunity(keyword: str, score: int) -> dict:
    """Estimates competition level and calculates Opportunity Score."""
    words = keyword.strip().split()
    word_count = len(words)
    
    if word_count <= 1:
        competition = "High"
        opportunity = max(int(score * 0.70), 30)
    elif word_count == 2:
        competition = "Medium"
        opportunity = min(int(score * 0.90), 92)
    elif word_count in (3, 4):
        competition = "Low"
        opportunity = min(int(score * 1.05), 98)
    else:
        competition = "Low"
        opportunity = min(int(score * 0.95), 95)

    return {
        "competition": competition,
        "opportunity_score": opportunity
    }

def detect_asset_recommendation(keyword: str, target_platform: str = "all") -> dict:
    """Detects best tool & format, respecting platform context."""
    kw = keyword.lower()
    
    # Platform forced preferences
    if target_platform in ("etsy", "platform-etsy"):
        if any(w in kw for w in ["svg", "cricut", "cut file", "silhouette"]):
            return {"tool": "Illustrator (SVG)", "format": "SVG + DXF + PNG Cut File", "best_marketplace": "Etsy"}
        return {"tool": "Canva", "format": "Canva Template Link + PDF", "best_marketplace": "Etsy"}
        
    if target_platform in ("iconscout", "platform-iconscout"):
        if any(w in kw for w in ["3d", "render", "clay"]):
            return {"tool": "AI / 3D Render", "format": "3D PNG Alpha + GLTF", "best_marketplace": "IconScout"}
        if any(w in kw for w in ["lottie", "motion", "animation"]):
            return {"tool": "Lottie Motion", "format": "Lottie JSON (60fps)", "best_marketplace": "IconScout"}
        return {"tool": "Illustrator", "format": "SVG Clean Vector (24px grid)", "best_marketplace": "IconScout"}

    if target_platform in ("graphicriver", "platform-graphicriver"):
        if any(w in kw for w in ["mockup", "tshirt", "hoodie", "packaging"]):
            return {"tool": "Photoshop (PSD)", "format": "Smart-Object PSD (300 DPI)", "best_marketplace": "GraphicRiver"}
        return {"tool": "Photoshop & Illustrator", "format": "CMYK 300 DPI Print Template", "best_marketplace": "GraphicRiver"}

    # General check
    if any(w in kw for w in ["template", "planner", "invitation", "instagram", "canva", "card", "sheet", "resume"]):
        return {"tool": "Canva", "format": "Canva Link + PDF Delivery", "best_marketplace": "Etsy"}

    if any(w in kw for w in ["vector", "icon", "svg", "logo", "badge", "pattern", "clipart", "illustration", "floral", "cute", "silhouette"]):
        return {"tool": "Illustrator", "format": "AI / EPS 10 / SVG", "best_marketplace": "Adobe Stock / IconScout / Etsy"}

    if any(w in kw for w in ["mockup", "psd", "poster", "brochure", "menu", "smart object", "flyer psd"]):
        return {"tool": "Photoshop", "format": "Layered PSD (300 DPI)", "best_marketplace": "GraphicRiver / Adobe Stock"}

    if any(w in kw for w in ["video", "footage", "loop", "4k", "cinematic", "drone", "b-roll", "b roll"]):
        return {"tool": "AI Video (Runway / Sora)", "format": "4K UHD ProRes / MP4", "best_marketplace": "Adobe Stock Video"}

    if any(w in kw for w in ["photo", "background", "wallpaper", "realistic", "texture", "3d render", "render"]):
        return {"tool": "AI Image (Midjourney/Flux)", "format": "JPEG (8K) sRGB", "best_marketplace": "Adobe Stock"}

    return {"tool": "Illustrator & AI Visuals", "format": "EPS Vector / 4K Visual", "best_marketplace": "Adobe Stock / Shutterstock"}

def generate_seo_title(keyword: str, tool: str, platform: str) -> str:
    """Generates an optimal commercial stock title for search engines."""
    clean = keyword.strip().title()
    t = tool.lower()
    p = platform.lower()
    
    if "illustrator" in t or "vector" in t or "svg" in t:
        if "etsy" in p:
            return f"{clean} SVG Cut File for Cricut Silhouette Sublimation Clipart Bundle"
        return f"{clean} Isolated Vector Illustration Graphic Design Element"
    elif "photoshop" in t or "psd" in t or "mockup" in t:
        return f"{clean} Layered PSD Mockup Template with Smart Object Replacement"
    elif "canva" in t:
        return f"{clean} Editable Canva Template Bundle Social Media Printable Kit"
    elif "video" in t:
        return f"{clean} 4K Slow Motion Cinematic Stock Footage Video Loop"
    else:
        return f"{clean} High Resolution Commercial Stock Photo Background Texture"

def search_keywords(query: str, platform_filter: str = "all", limit: int = 50) -> dict:
    """
    Executes search crawl. If platform_filter is a specific platform,
    tailors queries strictly for that marketplace!
    """
    clean_query = query.strip()
    pf = platform_filter.lower() if platform_filter else "all"
    if not clean_query:
        return {
            "query": "",
            "platform": pf,
            "total": 0,
            "results": [],
            "ai_brief": {
                "ai_image_prompt": "",
                "ai_video_prompt": "",
                "illustrator_spec": {},
                "photoshop_spec": {},
                "canva_spec": {}
            },
            "tags_adobe": [],
            "tags_etsy": []
        }

    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as executor:
        if pf in ("all", "combined"):
            # Combined cross-marketplace crawl
            tasks.append(executor.submit(fetch_adobe_stock_direct, clean_query))
            tasks.append(executor.submit(fetch_google_suggest, f"adobe stock {clean_query}", "Adobe Stock"))
            tasks.append(executor.submit(fetch_google_suggest, f"shutterstock {clean_query}", "Shutterstock"))
            tasks.append(executor.submit(fetch_google_suggest, f"etsy {clean_query}", "Etsy"))
            tasks.append(executor.submit(fetch_google_suggest, f"iconscout {clean_query}", "IconScout"))
            tasks.append(executor.submit(fetch_google_suggest, f"graphicriver {clean_query}", "GraphicRiver"))
            tasks.append(executor.submit(fetch_google_suggest, f"{clean_query} vector", "Illustrator (Vector)"))
            tasks.append(executor.submit(fetch_google_suggest, f"{clean_query} canva template", "Canva"))
            tasks.append(executor.submit(fetch_google_suggest, f"{clean_query} psd mockup", "Photoshop (PSD)"))
            tasks.append(executor.submit(fetch_google_suggest, f"{clean_query} 4k footage", "AI Video"))
            tasks.append(executor.submit(fetch_bing_suggest, f"{clean_query} stock", "Bing Stock"))
        elif "adobe" in pf:
            # Strictly Adobe Stock
            tasks.append(executor.submit(fetch_adobe_stock_direct, clean_query))
            tasks.append(executor.submit(fetch_google_suggest, f"adobe stock {clean_query}", "Adobe Stock"))
            tasks.append(executor.submit(fetch_google_suggest, f"adobe stock {clean_query} vector", "Adobe Stock Vector"))
            tasks.append(executor.submit(fetch_google_suggest, f"adobe stock {clean_query} 4k footage", "Adobe Stock Video"))
            tasks.append(executor.submit(fetch_google_suggest, f"adobe stock {clean_query} ai", "Adobe Generative AI"))
            tasks.append(executor.submit(fetch_google_suggest, f"adobe stock {clean_query} background", "Adobe Stock Visual"))
            tasks.append(executor.submit(fetch_bing_suggest, f"adobe stock {clean_query}", "Adobe Bing"))
        elif "etsy" in pf:
            # Strictly Etsy
            tasks.append(executor.submit(fetch_google_suggest, f"etsy {clean_query}", "Etsy Live"))
            tasks.append(executor.submit(fetch_google_suggest, f"etsy {clean_query} canva template", "Etsy Canva"))
            tasks.append(executor.submit(fetch_google_suggest, f"etsy {clean_query} svg cut file", "Etsy SVG Cut"))
            tasks.append(executor.submit(fetch_google_suggest, f"etsy {clean_query} digital planner", "Etsy Planner"))
            tasks.append(executor.submit(fetch_google_suggest, f"etsy {clean_query} printable", "Etsy Printable"))
            tasks.append(executor.submit(fetch_bing_suggest, f"etsy {clean_query}", "Etsy Bing"))
        elif "shutter" in pf:
            # Strictly Shutterstock
            tasks.append(executor.submit(fetch_google_suggest, f"shutterstock {clean_query}", "Shutterstock Live"))
            tasks.append(executor.submit(fetch_google_suggest, f"shutterstock {clean_query} vector", "Shutterstock Vector"))
            tasks.append(executor.submit(fetch_google_suggest, f"shutterstock {clean_query} footage", "Shutterstock Video"))
            tasks.append(executor.submit(fetch_google_suggest, f"shutterstock {clean_query} photo", "Shutterstock Photo"))
            tasks.append(executor.submit(fetch_bing_suggest, f"shutterstock {clean_query}", "Shutterstock Bing"))
        elif "iconscout" in pf:
            # Strictly IconScout
            tasks.append(executor.submit(fetch_google_suggest, f"iconscout {clean_query}", "IconScout Live"))
            tasks.append(executor.submit(fetch_google_suggest, f"iconscout {clean_query} 3d icon", "IconScout 3D"))
            tasks.append(executor.submit(fetch_google_suggest, f"iconscout {clean_query} icon pack", "IconScout Icons"))
            tasks.append(executor.submit(fetch_google_suggest, f"iconscout {clean_query} lottie animation", "IconScout Lottie"))
            tasks.append(executor.submit(fetch_google_suggest, f"{clean_query} 3d icon transparent", "3D UI Asset"))
        elif "graphicriver" in pf:
            # Strictly GraphicRiver
            tasks.append(executor.submit(fetch_google_suggest, f"graphicriver {clean_query}", "GraphicRiver Live"))
            tasks.append(executor.submit(fetch_google_suggest, f"graphicriver {clean_query} flyer psd", "GraphicRiver Flyer"))
            tasks.append(executor.submit(fetch_google_suggest, f"graphicriver {clean_query} mockup", "GraphicRiver Mockup"))
            tasks.append(executor.submit(fetch_google_suggest, f"graphicriver {clean_query} brochure", "GraphicRiver Brochure"))
            tasks.append(executor.submit(fetch_google_suggest, f"envato {clean_query} psd template", "Envato PSD"))

        raw_results = []
        for future in concurrent.futures.as_completed(tasks):
            try:
                res = future.result()
                if res:
                    raw_results.extend(res)
            except Exception:
                pass

    # Deduplicate and aggregate
    aggregated = {}
    for item in raw_results:
        kw = item["keyword"].strip().lower()
        # Clean prefix markers (e.g. remove "adobe stock ", "etsy ", "graphicriver ") for cleaner keyword representation
        clean_kw = kw
        for prefix in ["adobe stock ", "etsy ", "shutterstock ", "iconscout ", "graphicriver ", "envato "]:
            if clean_kw.startswith(prefix):
                clean_kw = clean_kw[len(prefix):].strip()

        if len(clean_kw) < 3 or clean_kw == clean_query.lower() or clean_kw.startswith("http"):
            continue
        
        if clean_kw not in aggregated:
            aggregated[clean_kw] = {
                "keyword": clean_kw,
                "sources": [item["source"]],
                "score": item["score"]
            }
        else:
            if item["source"] not in aggregated[clean_kw]["sources"]:
                aggregated[clean_kw]["sources"].append(item["source"])
            aggregated[clean_kw]["score"] = max(aggregated[clean_kw]["score"], item["score"])

    # If live network requests returned limited results (e.g. offline, rate-limited, or sparse niche),
    # activate Algorithmic Commercial Stock Expansions
    if len(aggregated) < 20:
        commercial_expansions = generate_commercial_keyword_expansions(clean_query, pf)
        for item in commercial_expansions:
            kw = item["keyword"].strip().lower()
            if kw not in aggregated and kw != clean_query.lower():
                aggregated[kw] = {
                    "keyword": kw,
                    "sources": [item.get("source", "Stock Algorithm")],
                    "score": item["score"]
                }

    # Enhance items
    enhanced_list = []
    for kw, data in aggregated.items():
        source_count = len(data["sources"])
        final_score = min(data["score"] + (source_count - 1) * 3, 99)
        metrics = estimate_competition_and_opportunity(kw, final_score)
        rec = detect_asset_recommendation(kw, pf)
        seo_title = generate_seo_title(kw, rec["tool"], rec["best_marketplace"])
        
        deadline = get_keyword_deadline(kw, rec["best_marketplace"])
        
        enhanced_list.append({
            "keyword": kw,
            "demand_score": final_score,
            "competition": metrics["competition"],
            "opportunity_score": metrics["opportunity_score"],
            "sources": data["sources"],
            "source_count": source_count,
            "recommended_tool": rec["tool"],
            "recommended_format": rec["format"],
            "best_marketplace": rec["best_marketplace"],
            "suggested_title": seo_title,
            "upload_deadline": deadline["upload_deadline"],
            "upload_deadline_short": deadline["upload_deadline_short"],
            "upload_date_range": deadline["upload_date_range"],
            "is_late": deadline["is_late"],
            "days_past_deadline": deadline["days_past_deadline"],
            "days_remaining": deadline["days_remaining"],
            "timing_status": deadline["timing_status"],
            "timing_badge": deadline["timing_badge"],
            "urgency_badge_color": deadline["urgency_badge_color"],
            "status_note": deadline["status_note"]
        })

    # Sort
    sorted_results = sorted(
        enhanced_list,
        key=lambda x: (x["opportunity_score"], x["source_count"], x["demand_score"]),
        reverse=True
    )[:limit]

    top_keyword = sorted_results[0]["keyword"] if sorted_results else clean_query
    related_kws = [r["keyword"] for r in sorted_results[:20]]
    
    ai_brief = generate_ai_prompts(clean_query)
    tags_adobe = generate_stock_tags(clean_query, related_kws, "adobe_stock")
    tags_etsy = generate_stock_tags(clean_query, related_kws, "etsy")
    marketplace_kit = generate_cross_marketplace_kit(clean_query)

    return {
        "query": clean_query,
        "platform": pf,
        "total": len(sorted_results),
        "results": sorted_results,
        "ai_brief": ai_brief,
        "tags_adobe": tags_adobe,
        "tags_etsy": tags_etsy,
        "marketplace_kit": marketplace_kit
    }

def generate_commercial_keyword_expansions(query: str, platform: str) -> list:
    """Generates high-converting commercial stock longtails when network queries are sparse."""
    q = query.strip().lower()
    expansions = []
    
    # Generic commercial modifiers
    patterns = [
        (f"{q} vector illustration", "Illustrator Vector", 95),
        (f"minimalist {q} icon set", "Illustrator Icon", 94),
        (f"isolated {q} graphic element", "Stock Vector", 92),
        (f"flat {q} symbol pack", "Icon Design", 91),
        (f"modern {q} logo design", "Vector Branding", 90),
        (f"seamless {q} pattern background", "Surface Pattern", 89),
        (f"vintage retro {q} badge", "Retro Vector", 88),
        (f"{q} clipart bundle", "Digital Clipart", 87),
        (f"3d {q} claymorphism icon", "3D UI Render", 95),
        (f"glossy {q} 3d render transparent", "3D PNG Asset", 93),
        (f"isometric {q} ui kit", "3D Isometric", 91),
        (f"3d glassmorphism {q} background", "3D Wallpaper", 89),
        (f"{q} mockup smart object psd", "Photoshop PSD", 94),
        (f"realistic {q} packaging mockup", "PSD Mockup", 92),
        (f"corporate {q} flyer template psd", "Print Flyer", 90),
        (f"modern {q} trifold brochure", "Brochure Template", 88),
        (f"{q} canva template editable", "Canva Template", 96),
        (f"{q} svg cut file for cricut", "Etsy SVG Cut", 95),
        (f"{q} digital planner goodnotes", "Digital Planner", 93),
        (f"{q} printable wall art poster", "Printable Art", 91),
        (f"{q} social media instagram post", "Canva Social", 89),
        (f"cinematic {q} 4k slow motion footage", "4K Stock Video", 94),
        (f"{q} seamless b-roll video loop", "Stock Video Loop", 92),
        (f"photorealistic commercial stock {q}", "AI Stock Photo", 95),
        (f"studio lighting {q} 8k background", "Commercial Visual", 91)
    ]
    
    for phrase, source, score in patterns:
        expansions.append({
            "keyword": phrase,
            "source": source,
            "score": score
        })
    return expansions

def run_alphabet_soup_crawl(base_keyword: str, platform: str = "all") -> dict:
    """Cycles base_keyword + a..z to extract 100-250+ longtail keywords."""
    clean_kw = base_keyword.strip()
    letters = list(string.ascii_lowercase)
    found_keywords = {}

    def crawl_letter(letter):
        q = f"{clean_kw} {letter}"
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={quote(q)}"
        try:
            r = SESSION.get(url, headers=HEADERS, timeout=2.5)
            if r.status_code == 200:
                data = r.json()
                return data[1] if len(data) > 1 else []
        except Exception:
            return []
        return []

    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as executor:
        futures = {executor.submit(crawl_letter, l): l for l in letters}
        for f in concurrent.futures.as_completed(futures):
            letter = futures[f]
            try:
                suggestions = f.result()
                for idx, s in enumerate(suggestions):
                    kw = s.strip().lower()
                    if kw not in found_keywords:
                        score = max(95 - idx * 4, 30)
                        metrics = estimate_competition_and_opportunity(kw, score)
                        rec = detect_asset_recommendation(kw, platform)
                        seo_title = generate_seo_title(kw, rec["tool"], rec["best_marketplace"])
                        deadline = get_keyword_deadline(kw, rec["best_marketplace"])
                        found_keywords[kw] = {
                            "keyword": kw,
                            "letter_trigger": letter,
                            "demand_score": score,
                            "competition": metrics["competition"],
                            "opportunity_score": metrics["opportunity_score"],
                            "recommended_tool": rec["tool"],
                            "best_marketplace": rec["best_marketplace"],
                            "suggested_title": seo_title,
                            "upload_deadline": deadline["upload_deadline"],
                            "upload_date_range": deadline["upload_date_range"],
                            "is_late": deadline["is_late"],
                            "timing_status": deadline["timing_status"],
                            "timing_badge": deadline["timing_badge"]
                        }
            except Exception:
                pass

    # If network returned few or zero terms, use Alphabet Soup knowledge base generator
    if len(found_keywords) < 26:
        alphabet_seeds = {
            'a': ['app', 'aesthetic', 'abstract', 'art'],
            'b': ['bundle', 'badge', 'background', 'branding'],
            'c': ['collection', 'clean', 'canva', 'clipart'],
            'd': ['design', 'digital', 'dark', 'drawing'],
            'e': ['element', 'ecommerce', 'editable', 'eps'],
            'f': ['flat', 'flyer', 'floral', 'futuristic'],
            'g': ['graphic', 'glossy', 'geometric', 'gradient'],
            'h': ['hand drawn', 'high resolution', 'holiday', 'hoodie'],
            'i': ['icon', 'isolated', 'illustration', 'isometric'],
            'j': ['journal', 'jpeg', 'japanese', 'jewelry'],
            'k': ['kit', 'kids', 'kitchen', 'keynote'],
            'l': ['line art', 'logo', 'lottie', 'luxury'],
            'm': ['mockup', 'minimalist', 'modern', 'motion'],
            'n': ['neon', 'nature', 'newsletter', 'night'],
            'o': ['outline', 'organized', 'office', 'outdoor'],
            'p': ['pack', 'pattern', 'psd', 'planner'],
            'q': ['quality', 'quick', 'quote', 'quantum'],
            'r': ['retro', 'render', 'realistic', 'real estate'],
            's': ['set', 'svg', 'seamless', 'symbol'],
            't': ['template', 'texture', 'typography', 'tshirt'],
            'u': ['ui asset', 'ux design', 'urban', 'ultra hd'],
            'v': ['vector', 'vintage', 'video loop', 'vibrant'],
            'w': ['wallpaper', 'wedding', 'watercolor', 'web'],
            'x': ['xmas', 'xml', 'xray', 'xenon'],
            'y': ['yellow', 'young', 'yoga', 'yard sign'],
            'z': ['zero waste', 'zen', 'zoom background', 'zodiac']
        }
        for l, words in alphabet_seeds.items():
            for idx, w in enumerate(words):
                kw = f"{clean_kw.lower()} {w}"
                if kw not in found_keywords:
                    score = max(95 - idx * 5, 40)
                    metrics = estimate_competition_and_opportunity(kw, score)
                    rec = detect_asset_recommendation(kw, platform)
                    seo_title = generate_seo_title(kw, rec["tool"], rec["best_marketplace"])
                    deadline = get_keyword_deadline(kw, rec["best_marketplace"])
                    found_keywords[kw] = {
                        "keyword": kw,
                        "letter_trigger": l,
                        "demand_score": score,
                        "competition": metrics["competition"],
                        "opportunity_score": metrics["opportunity_score"],
                        "recommended_tool": rec["tool"],
                        "best_marketplace": rec["best_marketplace"],
                        "suggested_title": seo_title,
                        "upload_deadline": deadline["upload_deadline"],
                        "upload_date_range": deadline["upload_date_range"],
                        "is_late": deadline["is_late"],
                        "timing_status": deadline["timing_status"],
                        "timing_badge": deadline["timing_badge"]
                    }

    sorted_list = sorted(
        found_keywords.values(),
        key=lambda x: (x["opportunity_score"], x["demand_score"]),
        reverse=True
    )

    return {
        "base_keyword": clean_kw,
        "total": len(sorted_list),
        "results": sorted_list[:150]
    }
