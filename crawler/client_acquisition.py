"""
Video Editor Client Acquisition & High-Ticket Outreach Engine
Comprehensive playbooks, current 2026 client requirements, battle-tested cold emails & DMs,
search operators, pricing benchmarks, and outreach scripts for professional video editors.
"""

from typing import Dict, List, Any, Optional

CURRENT_VIDEO_REQUIREMENTS: List[Dict[str, Any]] = [
    {
        "id": "youtube_retention",
        "title": "YouTube Long-Form Retention Edits",
        "style_category": "YouTube Creator Economy",
        "icon": "youtube",
        "market_demand": "Extremely High (★ 98/100)",
        "ideal_clients": "YouTubers (20k–500k subs), Tech Reviewers, Finance/Crypto Educators, Video Essayists",
        "avg_pricing": "$200 – $600 per video | $2,000 – $4,500/mo retainer (4–8 videos)",
        "deliverable_specs": "1080p / 4K 60fps, Premiere Pro / DaVinci Resolve project file, YouTube Chapter timestamps, exported high-res thumbnail frame grabs",
        "pacing_rules": "Visual switch/pattern interrupt every 2.5–4.0 seconds (B-roll, kinetic text, punch-in zooms, graphic pop, SFX). Hook must establish stakes in first 15 seconds.",
        "software_stack": "Adobe Premiere Pro, After Effects (Essential Graphics / MOGRTs), Photoshop (Asset cutouts), DeNoise AI",
        "current_client_pains": [
            "Creators burn out spending 15–20 hours per video editing instead of filming and brainstorming high-CTR concepts.",
            "Audience retention drops below 40% in the first 2 minutes due to flat monotone delivery and lack of sound design.",
            "Inconsistent upload schedules hurting YouTube algorithm impressions."
        ],
        "winning_skills": [
            "Sound design layering (whoosh + pop + impact hit + subtle risers + adaptive ducking)",
            "Kinetic typography and floating 3D paper cutouts",
            "Pacing and storytelling (cutting breathing room, removing filler words)",
            "Audience retention graph analysis"
        ]
    },
    {
        "id": "short_form_viral",
        "title": "Viral 9:16 Short-Form Content Machine",
        "style_category": "Shorts / Reels / TikTok",
        "icon": "smartphone",
        "market_demand": "Massive Volume (★ 99/100)",
        "ideal_clients": "Personal Brands, Business Coaches, Real Estate Agents, Podcasters, B2B Founders",
        "avg_pricing": "$30 – $75 per Short | $1,000 – $2,500/mo retainer (30–45 Shorts/month)",
        "deliverable_specs": "1080x1920 (9:16 vertical), 30/60fps, burnt-in animated captions, custom brand hex colors, zero safe-zone text cutoff",
        "pacing_rules": "Visual shift every 1.5–2.5 seconds. First 1.0 second hook is critical (eye-catching text, sound pop, dynamic hand motion or prop). Sub-60 second duration.",
        "software_stack": "Premiere Pro / CapCut Pro / After Effects, Auto-Captions with custom font typography (TheBoldFont, Montserrat Black), sound pack library",
        "current_client_pains": [
            "Brands and influencers have hundreds of hours of raw footage, podcast audio, or webinars gathering dust.",
            "They know they need daily presence on Instagram Reels, YouTube Shorts, and TikTok but have no time to reformat.",
            "Amateur auto-generated captions looking robotic, cheap, and off-brand."
        ],
        "winning_skills": [
            "Hormozi / Ryan Pineda style colored keyword highlights (yellow, bright green, cyan)",
            "Micro-animations (animated emojis, green-screen memes, glowing badges)",
            "Punchy zoom-ins on voice emphasis",
            "Safe-zone mastery (avoiding TikTok/Reels UI overlay blocks)"
        ]
    },
    {
        "id": "b2b_saas_product",
        "title": "B2B SaaS, Software & Tech Product Explainers",
        "style_category": "Corporate & Tech",
        "icon": "monitor",
        "market_demand": "Highest Profit Margins (★ 94/100)",
        "ideal_clients": "SaaS Startups, Y Combinator Alumni, Tech Founders, Product Hunt Launchers, Venture-backed apps",
        "avg_pricing": "$800 – $3,000 per 60–90 second explainer | $3,500 – $7,000/mo product launch retainer",
        "deliverable_specs": "16:9 for Landing Pages & YouTube + 9:16 for LinkedIn Ads & Product Hunt, ProRes 422 or H.264 high-bitrate, seamless loop",
        "pacing_rules": "Smooth cursor movements (Screen Studio / After Effects ease-in-out), 3D isometric perspective tilts, dynamic camera pans over UI features, upbeat modern corporate indie background track.",
        "software_stack": "After Effects, Screen Studio, Figma asset exports, Adobe Illustrator (vector icons), Premiere Pro",
        "current_client_pains": [
            "Founders build great software, but their landing page has a boring static screenshot or a choppy 5-minute Loom demo that doesn't convert signups.",
            "They need high-converting videos for Product Hunt launches, investor pitch decks, and paid LinkedIn ads.",
            "Most freelance editors don't understand tech workflows or clean minimalist UI aesthetics."
        ],
        "winning_skills": [
            "Synthetic UI screen mockups inside sleek Apple MacBook / iPhone clay models",
            "Smooth kinetic typography matching modern Silicon Valley aesthetics (Inter, SF Pro, Satoshi)",
            "Figma to After Effects workflow",
            "Direct-response value proposition clarity (Problem -> Solution -> Feature Walkthrough -> CTA)"
        ]
    },
    {
        "id": "podcast_multicam",
        "title": "Podcast Repurposing & Multi-Cam Mastering",
        "style_category": "Podcasts & Media Shows",
        "icon": "mic",
        "market_demand": "Consistent Monthly Retainers (★ 92/100)",
        "ideal_clients": "Business, Tech, and Lifestyle Podcasters, Interviewers, Remote Zoom/Riverside Show Hosts",
        "avg_pricing": "$250 – $500 per episode (Full cut + 3–5 viral Shorts) | $1,500 – $3,500/mo retainer (4 episodes/mo)",
        "deliverable_specs": "Full 16:9 YouTube video + Spotify Video format + 3–5 high-retention 9:16 vertical highlight reels with captions and host/guest split-screen",
        "pacing_rules": "Dynamic multi-cam switching (cut to speaker within 0.3s of voice, two-shot camera on laughs or shared reactions). Audio leveled to -14 LUFS broadcast standard with background noise reduction.",
        "software_stack": "Premiere Pro (Multi-Camera Source Sequence), Adobe Audition / iZotope RX / Adobe Podcast AI, After Effects",
        "current_client_pains": [
            "Recording a 1-hour interview is fun for hosts, but cutting dead air, syncing audio, color-matching two cameras, and making social clips is a 10-hour chore.",
            "Episodes drop on Apple/Spotify with zero viral distribution because hosts fail to post vertical video clips.",
            "Echo, background hiss, and unbalanced host vs guest audio levels."
        ],
        "winning_skills": [
            "Studio audio cleanup (compression, de-reverb, de-esser, loudness normalization)",
            "Multi-cam auto-switching and facial tracking",
            "Editorial instinct to identify the exact 45-second golden takeaway quote for social media",
            "Split-screen vertical framing (Host on top, Guest on bottom)"
        ]
    },
    {
        "id": "ecommerce_ugc_ads",
        "title": "Direct-Response eCommerce & UGC Video Ads",
        "style_category": "eCommerce & Performance Marketing",
        "icon": "shopping-bag",
        "market_demand": "High Volume & Performance Bonuses (★ 95/100)",
        "ideal_clients": "Shopify DTC Brands, Amazon Sellers, TikTok Shop Creators, Media Buying Agencies",
        "avg_pricing": "$150 – $350 per ad package (1 core body + 3 different hook variations) | $2,000 – $4,000/mo creative testing retainer",
        "deliverable_specs": "9:16 TikTok/Meta format + 1:1 Instagram Square, 20–45s duration, punchy call-to-action end card with discount codes",
        "pacing_rules": "Test 3 different hooks for the first 3 seconds (Hook A: Question, Hook B: Negative shock statement, Hook C: Problem visualization). Fast-paced UGC cuts, customer review popups, urgency tickers.",
        "software_stack": "Premiere Pro / CapCut Pro, TikTok Creative Center trending audio, Photoshop (product cutouts)",
        "current_client_pains": [
            "Media buyers need 10–20 creative ad variations every week because ad fatigue sets in quickly on TikTok and Meta.",
            "They have raw footage from TikTok influencers but lack an editor who understands ROAS (Return On Ad Spend) and Hook Rate.",
            "Slow turnaround times kill seasonal campaigns (e.g. BFCM, Mother's Day, Summer drops)."
        ],
        "winning_skills": [
            "Hook Rate optimization (creating scroll-stopping first 3 seconds)",
            "Creating variations (3 hooks x 2 bodies x 2 CTAs = 12 testable ads with minimal extra work)",
            "Social proof overlays (Trustpilot 5-star badges, TikTok comments popup, before/after split screens)",
            "Rapid 24–48 hour turnaround"
        ]
    },
    {
        "id": "real_estate_luxury",
        "title": "Luxury Real Estate & Architectural Video Tours",
        "style_category": "High-Ticket Local Commercial",
        "icon": "home",
        "market_demand": "High Per-Project Ticket (★ 89/100)",
        "ideal_clients": "Luxury Real Estate Agents, Commercial Brokers, Architectural Firms, Airbnb Superhosts",
        "avg_pricing": "$350 – $900 per property tour video | $1,800 – $3,500/mo agency retainer",
        "deliverable_specs": "4K 60fps horizontal cinematic YouTube tour + 9:16 fast agent-guided vertical walkthrough with agent mic audio sync",
        "pacing_rules": "Smooth speed ramping between rooms, ambient sound design (subtle footsteps, bird chirps, fountain water, crackling fireplace), cinematic color grade (warm, bright, airy).",
        "software_stack": "Premiere Pro / DaVinci Resolve (color grading), Adobe Audition, Warp Stabilizer / Gyroflow",
        "current_client_pains": [
            "A luxury home sale earns an agent $20k–$80k in commissions, so high-end video marketing is non-negotiable.",
            "Agents have drone footage and handheld camera clips but don't know how to color grade or speed-ramp them into a multimillion-dollar aesthetic.",
            "Need both horizontal MLS listings and vertical Instagram Reels to impress affluent property buyers."
        ],
        "winning_skills": [
            "Speed ramps and whip pan transitions",
            "Cinematic color grading (clean whites, rich greenery, blue skies)",
            "Camera stabilization and horizon leveling",
            "Property spec text callouts (Bedrooms, Bathrooms, Sq Footage, Price floating in 3D tracking)"
        ]
    }
]

