"""
All-In-One Stock & Client Studio - YouTube Creator Engine
Complete 4-Channel Production Blueprint, Trending Topic Intelligence,
Hand-Drawn AI Doodle ("Ink Explainer") Studio, Script Hooks, and Thumbnail Formulas.
Tailored for Creator: Hamza Tufail
"""

from typing import Dict, List, Any, Optional
import random

YOUTUBE_CHANNELS: List[Dict[str, Any]] = [
    {
        "id": "ink_explainer",
        "name": "Ink Explainer (Doodle History & Human Nature)",
        "badge": "AI Hand-Drawn / Faceless",
        "language": "English (US / Global)",
        "creator_format": "Faceless AI Animation (2D Hand-Drawn / Whiteboard Cartoon)",
        "inspiration": "Ink Explainer (@Inkexplainer96 - 10M+ views / 16 videos), MinuteEarth, Casually Explained",
        "target_audience": "Global English-speaking curious minds (US 45%, UK, Canada, Australia, Europe)",
        "estimated_rpm": "$4.50 – $9.00 / 1K views",
        "upload_frequency": "1–2 videos per week (8–14 minutes long-form)",
        "core_thesis": "Exploring prehistoric human survival, bizarre ancient pleasures, evolutionary psychology, and existential curiosities using ultra-relatable, humorous hand-drawn stickman animations.",
        "visual_style": "Minimalist black-ink doodle stickmen with exaggerated facial expressions, fur tunics, wooden spears, warm textured vintage paper / savannah background, 12fps hand-drawn animation feel.",
        "production_stack": "AI Prompting (Midjourney v6 / Flux.1), Photoshop (layer separation), After Effects (Puppet Pin, Posterize Time 12fps, camera pans), ElevenLabs (natural conversational voiceover), Sound Design (Foley, pops, whooshes, comic impacts).",
        "monetization": "YouTube AdSense (millions of views), Sponsor Integrations (NordVPN, Nebula, CuriosityStream, Factor), Merch (illustrated hoodies/prints), Patreon exclusive art packs."
    },
    {
        "id": "trending_info",
        "name": "Curious Atlas (US Curiosities & Modern Video Essays)",
        "badge": "Documentary / AI Hybrid",
        "language": "English (US / Global)",
        "creator_format": "Faceless Documentary (Cinematic AI Visuals + 4K B-Roll + Motion Graphics)",
        "inspiration": "Vox, Johnny Harris, Magnates Media, Wendover Productions",
        "target_audience": "US/Western viewers fascinated by hidden economies, infrastructure quirks, modern mysteries, and societal shifts",
        "estimated_rpm": "$7.00 – $16.00 / 1K views (High-tier US advertiser niche)",
        "upload_frequency": "1 video every 7–10 days (10–18 minutes long-form)",
        "core_thesis": "Deep-dive investigations into bizarre American phenomena, $100B hidden industries, architectural enigmas, and consumer trends hiding in plain sight.",
        "visual_style": "High-contrast motion graphic maps, vintage paper archival popups, cinematic 4K video loops, custom AI-rendered historical and industrial scenes, dark cinematic color grade.",
        "production_stack": "Premiere Pro / After Effects (kinetic typography, 3D camera tracker), Midjourney v6 (cinematic editorial shots), Runway / Luma / Sora (AI B-roll), Epidemic Sound.",
        "monetization": "High US AdSense RPM, Premium Brand Sponsorships, Digital Newsletter, Masterclass affiliate deals."
    },
    {
        "id": "hamza_tech",
        "name": "Hamza Tufail (After Effects, Editing & Motion Design)",
        "badge": "Personal Brand / On-Camera",
        "language": "English",
        "creator_format": "Talking Head + Dual-Monitor Screen Recording (Hamza Tufail on camera)",
        "inspiration": "Ben Marriott, Premiere Gal, Mapal, Film Riot, Finzar",
        "target_audience": "Freelance video editors, content creators, motion designers, and YouTubers seeking elite editing skills & high-paying client workflows",
        "estimated_rpm": "$10.00 – $22.00 / 1K views (B2B Creative Software & Hardware Niche)",
        "upload_frequency": "1–2 videos per week (8–15 minutes tutorials & breakdowns)",
        "core_thesis": "Demystifying advanced After Effects motion design, high-retention YouTube editing techniques, time-saving workflow automations, and landing $3,000–$5,000/mo international freelance clients.",
        "visual_style": "Clean studio lighting, warm rim light, crisp screen capture with cursor zoom and key-press visualizations, live project timeline dissections, vibrant UI overlays.",
        "production_stack": "Sony / Mirrorless camera or iPhone 4K ProRes + Shure/Rode mic, OBS Studio (60fps lossless recording), Adobe After Effects 2026, Adobe Premiere Pro, Boris FX / Motion Bro plugins.",
        "monetization": "Digital Project Files (Gumroad / Patreon), Motion Graphic Template (MOGRT) packs, 1-on-1 Mentorship / High-Ticket Freelance Client Inquiries, Adobe / Plugin Affiliate links."
    },
    {
        "id": "urdu_dastaan",
        "name": "Dastaan-e-Tareekh with Hamza Tufail (Urdu Historical Stories)",
        "badge": "Personal Brand / Urdu Storytelling",
        "language": "Urdu / Hindi",
        "creator_format": "Talking Head + Dramatic Cinematic Visuals (Hamza Tufail as host & narrator)",
        "inspiration": "Dekho Suno Jano (Faisal Warraich), Haider Kaleem, Dhruv Rathee History, Dan Carlin Hardcore History",
        "target_audience": "Pakistan, India, Bangladesh diaspora across UAE, Saudi Arabia, UK, USA, Canada fascinated by intense history, conquests, and mysteries",
        "estimated_rpm": "$1.50 – $4.00 / 1K views (Massive view velocity: 500k–3M+ views per video)",
        "upload_frequency": "1 video every Sunday evening (15–25 minutes deep historical narrative)",
        "core_thesis": "Immersive storytelling of forgotten empires, psychological battles of legendary sultans and generals, espionage, and dramatic historical turnarounds with intense cinematic depth.",
        "visual_style": "Atmospheric warm studio lamp aesthetic, dramatic facial expressions, interspersed with AI-generated oil paintings, vintage archival maps with burning ember effects, slow camera push-ins.",
        "production_stack": "Shure SM7B / Rode PodMic for rich radio-broadcast baritone voice, Premiere Pro, After Effects for 3D map animations (GeoLayers), AI historical character generation, dramatic orchestra OST.",
        "monetization": "Massive AdSense volume, Pakistani/UAE national brand sponsorships (fintech, clothing, education apps), YouTube Memberships, podcast syndication."
    }
]

