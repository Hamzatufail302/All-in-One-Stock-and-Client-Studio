"""
Seasonal Demand & Stock Calendar Engine
Tracks global holidays, shopping seasons, and the 60-90 day advance stock production cycle.
"""

from datetime import datetime

MONTH_DATA = {
    1: {
        "month_name": "January",
        "current_peaking": ["New Year Resolutions", "Winter Sports", "Tax Season Preparation", "Martin Luther King Day"],
        "upload_now_target": "Upload for Spring & April/May (Easter, Earth Day, Mother's Day, Spring Florals)",
        "priority_niches": [
            {
                "theme": "Easter & Spring Bloom",
                "target_date": "March / April",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Illustrator (Floral vectors)", "Canva (Easter egg hunt flyers)"],
                "keywords": ["easter egg vector", "spring floral wreath", "easter bunny illustration", "spring sale canva banner", "botanical watercolor clipart"]
            },
            {
                "theme": "Earth Day & Climate Sustainability",
                "target_date": "April 22",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Illustrator (Infographics)", "AI Visuals (Green ecology concepts)"],
                "keywords": ["earth day vector", "eco friendly badge", "zero waste lifestyle", "save planet illustration", "green energy sustainability"]
            },
            {
                "theme": "Mother's Day & Spring Weddings",
                "target_date": "May",
                "lead_time": "120 Days Ahead",
                "recommended_for": ["Canva (Gift coupons, cards)", "Etsy (SVG bundles)"],
                "keywords": ["mothers day card canva", "best mom ever svg", "spring wedding invitation suite", "watercolor flowers frame", "mom mug sublimation"]
            }
        ]
    },
    2: {
        "month_name": "February",
        "current_peaking": ["Valentine's Day", "Super Bowl Parties", "Black History Month", "Presidents Day"],
        "upload_now_target": "Upload for Summer & Graduation (May/June: Memorial Day, Father's Day, Graduations, Pride Month)",
        "priority_niches": [
            {
                "theme": "Graduation & Class Celebration",
                "target_date": "May / June",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Canva (Announcements)", "Etsy (Graduation SVG cut files)"],
                "keywords": ["graduation announcement canva", "senior 2026 svg", "graduation cap diploma vector", "proud mom graduate shirt", "graduation yard sign"]
            },
            {
                "theme": "Father's Day & Summer BBQ",
                "target_date": "June",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Photoshop (BBQ flyers)", "Illustrator (Retro vintage badges)"],
                "keywords": ["fathers day card canva", "best dad ever svg", "bbq grill party flyer", "vintage father badge", "fishing dad sublimation"]
            }
        ]
    },
    3: {
        "month_name": "March",
        "current_peaking": ["St. Patrick's Day", "Spring Equinox", "Easter Preparations", "Ramadan"],
        "upload_now_target": "Upload for Summer Travel & Independence Day (4th of July, Summer Camps, Beach Vibe)",
        "priority_niches": [
            {
                "theme": "4th of July & Patriotic USA",
                "target_date": "July 4",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Illustrator (Patriotic vectors)", "Etsy (American flag SVG)"],
                "keywords": ["4th of july fireworks vector", "patriotic eagle svg", "independence day flyer psd", "red white and blue badge", "american flag vintage"]
            },
            {
                "theme": "Summer Vacations & Tropical Travel",
                "target_date": "June / July",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["AI Video (Beach loops)", "Photoshop (Travel agency brochures)"],
                "keywords": ["summer beach drone 4k", "tropical palm leaves vector", "travel agency trifold brochure", "summer camp flyer canva", "sunshine vibes svg"]
            }
        ]
    },
    4: {
        "month_name": "April",
        "current_peaking": ["Earth Day", "Easter", "Spring Weddings", "Arbor Day"],
        "upload_now_target": "Upload for Back to School & Autumn (Late Summer / August / September)",
        "priority_niches": [
            {
                "theme": "Back to School & Teacher Appreciation",
                "target_date": "August / September",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Canva (Classroom newsletters)", "Etsy (Teacher SVG)", "Illustrator (School supplies)"],
                "keywords": ["back to school vector", "teacher appreciation svg", "classroom newsletter canva", "first day of school sign", "school supplies isometric"]
            }
        ]
    },
    5: {
        "month_name": "May",
        "current_peaking": ["Cinco de Mayo", "Mother's Day", "Memorial Day", "Graduation Parties"],
        "upload_now_target": "Upload for Fall Foliage, Oktoberfest & Early Halloween Concepts",
        "priority_niches": [
            {
                "theme": "Autumn & Fall Foliage",
                "target_date": "September / October",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Illustrator (Fall leaves)", "AI Visuals (Cozy autumn aesthetic)"],
                "keywords": ["autumn watercolor leaves", "fall pumpkin vector", "cozy autumn coffee aesthetic", "fall festival flyer psd", "sweater weather svg"]
            }
        ]
    },
    6: {
        "month_name": "June",
        "current_peaking": ["Father's Day", "Juneteenth", "Summer Solstice", "Pride Month"],
        "upload_now_target": "Upload for Halloween & Autumn Harvest (October peaks)",
        "priority_niches": [
            {
                "theme": "Halloween & Spooky Season",
                "target_date": "October 31",
                "lead_time": "90-120 Days Ahead",
                "recommended_for": ["Illustrator (Ghosts & witches)", "Photoshop (Spooky party flyers)", "Etsy (Cute ghost SVG)"],
                "keywords": ["cute ghost halloween svg", "halloween party flyer psd", "spooky season tumbler wrap", "haunted house silhouette vector", "retro halloween graphics"]
            }
        ]
    },
    7: {
        "month_name": "July",
        "current_peaking": ["4th of July", "Summer Camps", "Midsummer Sales", "Amazon Prime Day Deals"],
        "upload_now_target": "Upload for Thanksgiving, Black Friday & Cyber Monday",
        "priority_niches": [
            {
                "theme": "Black Friday & Cyber Monday Mega Sale",
                "target_date": "November",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Canva (Social banners)", "Photoshop (E-commerce 3D badges)"],
                "keywords": ["black friday 3d banner", "cyber monday discount tag", "black friday instagram canva", "sale badge neon vector", "mega sale promo poster"]
            },
            {
                "theme": "Thanksgiving & Harvest Dinner",
                "target_date": "November",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Illustrator (Turkey & cornucopia)", "Canva (Thanksgiving dinner menu)"],
                "keywords": ["thanksgiving turkey vector", "fall harvest dinner menu canva", "grateful thankful blessed svg", "autumn leaves background", "thanksgiving greeting card"]
            }
        ]
    },
    8: {
        "month_name": "August",
        "current_peaking": ["Back to School", "Labor Day Preparations", "End of Summer Clearance"],
        "upload_now_target": "Upload for CHRISTMAS & HOLIDAY SEASON (The absolute biggest stock sales peak of the year!)",
        "priority_niches": [
            {
                "theme": "Christmas & Winter Holidays (Biggest Earner)",
                "target_date": "December",
                "lead_time": "90-120 Days Ahead",
                "recommended_for": ["Canva (Holiday cards)", "Illustrator (Snowflake vectors)", "Photoshop (Mockups)", "AI (Cinematic winter 4k)"],
                "keywords": ["christmas card template canva", "vintage santa illustration", "christmas tree vector pattern", "holiday mockup psd", "winter snow drone 4k"]
            }
        ]
    },
    9: {
        "month_name": "September",
        "current_peaking": ["Labor Day", "Fall Equinox", "Oktoberfest", "Halloween Costume Rush"],
        "upload_now_target": "Upload for Christmas, Hanukkah, New Year 2027 & Annual Planners (HIGH URGENCY)",
        "priority_niches": [
            {
                "theme": "Christmas & New Year Mega Wave",
                "target_date": "December / January",
                "lead_time": "60-90 Days Ahead (PEAK PRODUCTION WINDOW)",
                "recommended_for": ["Canva (Photo cards, invitations)", "Etsy (Digital planners 2026/2027)", "Photoshop (Apparel mockups)", "Illustrator (Xmas icons)"],
                "keywords": ["christmas party flyer psd", "merry christmas canva card", "new year 2027 vector logo", "christmas sweater mockup", "winter wonderland 3d icons"]
            },
            {
                "theme": "New Year 2027 Planners & Goal Trackers",
                "target_date": "December / January",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Canva (Hyperlinked GoodNotes Planners)", "Etsy (Budget printables)"],
                "keywords": ["digital planner 2027 goodnotes", "daily habit tracker canva", "new year resolution journal", "financial budget planner pdf", "minimalist ipad planner"]
            },
            {
                "theme": "Winter Aesthetics & Snow Landscapes",
                "target_date": "December - February",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["AI Images (Hyper-realistic winter scenes)", "AI Video (Slow falling snow 4K loops)"],
                "keywords": ["snow falling loop 4k", "cozy winter cabin fireplace 3d", "abstract frozen ice texture", "winter corporate holiday banner", "nordic winter landscape"]
            }
        ]
    },
    10: {
        "month_name": "October",
        "current_peaking": ["Halloween", "Breast Cancer Awareness", "Fall Festivals", "Diwali"],
        "upload_now_target": "Upload for New Year Resolutions, Fitness Goals, Tax Season & Valentine's Day",
        "priority_niches": [
            {
                "theme": "Valentine's Day & Romantic Love",
                "target_date": "February 14",
                "lead_time": "90-120 Days Ahead",
                "recommended_for": ["Illustrator (Heart vectors)", "Canva (Romantic cards, menus)", "Etsy (Love quotes SVG)"],
                "keywords": ["valentines day vector hearts", "romantic dinner menu psd", "be my valentine card canva", "love quote sublimation svg", "3d red glossy hearts"]
            },
            {
                "theme": "Health, Fitness & New Year Resolutions",
                "target_date": "January",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Canva (Gym social templates)", "Illustrator (Workout icons)", "AI Video (Gym training b-roll)"],
                "keywords": ["gym flyer template psd", "fitness workout canva instagram", "weight loss tracker printable", "gym dumbbells vector icon", "athletic runner slow motion 4k"]
            }
        ]
    },
    11: {
        "month_name": "November",
        "current_peaking": ["Thanksgiving", "Black Friday", "Cyber Monday", "Veterans Day"],
        "upload_now_target": "Upload for Valentine's Day, St. Patrick's Day, and Spring Break",
        "priority_niches": [
            {
                "theme": "St. Patrick's Day & Irish Festival",
                "target_date": "March 17",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Illustrator (Shamrock clover vectors)", "Photoshop (Irish pub flyers)"],
                "keywords": ["st patricks day flyer psd", "four leaf clover vector", "irish leprechaun hat icon", "lucky shamrock svg bundle", "st patrick beer party poster"]
            }
        ]
    },
    12: {
        "month_name": "December",
        "current_peaking": ["Christmas", "Hanukkah", "Winter Solstice", "New Year's Eve"],
        "upload_now_target": "Upload for Easter, Earth Day, Spring Weddings & Tax Filing Season",
        "priority_niches": [
            {
                "theme": "Tax Season & Accounting Services",
                "target_date": "March / April",
                "lead_time": "90 Days Ahead",
                "recommended_for": ["Canva (Tax prep flyers)", "Illustrator (Finance infographics)", "Photoshop (Corporate brochures)"],
                "keywords": ["tax preparation flyer canva", "accounting firm trifold brochure", "tax refund vector icon", "financial planning infographic", "income tax filing banner"]
            }
        ]
    }
}