PROSPECTING_PLAYBOOKS: List[Dict[str, Any]] = [
    {
        "id": "youtube_sniping",
        "channel": "YouTube Creator Sniping",
        "tagline": "The 'Unedited Potential' Strategy",
        "difficulty": "Beginner Friendly",
        "conversion_rate": "25% – 35% response rate with custom sample",
        "icon": "target",
        "target_criteria": [
            "Subscribers between 15,000 and 150,000 (big enough to monetize and hire, small enough that the creator still reads their business email).",
            "Upload frequency: at least 1 video every 7–14 days.",
            "Identifiable editing bottlenecks: Monotone pacing, dead pauses, lack of sound design, boring standard font subtitles, or low view-to-sub ratio."
        ],
        "step_by_step": [
            "1. Search YouTube for profitable niches: Personal Finance, B2B Marketing, AI Tools, Real Estate, Fitness, Productivity, Coding Tutorials.",
            "2. Filter by 'Upload date: This month' to find active creators.",
            "3. Watch their latest video. Look for the first 60 seconds (the hook) or a 45-second high-value segment.",
            "4. Download that 45-second clip and re-edit it into an explosive, retention-packed masterpiece: add sound effects, dynamic punch-ins, B-roll, and clean animated text.",
            "5. Upload the re-edited clip to an unlisted Google Drive or Loom link.",
            "6. Find their email in the 'About' section -> 'View email address' (or in video description).",
            "7. Send Email Template #1: 'Re-edited your latest video hook (No charge)'. Never pitch a resume; pitch the live result!"
        ],
        "search_queries": [
            'site:youtube.com "business inquiries" "subscriber" "productivity"',
            'site:youtube.com "contact" "email" "real estate" "channel"',
            'site:youtube.com "sponsor" "business email" "finance"',
            'site:youtube.com "for business" "tech reviews" "uploads"'
        ],
        "pro_tips": [
            "Never send an attachment (it triggers spam filters). Send a clean Google Drive link or Loom embed.",
            "Compliment a specific point they made in minute 03:20 so they know you actually watched their content.",
            "Keep the email under 120 words. Creators read emails on their phones while on the go."
        ]
    },
    {
        "id": "twitter_linkedin_founders",
        "channel": "Twitter / X & LinkedIn B2B Founders",
        "tagline": "The Founder Personal Brand Repurposing Playbook",
        "difficulty": "Intermediate",
        "conversion_rate": "30% – 45% positive reply rate",
        "icon": "twitter",
        "target_criteria": [
            "SaaS Founders, Venture Capitalists, Marketing Agency Owners, High-Ticket Consultants.",
            "They post text content regularly on LinkedIn/Twitter, but have almost zero vertical video.",
            "They frequently appear on podcasts, webinars, or Twitter Spaces."
        ],
        "step_by_step": [
            "1. Search Twitter / X or LinkedIn for founders in your target niche (e.g. AI SaaS, FinTech, E-commerce).",
            "2. Check if they have done any recent podcast interviews (search their name on YouTube or Apple Podcasts).",
            "3. Take their best 30–60 second quote, clean their audio, add kinetic captions, brand colors, and an attention-grabbing hook.",
            "4. Send a direct message (DM) on Twitter or LinkedIn: 'Hey [Name], saw your podcast appearance with [Host]. Loved your insight on [Topic], so I turned it into a 9:16 viral clip for your personal brand. Feel free to post it!'",
            "5. Include the video directly in the chat. Do not ask for money upfront.",
            "6. Once they reply thanking you, follow up: 'Glad you loved it! I do this for founders on a monthly retainer—turning 1 monthly interview into 20 viral clips so you stay top-of-mind without lifting a finger. Open to a 10-minute chat?'"
        ],
        "search_queries": [
            '"looking for a video editor" lang:en -filter:replies',
            '"hiring video editor" lang:en (shorts OR youtube)',
            '"need a video editor" (retainer OR freelance)',
            'site:linkedin.com/in "Founder" "SaaS" "podcast host"'
        ],
        "pro_tips": [
            "Founders value speed and reliability over complex visual tricks. Highlight how much time you save them.",
            "Offer a trial package: 'Let's do 5 clips this week. If you love them, we can talk monthly retainer; if not, you keep them for free.'"
        ]
    },
    {
        "id": "google_maps_local",
        "channel": "Google Maps & Local Commercial Outreach",
        "tagline": "The High-Ticket Local Retainer Engine",
        "difficulty": "Beginner Friendly",
        "conversion_rate": "15% – 25% closing rate",
        "icon": "map-pin",
        "target_criteria": [
            "High-ticket local businesses where 1 new customer = $1,500 – $10,000+ (Cosmetic Dentists, Med Spas, Luxury Car Detailers, Remodeling Contractors, High-End Realtors).",
            "Location: Wealthy suburbs, major metro areas (Austin, Miami, Los Angeles, London, Sydney, Toronto).",
            "Their website or Instagram has low-quality amateur videos or hasn't posted in 3 months."
        ],
        "step_by_step": [
            "1. Open Google Maps. Search: 'Med Spa near [City]', 'Cosmetic Dentist near [City]', 'Exotic Car Detailer near [City]'.",
            "2. Look for businesses with 4.5+ stars and 50+ reviews (they have marketing budget).",
            "3. Check their linked Instagram, TikTok, or YouTube channel.",
            "4. If their reels are low quality, record a 2-minute personalized video review: 'Hey Dr. [Name], love your dental clinic work! I noticed your Instagram reels are missing dynamic captions and sound hooks. Here is how your before-and-after cases could look with professional commercial pacing.'",
            "5. Show a 15-second mockup or sample template.",
            "6. Email the practice manager or DM their business Instagram.",
            "7. Pitch an 'All-in-One Local Social Video Package': 8–12 polished Reels/month for $1,200 – $2,000/mo."
        ],
        "search_queries": [
            'site:instagram.com "cosmetic dentist" "reels" "city"',
            'site:instagram.com "med spa" "aesthetic injector" "dr"',
            'site:instagram.com "luxury real estate" "listing video"'
        ],
        "pro_tips": [
            "Always mention client acquisition: 'This will help you attract 3–5 additional high-ticket invisalign / aesthetic clients each month.'",
            "Local business owners prefer phone calls or quick WhatsApp/Instagram DMs over formal cold emails."
        ]
    },
    {
        "id": "podcast_directory",
        "channel": "Apple Podcasts & Spotify Directories",
        "tagline": "The Zero-Effort Show Repurposing Engine",
        "difficulty": "Beginner to Intermediate",
        "conversion_rate": "20% – 30% response rate",
        "icon": "headphones",
        "target_criteria": [
            "Podcasts in the Top 50–250 charts in Business, Marketing, Tech, Fitness, and True Crime.",
            "Hosts record video (you can see YouTube video links in their show notes) but don't post Shorts.",
            "Show has sponsors (meaning they have active marketing budgets)."
        ],
        "step_by_step": [
            "1. Browse Apple Podcasts / Chartable / Spotify top rankings in Business, Health, or Entrepreneurship.",
            "2. Find podcasts with weekly episodes.",
            "3. Check their YouTube or Instagram. If they just upload a full 1-hour episode with no vertical short clips, they are leaving 90% of their organic reach on the table.",
            "4. Cut 2 viral vertical clips from their latest episode. Format with host/guest split-screen, dynamic subtitles, and engaging B-roll.",
            "5. Email the host with the subject: 'Made 2 viral clips from episode #[XX] for you'.",
            "6. Offer a monthly podcast distribution retainer: 4 full episodes edited + 16 viral vertical shorts = $1,500/mo."
        ],
        "search_queries": [
            'site:chartable.com/charts/spotify "business" "podcast"',
            'site:youtube.com "podcast episode" "full interview" "2026"'
        ],
        "pro_tips": [
            "Include audio waveform visualizers or animated subtitles that match their podcast cover art colors."
        ]
    },
    {
        "id": "upwork_hiring_boards",
        "channel": "High-Ticket Upwork & Specialized Boards",
        "tagline": "The Anti-Fluff Proposal System",
        "difficulty": "Intermediate",
        "conversion_rate": "35% – 50% interview rate",
        "icon": "briefcase",
        "target_criteria": [
            "Jobs posted within the last 60 minutes with < 10 proposals.",
            "Client history: Payment Verified, > $10,000 spent, 4.8+ rating, Client location: US, UK, Canada, Australia, Western Europe.",
            "Hourly rate $35 – $75/hr or Fixed Price $500 – $3,000."
        ],
        "step_by_step": [
            "1. Set up an Upwork saved search query with strict filters (Payment verified, spent > $5k, < 10 proposals).",
            "2. Read the client's job description. Identify their #1 bottleneck (e.g. 'Looking for an editor who knows how to make retention-focused YouTube videos like Iman Gadzhi').",
            "3. Write a 4-sentence proposal. Never start with 'Dear Sir' or 'I have 5 years experience'. Start directly with the answer to their problem.",
            "4. Attach 2 specific portfolio links that match EXACTLY their requested style.",
            "5. End with an open-ended low-friction question: 'Do you already have a storyboard/script ready, or should I cut directly from raw footage?'"
        ],
        "search_queries": [
            '("video editor" OR "premiere pro" OR "after effects") AND ("youtube" OR "shorts" OR "retention")',
            '("video editor" OR "video editing") AND ("retainer" OR "monthly" OR "long term")'
        ],
        "pro_tips": [
            "Check client's past reviews to find their first name. Starting your proposal with 'Hey [First Name]' immediately sets you apart from 95% of copy-paste proposals.",
            "Also monitor YTJobs.co (official hiring board for top YouTubers) and Contra.com."
        ]
    }
]

