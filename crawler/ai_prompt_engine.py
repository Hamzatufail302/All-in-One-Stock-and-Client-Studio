"""
AI Prompt & Creative Asset Generation Engine
Produces commercial-grade AI image/video prompts and asset production guidelines
tailored specifically for Adobe Stock, Shutterstock, Etsy, IconScout, and GraphicRiver.
Includes clear, precise multi-model prompts (Midjourney v6.1, Flux.1 Pro, 4K Video),
visual style references (--sref), benchmark moodboards, and rejection-proof quality parameters.
"""

import re
from .deadline_engine import get_keyword_deadline

PLATFORM_AI_POLICIES = {
    "adobe_stock": {
        "status": "Accepted & Encouraged",
        "badge_color": "emerald",
        "accepts_images": True,
        "accepts_videos": True,
        "policy_summary": "Adobe Stock fully accepts both Generative AI images and video footage. You must toggle the 'Created using generative AI tools' checkbox during upload.",
        "key_rules": [
            "Do NOT include trademarked names, logos, or recognizable celebrity likenesses.",
            "Property release is required if depicting private property or real landmarks.",
            "Must be upscaled to minimum 4 Megapixels (standard 4000x3000px or higher) with zero artifacts.",
            "Video must be clean 4K or 1080p without AI warping, weird limb deformations, or flickers."
        ]
    },
    "shutterstock": {
        "status": "Internal Engine Only (Strict Third-Party Rules)",
        "badge_color": "amber",
        "accepts_images": False,
        "accepts_videos": False,
        "policy_summary": "Shutterstock only sells AI images generated directly on their internal AI tool (powered by OpenAI). External Midjourney/Flux/Google Flow AI visuals are generally rejected to protect commercial indemnification.",
        "key_rules": [
            "Do not upload external Midjourney or third-party AI images as standard stock photos.",
            "Contributors earn passively if their historical portfolio was used to train Shutterstock AI models (Contributor Fund).",
            "Stick to your vectors, PSD mockups, and real camera footage for Shutterstock."
        ]
    },
    "etsy": {
        "status": "100% Accepted & Huge Market",
        "badge_color": "emerald",
        "accepts_images": True,
        "accepts_videos": True,
        "policy_summary": "Etsy fully permits AI-generated art, clipart bundles, printable wall art, and Canva templates utilizing AI graphics as long as you disclose your process.",
        "key_rules": [
            "Top seller on Etsy: AI Clipart PNG bundles (300 DPI transparent background).",
            "AI Printable Wall Art (provided in 5 aspect ratios: 2:3, 3:4, 4:5, ISO, 11:14).",
            "Must provide high resolution (minimum 3000x3000px at 300 DPI)."
        ]
    },
    "iconscout": {
        "status": "Accepted for 3D Renders with Clean Alpha",
        "badge_color": "blue",
        "accepts_images": True,
        "accepts_videos": False,
        "policy_summary": "IconScout accepts 3D illustrations generated with AI if they are cleanly cut out with transparent backgrounds and meet UI asset quality.",
        "key_rules": [
            "Must be isolated on 100% transparent PNG, no fringe or halo artifacts around edges.",
            "Must be consistent in lighting and angle (claymorphism, isometric, or glassmorphism)."
        ]
    },
    "graphicriver": {
        "status": "Allowed as Design Elements in Layered PSD",
        "badge_color": "purple",
        "accepts_images": True,
        "accepts_videos": False,
        "policy_summary": "GraphicRiver allows AI-generated textures, background art, and composite elements when built into layered, editable Photoshop or Illustrator templates.",
        "key_rules": [
            "Raw flat AI images are not accepted; must be packaged as an editable template (Flyer, Poster, Mockup).",
            "Must be organized into color-coded PSD layers with editable text."
        ]
    }
}

# Curated High-Converting Style Reference Presets for Stock Contributors
CURATED_STYLE_REFERENCES = [
    {
        "id": "corporate_clean",
        "name": "Corporate Minimalist Clean",
        "benchmark": "Forbes & Monocle Modern Business Editorial",
        "sref_code": "https://images.unsplash.com/photo-1497366216548-37526070297c",
        "description": "High-key diffused daylight, crisp slate & glass architectural palette, clean professional aesthetic",
        "recommended_for": "Business, Tech, Office, Finance"
    },
    {
        "id": "kinfolk_lifestyle",
        "name": "Kinfolk Warm Editorial",
        "benchmark": "Kinfolk & Cereal Magazine Lifestyle",
        "sref_code": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4",
        "description": "Warm golden morning light, authentic skin texture with real pores, muted terracotta and olive tones",
        "recommended_for": "Lifestyle, People, Travel, Coffee"
    },
    {
        "id": "luxury_podium",
        "name": "Luxury Studio Still Life",
        "benchmark": "Architectural Digest & Aesop Cosmetics",
        "sref_code": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9",
        "description": "Travertine marble pedestal, dramatic architectural window shadow casting, ample negative space",
        "recommended_for": "Products, Mockups, Packaging, Flatlays"
    },
    {
        "id": "octane_3d",
        "name": "3D Octane / Cinema 4D Iridescent",
        "benchmark": "Apple Keynote & Behance 3D Art",
        "sref_code": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe",
        "description": "Translucent glass refraction, soft caustics, vibrant pearlescent fluid waves, studio specular shine",
        "recommended_for": "Abstract, Backgrounds, AI, Web Graphics"
    },
    {
        "id": "scandi_nordic",
        "name": "Nordic Scandi Minimalist",
        "benchmark": "IKEA Design & Scandinavian Interior",
        "sref_code": "https://images.unsplash.com/photo-1513694203232-719a280e022f",
        "description": "Light oak wood, matte off-white ceramics, soft shadow falloff, spacious tranquil atmosphere",
        "recommended_for": "Home, Cozy, Food, Flatlay"
    },
    {
        "id": "cyberpunk_neon",
        "name": "Cyberpunk Holographic Tech",
        "benchmark": "Wired & Sci-Fi Concept Art",
        "sref_code": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5",
        "description": "Dark atmospheric backdrop, electric cyan and magenta neon accents, volumetric particle rays",
        "recommended_for": "Cybersecurity, Gaming, Sci-Fi, Data"
    }
]

NEGATIVE_PROMPT_DEFAULT = (
    "text, watermark, typography, font, company logo, trademark, brand label, signature, "
    "extra fingers, deformed hands, missing fingers, fused digits, malformed limbs, bad anatomy, "
    "blurry, plastic airbrushed skin, unnatural doll face, distorted eyes, digital noise, "
    "jpeg artifacts, oversaturated colors, harsh chromatic aberration, duplicate subjects, uncanny valley"
)

def detect_keyword_genre(keyword: str) -> str:
    """Intelligently detects commercial stock photography genre from search query."""
    kw = keyword.lower()

    if any(w in kw for w in ["business", "corporate", "office", "team", "meeting", "finance", "money", "startup", "entrepreneur", "workspace", "executive", "leadership", "professional", "presentation", "handshake", "consulting", "banking", "investment", "coworking", "remote work"]):
        return "corporate"
    if any(w in kw for w in ["tech", "technology", "ai", "artificial intelligence", "cyber", "code", "coding", "data", "cloud", "network", "robot", "robotics", "futuristic", "circuit", "server", "software", "machine learning", "virtual", "hologram", "algorithm", "iot"]):
        return "technology"
    if any(w in kw for w in ["medical", "doctor", "nurse", "hospital", "health", "healthcare", "clinic", "medicine", "patient", "therapy", "dental", "pharma", "laboratory", "lab", "dna", "biotech", "virus", "vaccine", "science", "biology", "wellness"]):
        return "healthcare"
    if any(w in kw for w in ["food", "coffee", "cafe", "restaurant", "culinary", "cooking", "chef", "recipe", "breakfast", "dinner", "lunch", "bakery", "dessert", "tea", "drink", "cocktail", "wine", "fruit", "vegetable", "gourmet", "meal", "plate"]):
        return "culinary"
    if any(w in kw for w in ["product", "mockup", "packaging", "cosmetic", "bottle", "jar", "box", "podium", "pedestal", "flatlay", "perfume", "skincare", "tube", "can", "label", "stationery", "soap", "candle"]):
        return "product"
    if any(w in kw for w in ["abstract", "3d", "background", "wallpaper", "texture", "fluid", "wave", "liquid", "glass", "glassmorphism", "iridescent", "gradient", "pattern", "render", "geometric", "sphere", "particle", "ribbon", "marble"]):
        return "abstract_3d"
    if any(w in kw for w in ["nature", "landscape", "travel", "mountain", "forest", "ocean", "sea", "beach", "sunrise", "sunset", "river", "eco", "green energy", "solar", "wind turbine", "sustainable", "environment", "earth", "climate", "flower", "foliage"]):
        return "nature_eco"
    if any(w in kw for w in ["lifestyle", "people", "family", "child", "children", "kid", "woman", "man", "fitness", "gym", "yoga", "workout", "running", "sport", "home", "cozy", "autumn", "winter", "spring", "summer", "christmas", "holiday", "portrait"]):
        return "lifestyle_people"

    return "general_commercial"

