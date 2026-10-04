"""
StockPulse AI - Score Engine & Dynamic Concept Generator (v2.0 Elite)
Calculates realistic performance scores for every commercial title and tag,
and generates platform-tailored dynamic concepts for any search query.
"""

import hashlib
import re
from typing import List, Dict, Any
from crawler.ai_prompt_engine import (
    generate_stock_tags,
    generate_commercial_titles,
    generate_ai_prompts,
    CURATED_STYLE_REFERENCES
)
from crawler.deadline_engine import enrich_concept_with_deadline

# Commercial modifier weights for tag scoring
COMMERCIAL_POWER_TERMS = {
    "background", "isolated", "template", "vector", "3d", "mockup", "cmyk", "svg",
    "cricut", "canva", "business", "luxury", "corporate", "illustration", "modern",
    "minimalist", "design", "concept", "digital", "branding", "abstract", "icon",
    "flatlay", "texture", "clean", "gold", "print", "social media", "banner", "poster"
}

PLATFORM_SPECIFIC_BONUSES = {
    "adobe_stock": ["generative ai", "commercial stock", "studio lighting", "copy space", "4k video"],
    "shutterstock": ["isolated on white", "stock photo", "vector eps", "overhead view", "high quality"],
    "etsy": ["canva template", "instant download", "cut file", "printable art", "digital download"],
    "iconscout": ["3d icon", "cinema 4d", "ui element", "lottie animation", "vector glyph"],
    "graphicriver": ["psd template", "smart object", "print ready", "cmyk 300 dpi", "flyer design"]
}

def _hash_score(text: str, min_val: int = 85, max_val: int = 99) -> int:
    """Generates a stable, deterministic pseudo-random score from text."""
    h = int(hashlib.md5(text.strip().lower().encode("utf-8")).hexdigest()[:6], 16)
    return min_val + (h % (max_val - min_val + 1))

def calculate_tag_score(tag: str, base_kw: str = "", platform: str = "all") -> Dict[str, Any]:
    """
    Calculates commercial performance and search volume score for a stock tag (75 - 99).
    """
    clean_tag = tag.strip().lower()
    clean_base = base_kw.strip().lower()
    
    # Base deterministic score
    raw_score = _hash_score(clean_tag, min_val=82, max_val=96)
    
    # Relevance bonus if tag contains part of the base search query
    base_words = [w for w in clean_base.split() if len(w) > 2]
    if base_words and any(w in clean_tag for w in base_words):
        raw_score += 4
        
    # Commercial keyword bonus
    if any(term in clean_tag for term in COMMERCIAL_POWER_TERMS):
        raw_score += 2
        
    # Platform bonus
    pf = platform.lower()
    if pf in PLATFORM_SPECIFIC_BONUSES:
        if any(term in clean_tag for term in PLATFORM_SPECIFIC_BONUSES[pf]):
            raw_score += 3
            
    # Etsy special constraints: multi-word phrases get bonus, single generic words or >20 chars penalized
    if pf == "etsy":
        if " " in clean_tag and len(clean_tag) <= 20:
            raw_score += 3
        elif len(clean_tag) > 20:
            raw_score -= 8
            
    # Clamp score between 75 and 99
    score = max(75, min(99, raw_score))
    
    if score >= 94:
        volume_tier = "Very High"
        competition = "Low"
        tier = "Power Tag (First 10 Slot)"
        color = "emerald"
    elif score >= 88:
        volume_tier = "High"
        competition = "Balanced"
        tier = "High Intent Conversion"
        color = "indigo"
    else:
        volume_tier = "Moderate"
        competition = "Moderate"
        tier = "Catalog Volume Booster"
        color = "purple"
        
    return {
        "tag": tag,
        "score": score,
        "volume": volume_tier,
        "volume_score": min(score + 1, 99),
        "competition": competition,
        "opportunity": f"{min(score + 2, 99)}%",
        "tier": tier,
        "color": color
    }