COLD_EMAIL_TEMPLATES: List[Dict[str, Any]] = [
    {
        "id": "free_sample_pitch",
        "title": "The 'Free 60-Second Re-Edit' Golden Pitch",
        "channel": "Cold Email / Business Inquiries",
        "ideal_for": "YouTube Creators & Podcasters",
        "conversion_metric": "32% Positive Response Rate (Industry Leading)",
        "subject_lines": [
            "Re-edited your latest video hook (No charge, [Name])",
            "Quick retention edit for [Channel Name] (Check this out)",
            "Made a viral short from your latest video (For you)"
        ],
        "body": """Hey [Client Name],

Big fan of your latest video on [Specific Topic / Video Title]. The point you made around [Specific Timestamp, e.g. 03:15] regarding [Specific Insight] was super insightful.

I noticed your viewer retention might be dropping slightly in the first 30 seconds due to the static pacing.

To show you what I mean rather than pitch you, I went ahead and re-edited the first 45 seconds of that video with retention-focused pacing, sound design, and kinetic visual pops:

👉 Watch your 45-second re-edit here: [Loom or Google Drive Link]

No invoice or catch at all—feel free to use it or test it!

I'm a full-time video editor helping creators in the [Niche] space scale their watch time and reach. If you like the pacing and want someone reliable to take editing off your plate so you can focus 100% on filming, let me know!

Best,
[Your Name]
Portfolio: [Your Portfolio Link]
WhatsApp/Telegram: [Your Contact]""",
        "why_it_works": "99% of editors send generic resumes asking for work. By handing them a finished, high-quality asset upfront with zero risk, you prove competence immediately.",
        "golden_rule": "Make sure your Google Drive link has 'Anyone with the link can view' permissions turned on before sending!"
    },
    {
        "id": "founder_b2b_repurpose",
        "title": "The B2B Founder & CEO Repurposing Pitch",
        "channel": "LinkedIn Message / Twitter DM / Founder Email",
        "ideal_for": "SaaS Founders, Coaches, Agency CEOs",
        "conversion_metric": "28% Positive Response Rate",
        "subject_lines": [
            "Turning your podcast appearances into 20 qualified leads, [Name]",
            "Video content engine for [Company Name]",
            "Quick idea on your recent [Podcast/Webinar Name]"
        ],
        "body": """Hey [Founder Name],

Loved your recent interview on [Podcast Name] discussing [Specific Topic / Key Takeaway].

You have incredible insights, but I noticed you aren't repurposing these interviews into vertical video clips for LinkedIn, YouTube Shorts, and X.

I turned one of your top insights from that episode into a 45-second high-retention clip with clean corporate kinetic typography and sound design:

👉 [Drive/Loom Link to Sample Clip]

Feel free to post this directly on your profile!

I run a plug-and-play video system for tech founders: you record 1 hour of video or podcasts a month, and I turn it into 20 viral clips, thumbnails, and captions so you stay top-of-mind with investors and prospective clients without wasting hours editing.

Open to checking out 3 more sample concepts this week?

Cheers,
[Your Name]
[Your Website/Portfolio]""",
        "why_it_works": "Founders don't care about video editing techniques; they care about saving time, generating pipeline leads, and building their personal brand.",
        "golden_rule": "Keep the tone professional, concise, and focused on business ROI rather than editing jargon."
    },
    {
        "id": "short_dm_pitch",
        "title": "The 3-Sentence High-Impact Twitter / Instagram DM",
        "channel": "Instagram DM / Twitter / X DM",
        "ideal_for": "Fast Casual Outreach to Active Creators",
        "conversion_metric": "35% Response Rate",
        "subject_lines": ["N/A (Direct Message)"],
        "body": """Hey [Name]! Loved your reel on [Topic].

I noticed your hook retention could easily double with dynamic sound design and punchy captions, so I cut a 30s version of your video to show you what it looks like: [Loom/Drive Link].

Feel free to post it! If you want someone to handle 30 of these for you each month so you never have to edit again, let me know! 🙌""",
        "why_it_works": "Zero fluff. Creators swipe through DMs in 5 seconds. A direct link with a personalized video catches their attention immediately.",
        "golden_rule": "Always follow them first, engage with their recent post (leave a thoughtful comment), then send the DM 10 minutes later."
    },
    {
        "id": "upwork_proposal_script",
        "title": "The Upwork 'Anti-Fluff' High-Winning Proposal",
        "channel": "Upwork Cover Letter",
        "ideal_for": "Winning $500–$2,000+ Upwork Projects",
        "conversion_metric": "42% Interview Rate",
        "subject_lines": ["Upwork Proposal"],
        "body": """Hey [Client First Name if known, else 'there'],

I read your job post and you need an editor who understands [exact style requested, e.g. Hormozi retention-style pacing with custom SFX and fast cuts], not someone who just slaps basic subtitles on raw footage.

Here are two exact samples of videos I edited in this exact retention format:
1. [Link to specific relevant video sample #1]
2. [Link to specific relevant video sample #2]

My workflow:
- 24 to 48-hour turnaround per video.
- Complete sound design (whooshes, risers, impacts, room tone ducking).
- Color grading + high-retention kinetic typography.
- Unlimited revisions on the first milestone until you are 100% happy.

Do you have the raw footage and script ready, or do you need help structuring the 3-second hook first?

Best,
[Your Name]""",
        "why_it_works": "Directly tackles their exact requirement in line 1. Shows 2 hyper-relevant samples immediately. Ends with a low-friction qualifying question.",
        "golden_rule": "Never paste generic agency copy. If the client asked for a codeword in the description, place it on line 1."
    },
    {
        "id": "follow_up_sequence",
        "title": "The 3-Stage Follow-Up Sequence (Never Leave Money on the Table)",
        "channel": "Email / DM Follow-Ups",
        "ideal_for": "Unanswered Cold Pitches (Converts 60% of Closed Deals)",
        "conversion_metric": "Recovers 3x more clients than initial pitch alone",
        "subject_lines": [
            "Re: [Original Subject]",
            "Quick follow-up on your video hook, [Name]",
            "Closing your editing file / Permission to archive"
        ],
        "body": """--- STAGE 1: Day 3 Gentle Bump ---
Hey [Name], quick bump on this! Did you get a chance to check out that 45-second re-edit I sent over? (Here's the link again: [Link]). 
No rush at all, just wanted to make sure it didn't get buried in your inbox!

--- STAGE 2: Day 7 Value Drop ---
Hey [Name], was thinking about your channel's upcoming videos. Noticed your competitors in the [Niche] space are getting 3x more watch time by using [Specific Trend, e.g. 3D paper texture graphics]. 
I put together a quick 3-point checklist of easy tweaks you can make to your current videos to boost average percentage viewed. Let me know if you'd like me to send it over!

--- STAGE 3: Day 14 Permission to Close / Break-Up Email ---
Hey [Name], usually when I don't hear back it means either you're completely sorted with video editing, or your priorities have shifted. 
Totally understand! I'll archive your project file for now. If you ever need a reliable editor for a sudden project or want to test high-retention edits down the road, you know where to find me. 
Wishing you continued growth on [Channel Name]!""",
        "why_it_works": "Over 60% of client deals close on the 2nd or 3rd follow-up. Creators are busy, not rude. Stage 3 uses reverse psychology ('permission to close') which triggers fear of missing out.",
        "golden_rule": "Always reply to the same email thread so the original context and sample link are right below your message."
    }
]