def build_commercial_prompt_components(clean_kw: str, genre: str, custom_ref_url: str = None) -> dict:
    """
    Builds precise, high-fidelity prompt components tailored to specific commercial genres.
    Eliminates vague buzzwords and specifies exact scene composition, lighting, camera optics,
    commercial negative copy space, and visual style benchmarks.
    """
    title_kw = clean_kw.title()

    if genre == "corporate":
        scene = (
            f"An authentic commercial stock photograph of a collaborative team engaged in {clean_kw}. "
            f"Diverse professionals in contemporary business-casual attire (fine merino wool, crisp linen) "
            f"reviewing analytical blueprints and digital metrics around a natural oak standing desk in a bright architectural boardroom. "
            f"Genuine, spontaneous unposed facial expressions, relaxed and confident demeanor with zero artificial corporate smiles."
        )
        camera = "Shot on Sony A7R V with 50mm f/1.8 G Master prime lens at f/2.2, crisp focal plane on primary subjects with creamy organic depth of field falloff"
        lighting = "Soft directional morning daylight streaming through floor-to-ceiling glass windows from the left, subtle warm ambient fill, natural 1:2 lighting ratio"
        negative_space = "Generous clean negative copy space on the upper left third, optimized for commercial advertising headlines and pitch deck typography"
        color_palette = "Refined corporate palette: warm light oak, matte architectural slate, neutral whites, and authentic human skin tones with visible skin pores and fabric weave"
        benchmark = "Forbes & Monocle Modern Business Editorial"
        ref_preset = CURATED_STYLE_REFERENCES[0]

        flux_desc = (
            f"A high-resolution commercial stock photograph capturing an authentic business moment of {clean_kw} in a modern sunlit architectural office. "
            f"A diverse group of three professionals are naturally engaged in discussion around a light oak conference desk. "
            f"Shot at eye level with a 50mm prime lens at f/2.2, creating a gentle background blur that softly separates the subjects from the glass interior. "
            f"The lighting is diffuse natural daylight entering from large side windows, casting soft realistic contact shadows. "
            f"Real human details include authentic skin texture, natural catchlights in the eyes, and crisp fabric weaves. "
            f"The upper left flank provides ample negative space suitable for commercial text overlay. Neutral, clean color grading."
        )
        video_motion = (
            f"Cinematic 4K 60fps slow-motion stock video b-roll of diverse business colleagues collaborating on {clean_kw}. "
            f"Smooth motorized gimbal push-in shot, soft rack focus from natural wood table to engaged smiling faces, "
            f"natural morning window lighting with warm ambient bounce, stabilized tracking, ProRes 422 color profile, zero AI warping or flickering"
        )

    elif genre == "technology":
        scene = (
            f"A cutting-edge commercial visualization of {clean_kw}, featuring layered translucent frosted glassmorphism HUD data panels, "
            f"luminous fiber-optic data streams, and holographic network nodes floating in a pristine cleanroom tech laboratory setting. "
            f"Crisp geometric interfaces, subtle ambient volumetric haze, and refined specular caustics reflecting off polished dark anodized aluminum."
        )
        camera = "Shot on Hasselblad H6D-100c with 85mm f/2.0 lens, tack-sharp focal clarity on central data interface with gentle atmospheric depth"
        lighting = "Deep studio ambient lighting illuminated with volumetric electric cyan and subtle neon violet rim highlights, soft internal bioluminescent glow"
        negative_space = "Spacious dark-mode negative copy space across the right half, tailored for enterprise SaaS website hero headers and keynote presentation slides"
        color_palette = "Cybernetic deep obsidian, cool slate gray, vibrant electric cyan, and soft holographic magenta accents with realistic optical glass reflections"
        benchmark = "Apple Keynote Graphics & Wired Magazine Tech Visualization"
        ref_preset = CURATED_STYLE_REFERENCES[3]

        flux_desc = (
            f"A sophisticated commercial technology visual representing {clean_kw} in a minimalist futuristic laboratory. "
            f"Translucent frosted glass UI cards and luminous floating data nodes are arranged in clean dimensional layers. "
            f"Captured with an 85mm lens with volumetric depth, featuring sharp specular reflections and refractive light bending through optical glass. "
            f"Volumetric cyan and deep violet accent lighting against a dark neutral studio background. "
            f"The right half of the frame remains clear with expansive negative space for modern typography and headline text. Clean high-tech commercial finish."
        )
        video_motion = (
            f"Seamless 4K 60fps stock video loop of holographic data particles and glowing circuit streams flowing around {clean_kw}. "
            f"Smooth 360-degree turntable camera rotation, gentle volumetric light pulses, dark futuristic studio atmosphere, "
            f"ProRes 422, zero jitter or motion distortion, perfect infinite loop for enterprise tech hero banners"
        )

    elif genre == "healthcare":
        scene = (
            f"An authentic and empathetic commercial stock photograph of {clean_kw} in a contemporary, sunlit clinical environment. "
            f"A caring medical professional interacting warmly with a patient, holding a modern digital diagnostic tablet, "
            f"reassuring body language, genuine human connection, clean architectural clinic with soft pastel accents and green indoor plants."
        )
        camera = "Shot on Leica SL2 with Summilux 50mm f/1.4 ASPH lens at f/2.0, intimate medium close-up, sharp eye catchlights, natural authentic skin texture"
        lighting = "Diffused natural northern daylight combined with a soft 120cm octabox fill, soft shadow transitions, warm comforting clinical atmosphere"
        negative_space = "Clean, uncluttered negative copy space on the upper right flank for healthcare insurance slogans, hospital branding, and editorial text"
        color_palette = "Soft medical teal, clean crisp white, warm natural beech wood, and genuine unblemished human skin tones with visible natural pores"
        benchmark = "Mayo Clinic & Scientific American Modern Healthcare Editorial"
        ref_preset = CURATED_STYLE_REFERENCES[0]

        flux_desc = (
            f"A photorealistic commercial stock photograph depicting {clean_kw} inside a bright, modern medical consultation office. "
            f"A compassionate doctor and patient share an authentic, reassuring moment with genuine facial expressions. "
            f"Captured at eye level with a 50mm lens at f/2.0, providing realistic shallow depth of field that gently blurs the clean hospital background. "
            f"The lighting is soft, diffused daylight creating gentle contours with no harsh glares or artificial smoothing. "
            f"Ample negative copy space on the right side suitable for healthcare brochures and digital banners. Clean, trustworthy commercial aesthetic."
        )
        video_motion = (
            f"Cinematic 4K slow-motion b-roll of a healthcare professional reassuring a patient during {clean_kw}. "
            f"Smooth motorized slider tracking shot, gentle rack focus from stethoscope to warm reassuring smile, "
            f"natural clinical daylight, stabilized camera movement, ProRes 422, clean authentic medical footage"
        )

    elif genre == "culinary":
        scene = (
            f"Editorial gourmet food photography of {clean_kw}, freshly prepared and styled on a handcrafted dark matte ceramic plate. "
            f"Delicate fresh microgreen garnish, visible steaming vapor or crisp micro-droplets, resting on a textured natural linen runner and rustic weathered oak table."
        )
        camera = "Shot on Canon EOS R5 with 100mm f/2.8L Macro lens at f/3.2, 45-degree angle, razor-sharp focus on primary culinary texture with velvety bokeh falloff"
        lighting = "Soft directional daylight pouring in from a large window at 10 o'clock, subtle black foil negative fill to enhance mouth-watering contrast and appetizing specular highlights"
        negative_space = "Spacious tabletop negative copy space on the upper half, perfectly formatted for restaurant menu design, gourmet packaging, and food magazine covers"
        color_palette = "Rich appetizing organic palette: deep ceramic charcoal, warm golden crusts, vivid botanical greens, and warm natural timber tones"
        benchmark = "Bon Appétit & Cereal Magazine Gourmet Editorial"
        ref_preset = CURATED_STYLE_REFERENCES[4]

        flux_desc = (
            f"A gourmet commercial stock photograph of {clean_kw} served in an upscale artisanal restaurant. "
            f"The dish is presented on a textured artisanal ceramic plate with fresh botanical herbs and subtle glistening olive oil droplets. "
            f"Captured at a 45-degree angle using a 100mm macro lens at f/3.2, providing crisp detail on the central food textures while softly blurring the rustic wooden tabletop. "
            f"Side-window natural daylight creates beautiful dimensional highlights and deep rich shadows. "
            f"The upper third of the composition offers clean negative space for food branding and culinary typography. Appetizing, authentic restaurant quality."
        )
        video_motion = (
            f"High-speed 120fps slow-motion 4K stock video b-roll of {clean_kw} with delicate steam rising or sauce drizzling smoothly. "
            f"Macro slider push-in, shallow depth of field, warm natural side lighting, stabilized gimbal, ProRes 422, irresistible commercial food footage"
        )

    elif genre == "product":
        scene = (
            f"Minimalist luxury commercial product stage and mockup of {clean_kw}, displayed on a geometric honed travertine stone pedestal. "
            f"Delicate organic shadow silhouettes cast by an olive branch in the foreground, clean architectural studio background with subtle matte plaster texture."
        )
        camera = "Shot on Hasselblad X2D 100C with 90mm f/2.5 lens at f/4.0, eye-level commercial hero perspective, tack-sharp geometric edges and pristine surface fidelity"
        lighting = "Crisp low-angle afternoon sunlight casting elegant soft-edged architectural shadows, gentle white reflector bounce softening pedestal underside"
        negative_space = "Expansive clean negative copy space across the upper two-thirds, ideal for luxury e-commerce product banners, cosmetics advertising, and typography"
        color_palette = "Warm travertine limestone beige, muted cream, warm alabaster, and organic olive green shadow tones with high-key elegance"
        benchmark = "Architectural Digest & Aesop Luxury Product Still Life"
        ref_preset = CURATED_STYLE_REFERENCES[2]

        flux_desc = (
            f"A luxury commercial product photography mockup featuring {clean_kw} positioned on a clean honed travertine stone podium. "
            f"An organic botanical branch casts soft, natural sunlight shadows across the background plaster wall. "
            f"Captured with a 90mm medium-format prime lens at f/4, ensuring tack-sharp clarity on the product and pedestal while maintaining realistic perspective. "
            f"Warm low-angle afternoon sunlight provides rich dimensionality and soft contact shadows. "
            f"The upper two-thirds of the image provides abundant negative space designed for product branding and advertising copy. Sophisticated commercial finish."
        )
        video_motion = (
            f"Cinematic 4K slow-motion product b-roll of {clean_kw} resting on a travertine pedestal. "
            f"Smooth motorized turntable 360-degree slow rotation, shifting afternoon sunlight shadows, luxury studio lighting, ProRes 422, seamless product showcase"
        )

    elif genre == "abstract_3d":
        scene = (
            f"Abstract 3D parametric sculptural wave and fluid ribbon geometry representing {clean_kw}. "
            f"Dynamic flowing curves with pearlescent iridescent dispersion, frosted glassmorphism translucency, and internal refractive caustics. "
            f"Rendered in Cinema 4D and Octane Render with hyper-detailed subsurface light scattering and smooth gloss."
        )
        camera = "Virtual 85mm prime camera, cinematic macro hero angle, shallow depth of field focused on curving ribbon crest with soft atmospheric depth falloff"
        lighting = "Three-point volumetric studio lighting, subtle neon rim glow defining the ribbon contours, soft internal bioluminescence transmission"
        negative_space = "Generous negative copy space on the center-left, tailored for tech company keynote slides, app splash screens, and website hero headers"
        color_palette = "Holographic pearlescent gradient: iridescent lavender, electric cyan, champagne gold, and deep violet against a clean neutral studio backdrop"
        benchmark = "Apple Keynote Graphics & Behance 3D Octane Masterpiece"
        ref_preset = CURATED_STYLE_REFERENCES[3]

        flux_desc = (
            f"An abstract 3D digital art composition representing {clean_kw} with dynamic flowing liquid ribbons and translucent frosted glass waves. "
            f"The undulating ribbons feature iridescent pearlescent color dispersion with realistic internal refractive caustics and glossy specular highlights. "
            f"Rendered with realistic optical depth of field, bringing the central wave crest into sharp focus while the outer curves blur softly. "
            f"Volumetric studio illumination highlights the smooth curves and transparent glass layers. "
            f"Expansive negative space on the left side suitable for website hero copy and presentation titles. Modern tech aesthetic."
        )
        video_motion = (
            f"Seamless 4K 60fps infinite loop of abstract 3D iridescent liquid ribbons undulating gently for {clean_kw}. "
            f"Translucent frosted glass refraction, soft ambient caustics, smooth camera dolly motion, ProRes 422, flawless looping background for tech websites"
        )

    elif genre == "nature_eco":
        scene = (
            f"Inspiring panoramic commercial stock landscape of {clean_kw}, highlighting clean environmental harmony and sustainability. "
            f"Lush green undulating meadows, pristine horizon under atmospheric morning mist, renewable clean tech infrastructure integrated harmoniously with nature."
        )
        camera = "Shot on Sony A1 with 24-70mm f/2.8 GM II at 35mm f/8, hyperfocal sharpness from textured foreground flora to distant mountain ridge"
        lighting = "Breathtaking golden hour sunrise lighting, low-angle warm sun rays piercing through morning mist, wide dynamic range with preserved cloud highlights"
        negative_space = "Expansive open sky negative copy space across the upper half, ideal for environmental campaign slogans, ESG annual reports, and website banners"
        color_palette = "Vivid natural emerald greens, clean atmospheric sky blues, and warm golden sunrise amber with authentic natural dynamic range"
        benchmark = "National Geographic Environmental & Patagonia Outdoor Commercial"
        ref_preset = CURATED_STYLE_REFERENCES[1]

        flux_desc = (
            f"A breathtaking commercial landscape photograph of {clean_kw} at early morning sunrise. "
            f"Crisp natural details across the foreground vegetation and misty undulating green landscape leading to a clear mountain horizon. "
            f"Shot with a wide 35mm lens at f/8 for tack-sharp depth from foreground to background. "
            f"Warm golden hour sunlight filters through light morning fog, casting long soft shadows with beautiful atmospheric depth. "
            f"The upper half features clear open sky offering ample negative space for environmental copy and corporate sustainability reports. Authentic outdoor photo."
        )
        video_motion = (
            f"Cinematic 4K 60fps aerial drone slow push forward over {clean_kw} during golden hour sunrise. "
            f"Smooth stabilized gimbal descent, morning mist rolling gently over green hills, ProRes 422, majestic environmental stock b-roll"
        )

    elif genre == "lifestyle_people":
        scene = (
            f"Authentic candid commercial lifestyle portrait of {clean_kw}. "
            f"Genuine spontaneous human emotion, natural laughter, unposed gesture, wearing modern high-texture casual clothing (stonewashed denim, knit cotton, linen). "
            f"Set in a warm sunlit contemporary living space or urban outdoor café, natural environmental context without staged artificiality."
        )
        camera = "Shot on Leica M11 with Summicron 35mm f/2 lens at f/2.5, intimate documentary framing, razor-sharp eye catchlights, genuine skin texture with visible pores"
        lighting = "Soft natural side window daylight with gentle warm ambient bounce, gentle organic shadow falloff, realistic contrast without digital glare"
        negative_space = "Balanced negative space on the flank, optimized for lifestyle brand advertising, magazine editorial spreads, and social media campaigns"
        color_palette = "Warm filmic editorial palette: muted terracotta, warm slate, creamy neutrals, and authentic human skin tones with zero plastic airbrushing"
        benchmark = "Kinfolk & Condé Nast Traveler Lifestyle Documentary"
        ref_preset = CURATED_STYLE_REFERENCES[1]

        flux_desc = (
            f"An authentic documentary-style commercial stock photo capturing {clean_kw} in a warm, natural environment. "
            f"The subjects display genuine unposed emotion with natural body language and authentic eye contact. "
            f"Captured with a 35mm prime lens at f/2.5, producing a warm environmental portrait with natural focus falloff. "
            f"Soft natural window light fills the scene with warm, flattering illumination and realistic skin textures. "
            f"The composition leaves clear negative space on the side for editorial text and commercial headlines. Authentic, relatable lifestyle imagery."
        )
        video_motion = (
            f"Cinematic 4K 60fps slow-motion stock clip of candid human interaction during {clean_kw}. "
            f"Handheld gimbal tracking shot, natural golden afternoon light, genuine smiles and authentic laughter, ProRes 422, heart-warming lifestyle b-roll"
        )

    else: # general_commercial
        scene = (
            f"Professional commercial stock photography of {clean_kw}, high-end commercial aesthetic. "
            f"Crisp focal subject isolation, authentic tactile surface textures, immaculate commercial styling, and refined environmental context."
        )
        camera = "Shot on Hasselblad H6D-100c with 85mm f/1.8 prime lens, tack-sharp focal plane with creamy commercial bokeh falloff"
        lighting = "Soft diffused 45-degree studio softbox lighting with gentle fill, natural contrast, zero harsh specular hotspots"
        negative_space = "Generous negative copy space across the upper third, designed specifically for commercial advertising typography and brand slogans"
        color_palette = "Refined, color-calibrated commercial stock palette with rich midtones and authentic surface details"
        benchmark = "Commercial Stock Photo & Advertising Editorial"
        ref_preset = CURATED_STYLE_REFERENCES[0]

        flux_desc = (
            f"A high-resolution commercial stock photograph of {clean_kw} in a clean, modern setting. "
            f"Detailed surface textures, authentic materials, and crisp optical focus captured with an 85mm prime lens at f/2.8. "
            f"Soft diffused commercial studio lighting provides clean tonal transitions with realistic contact shadows. "
            f"The upper third provides ample negative copy space for commercial typography. Crisp, award-winning stock quality."
        )
        video_motion = (
            f"Cinematic 4K 60fps slow-motion stock video b-roll of {clean_kw}. "
            f"Smooth motorized slider tracking shot, natural diffused studio lighting, stabilized movement, ProRes 422, clean commercial b-roll"
        )

    # Active Reference URL selection
    active_ref = custom_ref_url.strip() if isinstance(custom_ref_url, str) and custom_ref_url.strip() else ref_preset["sref_code"]

    # Midjourney v6.1 Command Assembly
    mj_base_prompt = (
        f"{scene} {camera}, {lighting}, {negative_space}, {color_palette} "
        f"--ar 16:9 --style raw --stylize 150 --v 6.1 --no {NEGATIVE_PROMPT_DEFAULT}"
    )

    mj_with_sref = (
        f"{scene} {camera}, {lighting}, {negative_space}, {color_palette} "
        f"--ar 16:9 --style raw --stylize 150 --v 6.1 --sref {active_ref} --sw 100 --sv 6 --no {NEGATIVE_PROMPT_DEFAULT}"
    )

    # ChatGPT / DALL-E 3 & GPT-4o Image Prompt Assembly
    chatgpt_prompt = (
        f"A commercial stock photograph representing '{clean_kw}'. "
        f"{scene.strip()} "
        f"Optics & camera: {camera.strip()}. "
        f"Lighting: {lighting.strip()}. "
        f"Framing: {negative_space.strip()}. "
        f"Color scheme: {color_palette.strip()}. "
        f"Critical stock instructions: Natural realistic lighting, authentic physical textures without plastic airbrushing, "
        f"zero artificial oversaturation, and absolutely no text, words, brand names, or watermarks anywhere in the image."
    )

    # Google Nano Banana (Gemini 2.5 / 3 Image) Prompt Assembly
    nano_banana_prompt = (
        f"[Subject]: Authentic commercial stock representation of '{clean_kw}', {scene.strip()}\n"
        f"[Atmosphere & Color Palette]: {color_palette.strip()}\n"
        f"[Lighting Architecture]: {lighting.strip()}\n"
        f"[Camera & Lens Optics]: {camera.strip()}\n"
        f"[Composition & Copy Space]: {negative_space.strip()}\n"
        f"[Aesthetic Benchmark]: {benchmark}\n"
        f"[Stock Compliance]: Professional commercial stock asset, zero anatomical distortions, clean edges, no text or logo overlay, high commercial buyer intent."
    )

    return {
        "genre": genre,
        "clean_kw": clean_kw,
        "scene": scene,
        "camera": camera,
        "lighting": lighting,
        "negative_space": negative_space,
        "color_palette": color_palette,
        "benchmark": benchmark,
        "ref_preset": ref_preset,
        "active_ref_url": active_ref,
        "midjourney_prompt": mj_base_prompt,
        "midjourney_with_ref": mj_with_sref,
        "flux_prompt": flux_desc,
        "chatgpt_prompt": chatgpt_prompt,
        "nano_banana_prompt": nano_banana_prompt,
        "video_prompt": video_motion,
        "negative_prompt": NEGATIVE_PROMPT_DEFAULT
    }