# --- VIRAL TOPICS & VIDEO BLUEPRINTS BANK ---
VIRAL_VIDEO_BLUEPRINTS: Dict[str, List[Dict[str, Any]]] = {
    "ink_explainer": [
        {
            "id": "ink_01",
            "title": "What Did Ancient Humans Actually Do All Day?",
            "thumbnail_text": "NO JOBS?",
            "thumbnail_concept": "Relaxed stickman lying down with hands behind head on savannah grass, smiling blissfully while looking at sun. Fur tunic, tiny campfire in background. Bold yellow comic font with black stroke.",
            "duration": "11:15",
            "views_benchmark": "10M+ Views",
            "virality_score": 99,
            "hook_script": "Before 9-to-5 alarms, rent deadlines, and corporate spreadsheets existed... what did a human actually wake up and DO? For 200,000 years, your ancestors didn't have jobs, bosses, or groceries. But anthropologist studies reveal something shocking: ancient hunter-gatherers only worked about 15 hours a week. The rest of the time? They were doing things that would get modern humans fired...",
            "content_beats": [
                "The 15-Hour Work Week myth vs. brutal reality of foraging",
                "How cavemen kept themselves from dying of boredom during 40-day rains",
                "Storytelling around the embers: The birth of religion and mythology",
                "Grooming, joking, and ancient comedy clubs around the mammoth carcass",
                "The shock of modern agricultural slavery: Why farming made humans work 3x harder"
            ],
            "ai_prompt": "minimalist hand-drawn doodle cartoon illustration, relaxed prehistoric caveman stick figure lying comfortably on savannah grass, smiling with hands behind head, wearing primitive brown animal fur, tiny campfire in distant background, simple black ink linework, warm paper texture background, clean 2D animation frame --ar 16:9 --style raw"
        },
        {
            "id": "ink_02",
            "title": "What Did Ancient Humans Do For Pleasure?",
            "thumbnail_text": "ANCIENT PLEASURE?",
            "thumbnail_concept": "Male caveman stickman and female caveman leaning back on animal pelts, eating purple grapes, campfire crackling, funny relaxed expressions. Bright sunny background.",
            "duration": "14:48",
            "views_benchmark": "2.5M+ Views",
            "virality_score": 97,
            "hook_script": "If you lock a modern human in a room without Wi-Fi for 30 minutes, they will lose their mind. But ancient humans had no Netflix, no alcohol shops, no video games, and no TikTok. So how did they escape the sheer existential dread of being hunted by saber-toothed cats? It turns out, prehistoric humans discovered some of the wildest, most bizarre methods to get dopamine...",
            "content_beats": [
                "Accidental fermentation: How rotten fruit turned entire tribes into party animals",
                "Cave wall psychedelics: Why cave paintings only appear in pitch-black acoustic chambers",
                "Ancient board games carved into river stones 12,000 years ago",
                "Pranks and tribe teasing: The universal evolutionary purpose of laughter",
                "The ancient mating rituals that look hilariously similar to modern dating apps"
            ],
            "ai_prompt": "hand-drawn doodle cartoon illustration of two happy prehistoric cavemen stick figures relaxing on fur rug by campfire eating wild berries, humorous expressive faces, simple black ink contour lines, textured pale yellow parchment background, clean 2D comic art --ar 16:9 --style raw"
        },
        {
            "id": "ink_03",
            "title": "How Did Ancient Humans Survive the Deadliest Predators on Earth?",
            "thumbnail_text": "SURVIVED HOW?",
            "thumbnail_concept": "Tired, dirty caveman family carrying primitive wooden spears through tall grass, looking behind nervously at giant lion shadow. Stickman style with funny determined grimace.",
            "duration": "10:27",
            "views_benchmark": "5M+ Views",
            "virality_score": 98,
            "hook_script": "Look at your own hand. No 6-inch claws. Look at your teeth. No bone-crushing fangs. You can't outrun a cheetah, and a single hyena could snap your femur in half. Biologically, humans are naked, squishy prey. Yet somehow, our ancestors didn't just survive creatures 5 times their size—they drove them completely extinct. How did a scrawny ape turn the savannah into a slaughterhouse?",
            "content_beats": [
                "The biological cheat code: Sweat glands and persistence hunting (running animals to hyperthermia)",
                "The invention that broke physics: Why throwing rocks with high shoulder torque terrified beasts",
                "Fire as a psychological weapon: The night predators lost control of darkness",
                "Wolf alliance: Turning nature's most ruthless hunters into tribal perimeter alarms",
                "Why animals still retain a genetic terror of human silhouettes today"
            ],
            "ai_prompt": "hand-drawn 2D cartoon doodle illustration of primitive stickman caveman holding sharp wooden spear standing tall in savannah grass, menacing giant saber tooth tiger shadow in corner, humorous expressive face, black ink pen stroke, clean flat color vintage paper texture --ar 16:9 --style raw"
        },
        {
            "id": "ink_04",
            "title": "Why Ancient Humans Were The Most TERRIFYING Animal Alive",
            "thumbnail_text": "BORN TO KILL?",
            "thumbnail_concept": "Crazy-eyed stickman with wild messy hair covered in red mud, grinning intensely, holding a sharpened rock. Bright cyan contrast background with bold yellow text.",
            "duration": "09:07",
            "views_benchmark": "3.8M+ Views",
            "virality_score": 96,
            "hook_script": "In nature documentaries, humans are always portrayed as fragile victims hiding in caves. But from the perspective of literally every other creature on planet Earth... Homo sapiens were the stuff of pure cosmic horror. We didn't sleep when they slept. We didn't stop when they ran. And if they escaped... we simply tracked their footprints for 40 miles until their heart exploded...",
            "content_beats": [
                "The horror of persistence hunting: The monster that never stops walking",
                "Tool crafting in front of prey: Weaponizing flint, sinew, and poison",
                "The extinction wave: Everywhere humans arrived, 80% of megafauna died in 200 years",
                "Tribal coordination: 30 hairless apes surrounding a 6-ton woolly mammoth",
                "The psychological burden of being the undisputed apex monster"
            ],
            "ai_prompt": "minimalist doodle comic illustration, wild stickman caveman with unhinged humorous grin holding stone club, black ink sketch, comic book style, bold outlines, vivid blue and parchment paper background --ar 16:9 --style raw"
        },
        {
            "id": "ink_05",
            "title": "The Disturbing Ways Ancient Humans Survived Winter",
            "thumbnail_text": "COZY INSIDE?",
            "thumbnail_concept": "Stickman family huddled inside a hollowed-out mammoth carcass with glowing campfire, snowy blizzards raging outside. Dark warm interior contrast with freezing exterior.",
            "duration": "11:31",
            "views_benchmark": "4.2M+ Views",
            "virality_score": 97,
            "hook_script": "Imagine standing in the European tundra 25,000 years ago. The temperature is -35 degrees Celsius. The blizzard has been howling for 14 straight days. You have no radiator, no down jackets, and the ground is frozen solid rock. How did humans survive an Ice Age with nothing but flint and mammoth bones? The answer involves architectural madness, body fat diets, and shelters made of literal corpses...",
            "content_beats": [
                "Mammoth bone architecture: The Ukrainian huts built from 70 mammoth skulls",
                "Sewing bone needles: The microscopic invention that saved humanity from freezing",
                "The 8,000-calorie winter diet: Eating raw bone marrow and seal blubber",
                "Hypothermia hallucinations: What ancient elders experienced in dark blizzards",
                "The spiritual rebirth of Spring: Why almost every human religion celebrates the sun"
            ],
            "ai_prompt": "hand-drawn doodle illustration of cavemen stick figures huddled inside cozy mammoth bone shelter around fire while blizzard snow blows outside, whimsical cartoon sketch, black ink contours, warm orange glow and cold blue exterior, textured aged paper --ar 16:9 --style raw"
        },
        {
            "id": "ink_06",
            "title": "How Did Ancient Humans Travel Across Entire Continents?",
            "thumbnail_text": "TRAVEL HOW?",
            "thumbnail_concept": "Two stickmen with funny tired eyes carrying woven backpacks, walking through an endless golden desert pointing into the distance. Bright blue sky.",
            "duration": "09:23",
            "views_benchmark": "1.8M+ Views",
            "virality_score": 93,
            "hook_script": "60,000 years ago, a group of humans stood on the eastern coast of Africa. There were no maps, no compasses, no roads, and no domesticated horses. Yet within a few thousand years, their descendants were living in the arctic freezing zones of Siberia and sailing canoes across 1,000 miles of open Pacific Ocean. How did naked apes navigate an untamed, monster-infested planet without ever getting lost?",
            "content_beats": [
                "The celestial GPS: Reading star alignments and bird migrations",
                "Coastline highways: Why beachcombing was the fastest transit system in history",
                "Water carrying secrets: Storing drinking water in buried ostrich eggshells",
                "Crossing the Bering Land Bridge into the Americas",
                "The mystery of Australian aboriginal navigation songs (Songlines)"
            ],
            "ai_prompt": "hand-drawn doodle stick figures walking through vast desert with primitive wooden walking sticks, funny expressions, black ink lines, pastel desert tones, retro cartoon storybook style --ar 16:9 --style raw"
        }
    ],

    "trending_info": [
        {
            "id": "info_01",
            "title": "Why American Suburbs Are Designed To Make You Lonely",
            "thumbnail_text": "TRAPPED IN SUBURBIA",
            "thumbnail_concept": "Endless identical cul-de-sac houses seen from aerial drone view, completely empty asphalt street, single sad silhouette looking out window. High contrast architectural graphic.",
            "duration": "14:10",
            "views_benchmark": "3.5M+ Views",
            "virality_score": 96,
            "hook_script": "If you look at an aerial photograph of any American city built after 1950, you will notice a bizarre pattern: thousands of identical houses, endless curving cul-de-sacs, and not a single grocery store, cafe, or park within walking distance. This wasn't an accident. It was the deliberate result of a 70-year lobbying experiment that made walking illegal and engineered modern isolation...",
            "content_beats": [
                "Euclidean Zoning: Why mixing bakeries with houses became a federal violation",
                "The destruction of the 'Third Place' (neither home nor work)",
                "How General Motors systematically bought and tore down electric streetcars",
                "The psychological toll of cul-de-sac isolation on teenagers and elderly",
                "The European contrast: Why 15-minute walkable cities report 40% lower loneliness"
            ],
            "ai_prompt": "aerial editorial photo of endless identical suburban houses in American cul-de-sac, empty concrete road, gloomy cinematic twilight lighting, dramatic architectural photography --ar 16:9 --style raw"
        },
        {
            "id": "info_02",
            "title": "The $100 Billion Industry Hiding in Abandoned US Malls",
            "thumbnail_text": "GHOST MALL BILLIONS",
            "thumbnail_concept": "Dimly lit abandoned 1980s shopping mall with shattered skylights, glowing server racks and robotic fulfillment machines operating in the dark. Intriguing retro-futuristic vibe.",
            "duration": "12:45",
            "views_benchmark": "2.2M+ Views",
            "virality_score": 94,
            "hook_script": "Across America, over 1,000 giant shopping malls sit abandoned, rotting in silence. To the average person, they look like bankrupt relics of the 90s. But behind boarded-up Sears doors and broken escalators, the world's richest tech giants and medical conglomerates are quietly buying them for pennies on the dollar. Inside these dead malls, a secret $100 billion goldmine has just been activated...",
            "content_beats": [
                "The death spiral of anchor department stores (Macy's, JCPenney, Sears)",
                "Why Amazon and logistics firms love the physical infrastructure of dead malls",
                "Conversion into hyperscale AI data centers: Power grid access and cooling towers",
                "Micro-fulfillment ghost kitchens and outpatient mega-clinics",
                "The future of American retail: Can real estate ever recover?"
            ],
            "ai_prompt": "cinematic moody shot inside a massive abandoned 1990s shopping mall being retrofitted with glowing blue high-tech server racks, neon reflections on dusty marble tiles, cinematic depth of field --ar 16:9"
        },
        {
            "id": "info_03",
            "title": "Why Gen Z Is Ditching Smartphones For $20 Flip Phones",
            "thumbnail_text": "DUMBPHONES WINNING?",
            "thumbnail_concept": "Hand holding a classic silver Motorola Razr flip phone illuminated against a dark background, contrasted with cracked glowing iPhone showing notification chaos. Clean tech aesthetic.",
            "duration": "10:50",
            "views_benchmark": "1.9M+ Views",
            "virality_score": 93,
            "hook_script": "Every year, Apple and Samsung spend billions trying to convince you that you need a faster 120Hz display, 48 megapixels, and titanium frames. Yet in 2026, millions of teenagers and college students across the US and Europe are doing the unthinkable: tossing their $1,200 iPhones in drawers and buying 2005 Nokia bricks and flip phones. Why are the most digitally native humans in history choosing to go blind?",
            "content_beats": [
                "The dopamine fatigue epidemic: How infinite scroll broke attention spans",
                "The rise of the 'Luddite Club' in Brooklyn and universities worldwide",
                "What actually happens to your brain chemistry after 7 days without push notifications",
                "The underground economy of refurbished vintage cellphones",
                "Can you actually survive in 2026 without QR codes, two-factor apps, and Uber?"
            ],
            "ai_prompt": "modern minimalist studio photograph of a vintage silver flip phone resting on a slate dark desk next to a notebook and coffee, cinematic moody side lighting --ar 16:9"
        }
    ],

    "hamza_tech": [
        {
            "id": "tech_01",
            "title": "After Effects Secrets I Wish I Knew 5 Years Ago",
            "thumbnail_text": "AE SECRETS! ⚡",
            "thumbnail_concept": "Hamza Tufail on left with an expressive surprised expression looking at glowing holographic After Effects timeline, bold neon purple/cyan speed lines, '10X FASTER' badge.",
            "duration": "13:20",
            "views_benchmark": "450K+ Views",
            "virality_score": 98,
            "hook_script": "If your After Effects previews lag like a slideshow, or you spend 45 minutes manually moving keyframes for a simple text bounce... you are working against the software. In this video, I'm breaking down the exact 7 secret shortcuts, expression rigs, and caching settings that took me from an exhausted, underpaid editor to delivering Hollywood-tier motion graphics in half the time...",
            "content_beats": [
                "Secret #1: The one memory cache configuration that stops AE from freezing forever",
                "Secret #2: The universal bounce & overshoot expression you can copy-paste in 2 seconds",
                "Secret #3: Master of Graph Editor: Value vs Speed Graph simplified once and for all",
                "Secret #4: Essential Graphics (MOGRTs): Turning 5 hours of work into a 30-second drag-and-drop",
                "Secret #5: Null Object parenting hierarchies for cinematic 3D camera sweeps"
            ],
            "ai_prompt": "professional YouTuber studio photography, young confident creative male tech editor sitting at modern desk with dual curved monitors displaying Adobe After Effects timeline, moody ambient purple and cyan studio rim lighting, 8k resolution, crisp focus --ar 16:9"
        },
        {
            "id": "tech_02",
            "title": "How to Recreate The Vox / Johnny Harris Map & Paper Animation in AE",
            "thumbnail_text": "VOX STYLE MAPS",
            "thumbnail_concept": "Hamza pointing towards a 3D isometric vintage map with realistic torn paper edges, glowing red route line, and 3D pin. Bold yellow text on dark background.",
            "duration": "16:45",
            "views_benchmark": "650K+ Views",
            "virality_score": 97,
            "hook_script": "You've seen it on Vox, Johnny Harris, and every multi-million view documentary on YouTube: that tactile, organic animation where a vintage map folds out, paper textures crumble, and the camera flies over the topography like a spy thriller. Today, I'm opening After Effects and showing you how to build this exact signature look from scratch without paying $300 for expensive plugins...",
            "content_beats": [
                "Sourcing high-res open-source archival maps and satellite elevation data",
                "Creating realistic paper folds and displacement maps in Photoshop",
                "After Effects 3D camera animation with depth of field and organic camera wiggle",
                "The 'Trim Paths' glowing route trick that guides the viewer's eye",
                "Layering paper foley, tape crinkles, and projection sounds for 100% immersion"
            ],
            "ai_prompt": "3D motion graphics isometric render of vintage textured world map with glowing neon topographic elevation contours, torn paper edges, cinematic dramatic lighting --ar 16:9"
        },
        {
            "id": "tech_03",
            "title": "How I Land $3,000/mo International Video Editing Clients from Home",
            "thumbnail_text": "$3,000/MO CLIENTS",
            "thumbnail_concept": "Hamza holding coffee mug at desk with laptop displaying Stripe dashboard ($3,500 payout notification) and Premiere Pro project. Bold green dollar badge.",
            "duration": "15:10",
            "views_benchmark": "380K+ Views",
            "virality_score": 95,
            "hook_script": "Upwork is saturated. Fiverr is a race to the bottom where people edit videos for $5. So how are editors in Pakistan, India, and across the globe making $3,000 to $6,000 every single month working remotely with US and UK creators? The secret isn't having the fastest computer. It's understanding client acquisition. In this video, I'll give you my exact cold outreach email, portfolio template, and the one offer creators can't say no to...",
            "content_beats": [
                "Why freelance platforms are designed to keep you broke",
                "The 'Free 60-Second Retention Sample' method that has a 45% reply rate",
                "How to audit a YouTuber's channel and find their exact retention drop points",
                "Pricing psychology: Transitioning from per-video gig to $2,500/mo retainers",
                "Contract templates, international payment gateways (Wise, Payoneer), and onboarding"
            ],
            "ai_prompt": "stylish cinematic portrait of a professional video editor working in a cozy modern creative home studio with warm wooden desk, mechanical keyboard, and glowing monitors --ar 16:9"
        }
    ],

    "urdu_dastaan": [
        {
            "id": "urdu_01",
            "title": "Sultan Salahuddin Ayyubi Aur Third Crusade Ki Khufia Hikmat-e-Amli",
            "thumbnail_text": "صلاح الدین کا وار؟",
            "thumbnail_concept": "Dramatic cinematic silhouette of Sultan Salahuddin in royal golden armor on horse overlooking burning Jerusalem walls at sunset. Arabic calligraphy accent with glowing embers.",
            "duration": "22:15",
            "views_benchmark": "1.2M+ Views",
            "virality_score": 99,
            "hook_script": "Hittin ke maidan mein jab 20,000 Crusader sipahion ko pyas aur aag ne gher liya... to unhein pata nahi tha ke unka samna tareekh ke sabse ba-sha'oor aur reham-dil commander se hone ja raha hai. Salahuddin Ayyubi ne na sirf Bait-ul-Muqaddas ko 88 saal baad azaad karwaya, balke unke dushman Richard the Lionheart unki tareef karne par majboor kyun hue? Ye hai dastaan us sultan ki jiski talwar insaf karti thi...",
            "content_beats": [
                "Battle of Hattin: The psychological water trap that broke the Crusader army",
                "The Liberation of Jerusalem without spilling innocent blood (Contrast with 1099 massacre)",
                "The personal duel of wits: Sultan Salahuddin vs. King Richard the Lionheart",
                "Secret diplomacy, mutual respect, and medicine sent to the wounded enemy king",
                "Lessons in leadership, character, and strategic endurance for our modern world"
            ],
            "ai_prompt": "epic cinematic oil painting illustration of Sultan Saladin in medieval ornate armor with turban, riding a majestic Arabian horse on a hill overlooking desert battle at golden sunset, intense dust and cinematic drama --ar 16:9"
        },
        {
            "id": "urdu_02",
            "title": "Babur Ki 12,000 Fouj Ne Ibrahim Lodi Ke 100,000 Lashkar Ko Kaise Shikast Di? (Panipat 1526)",
            "thumbnail_text": "12,000 VS 100,000!",
            "thumbnail_concept": "Zahiruddin Muhammad Babur aiming matchlock muskets and cannons against waves of 1,000 war elephants. Explosions, smoke, and thunderous battlefield clash in Panipat.",
            "duration": "18:40",
            "views_benchmark": "950K+ Views",
            "virality_score": 98,
            "hook_script": "Subah ke 6 baj rahe the. Panipat ke maidan mein ek taraf Delhi ke Sultan Ibrahim Lodi ka 100,000 ka azeem-o-shaan lashkar aur 1,000 jung-ju haathi kharay thay. Dusri taraf Fergana se nikala gaya be-watan shahzada Zahiruddin Muhammad Babur sirf 12,000 thakay hue sipahion ke sath khara tha. Qanoon-e-qudrat ke mutabiq Babur ki maut yaqini thi. Lekin dhoop dhalte hi Lodi mara ja chuka tha aur Hindustan par Mughal Saltanat ki buniyaad rakh di gayi...",
            "content_beats": [
                "Babur's Fergana exile and desperate quest for a kingdom",
                "The Ottoman Tulghuma military formation and Rumi cart barricades",
                "The deafening debut of gunpowder and cannons in the Indian Subcontinent",
                "How elephants panicked and trampled their own royal Delhi army",
                "Babur's diary entry (Baburnama) describing the psychological aftermath of victory"
            ],
            "ai_prompt": "dramatic historical painting of Emperor Babur on horseback directing Ottoman gunpowder cannons and musketeers behind chained wooden wagons in Battle of Panipat 1526, war elephants retreating in chaos, smoke and battlefield dust --ar 16:9"
        },
        {
            "id": "urdu_03",
            "title": "Hasan Bin Sabah Aur Alamut Ke Assassins: Tareekh Ka Sabse Khaufnak Secret Order",
            "thumbnail_text": "قاتلوں کا قلعہ؟",
            "thumbnail_concept": "Misty, impenetrable mountain fortress of Alamut perched on sheer cliffs under moonlight, hooded shadow assassin figure with dagger in foreground.",
            "duration": "20:05",
            "views_benchmark": "1.5M+ Views",
            "virality_score": 98,
            "hook_script": "Iran ke Alborz paharon ki 6,000 foot buland choti par ek qila tha jiska naam sun kar Baghdad ke Abbasi Khalifa aur Isfahan ke Saljuqi Sultan raat ko khauf se kaanp uthte thay. Yeh tha Alamut—aur iska malik tha ek azeem riyazi-dan aur philosopher Hasan Bin Sabah. Jisne aam lashkar banane ke bajaye aise 'Fedayeen' tayyar kiye jo dushman ke bistar mein dagger gaarh kar nikal jate thay...",
            "content_beats": [
                "The enigmatic life of Hasan Bin Sabah and the bloodless capture of Alamut Castle",
                "The psychological conditioning and secret garden of the Hashashin (Assassins)",
                "The terrifying assassination of Nizam al-Mulk: How one shadow changed an empire",
                "Why Saladin woke up with a poisoned dagger and fresh loaf of bread next to his pillow",
                "The Mongol onslaught of Hulagu Khan and the fiery destruction of Alamut"
            ],
            "ai_prompt": "atmospheric dark fantasy oil painting of the mysterious mountain fortress of Alamut built into sheer mountain cliffs under moonlight, fog rolling through valleys, dark hooded assassin with dagger silhouette in foreground --ar 16:9"
        }
    ]
}