OBJECTION_HANDLING_PLAYBOOK: List[Dict[str, str]] = [
    {
        "objection": "Your price is too high / We don't have the budget.",
        "framework": "De-risk & Scope Reduction",
        "script": "Totally understand! Rather than doing the full 8-video package, how about we start with a smaller test sprint of 2 videos at $[Lower Amount]? That way you can test the turnaround speed and retention metrics with minimal upfront risk."
    },
    {
        "objection": "Can you do a free full 15-minute test video?",
        "framework": "Firm Value Boundary",
        "script": "I completely understand wanting to verify fit before committing! While I can't edit a full 15-minute episode for free, I'd be happy to edit the first 60 seconds (the hook) completely free, or do 1 full video at a 50% trial discount. If you love it, we proceed with the monthly retainer. How does that sound?"
    },
    {
        "objection": "We already have an editor.",
        "framework": "Backup Editor / Overflow Position",
        "script": "That's awesome! A good editor is invaluable. Keep my contact handy as your backup. If your current editor ever gets sick, takes vacation, or has too much overflow footage, shoot me a message and I can turn around an emergency project in 24 hours."
    },
    {
        "objection": "Send me your portfolio / resume.",
        "framework": "Curated Relevance",
        "script": "Here are my top 3 most relevant edits that match your exact channel style: [Link 1], [Link 2], [Link 3]. Notice how the retention hook at 00:03 keeps viewers locked in. Which of these two styles resonates closest with your vision for [Channel Name]?"
    }
]