def generate_ai_prompts(keyword: str, style: str = "commercial_stock", reference_url: str = None) -> dict:
    """
    Generates high-converting commercial AI prompts and camera parameters
    for Midjourney v6.1, Flux.1 Pro, and 4K AI Video (Runway / Luma / Sora / Google Flow).
    Maintains full backward compatibility while providing deep, precise commercial specs.
    """
    clean_kw = keyword.strip()
    genre = detect_keyword_genre(clean_kw)
    comp = build_commercial_prompt_components(clean_kw, genre, reference_url)

    icon_3d_prompt = (
        f"Isolated 3D isometric asset of {clean_kw}, smooth claymorphism finish with subtle frosted glass accents, "
        f"vibrant modern pastel color palette, soft ambient occlusion contact shadows, centered composition, "
        f"isolated on 100% pure solid white background, rendered in Cinema 4D and Octane Render, 8k resolution, "
        f"minimalist UI/UX icon asset --ar 1:1 --no ground, shadows, floor, borders"
    )

    vector_concept = {
        "tool": "Adobe Illustrator",
        "format": "AI & EPS 10 + High-res Transparent PNG (300 DPI)",
        "color_mode": "RGB (Stock) / CMYK (Print)",
        "style_recommendation": "Flat design with subtle gradient accents, clean 2-3px outlines, organized grouped layers, outlined text.",
        "concept_idea": f"A comprehensive vector set featuring {clean_kw} with 12 distinct elements, cohesive color harmony, and isolated artboards."
    }

    photoshop_concept = {
        "tool": "Adobe Photoshop",
        "format": "Layered PSD with Smart Objects (3000x2000px, 300 DPI)",
        "features": "Realistic drop shadows on separate multiply layers, displacement map for fabric or texture warp, organized color-coded layer folders.",
        "concept_idea": f"A multi-angle realistic mockup template showcasing {clean_kw} with customizable background colors and lighting."
    }

    canva_concept = {
        "tool": "Canva",
        "format": "Shareable Canva Template Link + Printable PDF Guide with clickable access",
        "deliverables": "10-20 cohesive templates (Instagram carousels, stories, A4/US Letter worksheets, or cards) utilizing free Canva elements only.",
        "concept_idea": f"An all-in-one customizable Canva template kit for {clean_kw}, featuring modern typography and drag-and-drop image frames."
    }

    return {
        "keyword": clean_kw,
        "genre": genre,
        # Standard strings (Backward Compatibility)
        "ai_image_prompt": comp["midjourney_prompt"],
        "ai_3d_icon_prompt": icon_3d_prompt,
        "ai_video_prompt": comp["video_prompt"],
        "illustrator_spec": vector_concept,
        "photoshop_spec": photoshop_concept,
        "canva_spec": canva_concept,
        "prompt_breakdown": {
            "subject_and_scene": comp["scene"],
            "camera_and_optics": comp["camera"],
            "optics": comp["camera"],
            "lighting_setup": comp["lighting"],
            "lighting": comp["lighting"],
            "composition_and_framing": comp["negative_space"],
            "composition": comp["negative_space"],
            "color_palette": comp["color_palette"]
        },
        "reference_guide": {
            "aesthetic_benchmark": comp["benchmark"],
            "reference_mood": comp["ref_preset"]["description"],
            "sref_url": comp["active_ref_url"],
            "sref_command": f"--sref {comp['active_ref_url']} --sw 100 --sv 6",
            "curated_presets": CURATED_STYLE_REFERENCES
        },
        "models": {
            "midjourney": comp["midjourney_prompt"],
            "midjourney_with_ref": comp["midjourney_with_ref"],
            "flux": comp["flux_prompt"],
            "chatgpt": comp["chatgpt_prompt"],
            "nano_banana": comp["nano_banana_prompt"],
            "video_4k": comp["video_prompt"]
        },
        "negative_prompt": comp["negative_prompt"]
    }