# --- SPECIALIZED "INK EXPLAINER" AI PROMPT GENERATOR ENGINE ---
INK_EXPLAINER_STYLE_CONFIG = {
    "core_aesthetic": "hand-drawn doodle cartoon illustration, minimalist 2D black ink outline, expressive humorous stickman character, flat vintage parchment background, storybook animation still",
    "character_presets": [
        "prehistoric caveman stick figure in ragged brown animal fur tunic holding flint spear",
        "worried modern human stickman wearing necktie and carrying briefcase looking stressed",
        "ancient Egyptian stickman builder staring in confusion at giant pyramid stone",
        "medieval armored knight stickman holding bent wooden shield and sword",
        "curious philosopher stickman with cartoon beard sitting under olive tree scratching head"
    ],
    "setting_presets": [
        "sun-drenched prehistoric savannah grass with distant acacia trees under warm pale sky",
        "cozy flickering campfire inside limestone cave with faint charcoal stickman drawings on walls",
        "endless rolling golden sand dunes under scorching desert sun",
        "freezing glacial Ice Age blizzard with huddling mammoth silhouettes in background",
        "primitive tribal village with straw huts and smoking cooking pit"
    ],
    "mood_presets": [
        "humorous, comically relaxed and oblivious to danger",
        "panicked, wide-eyed with exaggerated comical sweat drops",
        "smug and clever, pointing finger up having a eureka lightbulb moment",
        "exhausted and groaning, flat on back after running for hours",
        "curious and bewildered, poking a strange object with a long wooden stick"
    ]
}