RETAINER_CALCULATOR_PRESETS: List[Dict[str, Any]] = [
    {
        "target_income": "$3,000 / month",
        "title": "Full-Time Freelancer Baseline",
        "formula": "2 Retainers @ $1,500/mo OR 4 Retainers @ $750/mo",
        "workload": "4 Long-form YouTube videos + 16 Shorts per month (approx. 20 hours/week)",
        "daily_pitch_target": "5 personalized pitches/day (100/mo) -> 3% close rate = 3 new clients"
    },
    {
        "target_income": "$5,000 / month",
        "title": "High-Ticket Creative Partner",
        "formula": "2 YouTube Retainers @ $2,000/mo + 1 Short-Form Machine @ $1,000/mo",
        "workload": "8 Long-form videos + 30 Shorts per month (approx. 32 hours/week)",
        "daily_pitch_target": "8 personalized pitches/day (160/mo) -> 2.5% close rate = 4 new clients"
    },
    {
        "target_income": "$10,000 / month",
        "title": "Agency / Mini-Studio Scale",
        "formula": "4 Enterprise Retainers @ $2,500/mo (B2B SaaS / Top YouTubers)",
        "workload": "16 Long-form videos + 40 Shorts (hire 1 junior editor to assist with B-roll/captions)",
        "daily_pitch_target": "12 personalized pitches/day + active LinkedIn founder outreach"
    }
]