def generate_daily_quota_batch(seed_topic: str = "future technology", total_count: int = 20, reference_url: str = None) -> list:
    """
    Generates a full day's quota of 15-20 distinct, production-ready AI prompts
    (split across Images and 4K Videos) with ready titles, tags, visual references, and parameters.
    """
    clean_topic = seed_topic.strip()
    deadline = get_keyword_deadline(clean_topic)
    prompts = []

    # 10 Variations for Commercial Stock Photos / Backgrounds with precise specs & references
    image_variations = [
        {
            "subtheme": "Minimalist Studio Flatlay & Negative Space",
            "aspect": "--ar 16:9",
            "camera": "Top-down overhead flatlay, Hasselblad 50mm f/4, soft diffused natural northern daylight, clean matte surface with generous negative copy space",
            "title_prefix": "Overhead Flatlay View of",
            "format": "Commercial Stock Photo",
            "benchmark": "Kinfolk & Cereal Magazine Still Life",
            "ref_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f",
            "scene_desc": f"Top-down commercial flatlay arrangement of {clean_topic}, styled with clean negative copy space on the left, organic matte linen textures, and subtle soft contact shadows."
        },
        {
            "subtheme": "Futuristic Glassmorphism & Abstract 3D",
            "aspect": "--ar 16:9",
            "camera": "Macro shot virtual 85mm prime, iridescent liquid glass refraction, ambient neon edge glow, volumetric lighting, rendered in Cinema 4D Octane",
            "title_prefix": "Abstract 3D Glassmorphism Concept of",
            "format": "3D Render Background",
            "benchmark": "Apple Keynote Graphics & Behance 3D Art",
            "ref_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe",
            "scene_desc": f"Translucent frosted glass panels and pearlescent fluid waves representing {clean_topic}, internal caustic refraction, volumetric studio specular lighting."
        },
        {
            "subtheme": "Diverse Modern Professional Lifestyle",
            "aspect": "--ar 16:9",
            "camera": "Eye-level candid portrait, 85mm f/1.4 shallow depth of field, warm sun flare, genuine smile, authentic corporate casual setting",
            "title_prefix": "Authentic Business Professional Engaged in",
            "format": "Lifestyle Stock Photo",
            "benchmark": "Forbes & Monocle Modern Business",
            "ref_url": "https://images.unsplash.com/photo-1497366216548-37526070297c",
            "scene_desc": f"Confident diverse professional smiling naturally while engaged in {clean_topic} in a bright architectural corporate workspace, authentic skin pores, sharp fabric weaves."
        },
        {
            "subtheme": "Cinematic Editorial Portrait",
            "aspect": "--ar 4:5",
            "camera": "Dramatic chiaroscuro studio lighting, high contrast, Leica SL2, 50mm Summilux at f/1.8, sharp skin pores and authentic facial expression",
            "title_prefix": "Dramatic Editorial Portrait Featuring",
            "format": "Editorial Stock Portrait",
            "benchmark": "Vogue & Vanity Fair Editorial Lighting",
            "ref_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb",
            "scene_desc": f"A captivating, authentic editorial portrait related to {clean_topic}, expressive genuine human gaze, controlled rim lighting, textured styling, zero airbrushed sheen."
        },
        {
            "subtheme": "Isolated 3D Icon Asset for UI",
            "aspect": "--ar 1:1",
            "camera": "Isometric 45-degree angle, smooth claymorphism, pastel color accents, isolated on pure solid white background, zero ground shadows",
            "title_prefix": "Isolated 3D Clay Icon of",
            "format": "UI/UX 3D Graphic",
            "benchmark": "Stripe & Linear Modern App Iconography",
            "ref_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe",
            "scene_desc": f"A clean, isolated 3D claymorphic UI icon of {clean_topic}, smooth matte texture, soft ambient occlusion, isolated cleanly on pure white."
        },
        {
            "subtheme": "Atmospheric Landscape & Nature",
            "aspect": "--ar 16:9",
            "camera": "Wide angle 24mm f/8, golden hour sunrise mist, long exposure atmospheric haze, national geographic award-winning composition",
            "title_prefix": "Scenic Atmospheric Sunrise Landscape of",
            "format": "Nature Landscape Visual",
            "benchmark": "National Geographic Outdoor Editorial",
            "ref_url": "https://images.unsplash.com/photo-1509391365360-2e959784a276",
            "scene_desc": f"Panoramic wide-angle commercial landscape of {clean_topic} at early sunrise, golden light breaking through low-lying valley fog, deep organic color harmony."
        },
        {
            "subtheme": "Cyberpunk Neon Tech Cityscape",
            "aspect": "--ar 16:9",
            "camera": "Night aerial drone perspective, wet asphalt reflection, vibrant magenta and cyan neon lighting, hyper-detailed futuristic city",
            "title_prefix": "Futuristic Cyberpunk Smart City Concept with",
            "format": "Sci-Fi Concept Art",
            "benchmark": "Wired & Blade Runner Atmospheric Sci-Fi",
            "ref_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5",
            "scene_desc": f"Futuristic high-tech urban environment featuring {clean_topic}, holographic billboards, wet reflective streets, glowing cyan and violet lighting."
        },
        {
            "subtheme": "Clean Sustainable Eco-Tech",
            "aspect": "--ar 16:9",
            "camera": "Bright sunlit laboratory with green plants, solar panel reflections, clean minimalist white interior, renewable energy aesthetics",
            "title_prefix": "Sustainable Green Energy and Environmental Concept of",
            "format": "Eco Technology Visual",
            "benchmark": "Patagonia & Tesla Clean Energy Campaign",
            "ref_url": "https://images.unsplash.com/photo-1509391365360-2e959784a276",
            "scene_desc": f"Modern sustainable technology lab developing {clean_topic}, clean white architectural lines, flourishing indoor botanical plants, sunlit solar reflections."
        },
        {
            "subtheme": "Luxury Packaging & Product Stage",
            "aspect": "--ar 4:5",
            "camera": "Honed travertine marble podium, soft afternoon window shadow casting, luxury cosmetic packaging aesthetic, hyper-minimalist elegance",
            "title_prefix": "Luxury Minimalist Product Display Stage for",
            "format": "E-Commerce Mockup Background",
            "benchmark": "Architectural Digest & Aesop Luxury Product",
            "ref_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9",
            "scene_desc": f"Geometric travertine stone pedestal showcasing {clean_topic}, organic branch shadow patterns, generous top copy space for luxury advertising branding."
        },
        {
            "subtheme": "Cozy Autumn / Seasonal Warmth",
            "aspect": "--ar 16:9",
            "camera": "Warm vintage tone, steaming ceramic mug, knit wool texture, soft bokeh background, nostalgic comforting atmosphere",
            "title_prefix": "Cozy Warm Aesthetic Flatlay Featuring",
            "format": "Seasonal Lifestyle Photo",
            "benchmark": "Kinfolk Nordic Warmth Lifestyle",
            "ref_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4",
            "scene_desc": f"Warm seasonal cozy still life incorporating {clean_topic}, chunky knit blanket, steaming hot beverage, gentle golden window lighting."
        }
    ]

    # 10 Variations for 4K Stock Video B-Roll Loops
    video_variations = [
        {
            "movement": "Slow Cinematic Aerial Drone Descent",
            "lighting": "Golden hour twilight, smooth motorized gimbal 60fps tilt down, seamless looping motion, 4k ProRes",
            "title_prefix": "Cinematic Aerial Drone 4K Loop Over",
            "duration": "10-15s Loop"
        },
        {
            "movement": "Smooth Slider Dolly-In Shot",
            "lighting": "Modern sunlit corporate office, shallow depth of field, slow forward dolly movement on motorized track",
            "title_prefix": "Smooth Dolly Camera Push Towards",
            "duration": "8-12s Clip"
        },
        {
            "movement": "Abstract Digital Data Particles Flow",
            "lighting": "Glowing blue and golden particle vortex, floating in dark space, seamless infinite loop, 60fps high bitrate",
            "title_prefix": "Seamless Abstract Data Particle Flow Loop for",
            "duration": "Seamless Loop"
        },
        {
            "movement": "Slow Motion Macro Liquid Pour",
            "lighting": "120fps high-speed capture, crystal clear water drops or espresso pouring with beautiful meniscus surface tension",
            "title_prefix": "High Speed Slow Motion Macro Video of",
            "duration": "5-8s Slow-Mo"
        },
        {
            "movement": "Urban City Traffic Night Timelapse",
            "lighting": "Long exposure vehicle light trails streaming along elevated highway, sharp skyscrapers backdrop",
            "title_prefix": "Night Traffic Light Trails Urban Timelapse in",
            "duration": "10s Timelapse"
        },
        {
            "movement": "Rotating 3D Hologram Loop",
            "lighting": "360-degree smooth constant turntable rotation, luminous holographic wireframe interface in dark studio",
            "title_prefix": "Rotating 3D Holographic Visual Loop of",
            "duration": "Seamless 360 Loop"
        },
        {
            "movement": "Peaceful Nature Wind & Leaves Rustling",
            "lighting": "Sunlight filtering through forest canopy (Komorebi), gentle breeze rustling emerald leaves in slow motion",
            "title_prefix": "Sunlight Filtering Through Trees Wind Motion in",
            "duration": "15s Nature Clip"
        },
        {
            "movement": "Hands Typing on Laptop in Modern Cafe",
            "lighting": "Soft natural side window light, rack focus from coffee mug to hands smoothly typing on sleek aluminum keyboard",
            "title_prefix": "Rack Focus Close Up of Hands Working on",
            "duration": "8s B-Roll"
        },
        {
            "movement": "Cyber Matrix Binary Stream Falling",
            "lighting": "Emerald and cyan digital data raining down code stream, dark matrix background, smooth 60fps seamless loop",
            "title_prefix": "Cybersecurity Binary Code Data Stream Loop for",
            "duration": "Seamless Loop"
        },
        {
            "movement": "Gentle Snow Falling in Winter Forest",
            "lighting": "Slow fluttering snowflakes falling against dark evergreen pine trees, calm winter tranquility 4K 60fps",
            "title_prefix": "Realistic Snow Falling in Slow Motion 4K B-Roll of",
            "duration": "Seamless Winter Loop"
        }
    ]

    # Build 10 Image Prompts
    for i, v in enumerate(image_variations):
        title = f"{v['title_prefix']} {clean_topic.title()} - {v['format']}"
        active_ref = reference_url if reference_url else v['ref_url']
        
        mj_prompt = (
            f"Commercial stock photography of {clean_topic}, {v['subtheme'].lower()}, {v['camera']}, "
            f"8k resolution, crisp focal clarity, color graded, zero text, award-winning editorial quality {v['aspect']} --style raw --v 6.1 --no {NEGATIVE_PROMPT_DEFAULT}"
        )
        
        mj_with_ref = (
            f"Commercial stock photography of {clean_topic}, {v['subtheme'].lower()}, {v['camera']}, "
            f"8k resolution, crisp focal clarity, color graded, zero text, award-winning editorial quality {v['aspect']} --style raw --v 6.1 --sref {active_ref} --sw 100 --sv 6 --no {NEGATIVE_PROMPT_DEFAULT}"
        )

        flux_prompt = (
            f"A high-resolution commercial stock photograph depicting {v['scene_desc']} "
            f"{v['camera']}. The lighting is authentic with natural shadow falloff and realistic textures. "
            f"Clean composition leaving generous negative space for advertising typography. Commercial color grading."
        )

        chatgpt_prompt = (
            f"A commercial stock photograph representing '{clean_topic}', styled with {v['subtheme'].lower()}. "
            f"{v['scene_desc']} "
            f"Camera perspective: {v['camera']}. "
            f"Lighting: Natural, professional studio illumination with authentic contact shadows. "
            f"Composition: Designated negative copy space for commercial typography. "
            f"Important rules: Natural physical textures without plastic airbrushing, zero oversaturation, and absolutely no text or watermarks."
        )

        nano_banana_prompt = (
            f"[Subject]: Commercial stock visual of '{clean_topic}', {v['scene_desc']}\n"
            f"[Style & Atmosphere]: {v['subtheme']}, aesthetic benchmark {v['benchmark']}\n"
            f"[Optics & Lighting]: {v['camera']}\n"
            f"[Composition]: Clean composition with negative copy space for commercial licensing\n"
            f"[Commercial Standards]: Clean high-resolution stock asset, zero AI artifacts, no text or borders."
        )

        tags = [
            clean_topic.lower(), v['format'].lower(), "stock photo", "commercial", "isolated",
            "background", "modern", "high resolution", "concept", "editorial"
        ]
        prompts.append({
            "slot": f"Image Quota #{i+1}",
            "type": "AI Image",
            "title": title,
            "prompt": mj_prompt,
            "prompt_with_ref": mj_with_ref,
            "flux_prompt": flux_prompt,
            "chatgpt_prompt": chatgpt_prompt,
            "nano_banana_prompt": nano_banana_prompt,
            "target_platform": "Adobe Stock & Etsy",
            "aspect_ratio": v['aspect'],
            "tags": ", ".join(tags),
            "reference_guide": {
                "aesthetic_benchmark": v['benchmark'],
                "sref_syntax": f"--sref {active_ref} --sw 100",
                "ref_url": active_ref
            },
            "negative_prompt": NEGATIVE_PROMPT_DEFAULT,
            "lighting": v['camera'],
            "composition": v['subtheme'],
            "upload_deadline": deadline["upload_deadline"],
            "upload_deadline_short": deadline["upload_deadline_short"],
            "upload_date_range": deadline["upload_date_range"],
            "is_late": deadline["is_late"],
            "days_past_deadline": deadline["days_past_deadline"],
            "days_remaining": deadline["days_remaining"],
            "timing_status": deadline["timing_status"],
            "timing_badge": deadline["timing_badge"],
            "urgency_badge_color": deadline["urgency_badge_color"]
        })

    # Build 10 Video Prompts
    for j, v in enumerate(video_variations):
        title = f"{v['title_prefix']} {clean_topic.title()} 4K Stock Footage"
        prompt = (
            f"Cinematic 4K stock video footage of {clean_topic}, {v['movement'].lower()}, {v['lighting']}, "
            f"natural motion, stabilized camera tracking, professional color grading, ProRes 422, 60fps, zero artifacts, no warping"
        )
        tags = [
            clean_topic.lower(), "4k video", "stock footage", "b-roll", "cinematic",
            "slow motion", "loop", "commercial video", "prores", "background"
        ]
        prompts.append({
            "slot": f"Video Quota #{j+1}",
            "type": "AI Video",
            "title": title,
            "prompt": prompt,
            "target_platform": "Adobe Stock Video",
            "aspect_ratio": "16:9 4K UHD",
            "tags": ", ".join(tags),
            "reference_guide": {
                "aesthetic_benchmark": "Cinematic 4K ProRes Stock Footage",
                "movement": v['movement'],
                "lighting": v['lighting']
            },
            "duration": v['duration'],
            "upload_deadline": deadline["upload_deadline"],
            "upload_deadline_short": deadline["upload_deadline_short"],
            "upload_date_range": deadline["upload_date_range"],
            "is_late": deadline["is_late"],
            "days_past_deadline": deadline["days_past_deadline"],
            "days_remaining": deadline["days_remaining"],
            "timing_status": deadline["timing_status"],
            "timing_badge": deadline["timing_badge"],
            "urgency_badge_color": deadline["urgency_badge_color"]
        })

    return prompts[:total_count]