def get_current_seasonal_intel():
    now = datetime.now()
    cur_month = now.month
    month_info = MONTH_DATA.get(cur_month, MONTH_DATA[9])
    
    # Calculate next two upcoming months
    next_m1 = (cur_month % 12) + 1
    next_m2 = ((cur_month + 1) % 12) + 1

    from crawler.deadline_engine import get_keyword_deadline
    enriched_niches = []
    for niche in month_info.get("priority_niches", []):
        n_dict = dict(niche)
        theme_query = f"{niche.get('theme', '')} " + " ".join(niche.get("keywords", [])[:3])
        d_info = get_keyword_deadline(theme_query)
        n_dict["upload_date_range"] = d_info["upload_date_range"]
        n_dict["upload_deadline"] = d_info["upload_deadline"]
        n_dict["upload_deadline_short"] = d_info["upload_deadline_short"]
        n_dict["is_late"] = d_info["is_late"]
        n_dict["days_past_deadline"] = d_info["days_past_deadline"]
        n_dict["days_remaining"] = d_info["days_remaining"]
        n_dict["timing_status"] = d_info["timing_status"]
        n_dict["timing_badge"] = d_info["timing_badge"]
        n_dict["urgency"] = d_info["urgency"]
        enriched_niches.append(n_dict)
    
    return {
        "current_month_name": month_info["month_name"],
        "current_date": now.strftime("%B %d, %Y"),
        "current_peaking": month_info["current_peaking"],
        "upload_now_target": month_info["upload_now_target"],
        "priority_niches": enriched_niches,
        "upcoming_forecast": [
            {"month": MONTH_DATA[next_m1]["month_name"], "target": MONTH_DATA[next_m1]["upload_now_target"]},
            {"month": MONTH_DATA[next_m2]["month_name"], "target": MONTH_DATA[next_m2]["upload_now_target"]}
        ]
    }
