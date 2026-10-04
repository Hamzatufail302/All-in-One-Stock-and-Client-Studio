"""
StockPulse AI - Upload Deadline & Indexing Lead Time Engine
Calculates optimal stock submission deadlines, upload date ranges, buyer search peak windows,
indexing lead times, and urgency/lateness countdowns for every keyword, asset concept,
platform guide, seasonal niche, and event.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Keyword / Theme rules mapping with event dates, indexing lead times, and demand windows
THEME_RULES = [
    # --- HOLIDAYS & MAJOR COMMERCIAL EVENTS ---
    {
        "keywords": ["halloween", "spooky", "jack o lantern", "ghost", "witch", "pumpkin", "horror", "cemetery", "costume"],
        "event_month": 10, "event_day": 31,
        "lead_time_days": 45,
        "peak_window": "October 01 – October 31",
        "theme_name": "Halloween Season",
        "guidance": "Upload 45-60 days ahead for early campaign planners. Late uploaders target rush digital printables."
    },
    {
        "keywords": ["cyber security", "cybersecurity", "firewall", "hacker", "data privacy", "infosec"],
        "event_month": 10, "event_day": 15,
        "lead_time_days": 30,
        "peak_window": "October 01 – October 31",
        "theme_name": "Cybersecurity Awareness Month",
        "guidance": "Corporate tech blogs and IT vendors license security graphics throughout October."
    },
    {
        "keywords": ["mental health", "mindfulness", "wellness", "therapy", "psychology", "self care"],
        "event_month": 10, "event_day": 10,
        "lead_time_days": 30,
        "peak_window": "October 01 – October 25",
        "theme_name": "World Mental Health Day",
        "guidance": "High engagement for healthcare social kits and clinic posters."
    },
    {
        "keywords": ["diwali", "deepavali", "rangoli", "diya lamp", "festival of lights", "indian festival"],
        "event_month": 11, "event_day": 1,
        "lead_time_days": 45,
        "peak_window": "October 10 – November 05",
        "theme_name": "Diwali Festival of Lights",
        "guidance": "High licensing of golden diya lamps, rangoli patterns, and festive corporate greeting cards."
    },
    {
        "keywords": ["thanksgiving", "autumn", "fall foliage", "fall harvest", "harvest", "turkey", "gratitude"],
        "event_month": 11, "event_day": 26,
        "lead_time_days": 45,
        "peak_window": "November 01 – November 28",
        "theme_name": "Thanksgiving & Autumn Harvest",
        "guidance": "Upload now so assets index before November family meal planning and school flyers."
    },
    {
        "keywords": ["black friday", "cyber monday", "singles day", "holiday sale", "discount badge", "shopping promo", "promo banner", "sale poster", "11.11"],
        "event_month": 11, "event_day": 27,
        "lead_time_days": 45,
        "peak_window": "November 05 – December 05",
        "theme_name": "Black Friday & Q4 E-Commerce Surge",
        "guidance": "Highest commercial volume period of the year. E-commerce merchants buy promo bundles."
    },
    {
        "keywords": ["christmas", "xmas", "santa", "winter holiday", "hanukkah", "festive", "snowflake", "gingerbread", "advent", "mistletoe", "ornament"],
        "event_month": 12, "event_day": 25,
        "lead_time_days": 55,
        "peak_window": "November 15 – December 25",
        "theme_name": "Christmas & Winter Holidays",
        "guidance": "Peak buying begins early November for corporate greeting cards and packaging designs."
    },
    {
        "keywords": ["new year", "new year's eve", "nye", "resolutions", "2027", "calendar", "fitness goal", "vision board"],
        "event_month": 12, "event_day": 31,
        "lead_time_days": 45,
        "peak_window": "December 10 – January 20",
        "theme_name": "New Year & Resolution Season",
        "guidance": "Gyms, habit trackers, and corporate planning templates sell heavily."
    },
    {
        "keywords": ["super bowl", "american football", "tailgate", "sports party", "football party"],
        "event_month": 2, "event_day": 10,
        "lead_time_days": 45,
        "peak_window": "January 15 – February 12",
        "theme_name": "Big Game & Winter Sports",
        "guidance": "Bar party flyers, game night social banners, and sports graphics peak."
    },
    {
        "keywords": ["valentine", "romantic", "love heart", "be my valentine", "dating", "couple portrait", "love quotes"],
        "event_month": 2, "event_day": 14,
        "lead_time_days": 50,
        "peak_window": "January 10 – February 14",
        "theme_name": "Valentine's Day",
        "guidance": "Jewelry, restaurant menus, SVG gift shirts, and greeting cards demand surge."
    },
    {
        "keywords": ["mardi gras", "carnival", "masquerade", "bourbon street", "beads mask"],
        "event_month": 3, "event_day": 3,
        "lead_time_days": 45,
        "peak_window": "February 01 – March 05",
        "theme_name": "Mardi Gras & Carnival",
        "guidance": "Nightclub party posters, purple-gold carnival masks, and festive bead graphics."
    },
    {
        "keywords": ["st patrick", "saint patrick", "shamrock", "leprechaun", "irish", "four leaf clover", "pot of gold"],
        "event_month": 3, "event_day": 17,
        "lead_time_days": 50,
        "peak_window": "February 15 – March 17",
        "theme_name": "St. Patrick's Day",
        "guidance": "Pub event flyers, green beer clipart, and Irish parade merchandise SVGs."
    },
    {
        "keywords": ["easter", "spring floral", "spring bloom", "botanical watercolor", "spring sale", "easter bunny", "easter egg"],
        "event_month": 4, "event_day": 10,
        "lead_time_days": 60,
        "peak_window": "March 01 – April 15",
        "theme_name": "Easter & Spring Awakening",
        "guidance": "Churches, schools, florists, and apparel brands license spring vectors in advance."
    },
    {
        "keywords": ["earth day", "sustainability", "eco friendly", "green energy", "climate", "solar panel", "wind turbine", "recycle"],
        "event_month": 4, "event_day": 22,
        "lead_time_days": 50,
        "peak_window": "March 15 – April 30",
        "theme_name": "Earth Day & Climate Sustainability",
        "guidance": "Corporate ESG annual reports, school ecology posters, and green tech agencies buy heavily."
    },
    {
        "keywords": ["mother's day", "mothers day", "best mom", "mom sublimation", "mama svg", "mother gift"],
        "event_month": 5, "event_day": 10,
        "lead_time_days": 60,
        "peak_window": "April 01 – May 15",
        "theme_name": "Mother's Day",
        "guidance": "High-margin digital invitations, Cricut SVG gift files, and floral frames."
    },
    {
        "keywords": ["father's day", "fathers day", "best dad", "dad sublimation", "bbq grill", "fishing dad"],
        "event_month": 6, "event_day": 15,
        "lead_time_days": 50,
        "peak_window": "May 01 – June 20",
        "theme_name": "Father's Day",
        "guidance": "Vintage typography, BBQ flyer templates, and apparel SVGs for dads."
    },
    {
        "keywords": ["pride month", "pride parade", "lgbtq", "rainbow flag", "love is love", "queer pride"],
        "event_month": 6, "event_day": 20,
        "lead_time_days": 50,
        "peak_window": "May 15 – June 30",
        "theme_name": "Pride Month & Diversity",
        "guidance": "Corporate diversity campaigns, parade banners, and rainbow merchandise designs."
    },
    {
        "keywords": ["4th of july", "independence day", "patriotic", "american flag", "fireworks", "memorial day"],
        "event_month": 7, "event_day": 4,
        "lead_time_days": 50,
        "peak_window": "June 01 – July 05",
        "theme_name": "4th of July & USA Patriotic",
        "guidance": "Community festival posters, red-white-blue vectors, and patriotic t-shirts."
    },
    {
        "keywords": ["back to school", "teacher", "classroom", "school supplies", "student", "education"],
        "event_month": 8, "event_day": 25,
        "lead_time_days": 60,
        "peak_window": "July 15 – September 10",
        "theme_name": "Back to School Season",
        "guidance": "Teachers Pay Teachers, school districts, and stationery brands buy year-round high volume."
    },
    {
        "keywords": ["tax season", "tax refund", "accounting", "cpa", "financial planning", "irs"],
        "event_month": 4, "event_day": 15,
        "lead_time_days": 60,
        "peak_window": "January 15 – April 15",
        "theme_name": "Tax & Financial Services",
        "guidance": "Accountants, bookkeeping firms, and fintech portals need corporate infographics."
    },

    # --- FASHION & APPAREL SEASONS ---
    {
        "keywords": ["spring fashion", "summer fashion", "fashion week", "runway", "couture", "apparel mockup", "clothing line", "linen", "y2k fashion", "tshirt design", "hoodie mockup", "pastel outfit", "cottagecore fashion"],
        "event_month": 3, "event_day": 20,
        "lead_time_days": 60,
        "peak_window": "February 01 – April 30",
        "theme_name": "Spring / Summer Fashion & Runway Drops",
        "guidance": "Fashion brands and apparel POD shops source mockups and lookbook visuals 60 days ahead."
    },
    {
        "keywords": ["autumn fashion", "fall fashion", "winter fashion", "coat mockup", "knitwear", "sweater weather", "boots", "leather jacket", "puffer jacket", "trench coat", "dark academia fashion", "streetwear drop"],
        "event_month": 9, "event_day": 22,
        "lead_time_days": 60,
        "peak_window": "August 15 – November 15",
        "theme_name": "Autumn / Winter Streetwear & Layering Drops",
        "guidance": "Apparel e-commerce sites license cozy textures, heavy fleece mockups, and streetwear aesthetics."
    },
    {
        "keywords": ["resort wear", "swimwear", "bikini", "beachwear", "cruise collection", "summer dress", "vacation style", "tropical fashion"],
        "event_month": 6, "event_day": 1,
        "lead_time_days": 60,
        "peak_window": "April 15 – July 15",
        "theme_name": "Summer Resort & Swimwear Collections",
        "guidance": "E-commerce lookbooks, sunglasses ads, and summer boutique marketing assets."
    },
    {
        "keywords": ["festival outfit", "coachella", "boho chic", "crochet top", "rave wear", "bohemian aesthetic", "festival makeup"],
        "event_month": 4, "event_day": 18,
        "lead_time_days": 50,
        "peak_window": "March 15 – May 15",
        "theme_name": "Music Festival & Boho Chic Season",
        "guidance": "Desert music festival aesthetics, glitter makeup b-roll, and bohemian cut files."
    },

    # --- BIRTHDAYS & LIFE MILESTONES (HIGH COMMERCIAL VALUE) ---
    {
        "keywords": ["30th birthday", "death to my 20s", "dirty thirty", "21st birthday", "18th birthday", "sweet 16", "50th birthday", "40th birthday", "60th birthday", "milestone birthday", "birthday invitation", "birthday svg", "cake topper", "birthday shirt", "happy birthday"],
        "event_month": 5, "event_day": 1, # Rolling peak with major late spring/summer celebrations
        "lead_time_days": 40,
        "peak_window": "Year-Round (Quarterly Celebration Peaks)",
        "theme_name": "Milestone Birthdays (18th, 21st, 30th, 50th)",
        "guidance": "Continuous high-margin demand on Etsy & Adobe Stock for custom invitations, SVG shirts, and cake toppers."
    },
    {
        "keywords": ["baby shower", "gender reveal", "oh baby", "baby announcement", "nursery decor", "welcome baby", "safari baby shower", "woodland baby shower"],
        "event_month": 4, "event_day": 25,
        "lead_time_days": 50,
        "peak_window": "March 01 – June 30 (Spring Baby Boom)",
        "theme_name": "Baby Showers & Nursery Milestone Season",
        "guidance": "Stationery printables, gender reveal party games, and watercolor nursery animal prints."
    },
    {
        "keywords": ["wedding", "bridal shower", "bachelorette party", "save the date", "wedding invitation", "wedding vows", "mr and mrs", "wedding menu", "place card wedding", "engagement"],
        "event_month": 5, "event_day": 25,
        "lead_time_days": 75,
        "peak_window": "January 15 – June 30 (Peak Wedding Booking)",
        "theme_name": "Spring & Summer Wedding Season",
        "guidance": "High-margin digital downloads: Canva invitation suites, seating charts, and Cricut vinyl decals."
    },
    {
        "keywords": ["graduation", "class of 2026", "class of 2027", "senior 2026", "senior 2027", "diploma", "grad party", "commencement", "valedictorian"],
        "event_month": 5, "event_day": 30,
        "lead_time_days": 60,
        "peak_window": "April 01 – June 15",
        "theme_name": "Graduation & Senior Year Commencement",
        "guidance": "Yard signs, party announcements, class shirt SVGs, and ceremony photo templates."
    },
    {
        "keywords": ["quinceanera", "mis quince", "quince party", "sweet sixteen invitation", "tiara svg"],
        "event_month": 6, "event_day": 15,
        "lead_time_days": 60,
        "peak_window": "April 15 – July 30",
        "theme_name": "Quinceañera & Sweet 16 Celebrations",
        "guidance": "Glamorous floral invitation suites, glitter acrylic cake topper SVGs, and party favors."
    },
    {
        "keywords": ["anniversary", "golden anniversary", "silver anniversary", "50th anniversary", "25th anniversary", "wedding anniversary"],
        "event_month": 6, "event_day": 20,
        "lead_time_days": 45,
        "peak_window": "May 01 – September 30",
        "theme_name": "Golden & Silver Wedding Anniversaries",
        "guidance": "Elegant gold foil certificates, family banquet programs, and milestone gift vectors."
    },
    {
        "keywords": ["retirement", "happy retirement", "legend has retired", "retirement party", "goodbye tension"],
        "event_month": 6, "event_day": 30,
        "lead_time_days": 45,
        "peak_window": "May 15 – July 15 & December",
        "theme_name": "Retirement & Farewell Milestones",
        "guidance": "Humorous t-shirt SVGs, company farewell greeting cards, and gold pension party banners."
    }
]

def _next_date(now: datetime, month: int, day: int) -> datetime:
    """Returns the next upcoming date for a given month and day."""
    try:
        candidate = datetime(now.year, month, day)
    except ValueError:
        candidate = datetime(now.year, month, 28)
    
    # If the date has passed this year by more than 3 days, roll to next year
    if candidate < now - timedelta(days=3):
        try:
            candidate = datetime(now.year + 1, month, day)
        except ValueError:
            candidate = datetime(now.year + 1, month, 28)
    return candidate

def _get_quarter_info(now: datetime) -> dict:
    """Calculates corporate quarterly cycle for evergreen, tech, and general stock."""
    month = now.month
    year = now.year

    if month in (7, 8, 9):
        # In Q3 -> Production target is Q4 budget spend & Holiday rollout
        deadline = datetime(year, 10, 20)
        start_date = datetime(year, 8, 1)
        peak_window = "October 20 – December 20, " + str(year) + " (Q4 Peak)"
        quarter_name = "Q4 Corporate Budget & Holiday Refresh"
    elif month in (10, 11, 12):
        # In Q4 -> Production target is Q1 New Year Kickoff & Tech Keynotes
        deadline = datetime(year, 11, 25) if month == 10 else datetime(year, 12, 20)
        start_date = datetime(year, 10, 1)
        peak_window = "January 05 – March 01, " + str(year + 1) + " (Q1 Launch)"
        quarter_name = "Q1 New Year Launch & Annual Keynotes"
    elif month in (1, 2, 3):
        # In Q1 -> Production target is Q2 Spring Refreshes
        deadline = datetime(year, 2, 20)
        start_date = datetime(year, 1, 1)
        peak_window = "March 15 – May 30, " + str(year) + " (Q2 Growth)"
        quarter_name = "Q2 Spring Refresh & Product Launch"
    else:
        # In Q2 -> Production target is Q3 Summer Campaigns
        deadline = datetime(year, 5, 20)
        start_date = datetime(year, 4, 1)
        peak_window = "June 15 – August 30, " + str(year) + " (Q3 Campaigns)"
        quarter_name = "Q3 Summer Marketing & Mid-Year Campaigns"

    # Make sure deadline is strictly in the future
    if deadline <= now:
        deadline = now + timedelta(days=21)
    if start_date > now:
        start_date = now - timedelta(days=10)

    return {
        "start_date": start_date,
        "deadline": deadline,
        "peak_window": peak_window,
        "quarter_name": quarter_name
    }

def get_keyword_deadline(keyword: str, platform: str = "Multi") -> dict:
    """
    Computes an exact upload deadline date, golden date range, and timing status
    (LATE, CLOSING SOON, PRIME, or EVERGREEN) for any keyword.
    """
    now = datetime.now()
    clean_kw = (keyword or "").strip().lower()

    # Search for matching seasonal/milestone rule
    matched_rule = None
    for rule in THEME_RULES:
        if any(trigger in clean_kw for trigger in rule["keywords"]):
            matched_rule = rule
            break

    if matched_rule:
        event_date = _next_date(now, matched_rule["event_month"], matched_rule["event_day"])
        lead_days = matched_rule.get("lead_time_days", 45)
        optimal_deadline = event_date - timedelta(days=lead_days)
        optimal_start = event_date - timedelta(days=lead_days + 45)

        # Check if optimal deadline has passed for this year's occurrence
        if optimal_deadline < now:
            days_to_event = (event_date - now).days
            if days_to_event > 4:
                # We are in the "LATE / RUSH WINDOW"
                is_late = True
                days_past_deadline = (now - optimal_deadline).days
                upload_deadline = now + timedelta(days=min(3, max(1, days_to_event - 2)))
                timing_status = "LATE"
                timing_badge = f"🔴 LATE ({days_past_deadline}d past golden window)"
                urgency = "Critical (Late Window)"
                urgency_badge_color = "rose"
                status_note = f"Late upload window! Event is on {event_date.strftime('%b %d')} (in {days_to_event}d). Upload immediately for last-minute digital download buyers."
            else:
                # Event is right now or past -> target next year's cycle
                event_date = _next_date(now + timedelta(days=30), matched_rule["event_month"], matched_rule["event_day"])
                optimal_deadline = event_date - timedelta(days=lead_days)
                optimal_start = event_date - timedelta(days=lead_days + 45)
                upload_deadline = optimal_deadline
                is_late = False
                days_past_deadline = 0
                timing_status = "ADVANCE_PREP"
                timing_badge = "🟣 ADVANCE PREP (Next Cycle)"
                urgency = "Advance Planning"
                urgency_badge_color = "indigo"
                status_note = f"Targets next annual cycle ({event_date.year}). Upload 45-60 days ahead for top indexing rank."
        else:
            is_late = False
            days_past_deadline = 0
            upload_deadline = optimal_deadline
            days_remaining = (upload_deadline - now).days

            if days_remaining <= 14:
                timing_status = "CLOSING_SOON"
                timing_badge = f"🟡 CLOSING SOON ({days_remaining}d left)"
                urgency = "Urgent (Closing Soon)"
                urgency_badge_color = "amber"
                status_note = f"Final call! Upload before {upload_deadline.strftime('%b %d')} to index before {matched_rule['theme_name']} demand surges."
            elif now >= optimal_start:
                timing_status = "PRIME_WINDOW"
                timing_badge = f"🟢 PRIME UPLOAD WINDOW ({days_remaining}d left)"
                urgency = "Prime Window (Create NOW)"
                urgency_badge_color = "emerald"
                status_note = f"Optimal production window! Upload between {optimal_start.strftime('%b %d')} – {optimal_deadline.strftime('%b %d')} for #1 rank."
            else:
                days_until_window = (optimal_start - now).days
                timing_status = "ADVANCE_PREP"
                timing_badge = f"🟣 EARLY PREP (Opens in {days_until_window}d)"
                urgency = "Advance Planning"
                urgency_badge_color = "indigo"
                status_note = f"Advance planning phase. Upload window formally opens on {optimal_start.strftime('%b %d')}."

        peak_window = matched_rule["peak_window"]
        theme_name = matched_rule["theme_name"]
        event_date_str = event_date.strftime("%B %d, %Y")
        event_date_short = event_date.strftime("%b %d")
        date_range_str = f"{optimal_start.strftime('%b %d')} – {optimal_deadline.strftime('%b %d, %Y')}"
    else:
        # Evergreen / Tech / Corporate / Lifestyle
        q_info = _get_quarter_info(now)
        upload_deadline = q_info["deadline"]
        optimal_start = q_info["start_date"]
        lead_days = 30
        theme_name = q_info["quarter_name"]
        peak_window = q_info["peak_window"]
        event_date_str = None
        event_date_short = None
        date_range_str = f"Continuous ({optimal_start.strftime('%b %d')} – {upload_deadline.strftime('%b %d')})"
        
        is_late = False
        days_past_deadline = 0
        days_remaining = (upload_deadline - now).days
        
        timing_status = "EVERGREEN"
        timing_badge = "⚡ EVERGREEN (Upload Anytime)"
        urgency = "Continuous Evergreen"
        urgency_badge_color = "emerald"
        status_note = f"Year-round evergreen commercial demand with peak licensing across {peak_window}."

    days_remaining = max(1, (upload_deadline - now).days)

    return {
        "upload_deadline": upload_deadline.strftime("%B %d, %Y"),
        "upload_deadline_short": upload_deadline.strftime("%b %d, %Y"),
        "upload_deadline_iso": upload_deadline.strftime("%Y-%m-%d"),
        "upload_date_range": date_range_str,
        "is_late": is_late,
        "days_past_deadline": days_past_deadline,
        "days_remaining": days_remaining,
        "event_date": event_date_str,
        "event_date_short": event_date_short,
        "timing_status": timing_status,
        "timing_badge": timing_badge,
        "peak_demand_window": peak_window,
        "lead_time_days": lead_days,
        "lead_time_label": f"{lead_days} Days Lead Time",
        "urgency": urgency,
        "urgency_badge_color": urgency_badge_color,
        "theme_name": theme_name,
        "status_note": status_note
    }

def enrich_concept_with_deadline(concept_dict: dict, platform_name: str = "Adobe Stock") -> dict:
    """
    Enriches a concept dictionary with dynamic upload deadline,
    date ranges, is_late flag, days left, and peak windows.
    """
    concept_title = concept_dict.get("concept", "")
    sample_tags = concept_dict.get("sample_tags", [])
    combined_query = f"{concept_title} " + " ".join(sample_tags[:5])

    deadline_info = get_keyword_deadline(combined_query, platform_name)

    enriched = dict(concept_dict)
    enriched["upload_deadline"] = deadline_info["upload_deadline"]
    enriched["upload_deadline_short"] = deadline_info["upload_deadline_short"]
    enriched["upload_deadline_iso"] = deadline_info["upload_deadline_iso"]
    enriched["upload_date_range"] = deadline_info["upload_date_range"]
    enriched["is_late"] = deadline_info["is_late"]
    enriched["days_past_deadline"] = deadline_info["days_past_deadline"]
    enriched["days_remaining"] = deadline_info["days_remaining"]
    enriched["event_date"] = deadline_info["event_date"]
    enriched["event_date_short"] = deadline_info["event_date_short"]
    enriched["timing_status"] = deadline_info["timing_status"]
    enriched["timing_badge"] = deadline_info["timing_badge"]
    enriched["peak_demand_window"] = deadline_info["peak_demand_window"]
    enriched["lead_time_days"] = deadline_info["lead_time_days"]
    enriched["lead_time_label"] = deadline_info["lead_time_label"]
    enriched["urgency"] = deadline_info["urgency"]
    enriched["urgency_badge_color"] = deadline_info["urgency_badge_color"]
    enriched["theme_name"] = deadline_info["theme_name"]
    enriched["status_note"] = deadline_info["status_note"]

    # Provide per-tag deadline dictionary if needed
    tag_deadlines = {}
    for tag in sample_tags:
        t_info = get_keyword_deadline(tag, platform_name)
        tag_deadlines[tag] = {
            "upload_deadline": t_info["upload_deadline"],
            "upload_deadline_short": t_info["upload_deadline_short"],
            "upload_date_range": t_info["upload_date_range"],
            "is_late": t_info["is_late"],
            "timing_status": t_info["timing_status"],
            "timing_badge": t_info["timing_badge"],
            "days_remaining": t_info["days_remaining"],
            "peak_window": t_info["peak_demand_window"],
            "urgency": t_info["urgency"]
        }
    enriched["tag_deadlines"] = tag_deadlines

    return enriched