PLATFORM_PREFLIGHT_CHECKLISTS = {
    "adobe_stock": [
        "Check 'Created using generative AI tools' box during upload if AI-generated.",
        "Ensure image is upscaled to 4 Megapixels minimum (standard 4000x3000px, up to 100MP).",
        "Zero trademarked brand names, logos, or recognizable celebrity likenesses.",
        "Verify 100% zoom: no deformed hands, uncanny pupils, or jpeg noise artifacts.",
        "Ensure first 10 tags contain your highest-intent commercial search phrases."
    ],
    "shutterstock": [
        "EPS 10 vector format: clean paths, zero rasterized embedded pixels or clipping masks.",
        "Strict Third-Party AI rule: Do NOT upload Midjourney/Flux images as commercial photos.",
        "All 50 tag slots used with relevant synonyms (singular, plural, descriptive).",
        "Model release attached for any recognizable human face or private property.",
        "Title is descriptive and factual without spammy keyword stuffing."
    ],
    "etsy": [
        "All 13 tags filled with multi-word long-tail search terms (under 20 chars per tag).",
        "Digital wall art provided in 5 standard aspect ratio folders (2:3, 3:4, 4:5, ISO, 11:14).",
        "High resolution 300 DPI minimum for all printables and transparent PNG clipart.",
        "Canva template provided via shareable template link inside a clickable PDF guide.",
        "Listing title uses high-intent buyer keywords separated with clear pipes (|) or dashes."
    ],
    "iconscout": [
        "3D icons exported on 100% transparent PNG with clean alpha cutouts (no halo fringe).",
        "Vector icons designed on strict 24px or 48px pixel-perfect grid with 2px stroke weight.",
        "Consistent perspective maintained (isometric, claymorphism, or glassmorphism).",
        "Organized bundle with SVG, high-res PNG, and source AI/C4D/Blender project files.",
        "No ground shadow or solid color background on isolated 3D icons."
    ],
    "graphicriver": [
        "Organized, color-coded Photoshop layers with Smart Objects for mockups and flyers.",
        "Print-ready CMYK color mode at 300 DPI with standard 0.125-inch bleed margins.",
        "All fonts used must be 100% free for commercial use with font links included in help.txt.",
        "Includes clean preview images (590x700px or higher) showcasing the product clearly.",
        "Packaged into a single clean ZIP archive with read-me instructions."
    ]
}