def generate_ink_explainer_prompt(topic: str, scene_type: Optional[str] = None) -> Dict[str, str]:
    """Generates an authentic Midjourney v6 / Flux prompt for Ink Explainer hand-drawn doodle art."""
    char = random.choice(INK_EXPLAINER_STYLE_CONFIG["character_presets"])
    setting = random.choice(INK_EXPLAINER_STYLE_CONFIG["setting_presets"])
    mood = random.choice(INK_EXPLAINER_STYLE_CONFIG["mood_presets"])
    
    clean_topic = topic.strip() if topic else "Ancient human survival and curiosity"
    
    prompt = (
        f"minimalist hand-drawn doodle cartoon illustration in Ink Explainer style, {char}, {mood}, "
        f"scene depicting '{clean_topic}', set in {setting}, "
        f"simple 2D clean black ink contours, expressive cartoon eyes, warm beige textured parchment background, "
        f"editorial book art style, flat muted pastel accents, no gradients, no photorealism --ar 16:9 --style raw"
    )
    
    after_effects_workflow = (
        "1. Import PNG into After Effects -> Pre-compose.\n"
        "2. Add effect 'Posterize Time' set to 12fps (gives true hand-drawn anime/doodle cadence).\n"
        "3. Add 'Turbulent Displace' (Size: 3, Amount: 4, Evolution expression: time*25) for boiling hand-drawn line jitter.\n"
        "4. Use Puppet Pin Tool on stickman arms/head for squash and stretch.\n"
        "5. Underlay paper texture JPG with Blend Mode 'Multiply' (Opacity: 45%).\n"
        "6. Layer dry wood pop, whoosh, and funny mouth vocal foley on every movement."
    )
    
    return {
        "topic": clean_topic,
        "full_prompt": prompt,
        "negative_prompt": "photorealistic, 3d render, glossy, high poly, gradients, blurry, complex shading, neon glow",
        "recommended_aspect_ratio": "--ar 16:9",
        "after_effects_recipe": after_effects_workflow
    }