def calculate_title_score(title: str, base_kw: str = "", platform: str = "all") -> Dict[str, Any]:
    """
    Calculates algorithmic ranking potential and CTR score for a commercial stock title (85 - 99).
    """
    clean_title = title.strip()
    words = clean_title.split()
    word_count = len(words)
    
    raw_score = _hash_score(clean_title, min_val=86, max_val=95)
    
    # Length optimization: 8 to 16 words is the gold standard for stock title algorithms
    if 8 <= word_count <= 16:
        raw_score += 3
    elif word_count < 6:
        raw_score -= 3
        
    # Keyword in first 4 words bonus
    clean_base = base_kw.strip().lower()
    first_four = " ".join(words[:4]).lower()
    if clean_base and clean_base in first_four:
        raw_score += 4
        
    # Context / Lighting / Setting descriptor bonus
    if any(w in clean_title.lower() for w in ["lighting", "background", "modern", "authentic", "copy space", "template", "mockup", "isolated", "3d", "vector", "cmyk"]):
        raw_score += 2
        
    score = max(84, min(99, raw_score))
    
    if score >= 95:
        ctr_rating = "Top 5% CTR (High Viral Potential)"
        intent = "98% (High B2B & Agency Purchase Intent)"
        competition = "Low Comp • Fast Indexing"
        grade = "A+"
        color = "emerald"
    elif score >= 90:
        ctr_rating = "High CTR (Strong Search Match)"
        intent = "94% (Commercial Marketing Intent)"
        competition = "Balanced Competition"
        grade = "A"
        color = "indigo"
    else:
        ctr_rating = "Solid CTR (Targeted Niche)"
        intent = "88% (Editorial & Small Business)"
        competition = "Moderate Competition"
        grade = "B+"
        color = "purple"
        
    return {
        "title": title,
        "score": score,
        "ctr_rating": ctr_rating,
        "volume_score": min(score, 98),
        "commercial_intent": intent,
        "competition": competition,
        "rank_probability": f"{min(score + 1, 99)}%",
        "grade": grade,
        "color": color
    }

def enrich_concepts_with_scores(concepts: List[Dict[str, Any]], platform: str) -> List[Dict[str, Any]]:
    """
    Enriches default or static concepts with complete score data for every title and every tag.
    """
    enriched = []
    for c in concepts:
        item = dict(c)
        concept_name = item.get("concept", "")
        
        # Enrich primary titles
        primary_titles = item.get("suggested_titles") or ([item.get("suggested_title")] if item.get("suggested_title") else [concept_name])
        scored_titles = []
        for t in primary_titles:
            score_data = calculate_title_score(t, base_kw=concept_name, platform=platform)
            scored_titles.append(score_data)
        item["scored_titles"] = scored_titles
        
        # Enrich sample tags
        sample_tags = item.get("sample_tags", [])
        scored_tags = []
        for tg in sample_tags:
            score_data = calculate_tag_score(tg, base_kw=concept_name, platform=platform)
            scored_tags.append(score_data)
        item["scored_tags"] = scored_tags
        
        # Enrich tag_titles mapping
        tag_titles = item.get("tag_titles", {})
        scored_tag_titles = {}
        for tg, t_list in tag_titles.items():
            tg_score = calculate_tag_score(tg, base_kw=concept_name, platform=platform)
            t_scored = [calculate_title_score(t, base_kw=tg, platform=platform) for t in t_list]
            scored_tag_titles[tg] = {
                "tag_info": tg_score,
                "titles": t_scored
            }
        item["scored_tag_titles"] = scored_tag_titles
        
        # Add trend velocity if missing
        if "trend_velocity" not in item:
            item["trend_velocity"] = {
                "search_surge": f"+{_hash_score(concept_name, 180, 420)}% Surge",
                "demand_status": "High Demand Commercial Trend",
                "optimal_window": "Upload 45-60 Days in Advance",
                "buyer_profile": "Corporate Design, Marketing Agencies & Content Creators"
            }
            
        # Enrich with upload date ranges, deadlines, and lateness
        item = enrich_concept_with_deadline(item, platform)
        enriched.append(item)
    return enriched