def generate_stock_tags(keyword: str, related_terms: list = None, platform: str = "adobe_stock") -> list:
    """
    Cleans, deduplicates, and generates algorithmic, platform-specialized tags
    strictly conforming to the marketplace's upload algorithm and character limits.
    """
    tags = []
    seen = set()

    def add_tag(t, max_len=None):
        cleaned = t.strip().lower()
        cleaned = "".join(c for c in cleaned if c.isalnum() or c in (" ", "-")).strip()
        if max_len and len(cleaned) > max_len:
            return
        if cleaned and len(cleaned) >= 2 and cleaned not in seen:
            seen.add(cleaned)
            tags.append(cleaned)

    clean_kw = keyword.strip().lower()
    words = clean_kw.split()

    if platform == "etsy":
        # Etsy: strictly 13 tags, multi-word phrases, max 20 chars per tag
        etsy_intent_modifiers = [
            "digital download", "canva template", "instant download", "printable art",
            "diy template", "commercial use", "svg cut file", "cricut craft", "planner printable",
            "branding kit", "small business", "wall decor", "sublimation png", "gift idea"
        ]
        # Primary multi-word term
        add_tag(clean_kw, max_len=20)
        # Combine with modifiers if under 20 chars
        for mod in etsy_intent_modifiers:
            combo = f"{clean_kw} {mod}"
            if len(combo) <= 20:
                add_tag(combo, max_len=20)
            if len(mod) <= 20:
                add_tag(mod, max_len=20)
        if related_terms:
            for rt in related_terms:
                if len(rt) <= 20:
                    add_tag(rt, max_len=20)
        return tags[:13]

    elif platform == "iconscout":
        # IconScout: 30 tags, UI/UX, 3D icon, glyph, vector focus
        add_tag(clean_kw)
        for w in words:
            add_tag(w)
        icon_modifiers = [
            "3d icon", "ui icon", "ux design", "app icon", "isolated", "transparent background",
            "claymorphism", "glassmorphism", "octane render", "web asset", "vector icon",
            "glyph", "isometric", "symbol", "sign", "minimalist", "clean render", "interface graphic",
            "mobile app", "dashboard element", "digital asset", "modern icon", "illustration"
        ]
        for im in icon_modifiers:
            add_tag(f"{clean_kw} {im}")
            add_tag(im)
        if related_terms:
            for rt in related_terms:
                add_tag(rt)
        return tags[:30]

    elif platform == "graphicriver":
        # GraphicRiver: 30 tags, PSD template, print-ready, mockup, flyer focus
        add_tag(clean_kw)
        for w in words:
            add_tag(w)
        gr_modifiers = [
            "psd template", "print ready", "flyer design", "mockup kit", "smart object",
            "cmyk 300 dpi", "corporate branding", "event poster", "stationery pack",
            "editable layers", "business template", "marketing flyer", "brochure layout",
            "graphic template", "photoshop psd", "vector eps", "clean layout", "modern design"
        ]
        for gm in gr_modifiers:
            add_tag(f"{clean_kw} {gm}")
            add_tag(gm)
        if related_terms:
            for rt in related_terms:
                add_tag(rt)
        return tags[:30]

    elif platform == "shutterstock":
        # Shutterstock: exactly 50 tags, synonym expansion
        add_tag(clean_kw)
        for w in words:
            add_tag(w)
        shutter_boosters = [
            "commercial stock", "isolated", "background", "modern", "concept", "illustration",
            "vector element", "high quality", "professional", "graphic design", "digital",
            "white background", "overhead view", "lifestyle", "business", "technology",
            "minimalist", "clean", "abstract", "creative", "textured", "studio shot",
            "symbol", "sign", "set", "collection", "bright", "contemporary", "composition"
        ]
        for b in shutter_boosters:
            add_tag(f"{clean_kw} {b}")
            add_tag(b)
        if related_terms:
            for rt in related_terms:
                add_tag(rt)
        return tags[:50]

    else:
        # Adobe Stock: 49 tags, first 10 carrying 80% algorithmic weight
        add_tag(clean_kw)
        for w in words:
            add_tag(w)
        if related_terms:
            for term in related_terms:
                add_tag(term)
        adobe_boosters = [
            "background", "modern", "high resolution", "concept", "commercial stock",
            "isolated", "creative", "generative ai", "design element", "illustration",
            "professional", "lifestyle", "technology", "abstract", "minimalist",
            "digital art", "studio lighting", "graphic", "texture", "contemporary"
        ]
        for b in adobe_boosters:
            add_tag(f"{clean_kw} {b}")
            add_tag(b)
        return tags[:49]