def get_youtube_studio_overview() -> Dict[str, Any]:
    """Returns complete channel blueprints, viral topics, and workflow setups."""
    return {
        "channels": YOUTUBE_CHANNELS,
        "video_blueprints": VIRAL_VIDEO_BLUEPRINTS,
        "ink_explainer_config": INK_EXPLAINER_STYLE_CONFIG,
        "quick_stats": {
            "total_channels": len(YOUTUBE_CHANNELS),
            "total_curated_ideas": sum(len(v) for v in VIRAL_VIDEO_BLUEPRINTS.values()),
            "creator_name": "Hamza Tufail",
            "production_ready": True
        }
    }

def generate_viral_video_idea(channel_id: str, seed_keyword: Optional[str] = None) -> Dict[str, Any]:
    """Generates a dynamic viral video concept tailored for the chosen channel."""
    keyword = (seed_keyword or "").strip()
    
    if channel_id == "ink_explainer":
        subjects = [
            ("How Did Ancient Humans Sleep Without Getting Eaten?", "SLEEP HOW?", "Stickman caveman sleeping in tree limb curled up, funny snoring bubble, hyena looking up comically."),
            ("What Did Ancient Humans Do When It Rained For Weeks?", "RAIN TRAPPED", "Stickman family bored inside cave listening to rain puddles, playing with pebbles with deadpan faces."),
            ("The First Human to Ever Eat A Mushroom (Accidental Discoveries)", "ATE WHAT?!", "Caveman holding giant polka-dot mushroom with spiraling hypnotic eyes, glowing aura."),
            ("Why Did Ancient Humans Wear Clothes If They Were Already Hairy?", "NO FUR?", "Caveman shivering in wind looking at woolly mammoth with envy, wearing goofy giant leaves."),
            ("How Ancient Humans Made Fire (Before Matches Existed)", "FIRE HOW?!", "Stickman furiously rubbing two twigs together with sweaty comic face, spark finally appearing.")
        ]
        chosen = random.choice(subjects)
        topic_title = f"{chosen[0]} ({keyword})" if keyword else chosen[0]
        return {
            "channel_id": channel_id,
            "channel_name": "Ink Explainer",
            "title": topic_title,
            "thumbnail_text": chosen[1],
            "thumbnail_concept": chosen[2],
            "estimated_rpm": "$4.50 – $9.00",
            "hook_duration": "First 15 seconds",
            "hook_formula": "Disrupt an assumed modern comfort -> Reveal what humans did for 200,000 years -> Pose the shocking consequence.",
            "virality_score": random.randint(94, 99),
            "ai_prompt": generate_ink_explainer_prompt(topic_title)["full_prompt"]
        }

    elif channel_id == "trending_info":
        subjects = [
            ("The Strange Reason Why American Grocery Stores Play French Accordion Music", "STORE PSYCHOLOGY", "Shopper in supermarket aisle reaching for expensive wine, hypnotic subtle musical notes floating."),
            ("Why 90% of US Fast Food Signs Use Only Red and Yellow", "THE HUNGER CODE", "Glowing McDonald's, Wendy's, and Burger King logos towering over highway at night."),
            ("How 1 Company Secretly Owns 80% of All Prescription Glasses (Luxottica)", "GLASSES MONOPOLY", "Rows of designer sunglasses (Ray-Ban, Oakley, Gucci) all wired back to one corporate boardroom."),
            ("The Million-Dollar Battle for the Bottom Shelf at Walmart", "SHELF WARS", "Grocery aisle with glowing golden bottom shelf vs invisible top shelf.")
        ]
        chosen = random.choice(subjects)
        topic_title = f"{chosen[0]} ({keyword})" if keyword else chosen[0]
        return {
            "channel_id": channel_id,
            "channel_name": "Curious Atlas (US Info)",
            "title": topic_title,
            "thumbnail_text": chosen[1],
            "thumbnail_concept": chosen[2],
            "estimated_rpm": "$8.00 – $16.00",
            "hook_duration": "First 20 seconds",
            "hook_formula": "Show an everyday object you take for granted -> Expose the multi-billion dollar manipulation behind it.",
            "virality_score": random.randint(92, 98),
            "ai_prompt": f"cinematic high contrast editorial photo of {chosen[1]}, moody documentary lighting, 8k resolution, cinematic color grade --ar 16:9"
        }

    elif channel_id == "hamza_tech":
        subjects = [
            ("5 Fast After Effects Hacks That Will Cut Your Editing Time By 50%", "5X FASTER AE!", "Hamza looking at timer showing 10 min vs 2 hours, glowing timeline."),
            ("How to Build a Reusable YouTube Title MOGRT in After Effects", "DRAG & DROP AE", "Hamza dragging animated kinetic title from Essential Graphics into Premiere Pro."),
            ("The Audio & Sound Design Secret That Makes Videos Feel 10x More Cinematic", "AUDIO SECRETS", "Audio waveform with glowing gold impact hits and sub-bass frequencies."),
            ("How to Get Your First $1,000 Video Editing Client (No Experience)", "FIRST $1,000 CLIENT", "Clean email inbox showing accepted proposal and contract.")
        ]
        chosen = random.choice(subjects)
        topic_title = f"{chosen[0]} ({keyword})" if keyword else chosen[0]
        return {
            "channel_id": channel_id,
            "channel_name": "Hamza Tufail Tech & Editing",
            "title": topic_title,
            "thumbnail_text": chosen[1],
            "thumbnail_concept": chosen[2],
            "estimated_rpm": "$12.00 – $22.00",
            "hook_duration": "First 10 seconds",
            "hook_formula": "State the common editor frustration -> Show the finished result in 3 seconds -> Promise the exact step-by-step breakdown.",
            "virality_score": random.randint(93, 98),
            "ai_prompt": f"modern creative tech YouTube thumbnail photography of Hamza Tufail demonstrating video editing techniques, studio lighting, vivid glowing UI accents --ar 16:9"
        }

    else: # urdu_dastaan
        subjects = [
            ("Tipu Sultan Ki Missile Technology: Jisne British East India Company Ko Khaufzada Kar Diya", "ٹیپو کے راکٹ!", "Tipu Sultan in green silk coat aiming iron-cased Mysorean rockets against British artillery lines."),
            ("Baghdad Ka Woh Khooni Saal 1258: Jab Darya-e-Dajla Siyahi Aur Khoon Se Bhar Gaya", "بغداد کی تباہی", "Mongol siege towers surrounding Baghdad, smoke billowing from Grand Library of Wisdom (Bayt al-Hikma)."),
            ("Mughal Shehenshah Aurangzeb Alamgir: Tareekh Ka Sabse Mutanazia Badshah", "اورنگزیب کی حقیقت", "Emperor Aurangzeb sitting on simple prayer rug in battle tent, reading Quran with sword nearby at dusk."),
            ("Tariq Bin Ziyad Aur Kashti Jalane Ka Waqia: Jabal-e-Tariq (Gibraltar) Ka Ma'arka", "کشتیاں جلا دو!", "Tariq Bin Ziyad pointing sword towards Spain coast as ships burn in Mediterranean waters.")
        ]
        chosen = random.choice(subjects)
        topic_title = f"{chosen[0]} ({keyword})" if keyword else chosen[0]
        return {
            "channel_id": channel_id,
            "channel_name": "Dastaan-e-Tareekh with Hamza Tufail",
            "title": topic_title,
            "thumbnail_text": chosen[1],
            "thumbnail_concept": chosen[2],
            "estimated_rpm": "$2.00 – $4.50",
            "hook_duration": "First 30 seconds",
            "hook_formula": "Dhamakedar tareekhi sawal se aaghaz -> Maidan-e-jung ka naqsha khainchna -> Dastaan ke pehle mod par lana.",
            "virality_score": random.randint(95, 99),
            "ai_prompt": f"epic cinematic historical painting of {chosen[1]}, dramatic war scene, oil painting style, golden hour dust and atmosphere --ar 16:9"
        }