def generate_custom_pitch(client_name: str, channel_or_niche: str, pitch_type: str, custom_link: Optional[str] = None) -> Dict[str, str]:
    """Generates a personalized, tailored pitch script based on inputs."""
    c_name = client_name.strip() if client_name and client_name.strip() else "there"
    c_niche = channel_or_niche.strip() if channel_or_niche and channel_or_niche.strip() else "your niche"
    link = custom_link.strip() if custom_link and custom_link.strip() else "[Insert Loom/Drive Link]"
    
    if pitch_type == "youtube_sample":
        subject = f"Re-edited your latest video hook (No charge, {c_name})"
        body = f"""Hey {c_name},

Big fan of your content on {c_niche}. The insights you share are gold, but I noticed your viewer retention might be dropping in the opening 30 seconds due to static pacing.

To show you what I mean rather than pitch you, I went ahead and re-edited the first 45 seconds of your latest video with retention-focused pacing, sound design, and kinetic visual pops:

👉 Watch your 45-second re-edit here: {link}

Zero invoice or catch at all—feel free to use it or test it!

I'm a dedicated video editor helping creators in {c_niche} scale their watch time and reach. If you like the pacing and want someone reliable to take editing off your plate so you can focus 100% on filming, let me know!

Best,
[Your Name]
Portfolio: [Your Portfolio Link]"""
    elif pitch_type == "founder_repurpose":
        subject = f"Turning your podcast appearances into qualified pipeline leads, {c_name}"
        body = f"""Hey {c_name},

Loved your recent interview discussing {c_niche}.

You have incredible insights, but I noticed you aren't repurposing these interviews into vertical video clips for LinkedIn, YouTube Shorts, and X.

I turned one of your top insights into a 45-second high-retention clip with clean corporate kinetic typography and sound design:

👉 {link}

Feel free to post this directly on your profile!

I run a video system for founders: you record 1 hour of video or podcasts a month, and I turn it into 20 viral clips, thumbnails, and captions so you stay top-of-mind with prospective clients and investors without wasting hours editing.

Open to checking out 3 more sample concepts this week?

Cheers,
[Your Name]"""
    elif pitch_type == "short_dm":
        subject = f"Quick video sample for {c_name}"
        body = f"""Hey {c_name}! Loved your recent video on {c_niche}.

I noticed your hook retention could easily double with dynamic sound design and punchy captions, so I cut a 30s version of your video to show you what it looks like: {link}

Feel free to post it! If you want someone to handle 30 of these for you each month so you never have to edit again, let me know! 🙌"""
    else:  # upwork
        subject = "Upwork Proposal"
        body = f"""Hey {c_name},

I read your job post and you need an editor who understands {c_niche} retention pacing, not someone who just slaps basic subtitles on raw footage.

Here is an exact sample of a video I edited in this high-retention format:
👉 {link}

My workflow:
- 24 to 48-hour turnaround per video.
- Complete sound design (whooshes, risers, impacts, room tone ducking).
- Color grading + high-retention kinetic typography.
- Unlimited revisions on the first milestone until you are 100% happy.

Do you have the raw footage and script ready, or do you need help structuring the 3-second hook first?

Best,
[Your Name]"""
        
    return {
        "subject": subject,
        "body": body,
        "client_name": c_name,
        "niche": c_niche
    }

def get_client_acquisition_overview() -> Dict[str, Any]:
    """Returns the full master guide for client acquisition for video editors."""
    return {
        "current_requirements": CURRENT_VIDEO_REQUIREMENTS,
        "prospecting_playbooks": PROSPECTING_PLAYBOOKS,
        "cold_email_templates": COLD_EMAIL_TEMPLATES,
        "objection_handling": OBJECTION_HANDLING_PLAYBOOK,
        "retainer_presets": RETAINER_CALCULATOR_PRESETS
    }