def generate_commercial_titles(keyword: str, platform: str = "all") -> dict:
    """
    Generates 4-5 high-converting, platform-tailored listing titles answering
    Who, What, Where, and Context for any commercial stock keyword.
    """
    clean = keyword.strip()
    title_kw = clean.title()

    titles_by_platform = {
        "adobe_stock": [
            f"{title_kw} Commercial Stock Asset with Modern Studio Lighting and Copy Space",
            f"Authentic {title_kw} in Contemporary Architectural Setting with Natural Daylight",
            f"Minimalist Abstract {title_kw} Background for Digital Marketing and Hero Header",
            f"Professional {title_kw} Concept for Business Pitch Deck and Technology Presentation",
            f"Close-Up High-Resolution View of {title_kw} with Crisp Optical Depth of Field"
        ],
        "shutterstock": [
            f"{title_kw} isolated on clean background, commercial stock photo illustration",
            f"Modern {clean.lower()} concept in bright contemporary environment with soft lighting",
            f"Creative high-resolution representation of {clean.lower()} for advertising and marketing",
            f"Professional overhead flatlay of {clean.lower()} with generous negative copy space",
            f"Detailed {clean.lower()} design element for corporate branding and digital publications"
        ],
        "etsy": [
            f"{title_kw} Canva Template | Editable {title_kw} Digital Download | Small Business Branding Kit",
            f"{title_kw} SVG Cut File for Cricut & Silhouette | Instant Download Commercial Use PNG Clipart",
            f"{title_kw} Printable Wall Art Poster | 5 Aspect Ratios (300 DPI) | Minimalist Digital Decor",
            f"Customizable {title_kw} Planner Bundle | A4 & US Letter Printable | Instant Digital Access",
            f"Modern {title_kw} Social Media Kit | 20 Instagram Carousel & Story Templates for Canva"
        ],
        "iconscout": [
            f"3D Isolated {title_kw} Icon - Cinema 4D Octane Render for Modern UI/UX",
            f"Minimalist {title_kw} Vector Glyph Icon on 24px Grid (SVG & PNG)",
            f"Modern Claymorphism 3D {title_kw} Asset on 100% Transparent Background",
            f"Isometric {title_kw} Tech Concept Illustration for Mobile App Dashboard",
            f"Clean Gradient {title_kw} UI Element for Web Design and App Navigation"
        ],
        "graphicriver": [
            f"{title_kw} Corporate Business Flyer Template PSD - Print Ready 300 DPI CMYK",
            f"Modern {title_kw} Branding Mockup Kit - Smart Object Layered Photoshop PSD",
            f"Minimalist {title_kw} Event Poster & Social Media Pack - Fully Editable Layers",
            f"Creative {title_kw} Presentation Slides & Stationery Template - Illustrator AI & EPS",
            f"Professional {title_kw} Trifold Brochure Template - Clean Typography & Print Margins"
        ]
    }

    if platform in titles_by_platform:
        return {platform: titles_by_platform[platform]}
    return titles_by_platform