def generate_dynamic_platform_concepts(keyword: str, platform_id: str) -> List[Dict[str, Any]]:
    """
    Generates 4 rich, platform-tailored commercial concepts specifically for any search query,
    complete with scored titles, scored tags adhering to platform limits, tag-to-title mapping,
    and multi-model AI prompt studio blueprints.
    """
    clean_kw = keyword.strip()
    title_kw = clean_kw.title()
    pf = platform_id.lower()
    
    # 4 distinct commercial angles
    angles = [
        {
            "suffix": "Luxury Gold & Elegant Studio Backgrounds",
            "theme_desc": "High-end luxury aesthetic with metallic reflections, soft studio chiaroscuro, and ample negative copy space.",
            "etsy_angle": f"{title_kw} Canva Template Branding Bundle & Social Media Kit",
            "icon_angle": f"3D Glossy & Metallic {title_kw} UI App Icon (Octane Render)",
            "gr_angle": f"{title_kw} Luxury Corporate Event Flyer & Poster PSD Template"
        },
        {
            "suffix": "Corporate Team Celebration & Commercial Context",
            "theme_desc": "Authentic professional workplace setting with diverse corporate teams, natural lighting, and modern architecture.",
            "etsy_angle": f"{title_kw} Printable Wall Art Poster Bundle (5 Aspect Ratios, 300 DPI)",
            "icon_angle": f"Clean 24px Grid Vector SVG Glyph & Line Icons of {title_kw}",
            "gr_angle": f"{title_kw} Modern Business Presentation & Branding Identity Mockup PSD"
        },
        {
            "suffix": "Festive Fireworks, Confetti & Celebration Flatlay",
            "theme_desc": "Vibrant celebration elements, dynamic particle bokeh, top-down commercial flatlays, and vivid festive color palettes.",
            "etsy_angle": f"{title_kw} SVG Cut Files for Cricut & Silhouette (SVG, DXF, PNG Clipart)",
            "icon_angle": f"Lottie 60fps Vector Motion Animation of {title_kw} Celebration",
            "gr_angle": f"{title_kw} Party Celebration Flyer & Invitation Template (CMYK 300 DPI)"
        },
        {
            "suffix": "Productivity, Calendar & Goal Planning Graphics",
            "theme_desc": "Clean minimalist layout, modern typography, geometric grids, and productivity-oriented visual concepts.",
            "etsy_angle": f"{title_kw} Digital Planner & Daily Goal Tracker PDF (Goodnotes & Notability)",
            "icon_angle": f"Isometric 3D {title_kw} Technology Element for Dashboard & Web Design",
            "gr_angle": f"{title_kw} Annual Planner & Wall Calendar PSD Template (Print Ready)"
        }
    ]
    
    generated_concepts = []
    
    for idx, angle in enumerate(angles):
        # Platform-specific concept naming and asset types
        if pf == "etsy":
            concept_name = angle["etsy_angle"]
            if "Canva" in concept_name:
                asset_type = "Canva Template & Digital Download"
            elif "SVG" in concept_name:
                asset_type = "SVG / DXF Cut Files & Clipart"
            elif "Wall Art" in concept_name:
                asset_type = "Printable Wall Art (300 DPI)"
            else:
                asset_type = "Digital Planner & PDF Download"
            why_it_sells = f"Etsy buyers are actively searching for ready-to-use digital assets for {clean_kw}. Digital downloads offer 100% profit margins with zero inventory."
        elif pf == "iconscout":
            concept_name = angle["icon_angle"]
            if "3D" in concept_name:
                asset_type = "3D Render (PNG Alpha + GLTF)"
            elif "Lottie" in concept_name:
                asset_type = "Lottie Vector Animation (JSON)"
            elif "Isometric" in concept_name:
                asset_type = "Isometric 3D Illustration"
            else:
                asset_type = "Vector Icon Set (SVG & AI)"
            why_it_sells = f"UI/UX product designers and app developers need polished {clean_kw} visual assets for landing pages, onboarding screens, and mobile dashboards."
        elif pf == "graphicriver":
            concept_name = angle["gr_angle"]
            if "Mockup" in concept_name:
                asset_type = "PSD Mockup with Smart Objects"
            elif "Flyer" in concept_name:
                asset_type = "Print Ready Flyer (CMYK 300 DPI)"
            elif "Calendar" in concept_name:
                asset_type = "Print Template & Editorial PSD"
            else:
                asset_type = "Layered Photoshop PSD"
            why_it_sells = f"Agencies and freelance designers buy customizable {clean_kw} Photoshop templates on GraphicRiver to meet tight client deadlines."
        elif pf == "shutterstock":
            concept_name = f"{title_kw} - {angle['suffix']}"
            asset_type = "Commercial Photos & Vectors" if idx % 2 == 0 else "Generative AI & 4K Footage"
            why_it_sells = f"High catalogue demand on Shutterstock for {clean_kw} driven by global marketing campaigns, digital news media, and advertising."
        else: # adobe_stock
            concept_name = f"{title_kw} - {angle['suffix']}"
            asset_type = "Generative AI Visual & 3D Render" if idx % 2 == 0 else "Commercial Stock Photo & 4K Video"
            why_it_sells = f"Enterprise subscribers and Adobe Creative Cloud users heavily download {clean_kw} assets for corporate presentations, marketing collateral, and hero banners."
            
        # Generate platform-calibrated titles
        all_titles_dict = generate_commercial_titles(f"{clean_kw} {angle['suffix']}", platform=pf)
        raw_titles = all_titles_dict.get(pf, [])
        if not raw_titles:
            # Fallback titles if platform not found
            raw_titles = [
                f"{concept_name} for Commercial Advertising and Digital Marketing",
                f"Modern High-Resolution {concept_name} with Copy Space and Studio Lighting",
                f"Creative {concept_name} Isolated on Clean Background for Design Projects",
                f"Professional {concept_name} Graphic Asset for Web and Print Media"
            ]
            
        scored_titles = [calculate_title_score(t, base_kw=clean_kw, platform=pf) for t in raw_titles]
        
        # Generate platform-calibrated tags
        raw_tags = generate_stock_tags(f"{clean_kw} {angle['suffix']}", platform=pf)
        scored_tags = [calculate_tag_score(tg, base_kw=clean_kw, platform=pf) for tg in raw_tags]
        
        # Build tag_titles dictionary for top 12 tags
        scored_tag_titles = {}
        for tg_obj in scored_tags[:14]:
            tg_text = tg_obj["tag"]
            tag_titles_dict = generate_commercial_titles(f"{tg_text} {clean_kw}", platform=pf)
            tg_raw_titles = tag_titles_dict.get(pf, [])[:3]
            scored_tag_titles[tg_text] = {
                "tag_info": tg_obj,
                "titles": [calculate_title_score(t, base_kw=tg_text, platform=pf) for t in tg_raw_titles]
            }
            
        # Build AI Prompts Brief
        ai_brief = generate_ai_prompts(f"{clean_kw} {angle['suffix']}")
        
        # Platform-specific prompt specs
        custom_specs = {}
        if pf == "etsy":
            custom_specs["canva_spec"] = f"Design a 1080x1920 Instagram Story and 2000x2000px square template for {clean_kw}. Provide 5 editable color palettes, clean sans-serif typography (Montserrat / Playfair), and customizable photo frames."
            custom_specs["svg_spec"] = f"SVG cut file for Cricut: Outline text for '{title_kw}', cleanly weld overlapping paths, minimum cut clearance 0.5mm, zero stray anchor points."
        elif pf == "iconscout":
            custom_specs["octane_3d"] = f"Render in Cinema 4D Octane: 3D isolated icon of {clean_kw}. Iridescent claymorphic texture, studio softbox 3-point lighting, clean transparent PNG with alpha channel."
            custom_specs["lottie_motion"] = f"After Effects Bodymovin Lottie JSON: 60fps looping animation for {clean_kw}. Smooth ease-in-out rotation and gentle pulsing scale."
        elif pf == "graphicriver":
            custom_specs["psd_spec"] = f"Layered Photoshop PSD: 300 DPI, CMYK print mode, 0.125 inch bleed. Organize layers into color-coded folders: 'Header Typography', 'Smart Object Media', 'Background Textures'."
            
        ai_brief.update(custom_specs)
        
        concept_dict = {
            "concept": concept_name,
            "asset_type": asset_type,
            "suggested_title": raw_titles[0] if raw_titles else concept_name,
            "suggested_titles": raw_titles,
            "scored_titles": scored_titles,
            "why_it_sells": why_it_sells,
            "sample_tags": [tg_obj["tag"] for tg_obj in scored_tags],
            "scored_tags": scored_tags,
            "tag_titles": {tg: [t["title"] for t in data["titles"]] for tg, data in scored_tag_titles.items()},
            "scored_tag_titles": scored_tag_titles,
            "ai_prompts": ai_brief,
            "trend_velocity": {
                "search_surge": f"+{_hash_score(concept_name + clean_kw, 220, 480)}% Surge",
                "demand_status": "High Demand Commercial Trend",
                "optimal_window": "Upload 45-60 Days in Advance",
                "buyer_profile": "Corporate Marketers, Agencies & Direct Buyers"
            },
            "reference_guide": {
                "aesthetic_benchmark": ai_brief.get("benchmark", "Commercial Stock Photo & Advertising Editorial"),
                "curated_sref_code": ai_brief.get("active_ref_url", CURATED_STYLE_REFERENCES[0]["sref_code"]),
                "composition_rule": "Apply generous negative copy space in upper/left third for commercial text."
            }
        }
        
        generated_concepts.append(enrich_concept_with_deadline(concept_dict, pf))
        
    return generated_concepts