def generate_cross_marketplace_kit(keyword: str, reference_url: str = None) -> dict:
    """
    Generates a full cross-marketplace production kit for any keyword or niche,
    containing ready titles, tags, pre-flight checklists, and production specs for all 5 platforms.
    """
    clean = keyword.strip()
    titles = generate_commercial_titles(clean)

    platforms = {
        "adobe_stock": {
            "id": "adobe_stock",
            "name": "Adobe Stock",
            "badge": "100% AI Accepted",
            "tag_limit": 49,
            "tags": generate_stock_tags(clean, platform="adobe_stock"),
            "titles": titles["adobe_stock"],
            "preflight_checklist": PLATFORM_PREFLIGHT_CHECKLISTS["adobe_stock"],
            "recommended_format": "JPEG / 4K MOV (ProRes 422)",
            "primary_focus": "Commercial Stock Photos, 3D Backgrounds, 4K Video B-Roll"
        },
        "shutterstock": {
            "id": "shutterstock",
            "name": "Shutterstock",
            "badge": "Strict Vectors & Real Media",
            "tag_limit": 50,
            "tags": generate_stock_tags(clean, platform="shutterstock"),
            "titles": titles["shutterstock"],
            "preflight_checklist": PLATFORM_PREFLIGHT_CHECKLISTS["shutterstock"],
            "recommended_format": "EPS 10 Vector / Camera JPEG / 4K MOV",
            "primary_focus": "Clean Scalable Vectors, Authentic Real Photos, B-Roll Video"
        },
        "etsy": {
            "id": "etsy",
            "name": "Etsy Digital",
            "badge": "Huge Buyer Intent",
            "tag_limit": 13,
            "tags": generate_stock_tags(clean, platform="etsy"),
            "titles": titles["etsy"],
            "preflight_checklist": PLATFORM_PREFLIGHT_CHECKLISTS["etsy"],
            "recommended_format": "Canva Link PDF / SVG Cut File / 300 DPI ZIP (5 Ratios)",
            "primary_focus": "Canva Templates, Cricut SVG Bundles, Printable Wall Art"
        },
        "iconscout": {
            "id": "iconscout",
            "name": "IconScout",
            "badge": "3D & UI Icons",
            "tag_limit": 30,
            "tags": generate_stock_tags(clean, platform="iconscout"),
            "titles": titles["iconscout"],
            "preflight_checklist": PLATFORM_PREFLIGHT_CHECKLISTS["iconscout"],
            "recommended_format": "Transparent PNG (Alpha) / SVG / GLTF 3D / Lottie JSON",
            "primary_focus": "Isolated 3D Renders, Claymorphism Icons, 24px Grid SVGs"
        },
        "graphicriver": {
            "id": "graphicriver",
            "name": "GraphicRiver",
            "badge": "PSD Design Templates",
            "tag_limit": 30,
            "tags": generate_stock_tags(clean, platform="graphicriver"),
            "titles": titles["graphicriver"],
            "preflight_checklist": PLATFORM_PREFLIGHT_CHECKLISTS["graphicriver"],
            "recommended_format": "Layered PSD (Smart Objects, 300 DPI CMYK) + AI / EPS",
            "primary_focus": "Print Flyers, Stationery Packs, Product Mockup Templates"
        }
    }

    # Add tags string convenience and score breakdowns
    try:
        from crawler.score_engine import calculate_title_score, calculate_tag_score
        for p_key, p_data in platforms.items():
            p_data["tags_string"] = ", ".join(p_data["tags"])
            p_data["primary_title"] = p_data["titles"][0] if p_data["titles"] else clean.title()
            p_data["scored_titles"] = [calculate_title_score(t, base_kw=clean, platform=p_key) for t in p_data["titles"]]
            p_data["scored_tags"] = [calculate_tag_score(tg, base_kw=clean, platform=p_key) for tg in p_data["tags"]]
    except Exception:
        for p_key, p_data in platforms.items():
            p_data["tags_string"] = ", ".join(p_data["tags"])
            p_data["primary_title"] = p_data["titles"][0] if p_data["titles"] else clean.title()

    deadline_info = get_keyword_deadline(clean)

    return {
        "keyword": clean,
        "deadline_info": deadline_info,
        "platforms": platforms,
        "marketplaces": platforms
    }
