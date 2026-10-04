"""
Marketplace Intelligence & Specifications Data
Detailed guidelines, technical standards, tag limits, separated vector/image/video requirements,
AI acceptance policies, and curated high-demand niches with titles for Adobe Stock, Shutterstock,
Etsy, IconScout, and GraphicRiver.
"""

PLATFORMS_INFO = {
    "adobe_stock": {
        "id": "adobe_stock",
        "name": "Adobe Stock",
        "color": "from-red-600 to-rose-700",
        "accent": "#ff0000",
        "badge": "Adobe Stock Contributor",
        "tag_limit": 49,
        "primary_focus": ["Generative AI Visuals", "Vector Art (AI/EPS)", "4K Stock Video", "PSD Mockups & Templates"],
        "ai_acceptance": {
            "status": "100% Accepted & High Earner",
            "badge_color": "emerald",
            "accepts_images": True,
            "accepts_videos": True,
            "details": "Adobe Stock fully accepts Generative AI images and video clips. You MUST toggle the 'Created using generative AI tools' checkbox during submission. No trademarked brands or recognizable real people."
        },
        "requirements": {
            "vectors": {
                "format": "AI or EPS format (version 8 or 10 compatible for widest buyer reach).",
                "artboard": "Minimum 4 Megapixels (e.g. 2000x2000px up to 15MP+). RGB color mode.",
                "rules": "All text must be outlined/converted to curves. No embedded raster images or stray points. Organized layers."
            },
            "images": {
                "format": "JPEG format, sRGB color profile, uncompressed or high-quality (10-12).",
                "resolution": "Minimum 4 Megapixels (standard 4000x3000px or higher, up to 100MP).",
                "rules": "Zero digital noise, lens dust, chromatic aberration, or AI distortions (check hands/eyes/textures at 100% zoom). Generative AI toggle ON."
            },
            "videos": {
                "format": "MOV or MP4 container. ProRes 422 (HQ/Standard) or H.264 high bitrate (50-100+ Mbps).",
                "resolution": "4K UHD (3840x2160) preferred for maximum royalties, or Full HD (1920x1080).",
                "framerate": "23.98, 24, 25, 29.97, 30, 50, or 60 fps. Duration: 5 to 60 seconds.",
                "rules": "Zero audio track unless it is high-fidelity authentic ambient sound. Seamless looping b-roll sells fastest."
            }
        },
        "ranking_tips": [
            "The FIRST 10 TAGS carry ~80% of Adobe Stock search weighting. Put your primary keywords first!",
            "Never use spammy brand names or generic words like 'image', 'picture', or 'illustration'.",
            "Titles should be descriptive (5-10 words) answering Who, What, Where, and Context.",
            "AI-generated assets are performing exceptionally well in conceptual business, sci-fi backgrounds, and 3D textures."
        ],
        "what_to_create": [
            {
                "concept": "Abstract 3D Liquid Waves & Glassmorphism Backgrounds",
                "asset_type": "AI Image & 3D Render",
                "suggested_title": "Abstract 3D Iridescent Liquid Wave and Glassmorphism Technology Background",
                "suggested_titles": [
                    "Abstract 3D Iridescent Liquid Wave and Glassmorphism Technology Background",
                    "Futuristic 3D Flowing Liquid Wave Texture with Glassmorphism Frosted Overlay",
                    "Vibrant Iridescent Fluid Waves Background for Digital Marketing and Hero Header",
                    "Modern Abstract Curved 3D Wave Flowing Stream with Studio Specular Lighting"
                ],
                "why_it_sells": "Tech startups and marketing agencies use these continuously for landing pages, keynote slides, and product banners.",
                "ai_prompts": {
                    "midjourney": "Abstract 3D parametric fluid ribbons and undulating liquid waves, pearlescent iridescent chromatic dispersion, translucent frosted glassmorphism layers with internal refractive caustics. Virtual 85mm prime lens, macro hero angle, three-point volumetric studio lighting, clean negative copy space on center-left for keynote slides and web banners --ar 16:9 --style raw --stylize 150 --v 6.1 --sref https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe --sw 100 --sv 6 --no text, watermarks, noisy grain, lowres, borders",
                    "flux": "A modern commercial 3D abstract visual featuring translucent frosted glassmorphism panels and dynamic iridescent fluid ribbons flowing gracefully across the composition. Captured with realistic optical depth of field, sharp specular reflections on curved wave crests, and internal caustic light dispersion. Rendered in Cinema 4D and Octane with studio lighting against a clean neutral background. Generous negative space on the left suitable for typography overlay.",
                    "chatgpt": "Create a high-end commercial 3D abstract visual featuring translucent frosted glassmorphism panels and dynamic iridescent fluid ribbons flowing across the frame. Virtual 85mm prime lens perspective with sharp specular reflections on wave crests. Professional studio lighting with caustics against a neutral background. Generous clean negative space on the left suitable for typography overlay. No text, words, labels, or watermarks.",
                    "nano_banana": "[Subject]: Abstract 3D parametric fluid ribbons and undulating liquid waves with translucent frosted glassmorphism layers and internal refractive caustics.\n[Setting]: Clean virtual studio environment with soft neutral backdrop.\n[Lighting]: Three-point volumetric studio lighting with subtle rim glow.\n[Optics]: 85mm prime perspective, shallow depth of field.\n[Composition]: Negative copy space on the center-left for advertising headline overlay.\n[Commercial Requirements]: Pristine commercial stock asset, zero noise, high resolution, no text.",
                    "video": "Seamless 4K 60fps loop of abstract 3D iridescent liquid waves undulating smoothly in space. Translucent glass refraction, soft ambient caustics, smooth camera dolly motion, ProRes 422, flawless looping background for tech websites.",
                    "negative_prompt": "text, watermarks, logo, harsh noise, jpeg artifacts, blurry, borders, frame, low poly",
                    "reference_guide": {
                        "benchmark": "Apple Keynote Graphics & Behance 3D Octane Masterpiece",
                        "sref_syntax": "--sref https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe --sw 100",
                        "mood": "Iridescent pearlescent liquid waves with translucent frosted glass and soft caustic lighting."
                    }
                },
                "sample_tags": ["abstract 3d background", "iridescent fluid waves", "futuristic tech wallpaper", "generative ai backdrop", "glassmorphism texture", "liquid hologram", "cyberpunk neon gradient", "smooth glossy surface", "modern digital art", "creative presentation background"],
                "tag_titles": {
                    "abstract 3d background": [
                        "Abstract 3D Background with Flowing Liquid Waves and Vibrant Gradient Wallpaper",
                        "Modern Abstract 3D Geometric Background for Tech Website Banner and App Header",
                        "Futuristic Abstract 3D Curved Wave Backdrop with Soft Ambient Studio Lighting"
                    ],
                    "iridescent fluid waves": [
                        "Iridescent Fluid Waves Flowing in Dynamic Motion for Futuristic UI Presentation",
                        "Vibrant Iridescent Fluid Wave Pattern for Keynote Slide and Web Hero Backdrop",
                        "Holographic Liquid Waves with Pearlescent Luster and Flowing Organic Curves"
                    ],
                    "futuristic tech wallpaper": [
                        "Futuristic Tech Wallpaper with Glowing Glassmorphism Digital Curves and Soft Light",
                        "Sci-Fi Futuristic Tech Wallpaper for Cyberpunk Desktop and Mobile Interface",
                        "High Tech Futuristic Digital Grid and Luminous Wave Lines for IT Presentation"
                    ],
                    "generative ai backdrop": [
                        "Generative AI Backdrop for Modern Technology Keynote and Startup Banner Concept",
                        "Creative Generative AI Backdrop with Colorful Holographic Waves and Copy Space",
                        "Artificial Intelligence Generative AI Concept Art Background with Flowing Streams"
                    ],
                    "glassmorphism texture": [
                        "Glassmorphism Texture Layer with Translucent Frosted Glass Effect and Vivid Neon Glow",
                        "Translucent Glassmorphism Frosted Glass Panels Over Colorful Fluid Gradient",
                        "Modern Glassmorphism UI Card Texture with Glossy Blur and Subtle Shadows"
                    ],
                    "liquid hologram": [
                        "Liquid Hologram Iridescent Wave Pattern for Creative Product Packaging and Hero Banner",
                        "Futuristic Liquid Hologram Ribbon Waves Shimmering in Cyan and Magenta Light",
                        "Psychedelic Liquid Hologram Fluid Motion with Refracted Rainbow Caustics"
                    ],
                    "cyberpunk neon gradient": [
                        "Cyberpunk Neon Gradient Liquid Waves Glowing in Dark Cybernetic Space",
                        "Vibrant Cyberpunk Neon Violet and Electric Cyan Gradient for Gaming Wallpaper",
                        "Night City Cyberpunk Neon Aesthetic Wave Distortion for Music Album Artwork"
                    ],
                    "smooth glossy surface": [
                        "Smooth Glossy Surface with Elegant Curving Ribbon Waves and Reflected Specular Highlights",
                        "Lustrous Smooth Glossy 3D Fluid Stream with High End Studio Reflections",
                        "Minimalist Smooth Glossy Plastic Liquid Wave with Soft Pastel Colors"
                    ],
                    "modern digital art": [
                        "Modern Digital Art 3D Render of Colorful Fluid Streams for Creative Web Design",
                        "Contemporary Modern Digital Art Fluid Sculpture for Gallery Exhibition Poster",
                        "Abstract Modern Digital Art Wave Formations with Vivid Volumetric Lighting"
                    ],
                    "creative presentation background": [
                        "Creative Presentation Background with Minimalist Organic Wave Geometry and Copy Space",
                        "Professional Creative Presentation Slide Background for Business Pitch Deck",
                        "Elegant Creative Presentation Backdrop with Flowing Waves for Corporate Branding"
                    ]
                }
            },
            {
                "concept": "Clean Energy & Climate Sustainability Infographic Elements",
                "asset_type": "Illustrator Vector (AI/EPS 10)",
                "suggested_title": "Renewable Clean Energy Solar Panels and Wind Turbine Isometric Vector Infographic",
                "suggested_titles": [
                    "Renewable Clean Energy Solar Panels and Wind Turbine Isometric Vector Infographic",
                    "Green Sustainable Eco Technology Infographic Vector Elements and Climate Charts",
                    "Net Zero Carbon Neutral Energy Transition Vector Illustration Set for ESG Report"
                ],
                "why_it_sells": "Corporate ESG reports and educational publishers buy these year-round.",
                "ai_prompts": {
                    "vector": "Clean isometric vector set of renewable clean energy: modern wind turbines on green hills, rooftop solar panels, electric vehicle charging stations, and smart power grid lines. Clean bezier paths, expanded strokes, EPS 10 format, isolated on pure white.",
                    "midjourney": "Commercial stock photograph of a sustainable clean energy landscape at golden hour. Modern wind turbines and solar panel arrays blending harmoniously with lush green rolling hills, electric vehicle on a scenic road, warm atmospheric sunlight, ample negative space on upper sky --ar 16:9 --style raw --stylize 150 --v 6.1 --sref https://images.unsplash.com/photo-1466611653911-95081537e5b7 --sw 100 --sv 6 --no text, pollution, smog, blurry",
                    "flux": "A photorealistic commercial stock photograph of a renewable solar farm and wind turbine array in a pristine rural valley. Captured with an 85mm prime lens during late afternoon golden hour. Clean renewable energy theme, realistic lighting, and generous negative copy space in the upper sky.",
                    "chatgpt": "Commercial stock photography concept representing clean green energy and sustainability. Modern wind turbines and blue solar panels under a clear expansive sky with soft golden sunlight. Crisp natural details, designated negative copy space in the sky for corporate sustainability slogans. No text or watermarks.",
                    "nano_banana": "[Subject]: Clean green energy landscape with modern white wind turbines and reflective solar panels.\n[Setting]: Rolling emerald green hills under a bright clear sky.\n[Lighting]: Warm directional golden hour sunlight with soft natural shadows.\n[Optics]: 50mm landscape prime lens, sharp focal plane.\n[Composition]: Negative copy space across the upper third sky for corporate ESG typography.\n[Commercial Requirements]: Clean commercial stock grade, authentic environmental setting, no text.",
                    "video": "Cinematic 4K 60fps drone sweep across modern wind turbines rotating gracefully over green hills at sunset. ProRes 422, smooth stabilized aerial tracking.",
                    "negative_prompt": "text, watermarks, smog, industrial pollution, dark gloomy clouds, distorted blades, blurry",
                    "reference_guide": {
                        "benchmark": "National Geographic & Tesla Energy Sustainable Future",
                        "sref_syntax": "--sref https://images.unsplash.com/photo-1466611653911-95081537e5b7 --sw 100",
                        "mood": "Pristine golden-hour sunlight, green rolling hills, modern white wind turbines, eco optimism."
                    }
                },
                "sample_tags": ["green energy vector", "renewable power illustration", "solar panel graphic", "wind turbine isometric", "eco mobility concept", "sustainable technology", "carbon neutral badge", "environmental infographic", "clean energy flat design", "earth conservation art"],
                "tag_titles": {
                    "green energy vector": [
                        "Green Energy Vector Elements with Solar Panels Wind Turbines and Eco Friendly Cityscape",
                        "Flat Design Green Energy Vector Set for Environmental Presentation and Brochure",
                        "Clean Green Energy Vector Badges with Leaves Sun Rays and Electric Power Icons"
                    ],
                    "renewable power illustration": [
                        "Renewable Power Illustration Featuring Hydroelectric Dam and Clean Electric Power Grid",
                        "Isometric Renewable Power Illustration with Offshore Wind Farm and Solar Arrays",
                        "Vector Renewable Power Flow Chart Showing Clean Energy Distribution from Source to Home"
                    ],
                    "solar panel graphic": [
                        "Solar Panel Graphic on Modern Residential Rooftop with Smart Energy Meter Vector",
                        "Blue Photovoltaic Solar Panel Graphic with Sunbeams and Clean Electric Current",
                        "Solar Panel Farm Flat Graphic for Green Technology and Zero Emission Concept"
                    ],
                    "wind turbine isometric": [
                        "Wind Turbine Isometric Vector Illustration for Clean Energy and Environmental Presentation",
                        "Modern Wind Turbine Isometric Icon with Rotating Blades and Power Substation",
                        "Isometric Wind Turbine Energy Generation Facility on Green Meadow Vector"
                    ],
                    "eco mobility concept": [
                        "Eco Mobility Concept with Electric Vehicles and Clean Transportation City Infrastructure",
                        "Sustainable Eco Mobility Illustration Showing EV Charging Station and Electric Bicycles",
                        "Future Eco Mobility Vector Banner with Zero Emission Public Transit and Bike Lanes"
                    ],
                    "sustainable technology": [
                        "Sustainable Technology Infographic Set with Carbon Footprint Tracker and Eco Icons",
                        "Smart Sustainable Technology Diagram Illustrating Circular Economy and Recycling Loop",
                        "Green Sustainable Technology Roadmap Vector for Corporate ESG Annual Report"
                    ],
                    "carbon neutral badge": [
                        "Carbon Neutral Badge Vector Collection with Net Zero and Eco Certified Stamps",
                        "Green Carbon Neutral Badge Sticker Set for Eco Friendly Packaging and Labels",
                        "Certified Carbon Neutral Emblem with Globe Leaf and Zero Emissions Guarantee"
                    ],
                    "environmental infographic": [
                        "Environmental Infographic Layout for Corporate Sustainability and ESG Annual Report",
                        "Climate Change and Environmental Infographic Poster with Data Charts and Graphs",
                        "Global Environmental Infographic Template with Ecology Indicators and Statistics"
                    ],
                    "clean energy flat design": [
                        "Clean Energy Flat Design Icons of Sun Wind and Geothermal Renewable Resources",
                        "Modern Clean Energy Flat Design Banner for Ecology Campaign and Website Header",
                        "Clean Energy Flat Design Vector Asset Kit with Battery Storage and Smart Grid"
                    ],
                    "earth conservation art": [
                        "Earth Conservation Art Illustration of Green Planet with Recycling and Nature Elements",
                        "Save The Planet Earth Conservation Art Graphic for World Environment Day",
                        "Hands Holding Green Earth Conservation Vector Art Symbolizing Environmental Protection"
                    ]
                }
            },
            {
                "concept": "Cinematic Diverse Corporate Team Collaboration 4K Video",
                "asset_type": "4K Stock Video (AI Video / B-Roll)",
                "suggested_title": "Diverse Business Professionals Brainstorming in Modern Sunlit Office 4K Slow Motion",
                "suggested_titles": [
                    "Diverse Business Professionals Brainstorming in Modern Sunlit Office 4K Slow Motion",
                    "Multiracial Corporate Team Celebrating Project Success in High Rise Boardroom",
                    "Authentic Startup Coworkers Collaborating on Laptops Around Open Studio Desk 4K"
                ],
                "why_it_sells": "Corporate websites, HR recruitment videos, and SaaS promotional ads constantly license authentic teamwork clips.",
                "ai_prompts": {
                    "video": "Cinematic 4K 60fps slow-motion stock video b-roll of diverse business professionals in collaborative discussion around a sunlit natural oak conference desk. Smooth motorized slider dolly-in, soft rack focus from laptop charts to genuine smiles, natural morning daylight through floor-to-ceiling windows, warm ambient bounce, ProRes 422, zero flicker or warping.",
                    "midjourney": "Authentic commercial stock photograph of a collaborative team of diverse professionals in a sunlit architectural corporate boardroom. Two women and a man casually discussing growth metrics on a natural oak table, genuine unposed smiles, contemporary smart-casual attire. Shot on Sony A7R V with 50mm f/1.8 G Master at f/2.2, soft morning window light from the left, generous negative copy space on upper left --ar 16:9 --style raw --stylize 150 --v 6.1 --sref https://images.unsplash.com/photo-1497366216548-37526070297c --sw 100 --sv 6 --no text, corporate logo, extra fingers, deformed limbs, plastic skin, blurry",
                    "flux": "An authentic high-resolution commercial stock photograph of a diverse business team in a bright modern office. Three colleagues review charts together around a wooden desk with natural body language. Soft natural morning window light, realistic skin textures, 50mm prime lens depth of field, ample negative space for text overlay.",
                    "chatgpt": "A photorealistic commercial stock photograph of a diverse corporate team collaborating naturally around a conference table in a modern sunlit glass office. One person points to a laptop while colleagues smile attentively. Shot on a 50mm lens at f/2.2 with soft directional morning daylight streaming from floor-to-ceiling windows. Clear negative space across the upper wall for corporate copy. Authentic expressions, real skin textures, zero corporate cheese, and absolutely no text or watermarks.",
                    "nano_banana": "[Subject]: Diverse multi-ethnic corporate team engaged in authentic collaboration around a contemporary conference table.\n[Setting]: High-ceiling modern glass office with architectural city views.\n[Lighting]: 5600K diffused morning daylight streaming from floor-to-ceiling windows, subtle ambient fill.\n[Optics]: 50mm prime lens, f/2.2 aperture, shallow depth of field.\n[Composition]: Balanced rule-of-thirds with generous negative copy space in the upper third for headline typography.\n[Commercial Requirements]: High-end business stock editorial, natural human expressions, authentic textures, no text.",
                    "negative_prompt": "text, watermark, corporate logo, extra fingers, deformed hands, bad anatomy, plastic airbrushed skin, oversaturated, blurry",
                    "reference_guide": {
                        "benchmark": "Forbes & Monocle Modern Business Editorial",
                        "sref_syntax": "--sref https://images.unsplash.com/photo-1497366216548-37526070297c --sw 100",
                        "mood": "High-key diffused daylight, architectural glass & oak boardroom, authentic human dynamics."
                    }
                },
                "sample_tags": ["diverse business team", "corporate office 4k video", "brainstorming meeting b-roll", "slow motion collaboration", "modern workspace footage", "prores corporate stock video", "professional teamwork clip"],
                "tag_titles": {
                    "diverse business team": [
                        "Diverse Business Team Brainstorming Strategy in Modern Corporate Conference Room 4K",
                        "Multiracial Diverse Business Team Smiling and Celebrating Quarter Target Success",
                        "Global Diverse Business Team Engaging in Inclusive Discussion in Bright Sunlit Office"
                    ],
                    "corporate office 4k video": [
                        "Corporate Office 4K Video of Professionals Discussing Financial Analytics Around Table",
                        "Modern Glass Corporate Office 4K Video with Executives Walking and Talking in Hallway",
                        "Dynamic Corporate Office Environment with Creative Workers at Standing Desks 4K"
                    ],
                    "brainstorming meeting b-roll": [
                        "Brainstorming Meeting B-Roll of Creative Colleagues Sharing Ideas with Sticky Notes",
                        "Startup Brainstorming Meeting B-Roll with Laptop and Whiteboard Problem Solving",
                        "Collaborative Brainstorming Meeting Footage Showing Active Team Engagement and Notes"
                    ],
                    "slow motion collaboration": [
                        "Slow Motion Collaboration of Startup Employees Smiling and Reviewing Project on Laptop",
                        "Cinematic Slow Motion Collaboration with Colleagues High-Fiving Over Successful Deal",
                        "Slow Motion Corporate Teamwork as Partners Shake Hands Across Conference Table"
                    ],
                    "modern workspace footage": [
                        "Modern Workspace Footage Showing Multiracial Coworkers in Sunlit Open Space Studio",
                        "Contemporary Modern Workspace B-Roll with Ergonomic Design and Green Plants",
                        "Trendy Tech Company Modern Workspace with Developers and Product Managers at Work"
                    ],
                    "prores corporate stock video": [
                        "ProRes Corporate Stock Video of Confident Business Leader Explaining Growth Roadmap",
                        "High Quality ProRes Corporate Stock Video for Commercial TV Ad and Website Hero",
                        "Cinematic ProRes Corporate Stock Video Showing Executive Presentation to Investors"
                    ],
                    "professional teamwork clip": [
                        "Professional Teamwork Clip of Young Executives High-Fiving After Successful Pitch",
                        "Authentic Professional Teamwork Video Clip Demonstrating Cross-Functional Agile Sprint",
                        "Inspiring Professional Teamwork Clip for HR Company Culture and Recruitment Video"
                    ]
                }
            },
            {
                "concept": "Biotechnology & Futuristic DNA Genetic Research",
                "asset_type": "AI Visual & 3D Render",
                "suggested_title": "DNA Genetic Helix Strand Glowing in Scientific Research Laboratory 3D Concept",
                "suggested_titles": [
                    "DNA Genetic Helix Strand Glowing in Scientific Research Laboratory 3D Concept",
                    "Futuristic Biotechnology Genetic Engineering Microscopic Cells Analysis Visual",
                    "Bio-Informatics Holographic DNA Sequencing Data Display for Medicine Discovery"
                ],
                "why_it_sells": "Pharmaceutical companies, medical news outlets, and scientific startups lack authentic photography and rely on high-end 3D AI visuals.",
                "ai_prompts": {
                    "midjourney": "Scientific commercial 3D visual of a luminous double-helix DNA strand and molecular genetic structures in an advanced biotechnology research laboratory. Luminous bioluminescent nodes, floating microscopic cellular particles, volumetric cyan and deep indigo ambient lighting, sharp focus on central genetic helix, clean negative space on the right for pharmaceutical editorial copy --ar 16:9 --style raw --stylize 150 --v 6.1 --sref https://images.unsplash.com/photo-1532187863486-abf9dbad1b69 --sw 100 --sv 6 --no text, watermarks, harsh grain, blurry, chaotic artifacts",
                    "flux": "A high-end 3D scientific visualization of a glowing DNA double helix structure inside a modern biopharmaceutical laboratory. Microscopic cells, floating molecular nodes, and subtle holographic data displays rendered with sharp optical clarity and volumetric blue-teal lighting. Clear negative space for medical headlines.",
                    "chatgpt": "A professional commercial stock photograph of a female scientist in clean lab attire analyzing a microplate in a modern biotechnology laboratory. Blue and amber ambient rim lighting from high-tech lab equipment, soft directional spotlight on her focused expression. Shot on an 85mm macro lens at f/2.0 with creamy background bokeh of pipettes and centrifuges. Ample negative copy space on the right for medical headlines. Natural skin texture, accurate laboratory equipment, and absolutely no text or watermarks.",
                    "nano_banana": "[Subject]: Professional female researcher in safety goggles pipetting a specimen in a modern sterile biotechnology laboratory.\n[Setting]: Cutting-edge life sciences laboratory with robotic liquid handlers and analytical monitors in soft focus.\n[Lighting]: Cool clean 6500K clinical lighting with warm amber rim light from benchtop instruments.\n[Optics]: 85mm macro prime lens, f/2.0 aperture, tack-sharp eye focus with smooth background blur.\n[Composition]: Ample negative copy space on the right third for healthcare and pharmaceutical typography.\n[Commercial Requirements]: Commercial stock grade, authentic scientific context, zero distortions, no text.",
                    "video": "Cinematic 4K 60fps slow-motion loop of glowing DNA double helix strand rotating smoothly with floating molecular particles. Volumetric cyan and deep blue illumination, shallow depth of field, ProRes 422, clean medical research b-roll.",
                    "negative_prompt": "text, watermarks, messy lines, low resolution, blurred artifacts, oversaturated colors",
                    "reference_guide": {
                        "benchmark": "Scientific American & Mayo Clinic Biotech Research Visualization",
                        "sref_syntax": "--sref https://images.unsplash.com/photo-1532187863486-abf9dbad1b69 --sw 100",
                        "mood": "Luminous bioluminescent DNA helix, molecular nodes, volumetric cyan and deep indigo lab lighting."
                    }
                },
                "sample_tags": ["biotech 3d render", "dna helix concept", "telemedicine doctor interface", "futuristic healthcare ai", "medical research laboratory", "nanotechnology visual", "digital health technology", "cellular biology 3d"],
                "tag_titles": {
                    "biotech 3d render": [
                        "Biotech 3D Render of Molecular Genetic Structure for Medical Science and Laboratory Research",
                        "Advanced Biotech 3D Render Showing Microscopic Cellular Engineering in Progress",
                        "Futuristic Biotech Visual of Gene Therapy and Biopharmaceutical Synthesis"
                    ],
                    "dna helix concept": [
                        "DNA Helix Concept Glowing with Luminous Particles in Futuristic Nanotechnology Laboratory",
                        "Double Helix DNA Strand Rotating with Molecular Connection Nodes in Blue Light",
                        "Abstract DNA Helix Concept Representing Human Genome Sequencing and Medical Innovation"
                    ],
                    "telemedicine doctor interface": [
                        "Telemedicine Doctor Interface with Holographic Genetic Data and Digital Health Diagnostics",
                        "Virtual Telemedicine HUD Screen Displaying Patient Biomarkers and Genetic Risk Factors",
                        "Smart Healthcare Telemedicine Visual with Futuristic Hologram Screen and Medical Charts"
                    ],
                    "futuristic healthcare ai": [
                        "Futuristic Healthcare AI Visual with Microscopic Cell Analysis and Genome Sequencing",
                        "Artificial Intelligence in Medicine Analyzing Molecular Biomarkers on Digital Display",
                        "Futuristic Healthcare AI Diagnostic System Scanning DNA Strands for Pathology Detection"
                    ],
                    "medical research laboratory": [
                        "Medical Research Laboratory Concept with Glowing DNA Strand and Pharmaceutical Discovery Visual",
                        "High Tech Medical Research Laboratory with Advanced Bio-Engineering Equipment and Samples",
                        "Scientific Medical Research Laboratory Workspace Investigating Cancer Immunotherapy"
                    ],
                    "nanotechnology visual": [
                        "Nanotechnology Visual of Bio-Engineering Molecular Cells for Advanced Gene Therapy",
                        "Microscopic Nanotechnology Robotics Interacting with Human Blood Cells 3D Visual",
                        "Futuristic Nanotechnology Medicine Delivering Targeted Pharmaceutical Particles"
                    ],
                    "digital health technology": [
                        "Digital Health Technology Displaying Automated Genome Sequencing and Biotechnology Metrics",
                        "Modern Digital Health Technology Platform Connecting Patients with Genomic Analysis",
                        "Next Generation Digital Health System Integrating Cloud Medicine and Bio-Informatics"
                    ],
                    "cellular biology 3d": [
                        "Cellular Biology 3D Scientific Illustration of Glowing Chromosomes and Gene Editing",
                        "Microscopic Cellular Biology 3D View of Cell Division and Protein Synthesis",
                        "Detailed Cellular Biology Render of Living Microscopic Organisms in Petri Culture"
                    ]
                }
            },
            {
                "concept": "Photorealistic AI Generative Commercial Lifestyle & Business Portraits",
                "asset_type": "AI Generative Stock Photo (Midjourney / Flux)",
                "suggested_title": "Confident Diverse Female Architect Reviewing Blueprints on Modern Sustainable Construction Site",
                "suggested_titles": [
                    "Confident Diverse Female Architect Reviewing Blueprints on Modern Sustainable Construction Site",
                    "Professional Woman Site Engineer Wearing White Safety Helmet and Holding Digital Tablet",
                    "Modern Sustainable Architecture Project Inspector Smiling Outdoors in Warm Natural Sunlight"
                ],
                "why_it_sells": "Adobe Stock buyers in AEC, real estate, and corporate HR license high-end commercial portraits of authentic professionals continuously.",
                "ai_prompts": {
                    "midjourney": "Authentic commercial stock portrait of an empowered diverse female architect and site engineer standing on an outdoor sustainable construction site during golden hour. Holding a digital tablet showing architectural blueprints, wearing a white safety hardhat and contemporary high-visibility vest, genuine confident warm smile, natural wind-blown hair. Shot on Leica SL2 with Summilux 50mm f/1.4 at f/2.0, razor-sharp eye catchlights, genuine skin pores and texture, warm golden-hour rim lighting, soft blurred modern eco-building background, negative copy space on upper left --ar 4:5 --style raw --stylize 150 --v 6.1 --sref https://images.unsplash.com/photo-1573496359142-b8d87734a5a2 --sw 100 --sv 6 --no text, watermarks, logo, extra fingers, deformed hands, plastic skin, uncanny valley, blurry",
                    "flux": "A photorealistic commercial stock portrait of a confident female civil engineer at an active sustainable building site. She is holding a tablet computer with structural drawings and looking warmly at the camera. Captured with an 85mm prime lens at f/2.0 during late afternoon golden hour. Realistic skin texture, authentic hardhat details, and soft directional sunlight. Clean negative space on the left suitable for architecture firm marketing.",
                    "chatgpt": "An authentic commercial stock photograph of a confident female architect examining architectural blueprints in a sunlit Scandinavian-style studio. Wearing a minimalist black turtleneck, pencil in hand, looking thoughtfully over floor plans. Warm afternoon sunlight streaming through industrial steel windows casting architectural grid shadows. Shot on an 85mm f/1.4 lens with shallow depth of field. Clean negative space on the left for design agency typography. Authentic textures, real skin pores, and no text, words, or watermarks.",
                    "nano_banana": "[Subject]: Confident modern female architect reviewing blueprint schematics at a wooden drafting table.\n[Setting]: Industrial loft architecture studio with concrete pillars, architectural models, and drafting tools in background.\n[Lighting]: Directional golden-hour window sunlight with soft ambient bounce, natural warm shadow falloff.\n[Optics]: 85mm prime lens at f/1.8, razor-sharp subject isolation.\n[Composition]: Hero framing with designated negative copy space on the upper left for creative branding.\n[Commercial Requirements]: Premium design editorial stock, authentic materials, natural human styling, no text.",
                    "video": "Cinematic 4K 60fps slow-motion stock clip of a female architect smiling confidently on a modern construction site. Warm sunset rim light, slow handheld camera track, authentic eye contact, ProRes 422, inspiring commercial STEM b-roll.",
                    "negative_prompt": "text, watermark, logo, deformed hands, extra fingers, plastic airbrushed skin, distorted facial features, oversaturated, blurry",
                    "reference_guide": {
                        "benchmark": "Architectural Record & Wired STEM Women Leaders",
                        "sref_syntax": "--sref https://images.unsplash.com/photo-1573496359142-b8d87734a5a2 --sw 100",
                        "mood": "Late afternoon golden-hour sunlight, authentic engineering site, natural skin texture with real pores."
                    }
                },
                "sample_tags": ["ai generated portrait", "female architect", "sustainable architecture", "commercial stock photo", "modern building construction", "diverse professional woman", "photorealistic ai lifestyle", "site engineer tablet"],
                "tag_titles": {
                    "ai generated portrait": [
                        "AI Generated Portrait of Confident Professional Engineer at Construction Site",
                        "Hyper-Realistic AI Generated Portrait of Modern Female Architect Smiling",
                        "Commercial AI Generated Portrait with Natural Bokeh and Cinematic Depth of Field"
                    ],
                    "female architect": [
                        "Female Architect Reviewing Blueprints and Engineering Plans on Digital Tablet",
                        "Young Female Architect in Safety Hardhat Inspecting Modern Building Development",
                        "Focused Female Architect Discussing Building Specifications on Outdoor Job Site"
                    ],
                    "sustainable architecture": [
                        "Sustainable Architecture Project Visual with Green Building Facade and Modern Construction",
                        "Eco-Friendly Sustainable Architecture Design with Solar Panels and Vertical Gardens",
                        "Innovations in Sustainable Architecture and Carbon Neutral Commercial Building Design"
                    ],
                    "commercial stock photo": [
                        "Commercial Stock Photo of Confident Woman in Hardhat Smiling Outdoors at Golden Hour",
                        "High Quality Commercial Stock Photo of Construction Manager at Urban Site",
                        "Authentic Commercial Stock Photo for Architecture Firm Marketing and Annual Report"
                    ],
                    "modern building construction": [
                        "Modern Building Construction Site Background with Professional Site Inspector",
                        "Urban Modern Building Construction with Concrete Steel Structures and Blue Sky",
                        "Active Modern Building Construction Site with Safety Standards and Crane in Background"
                    ],
                    "diverse professional woman": [
                        "Diverse Professional Woman in STEM Career Working on Urban Renewable Development",
                        "Empowered Diverse Professional Woman Leading Structural Engineering Inspection",
                        "Portrait of Diverse Professional Woman Contractor with Confident Warm Expression"
                    ],
                    "photorealistic ai lifestyle": [
                        "Photorealistic AI Lifestyle Portrait with Hasselblad Lighting and 85mm Lens Bokeh",
                        "Natural Photorealistic AI Lifestyle Visual of Corporate Contributor in Daylight",
                        "Photorealistic AI Lifestyle Photography for Modern Tech and Professional Editorial"
                    ],
                    "site engineer tablet": [
                        "Site Engineer Tablet Screen Showing BIM 3D Building Model on Construction Floor",
                        "Civil Site Engineer Using Tablet Computer to Verify Structural Measurements",
                        "Professional Site Engineer Holding Tablet Device at High-Rise Construction Site"
                    ]
                }
            }
        ]
    },

    "shutterstock": {
        "id": "shutterstock",
        "name": "Shutterstock",
        "color": "from-red-500 to-orange-600",
        "accent": "#ee2b24",
        "badge": "Shutterstock Contributor",
        "tag_limit": 50,
        "primary_focus": ["Commercial Stock Photos", "Vector Illustrations", "4K Video Clips", "Isolated Elements"],
        "ai_acceptance": {
            "status": "Internal Engine Only (Strict Third-Party Rejection)",
            "badge_color": "amber",
            "accepts_images": False,
            "accepts_videos": False,
            "details": "Shutterstock does NOT accept external Midjourney/Flux/Google Flow AI images through standard contributor upload. They only sell AI generated via their internal OpenAI tool. Focus on your Vectors, PSD Mockups, and real Video on Shutterstock!"
        },
        "requirements": {
            "vectors": {
                "format": "EPS 8 or EPS 10 format. Clean vector lines, zero embedded raster pixels.",
                "artboard": "Minimum 4 Megapixels. Outlined text, expanded paths for cut-ready elements.",
                "rules": "No gradients with complex transparency that rasterize upon EPS export. Keep vector clean and scalable."
            },
            "images": {
                "format": "JPEG, sRGB, uncompressed, minimum 4 Megapixels (standard 4000x3000px).",
                "resolution": "No visible noise or over-sharpening halos. Accurate metadata in EXIF.",
                "rules": "Model releases mandatory for recognizable faces. Commercial vs. Editorial strict separation."
            },
            "videos": {
                "format": "QuickTime MOV or MP4, H.264 or ProRes 422.",
                "resolution": "4K UHD (3840x2160) or Full HD 1080p, 23.98/24/29.97/30/60 fps.",
                "duration": "5 to 60 seconds. Steady stabilized camera gimbal movement."
            }
        },
        "ranking_tips": [
            "Use all 50 keyword slots. Shutterstock's engine indexes all 50 tags evenly.",
            "Isolated objects on clean white or transparent backgrounds have constant year-round sales.",
            "Check the 'Shutterstock Creative Flow' & Shot List every month for direct commercial buyer briefs.",
            "Include synonyms: e.g., 'autumn', 'fall', 'foliage', 'leaves', 'season'."
        ],
                "what_to_create": [
            {
                "concept": "Isolated Logistics & Supply Chain Warehouse Icons",
                "asset_type": "Illustrator Vector (EPS 10)",
                "suggested_title": "Smart Warehouse Logistics Automated Forklift and Cargo Delivery Drone Vector Set",
                "suggested_titles": [
                    "Smart Warehouse Logistics Automated Forklift and Cargo Delivery Drone Vector Set",
                    "Isometric Supply Chain Transportation and Global Freight Distribution Infographic Icons",
                    "Modern E-Commerce Fulfillment Logistics Vector Elements Isolated on White",
                    "Automated Robotic Warehouse Storage and Package Shipping Vector Set EPS 10"
                ],
                "why_it_sells": "Global trade, e-commerce, and logistics firms license these for presentations and training manuals.",
                "ai_prompts": {
                    "vector": "Clean EPS 10 isometric vector elements of smart automated logistics, pallet jacks, package sorting conveyors, delivery drones, and cargo trucks. Clean scalable bezier curves, expanded strokes, 100% white background, zero embedded raster pixels.",
                    "chatgpt": "An isometric 3D vector illustration set of smart warehouse logistics on a pure white background. Features electric forklifts, delivery drones, shipping crates, and automated robotic arms. Clean commercial look, sharp vector outlines, no text or logos.",
                    "video": "Smooth 4K 60fps stock animation loop of an automated warehouse fulfillment center with package conveyers and sorting robots moving in rhythmic motion. Clean industrial lighting, ProRes 422.",
                    "negative_prompt": "text, watermarks, blurry lines, raster pixels, gradient mesh, complex transparency, dark background",
                    "reference_guide": {
                        "benchmark": "DHL & Amazon Logistics Enterprise Visual System",
                        "mood": "Pristine white background, industrial safety yellow & navy accents, clean isometric geometry."
                    }
                },
                "sample_tags": ["smart warehouse vector", "isometric logistics", "cargo freight container", "delivery drone graphic", "supply chain infographic", "automated fulfillment center", "shipping truck vector"],
                "tag_titles": {
                    "smart warehouse vector": [
                        "Automated Smart Warehouse Vector Elements with Robots and Storage Shelves",
                        "High Tech Smart Warehouse Logistics Illustration for Supply Chain Presentation",
                        "Digital Warehouse Technology Concept Vector Graphic for Transportation Company"
                    ],
                    "isometric logistics": [
                        "Isometric Logistics and Cargo Shipping Vector Icons Set for E-Commerce",
                        "Modern Isometric Logistics Distribution Center Infographic Elements",
                        "Isometric Supply Chain Delivery and Freight Management Graphic"
                    ],
                    "cargo freight container": [
                        "Cargo Freight Container Stacking and Intermodal Shipping Vector Concept",
                        "Commercial Cargo Freight Transport for International Shipping Logistics",
                        "Industrial Shipping Containers Stacked at Terminal Port Vector Graphic"
                    ],
                    "delivery drone graphic": [
                        "Autonomous Delivery Drone Carrying Shipping Package Isolated on White",
                        "Modern Delivery Drone Technology Vector Icon for Quick Dispatch Service",
                        "Commercial Quadcopter Drone Dropping Parcel Delivery Illustration"
                    ],
                    "supply chain infographic": [
                        "Global Supply Chain Infographic Flowchart with Transportation Icons EPS 10",
                        "End to End Supply Chain Process Vector Graphic for Corporate Strategy Deck",
                        "Sustainable Supply Chain and Inventory Tracking Infographic Diagram"
                    ],
                    "automated fulfillment center": [
                        "Automated Fulfillment Center Robotic Conveyor Belt Sorting System Vector",
                        "E-Commerce Fulfillment Center Fast Parcel Processing Facility Graphic",
                        "Modern Distribution Warehouse Order Fulfillment Illustration Vector EPS"
                    ],
                    "shipping truck vector": [
                        "Modern Electric Cargo Shipping Truck Delivery Fleet Vector Illustration",
                        "Commercial Freight Transportation Logistics Van Isolated on White Background",
                        "Semi Trailer Delivery Truck for Cross Country Cargo Shipping Vector"
                    ]
                }
            },
            {
                "concept": "Authentic Remote Freelancer Home Office Desk Flatlay",
                "asset_type": "Stock Photography / Clean Render",
                "suggested_title": "Modern Minimalist Home Office Workspace with Laptop Coffee Mug and Plant Overhead Flatlay",
                "suggested_titles": [
                    "Modern Minimalist Home Office Workspace with Laptop Coffee Mug and Plant Overhead Flatlay",
                    "Top View Freelancer Desk Workspace with Aluminum Laptop Journal and Succulent Plant",
                    "Clean Scandinavian Work From Home Desk Setup with Organic Linen and Natural Daylight",
                    "Creative Digital Nomad Remote Workspace Flatlay for Productivity and Business Lifestyle"
                ],
                "why_it_sells": "Evergreen demand across productivity blogs, educational platforms, and tech company careers pages.",
                "ai_prompts": {
                    "midjourney": "Overhead flatlay photograph of a minimalist freelancer desk workspace. Sleek modern laptop, ceramic coffee mug with soft latte foam, natural craft paper notebook, small potted succulent, and wireless aluminum mouse arranged neatly on light birch wood table. Soft diffused morning daylight from top, gentle contact shadows, generous negative space on left --ar 16:9 --style raw --stylize 120 --no text, logos, clutter, blurry",
                    "flux": "A high-resolution commercial stock flatlay of a clean modern home office desk. Shot from directly above with a 50mm lens. Natural birch wood surface, contemporary laptop, warm latte in a ceramic mug, and green succulent plant. Soft diffused daylight creates realistic subtle contact shadows. Clear negative space for advertising typography.",
                    "chatgpt": "Top-down overhead view commercial photograph of a clean, minimalist home office desk. Modern laptop, ceramic coffee cup, neat journal with pen, and indoor plant on a light wooden desk. Soft natural daylight from the side. Ample negative copy space on the left. Natural realistic textures, no brand logos, no text.",
                    "video": "Cinematic 4K slow-motion overhead b-roll of hands typing comfortably on a laptop at a sunlit wooden desk with a steaming coffee cup. ProRes 422, smooth camera pan.",
                    "negative_prompt": "text, watermark, brand logo, messy cables, clutter, distorted keyboard, plastic shine, blurry",
                    "reference_guide": {
                        "benchmark": "Kinfolk & Cereal Magazine Still Life Editorial",
                        "mood": "Warm Scandinavian minimalism, light birch wood, natural daylight, generous negative copy space."
                    }
                },
                "sample_tags": ["remote work lifestyle", "digital nomad laptop", "home office desk setup", "freelancer working cafe", "telecommuting professional", "modern workspace indoor"],
                "tag_titles": {
                    "remote work lifestyle": [
                        "Authentic Remote Work Lifestyle Flatlay on Natural Wooden Workspace Desk",
                        "Modern Remote Work Lifestyle Concept with Laptop and Morning Coffee Cup",
                        "Work From Anywhere Remote Lifestyle Workspace for Technology Freelancer"
                    ],
                    "digital nomad laptop": [
                        "Digital Nomad Laptop Setup on Clean Minimalist Desk for Productive Day",
                        "Portable Digital Nomad Laptop Workspace for Remote Entrepreneur Lifestyle",
                        "Freelancer Digital Nomad Workspace Flatlay with Technology Accessories"
                    ],
                    "home office desk setup": [
                        "Scandinavian Home Office Desk Setup with Natural Oak Wood and Plants",
                        "Minimalist Home Office Workspace Desk Arrangement with Clean Negative Space",
                        "Organized Home Office Desk Layout for Productive Telecommuting Work"
                    ],
                    "freelancer working cafe": [
                        "Creative Freelancer Working Workspace Setup in Sunlit Morning Light",
                        "Modern Freelancer Work Environment with Coffee Mug and Notebook Flatlay",
                        "Productive Freelancer Workspace Concept for Small Business Owner"
                    ],
                    "telecommuting professional": [
                        "Telecommuting Professional Clean Workspace Flatlay for Corporate Blog",
                        "Modern Telecommuting Work Environment with Laptop and Task Planner",
                        "Work From Home Telecommuting Lifestyle Concept for Remote Employee"
                    ],
                    "modern workspace indoor": [
                        "Modern Workspace Indoor Architecture Flatlay with Light Wood Texture",
                        "Clean Contemporary Indoor Desk Space with Natural Plant and Office Tools",
                        "Aesthetic Indoor Workspace Layout for Digital Designer and Content Creator"
                    ]
                }
            },
            {
                "concept": "Minimalist Zen Meditation & Mental Wellness Concept",
                "asset_type": "Vector & Illustration",
                "suggested_title": "Mindfulness Meditation and Emotional Well Being Zen Silhouette Vector Illustration",
                "suggested_titles": [
                    "Mindfulness Meditation and Emotional Well Being Zen Silhouette Vector Illustration",
                    "Mental Health Wellness Concept with Serene Human Figure and Soft Sunburst Rays",
                    "Psychological Balance and Inner Peace Zen Meditation Graphic for Healthcare and Apps",
                    "Emotional Self Care and Mental Wellness Abstract Calm Vector Art Isolated on White"
                ],
                "why_it_sells": "Corporate wellness programs, psychology clinics, and app publishers need non-cliche wellness art.",
                "ai_prompts": {
                    "vector": "Clean vector illustration of a person sitting in tranquil lotus meditation pose. Gentle gradient aura radiating around the silhouette, delicate eucalyptus botanical branch accents, soothing earthy sage green and terracotta pastel palette, scalable EPS 10, clean cut-ready lines.",
                    "chatgpt": "A minimalist editorial commercial visual representing mental health and mindfulness. A silhouette meditating peacefully in soft morning golden light, surrounded by gentle organic botanical elements. Calming sage green and warm cream colors. Generous negative space for therapeutic slogan. No text or logos.",
                    "video": "Peaceful 4K 60fps seamless loop of soft golden light particles floating gently around a meditating silhouette in a calm zen garden. ProRes 422, relaxing ambient background.",
                    "negative_prompt": "text, watermark, anatomical distortion, harsh dark shadows, chaotic elements, blurry",
                    "reference_guide": {
                        "benchmark": "Headspace & Calm App Zen Wellness Aesthetic",
                        "mood": "Tranquil terracotta and sage tones, gentle sunbeam aura, organic botanical motifs."
                    }
                },
                "sample_tags": ["mental health awareness", "mindfulness meditation", "emotional wellness visual", "self care concept", "zen calming atmosphere", "psychological balance"],
                "tag_titles": {
                    "mental health awareness": [
                        "Mental Health Awareness Campaign Concept Graphic with Calm Silhouette",
                        "Promoting Mental Health Awareness and Emotional Balance Vector Illustration",
                        "Supportive Mental Health Awareness Visual for Therapy Clinic and Counseling"
                    ],
                    "mindfulness meditation": [
                        "Mindfulness Meditation Lotus Pose Silhouette for Wellness App and Yoga Studio",
                        "Daily Mindfulness Meditation Practice for Stress Reduction and Mental Clarity",
                        "Serene Mindfulness Meditation Vector Graphic with Radiant Inner Peace Aura"
                    ],
                    "emotional wellness visual": [
                        "Emotional Wellness and Holistic Health Graphic with Warm Calming Colors",
                        "Inspiring Emotional Wellness Concept for Psychological Well Being Guide",
                        "Balanced Emotional Wellness Illustration for Self Care Blog and Workshop"
                    ],
                    "self care concept": [
                        "Self Care Concept with Meditative Human Silhouette and Soothing Foliage",
                        "Healthy Self Care Routine for Stress Relief and Anxiety Management Graphic",
                        "Mindful Self Care Practice Illustration for Wellness Retreat and Therapy"
                    ],
                    "zen calming atmosphere": [
                        "Zen Calming Atmosphere Illustration with Balanced Stones and Soft Light",
                        "Tranquil Zen Calming Atmosphere Graphic for Spa and Relaxation Branding",
                        "Peaceful Zen Japanese Calming Aesthetic for Wellness Center Poster"
                    ],
                    "psychological balance": [
                        "Psychological Balance and Mental Harmony Concept Vector Illustration",
                        "Achieving Psychological Balance and Inner Resilience Graphic for Therapy",
                        "Symbolic Psychological Balance Visual for Life Coaching and Counseling App"
                    ]
                }
            }
        ]    },

    "etsy": {
        "id": "etsy",
        "name": "Etsy",
        "color": "from-orange-500 to-amber-600",
        "accent": "#f1641e",
        "badge": "Etsy Digital Shop",
        "tag_limit": 13,
        "primary_focus": ["Canva Templates", "SVG Cut Bundles (Cricut)", "Digital Planners", "Printable Wall Art", "PSD Mockups"],
        "ai_acceptance": {
            "status": "100% Accepted & Highest Volume",
            "badge_color": "emerald",
            "accepts_images": True,
            "accepts_videos": True,
            "details": "Etsy has a massive thriving market for AI clipart, AI printable wall art, and Canva templates utilizing AI elements. Disclose AI assistance in your shop description."
        },
        "requirements": {
            "vectors": {
                "format": "ZIP package containing SVG, DXF, EPS, and high-res transparent PNG (300 DPI).",
                "artboard": "Optimized for Cricut Design Space and Silhouette Studio. Single-layer and layered cut-ready paths.",
                "rules": "Clean welding: all overlapping vector shapes must be united so vinyl cutters cut smoothly."
            },
            "images": {
                "format": "300 DPI high-resolution JPG files for wall art. Formatted into 5 ratio folders (2:3, 3:4, 4:5, 11:14, ISO A1-A4).",
                "resolution": "Minimum 3600x4800px up to 7200x10800px for large poster printing without pixelation.",
                "rules": "Clipart must have 100% transparent PNG backgrounds with smooth anti-aliased edges."
            },
            "videos": {
                "format": "Short listing video (5 to 15 seconds), 1080x1080px or 1920x1080px.",
                "resolution": "1080x1080px (Square 1:1) or 1920x1080px (Landscape 16:9)",
                "rules": "Show the product in use: e.g. clicking through the Canva template, flicking through GoodNotes planner tabs, or unboxing files."
            },
            "templates": {
                "format": "PDF document with embedded clickable 'Access Your Canva Template' buttons and step-by-step video guide.",
                "artboard": "Multi-Page Canva Document / High-Res Printable PDF",
                "rules": "Use ONLY 100% free Canva elements and fonts so your customers never encounter Canva Pro paywalls."
            }
        },
        "ranking_tips": [
            "Etsy gives you EXACTLY 13 TAGS. Each tag can have up to 20 characters. Use all 13 slots!",
            "Use MULTI-WORD PHRASES in tags (e.g. 'canva wedding invite' instead of just 'wedding').",
            "Front-load your Title: First 40 characters show in Etsy search results on mobile.",
            "Include listing video (5-15s) demonstrating how easy it is to edit in Canva or unzipping the files."
        ],
                "what_to_create": [
            {
                "concept": "Modern Real Estate Agent Branding Suite (Canva)",
                "asset_type": "Canva Template Kit",
                "suggested_title": "Real Estate Marketing Template Bundle Canva Realtor Branding Kit Just Listed Open House Flyer",
                "suggested_titles": [
                    "Real Estate Marketing Template Bundle Canva Realtor Branding Kit Just Listed Open House Flyer",
                    "Modern Realtor Social Media Kit Canva Templates Instagram Post Story Carousels",
                    "Luxury Real Estate Seller Guide and Buyer Presentation Packet Editable Canva Link",
                    "Complete Real Estate Agent Branding Toolkit Just Sold Postcard Open House Flyer"
                ],
                "why_it_sells": "Real estate agents earn high commissions and gladly spend $15-$35 on turnkey professional marketing packages.",
                "ai_prompts": {
                    "canva_layout": "A cohesive 30-page Canva template kit for modern realtors: Just Listed square posts, Open House stories, 12-page Home Buyer Guide magazine layout, clean typography (Montserrat & Playfair), drag-and-drop photo frames, free Canva fonts only.",
                    "chatgpt": "Create an elegant flatlay mockup of a luxury real estate branding kit displayed on a marble desk. Features a printed home buyer guide, an iPad showing an Instagram carousel, and clean gold pen accessories. Clean professional lighting, ample negative space.",
                    "negative_prompt": "text errors, copyright fonts, premium paid elements, complex shapes, pixelated images",
                    "reference_guide": {
                        "benchmark": "Sotheby's Realty & Architectural Digest Clean Marketing",
                        "mood": "Luxury neutral palette (slate, champagne, gold), crisp layout, generous whitespace."
                    }
                },
                "sample_tags": ["real estate canva", "realtor branding kit", "just listed flyer", "realtor social media", "open house template", "buyer guide canva", "realtor instagram", "listing presentation", "realtor marketing", "modern real estate", "real estate flyer", "canva seller guide", "realtor templates"],
                "tag_titles": {
                    "real estate canva": [
                        "Real Estate Canva Template Bundle for Modern Agents and Brokers",
                        "Editable Real Estate Canva Marketing Kit with Social Media Posts",
                        "Turnkey Real Estate Canva Social Posts and Flyer Presentation"
                    ],
                    "realtor branding kit": [
                        "Realtor Branding Kit Canva Template with Business Card and Logo Layouts",
                        "Luxury Realtor Branding Kit for New Real Estate Agents and Teams",
                        "Professional Realtor Branding Kit Editable Templates Instant Download"
                    ],
                    "just listed flyer": [
                        "Just Listed Flyer Template Canva Editable Real Estate Property Handout",
                        "Modern Just Listed Real Estate Flyer Printable A4 and US Letter",
                        "Luxury Just Listed Property Flyer Template for Neighborhood Mailout"
                    ],
                    "realtor social media": [
                        "Realtor Social Media Posts Canva Template Kit Instagram and Facebook",
                        "Engaging Realtor Social Media Carousels and Real Estate Tips Templates",
                        "Modern Realtor Social Media Bundle with 50 Ready to Post Canva Graphics"
                    ],
                    "open house template": [
                        "Open House Template Canva Real Estate Invitation Sign and Welcome Packet",
                        "Chic Open House Flyer and Social Story Template for Weekend Showing",
                        "Complete Open House Checklist and Visitor Sign-In Sheet Canva Template"
                    ],
                    "buyer guide canva": [
                        "Home Buyer Guide Canva Template 12 Page Magazine Brochure for Realtors",
                        "First Time Home Buyer Guide Booklet Real Estate Agent Presentation PDF",
                        "Comprehensive Real Estate Home Buyer Guide Printable and Digital Link"
                    ],
                    "realtor instagram": [
                        "Realtor Instagram Carousel Templates Modern Real Estate Aesthetic Canva",
                        "Clean Realtor Instagram Story and Highlight Icons Pack for Agents",
                        "Viral Real Estate Realtor Instagram Post Templates Commercial Bundle"
                    ],
                    "listing presentation": [
                        "Real Estate Listing Presentation Packet Canva Slide Deck for Sellers",
                        "Winning Real Estate Listing Presentation Template Magazine Style PDF",
                        "Professional Realtor Listing Presentation Booklet for High End Properties"
                    ],
                    "realtor marketing": [
                        "All in One Realtor Marketing Toolkit Canva Templates Digital Download",
                        "Effective Realtor Marketing Postcards and Newsletter Layouts Canva",
                        "Modern Realtor Marketing Collateral Bundle for Busy Real Estate Professionals"
                    ],
                    "modern real estate": [
                        "Modern Real Estate Promotional Flyer and Social Media Graphics Kit",
                        "Minimalist Modern Real Estate Agent Template Pack Instant Access PDF",
                        "Aesthetic Modern Real Estate Branding Suite for Boutique Brokerages"
                    ],
                    "real estate flyer": [
                        "Printable Real Estate Flyer Template US Letter Format Canva Editable",
                        "Eye Catching Real Estate Flyer for Under Contract and Price Drop Notice",
                        "Real Estate Flyer Template Double Sided Handout with QR Code Slot"
                    ],
                    "canva seller guide": [
                        "Home Seller Guide Canva Template Packet Real Estate Marketing Book",
                        "Editable Canva Seller Guide Magazine for Staging and Pricing Strategy",
                        "Client Home Seller Guide Presentation Template for Modern Real Estate"
                    ],
                    "realtor templates": [
                        "Ultimate Realtor Templates Mega Bundle Over 100 Canva Designs Included",
                        "Essential Realtor Templates for Daily Lead Generation and Client Nurturing",
                        "Customizable Realtor Templates for Social Proof Client Testimonials and Sales"
                    ]
                }
            },
            {
                "concept": "Digital Life & Budget Planner for GoodNotes (iPad)",
                "asset_type": "Canva / Hyperlinked PDF",
                "suggested_title": "Digital Planner 2026 2027 GoodNotes iPad Planner Daily Weekly Monthly Undated Hyperlinked PDF",
                "suggested_titles": [
                    "Digital Planner 2026 2027 GoodNotes iPad Planner Daily Weekly Monthly Undated Hyperlinked PDF",
                    "All In One Digital Life Planner for Notability and GoodNotes Aesthetic iPad Tablet",
                    "Undated Digital Budget and Productivity Planner Hyperlinked Tabs Stickers Included",
                    "Deluxe Digital Life Planner iPad Android Tablet Habit Tracker Meal Planner PDF"
                ],
                "why_it_sells": "Consistent #1 digital download search on Etsy every single Q4 leading into the New Year.",
                "ai_prompts": {
                    "planner_spec": "Hyperlinked PDF planner built in Keynote or Canva: 500+ pages with smooth clickable side tab navigation. Includes Index, Yearly Overview, 12 Monthly spreads, Weekly schedule with timeblocks, Daily journaling, Habit tracker, and Financial budget ledger. Neutral aesthetic linen texture.",
                    "chatgpt": "A cozy, aesthetic flatlay photograph of an Apple iPad Pro with an Apple Pencil resting on its screen displaying a beautiful pastel digital planner page with hyperlinked tabs. Surrounded by an iced matcha latte, reading glasses, and a chunky knit blanket. Soft natural lighting.",
                    "negative_prompt": "broken links, low resolution, blurry text, harsh neon colors, misaligned tabs",
                    "reference_guide": {
                        "benchmark": "GoodNotes & Paperlike Aesthetic Productivity Still Life",
                        "mood": "Cozy minimalist beige & sage green, clickable hyperlinked layout, uncluttered design."
                    }
                },
                "sample_tags": ["digital planner 2026", "goodnotes planner", "ipad planner hyperlink", "undated daily planner", "notability template", "canva digital planner", "aesthetic planner pdf", "adhd friendly planner", "budget digital tracker", "minimalist ipad book", "habit tracker digital", "student ipad planner", "fitness planner ipad"],
                "tag_titles": {
                    "digital planner 2026": [
                        "Digital Planner 2026 2027 for GoodNotes and iPad with Hyperlinked Tabs",
                        "All In One Digital Planner 2026 Dated Daily Weekly Monthly Agenda PDF",
                        "Aesthetic Digital Planner 2026 for Tablets and Note Taking Applications"
                    ],
                    "goodnotes planner": [
                        "GoodNotes Planner Hyperlinked Digital Journal with 1000 Digital Stickers",
                        "Ultimate GoodNotes Planner for iPad with Smooth Navigation Tabs",
                        "Minimalist GoodNotes Planner Daily Routine and Life Organization Journal"
                    ],
                    "ipad planner hyperlink": [
                        "iPad Planner Hyperlinked PDF Document for Seamless Tap to Page Navigation",
                        "Modern iPad Planner Hyperlinked Monthly Calendars and Project Trackers",
                        "Interactive iPad Planner Hyperlink Template with Index and Quick Access Bar"
                    ],
                    "undated daily planner": [
                        "Undated Daily Planner Digital Download Use Year After Year Forever",
                        "Versatile Undated Daily Planner for Busy Moms Students and Professionals",
                        "Minimalist Undated Daily Planner Hourly Schedule and Top 3 Priorities"
                    ],
                    "notability template": [
                        "Notability Template Digital Life Planner Optimized for Apple Pencil",
                        "Smooth Notability Template with Hyperlinked Sidebar Navigation PDF",
                        "Productive Notability Template for Class Notes Work Meetings and Habits"
                    ],
                    "canva digital planner": [
                        "Canva Digital Planner Commercial Rights Template to Resell in Your Shop",
                        "Editable Canva Digital Planner Base Template with Hyperlink Instructions",
                        "Customizable Canva Digital Planner Layout for Digital Product Creators"
                    ],
                    "aesthetic planner pdf": [
                        "Aesthetic Planner PDF Pastel Warm Neutral Color Palette Digital Journal",
                        "Cozy Aesthetic Planner PDF with Clean Typography and Calming Visuals",
                        "Modern Aesthetic Planner PDF for Mindful Daily Reflection and Goal Setting"
                    ],
                    "adhd friendly planner": [
                        "ADHD Friendly Planner Digital Layout to Avoid Brain Overwhelm and Clutter",
                        "Structured ADHD Friendly Planner with Time Blocking and Dopamine Trackers",
                        "Simplified ADHD Friendly Planner Digital iPad PDF for Focus and Follow Through"
                    ],
                    "budget digital tracker": [
                        "Budget Digital Tracker Monthly Income Expense and Savings Goal Calculator",
                        "Annual Budget Digital Tracker with Debt Snowball and Sinking Funds Ledger",
                        "Personal Finance Budget Digital Tracker Hyperlinked Tab GoodNotes PDF"
                    ],
                    "minimalist ipad book": [
                        "Minimalist iPad Book Digital Planner with High Contrast Readable Layout",
                        "Clean Minimalist iPad Book for Professional Work Notes and Task Lists",
                        "Japanese Aesthetic Minimalist iPad Book Digital Journal Undated"
                    ],
                    "habit tracker digital": [
                        "Habit Tracker Digital Monthly Routine Checker and Wellness Checklist",
                        "Annual 365 Day Habit Tracker Digital Grid for iPad and Android Tablet",
                        "Visual Habit Tracker Digital Progress Chart for Health and Productivity"
                    ],
                    "student ipad planner": [
                        "Student iPad Planner Academic Year Semester Schedule and Exam Tracker",
                        "College Student iPad Planner Assignment Deadlines and GPA Calculator PDF",
                        "Complete Student iPad Planner for GoodNotes with Class Notes Sections"
                    ],
                    "fitness planner ipad": [
                        "Fitness Planner iPad Workout Tracker Meal Prep and Weight Loss Journal",
                        "Comprehensive Fitness Planner iPad Gym Routine and Body Measurement PDF",
                        "Weekly Fitness Planner iPad with Calorie Water and Exercise Log Spreads"
                    ]
                }
            },
            {
                "concept": "Retro Groovy Floral & Western SVG Cut Bundle",
                "asset_type": "Illustrator Vector / SVG Cut File",
                "suggested_title": "Retro Floral SVG Bundle Groovy 70s Daisy Flower Cricut Cut File Silhouette Sublimation PNG",
                "suggested_titles": [
                    "Retro Floral SVG Bundle Groovy 70s Daisy Flower Cricut Cut File Silhouette Sublimation PNG",
                    "Western Boho Cowgirl SVG Bundle Boots Hat Daisy Sublimation PNG Clipart",
                    "70s Groovy Flower SVG Bundle Daisy Smiley Face Vintage Tshirt Cut File",
                    "Retro Mama Daisy SVG Bundle Motherhood Groovy Cricut Cut Files Commercial Use"
                ],
                "why_it_sells": "Crafters and POD sellers buy bundles to print t-shirts, tote bags, and tumbler cups.",
                "ai_prompts": {
                    "svg_spec": "Clean vector SVG cut files: individual layers for multi-color vinyl, single unified outline for basic weeding, zero overlapping cut paths. Includes SVG, DXF, EPS, and 300 DPI transparent PNG (4500x5400px print ready).",
                    "chatgpt": "A vintage 1970s groovy aesthetic illustration of retro daisy flowers, smiling daisy face, and retro cursive typography. Warm muted mustard yellow, burnt orange, terracotta, and avocado green color scheme. Clean vector art, isolated on pure white.",
                    "negative_prompt": "raster artifacts, tiny unweedable specks, open vector contours, copyrighted brand slogans",
                    "reference_guide": {
                        "benchmark": "Urban Outfitters & Free People Vintage 70s Graphic Apparel",
                        "mood": "Warm earthy 70s nostalgia (mustard, terracotta, olive), bold clean cut lines."
                    }
                },
                "sample_tags": ["retro floral svg", "cricut cut file", "groovy flower svg", "western cowgirl svg", "mom shirt svg file", "silhouette cut file", "commercial use svg", "vintage daisy bundle", "sublimation png shirt", "retro boho graphics", "layered svg bundle", "tshirt design svg", "trendy craft bundle"],
                "tag_titles": {
                    "retro floral svg": [
                        "Retro Floral SVG Cut File Bundle for Cricut and Silhouette Cutters",
                        "Vintage Retro Floral SVG Clipart for T-Shirts and Coffee Tumblers",
                        "70s Style Retro Floral SVG Cut Ready Vector File for Crafters"
                    ],
                    "cricut cut file": [
                        "Cricut Cut File Easy Weeding Vinyl Design for DIY Gift Projects",
                        "Tested Cricut Cut File Bundle with Clean Smooth Layered Cut Paths",
                        "Commercial Cricut Cut File SVG and DXF for Small Business Crafters"
                    ],
                    "groovy flower svg": [
                        "Groovy Flower SVG 70s Aesthetic Daisy Cut File for Graphic Apparel",
                        "Smiling Groovy Flower SVG Vector Graphic for Tote Bags and Mugs",
                        "Vintage Groovy Flower SVG Silhouette File Instant Digital Download"
                    ],
                    "western cowgirl svg": [
                        "Western Cowgirl SVG Boots Hat and Daisy Cut File for Southern Apparel",
                        "Rustic Western Cowgirl SVG Vector Bundle for Country Music Concert Tee",
                        "Retro Western Cowgirl SVG Cut File with Howdy and Horseshoe Elements"
                    ],
                    "mom shirt svg file": [
                        "Mom Shirt SVG File Groovy Mama Motherhood Cricut Cut Graphic",
                        "Trendy Mom Shirt SVG File for Mothers Day Gift Apparel and Hoodies",
                        "Retro Mom Shirt SVG Cut Design Layered Vinyl and Sublimation File"
                    ],
                    "silhouette cut file": [
                        "Silhouette Cut File Compatible with Silhouette Cameo Studio Software",
                        "Layered Silhouette Cut File with Separate Color Groups for Decals",
                        "Precision Silhouette Cut File for Cardstock and Heat Transfer Vinyl"
                    ],
                    "commercial use svg": [
                        "Commercial Use SVG Bundle Sell Unlimited Physical Products in Shop",
                        "Commercial Use SVG Vector Graphics for POD Print on Demand Merch",
                        "Small Business Commercial Use SVG Cut Files for Apparel and Crafts"
                    ],
                    "vintage daisy bundle": [
                        "Vintage Daisy Bundle Botanical Wildflower SVG and Transparent PNG",
                        "Hand Drawn Vintage Daisy Bundle Clipart for Stationery and Stickers",
                        "Boho Vintage Daisy Bundle Cut File Pack for Summer and Spring Projects"
                    ],
                    "sublimation png shirt": [
                        "Sublimation PNG Shirt Graphic High Res 300 DPI Transparent Background",
                        "Retro Sublimation PNG Shirt Design Ready for Heat Press Transfer",
                        "Vibrant Sublimation PNG Shirt Artwork with Distressed Vintage Texture"
                    ],
                    "retro boho graphics": [
                        "Retro Boho Graphics Clipart Set with Earth Tones and Floral Motifs",
                        "Warm Retro Boho Graphics for Nursery Wall Art and Greeting Cards",
                        "Minimalist Retro Boho Graphics SVG and High Resolution PNG Bundle"
                    ],
                    "layered svg bundle": [
                        "Layered SVG Bundle Color Coded for Seamless HTV Vinyl Iron On",
                        "Multi Layered SVG Bundle Easy Alignment Registration Marks Included",
                        "Layered SVG Bundle for Paper Crafting Shadowboxes and Apparel"
                    ],
                    "tshirt design svg": [
                        "TShirt Design SVG Ready to Cut File for Boutique Clothing Brands",
                        "Trendy TShirt Design SVG Graphic for Modern Streetwear and Gifts",
                        "Best Selling TShirt Design SVG Vector File for Direct to Garment"
                    ],
                    "trendy craft bundle": [
                        "Trendy Craft Bundle 50+ Cut Files for Year Round Holiday Projects",
                        "Curated Trendy Craft Bundle for Cricut Silhouette and Glowforge Laser",
                        "Ultimate Trendy Craft Bundle SVG PNG DXF EPS for Creative Makers"
                    ]
                }
            }
        ]    },

    "iconscout": {
        "id": "iconscout",
        "name": "IconScout",
        "color": "from-blue-600 to-indigo-700",
        "accent": "#0055ff",
        "badge": "IconScout Designer",
        "tag_limit": 30,
        "primary_focus": ["3D Icons & Illustrations", "Vector Icon Packs", "Lottie Animations", "UI/UX Asset Kits"],
        "ai_acceptance": {
            "status": "Accepted for Isolated 3D Renders",
            "badge_color": "blue",
            "accepts_images": True,
            "accepts_videos": False,
            "details": "IconScout accepts 3D illustrations and icons rendered with AI tools provided they have pure transparent alpha backgrounds (PNG) or 3D formats (GLTF/OBJ) with clean lighting."
        },
        "requirements": {
            "vectors": {
                "format": "Clean SVG files, AI, EPS. Built strictly on 24x24px, 48x48px, or 64x64px pixel grids.",
                "artboard": "24x24px, 48x48px, or 64x64px Pixel Grid (RGB Color Mode)",
                "rules": "Provide both Outline (2px stroke) and Solid/Dual-tone styles in cohesive packs of 15, 30, or 60 icons."
            },
            "images": {
                "format": "3D Icons in transparent PNG, plus GLTF/Blender source files.",
                "resolution": "1000x1000px up to 4000x4000px Transparent PNG (300 DPI)",
                "rules": "Clean studio lighting, consistent claymorphism or glassmorphism aesthetic across the entire pack."
            },
            "videos": {
                "format": "Lottie JSON animation files (exported via Bodymovin / After Effects / LottieFiles).",
                "resolution": "60fps Vector Lottie JSON (<100KB file size)",
                "rules": "Smooth 30fps or 60fps loop, 2 to 4 seconds duration, optimized small JSON file size (<100KB)."
            }
        },
        "ranking_tips": [
            "Consistent icon sets sell 5x more than random single icons because UI/UX designers buy packs for entire apps.",
            "Glassmorphism 3D and Clay 3D styles remain the top earners on IconScout.",
            "Tag both functional and semantic words: e.g. for a shopping cart icon: 'cart', 'ecommerce', 'checkout', 'buy', 'store', 'shop'.",
            "Provide both Outline, Solid, and Dual-tone styles for every icon set."
        ],
                "what_to_create": [
            {
                "concept": "3D Fintech & Cryptocurrency Glossy Icon Pack",
                "asset_type": "3D Render / AI 3D PNG",
                "suggested_title": "3D Fintech Banking and Cryptocurrency Isolated Icons Pack for Mobile UI App",
                "suggested_titles": [
                    "3D Fintech Banking and Cryptocurrency Isolated Icons Pack for Mobile UI App",
                    "Modern 3D Gold Coin Wallet and Credit Card UI Icons on Transparent Background",
                    "Fintech Investment Graph and Blockchain Security 3D Icon Pack for Web Dashboard",
                    "Glossy Glassmorphism 3D Finance and Money Transfer Icons Set for Figma"
                ],
                "why_it_sells": "Fintech and Web3 startups constantly purchase 3D coin, wallet, credit card, and safe assets for modern landing pages.",
                "ai_prompts": {
                    "c4d_spec": "Rendered in Cinema 4D and Octane Render: 100% transparent PNG with zero halo fringe. Features vibrant gold coin with embossed bitcoin symbol, frosted translucent glass credit card with holographic chip, and smooth clay digital wallet. Soft ambient occlusion, subtle studio rim lighting.",
                    "chatgpt": "Isolated 3D icons representing modern financial technology: gold coin, floating credit card, digital lock, and upward growth graph. Rendered in clean glossy claymorphism style on a pure white background with subtle soft drop shadow. Zero text, immaculate edges.",
                    "negative_prompt": "ground floor, noisy background, halo artifacts, harsh jagged edges, low resolution",
                    "reference_guide": {
                        "benchmark": "Apple Pay & Stripe Modern 3D Design Systems",
                        "mood": "Vibrant emerald, gold & cobalt accents, specular glass reflections, clean alpha cutout."
                    }
                },
                "sample_tags": ["3d fintech icons", "crypto coin 3d", "digital wallet render", "credit card 3d icon", "banking app asset", "finance glassmorphism", "stock market arrow", "investment 3d badge", "smooth clay finance", "ui ux design asset", "money transfer icon", "decentralized finance"],
                "tag_titles": {
                    "3d fintech icons": [
                        "3D Fintech Icons Pack for Modern Mobile Banking and Investment Apps",
                        "Glossy 3D Fintech Icons Set with Transparent Backgrounds for Figma",
                        "High End 3D Fintech Icons for Financial SaaS Landing Page Banners"
                    ],
                    "crypto coin 3d": [
                        "Crypto Coin 3D Render Isolated Gold Bitcoin and Ethereum Token Asset",
                        "Floating Crypto Coin 3D Icon with Specular Studio Lighting PNG",
                        "Decentralized Crypto Coin 3D Illustration for Web3 Blockchain Interface"
                    ],
                    "digital wallet render": [
                        "Digital Wallet Render 3D Asset Showing Cash and Card Transactions",
                        "Smooth Clay Digital Wallet Render with Security Shield Icon PNG",
                        "Modern E-Wallet Digital Wallet Render for Online Checkout UI Mockup"
                    ],
                    "credit card 3d icon": [
                        "Credit Card 3D Icon Floating Translucent Glassmorphism Payment Graphic",
                        "Dual Credit Card 3D Icon Render for Cashless Payment and POS Checkout",
                        "Minimalist Credit Card 3D Icon with Holographic Chip Details"
                    ],
                    "banking app asset": [
                        "Banking App Asset 3D Renders Pack for iOS and Android UI Design",
                        "Clean Banking App Asset Pack with Account Balance and Loan Icons",
                        "Modern Mobile Banking App Asset Graphics on Pure Transparent Background"
                    ],
                    "finance glassmorphism": [
                        "Finance Glassmorphism 3D Icons with Refractive Caustics and Blur",
                        "Translucent Finance Glassmorphism Cards and Spheres for Web Design",
                        "Futuristic Finance Glassmorphism Element Pack for Keynote Presentation"
                    ],
                    "stock market arrow": [
                        "Stock Market Arrow 3D Upward Bullish Growth Trend Indicator Icon",
                        "Green Stock Market Arrow 3D Symbol for Portfolio Profit and Trading",
                        "Dynamic Stock Market Arrow 3D Render Floating Above Growth Chart"
                    ],
                    "investment 3d badge": [
                        "Investment 3D Badge Symbolizing Compound Interest and Financial Wealth",
                        "Modern Investment 3D Badge Asset for Venture Capital Pitch Deck",
                        "Glossy Gold Investment 3D Badge for Financial Advisory Marketing"
                    ],
                    "smooth clay finance": [
                        "Smooth Clay Finance Icon Set with Friendly Soft Rounded Geometry",
                        "Claymorphism Smooth Clay Finance 3D Asset for Gen-Z Banking App",
                        "Pastel Colored Smooth Clay Finance Icons Pack for Digital Wallet UI"
                    ],
                    "ui ux design asset": [
                        "UI UX Design Asset 3D Icon Bundle for Website Navigation and Headers",
                        "Professional UI UX Design Asset Kit for Mobile Product Prototype",
                        "Clean UI UX Design Asset Pack with Figma and PNG Files Included"
                    ],
                    "money transfer icon": [
                        "Money Transfer Icon 3D Curved Arrows and Flying Banknotes Graphic",
                        "Peer to Peer Money Transfer Icon 3D Render for Payment Gateway",
                        "Instant Money Transfer Icon 3D Visual with Dollar Symbol on Alpha"
                    ],
                    "decentralized finance": [
                        "Decentralized Finance DeFi 3D Smart Contract and Vault Icon Render",
                        "Blockchain Decentralized Finance 3D Holographic Cube and Node Element",
                        "Modern Decentralized Finance 3D Asset for Crypto Exchange Web Platform"
                    ]
                }
            },
            {
                "concept": "Minimalist Dual-Tone SaaS Enterprise Dashboard Icons",
                "asset_type": "Illustrator Vector (SVG/AI)",
                "suggested_title": "Enterprise Cloud SaaS Dashboard Navigation Vector Line Icons 24px Grid",
                "suggested_titles": [
                    "Enterprise Cloud SaaS Dashboard Navigation Vector Line Icons 24px Grid",
                    "Minimalist Dual-Tone SVG Icons Pack for Modern Web Application UI",
                    "B2B Cloud Software Navigation Icons 24px Pixel Perfect Grid (SVG & AI)",
                    "Clean Technology Vector System Icons for Figma Design Systems"
                ],
                "why_it_sells": "Product designers at B2B tech companies license scalable vector icon sets for design systems in Figma.",
                "ai_prompts": {
                    "vector_spec": "Built on strict 24x24px pixel grid: 2px stroke weight, rounded caps and corners. Dual-tone style pairing primary dark slate (#1e293b) with 20% opacity indigo fill (#6366f1) for secondary shapes. Clean expanded SVG and outlined stroke versions.",
                    "chatgpt": "A set of minimalist tech UI icons on a clean white background. 24px grid alignment, dual-tone indigo and dark navy colors. Icons include: server cloud, analytics bar chart, API integration key, user settings gear, and security shield. Crisp vector lines.",
                    "negative_prompt": "misaligned pixels, uneven stroke weights, complex gradients, raster elements",
                    "reference_guide": {
                        "benchmark": "Tailwind CSS Heroicons & Linear App Iconography",
                        "mood": "Dual-tone slate & indigo, pixel-perfect 24px grid, unified 2px stroke width."
                    }
                },
                "sample_tags": ["saas dashboard icons", "dual tone vector", "enterprise ui icon", "cloud hosting symbol", "api integration icon", "analytics line icon", "clean 24px grid", "app navigation icons", "user management symbol"],
                "tag_titles": {
                    "saas dashboard icons": [
                        "SaaS Dashboard Icons Vector Pack for Enterprise Web Application UI",
                        "Modern SaaS Dashboard Icons Set with 24px Pixel Perfect Alignment",
                        "Comprehensive SaaS Dashboard Icons Bundle for B2B Cloud Platforms"
                    ],
                    "dual tone vector": [
                        "Dual Tone Vector Icons with Clean Primary Line and Soft Pastel Fill",
                        "Professional Dual Tone Vector Icon Set for Software Control Panels",
                        "Modern Dual Tone Vector Icons Pack for Clean Interface Design Systems"
                    ],
                    "enterprise ui icon": [
                        "Enterprise UI Icon Library for Corporate Software and IT Infrastructure",
                        "Minimalist Enterprise UI Icon Pack with Outlined and Solid Variations",
                        "High Quality Enterprise UI Icon Collection for Web and Mobile Apps"
                    ],
                    "cloud hosting symbol": [
                        "Cloud Hosting Symbol Vector Icon for Server Network and Database",
                        "Secure Cloud Hosting Symbol Line Icon on 24px Pixel Grid SVG",
                        "Hybrid Cloud Hosting Symbol Illustration for DevOps and System Admin"
                    ],
                    "api integration icon": [
                        "API Integration Icon Vector Graphic for Developer Documentation",
                        "Webhook and API Integration Icon for Software Connection Diagram",
                        "Modern API Integration Icon Line Art for SaaS Feature Overview"
                    ],
                    "analytics line icon": [
                        "Analytics Line Icon Bar Chart and Growth Trendline Metric Graphic",
                        "Data Analytics Line Icon for Business Intelligence KPI Dashboard",
                        "Clean Analytics Line Icon Set Showing User Conversion and Traffic"
                    ],
                    "clean 24px grid": [
                        "Clean 24px Grid Pixel Perfect Vector Icons for Crisp Retina Displays",
                        "Harmonized Clean 24px Grid Icon System with Consistent Visual Weight",
                        "Standard Clean 24px Grid UI Icons Ready to Drag and Drop in Figma"
                    ],
                    "app navigation icons": [
                        "App Navigation Icons Header Menu Search Notifications and Profile",
                        "Mobile App Navigation Icons Pack for iOS Tab Bar and Android Drawer",
                        "Universal App Navigation Icons SVG EPS and High Resolution PNG"
                    ],
                    "user management symbol": [
                        "User Management Symbol Multi User Permissions and Role Assignment",
                        "Team User Management Symbol Vector Icon for Admin Account Settings",
                        "Secure User Management Symbol for Enterprise Authentication Flow"
                    ]
                }
            },
            {
                "concept": "Lottie Micro-Interaction App Success Animations",
                "asset_type": "Lottie JSON / Vector Motion",
                "suggested_title": "Interactive Lottie Animation Pack Success Checkmark Loading Spinner Confetti JSON",
                "suggested_titles": [
                    "Interactive Lottie Animation Pack Success Checkmark Loading Spinner Confetti JSON",
                    "Micro-Interaction Lottie Animations Set for Mobile App Checkout and Success States",
                    "Lightweight Vector Motion Lottie JSON Loops for Webflow and iOS Apps",
                    "Animated UI Delight Feedback Icons Pack Lottie JSON 60fps Smooth"
                ],
                "why_it_sells": "Mobile app developers require ready-to-code JSON animations for delight states and checkout flows.",
                "ai_prompts": {
                    "motion_spec": "Lottie JSON animation files exported via After Effects and Bodymovin plugin: 60fps, 2-3s duration, optimized vector paths under 40KB per file. Features bouncy spring physics: success checkmark burst with particle pop, subtle looping loading ring, and celebratory confetti shower.",
                    "video": "Smooth 60fps vector micro-interaction animation loop of a success checkmark popping into view with joyful colorful confetti particles. Clean dark background, ProRes 422 preview.",
                    "negative_prompt": "choppy framerate, heavy file size, raster images embedded in json, broken masks",
                    "reference_guide": {
                        "benchmark": "LottieFiles & Airbnb Mobile App Micro-Interactions",
                        "mood": "Elastic bouncy spring easing (cubic-bezier), lightweight JSON code, joyful delight states."
                    }
                },
                "sample_tags": ["lottie animation json", "success checkmark loop", "animated bell notification", "loading spinner ui", "confetti celebration", "pull to refresh lottie", "micro interaction app"],
                "tag_titles": {
                    "lottie animation json": [
                        "Lottie Animation JSON Pack for Seamless Integration in Mobile Apps",
                        "Lightweight Lottie Animation JSON Files Under 50KB for Fast Page Load",
                        "Interactive Lottie Animation JSON Loops for Webflow and React Developers"
                    ],
                    "success checkmark loop": [
                        "Success Checkmark Loop Lottie Animation with Satisfying Spring Pop",
                        "Payment Complete Success Checkmark Loop for E-Commerce App Checkout",
                        "Animated Success Checkmark Loop with Green Accent and Confetti Burst"
                    ],
                    "animated bell notification": [
                        "Animated Bell Notification Lottie JSON Icon for App Alert Triggers",
                        "Gentle Ringing Animated Bell Notification Vector Motion for Dashboard",
                        "Bouncing Animated Bell Notification with Red Badge Counter Element"
                    ],
                    "loading spinner ui": [
                        "Loading Spinner UI Smooth 60fps Infinite Vector Animation JSON",
                        "Modern Circular Loading Spinner UI for Web App Asynchronous Actions",
                        "Minimalist Loading Spinner UI with Gradient Ring and Eased Motion"
                    ],
                    "confetti celebration": [
                        "Confetti Celebration Lottie Animation for Gamification and Level Up",
                        "Joyful Confetti Celebration Particle Burst for Order Confirmation",
                        "Colorful Confetti Celebration Vector Motion Loop for Winner Announcement"
                    ],
                    "pull to refresh lottie": [
                        "Pull to Refresh Lottie Animation Loop for Mobile App Feed Updates",
                        "Interactive Pull to Refresh Lottie Indicator for iOS and Android",
                        "Clean Pull to Refresh Lottie Micro Interaction with Arrow to Spinner"
                    ],
                    "micro interaction app": [
                        "Micro Interaction App Asset Pack Elevating Product Experience and UX",
                        "Delightful Micro Interaction App Animations for Buttons and Toggles",
                        "Subtle Micro Interaction App Feedback Icons for Modern Digital Products"
                    ]
                }
            }
        ]    },

    "graphicriver": {
        "id": "graphicriver",
        "name": "GraphicRiver (Envato)",
        "color": "from-emerald-600 to-teal-700",
        "accent": "#82b541",
        "badge": "Envato Author",
        "tag_limit": 30,
        "primary_focus": ["Print Flyers & Posters", "PSD Apparel & Product Mockups", "Presentation Pitch Decks", "Business Stationery"],
        "ai_acceptance": {
            "status": "Allowed as Layered Design Elements",
            "badge_color": "purple",
            "accepts_images": True,
            "accepts_videos": False,
            "details": "GraphicRiver allows AI-generated textures, background imagery, and artistic elements when integrated into layered, editable Photoshop PSD or Illustrator design files."
        },
        "requirements": {
            "vectors": {
                "format": "Layered AI & EPS format, CMYK color mode for print or RGB for digital flyers.",
                "artboard": "CMYK 300 DPI with 0.125 inch (3mm) print bleed or RGB 72 DPI Web",
                "rules": "All text must use free commercial Google Fonts (provide links in help.txt). All shapes organized into labeled groups."
            },
            "images": {
                "format": "Photoshop PSD Smart Objects, 300 DPI, CMYK with 0.125 inch (3mm) bleed for print items.",
                "resolution": "Layered PSD Smart Object (3000x2000px+, 300 DPI, CMYK/RGB)",
                "rules": "Layer folders must be clearly color-coded (e.g. Green: Text Here, Red: Smart Object Artwork, Blue: Background)."
            },
            "videos": {
                "format": "GraphicRiver is primarily graphic templates. Video templates belong on VideoHive (Envato's sister marketplace).",
                "resolution": "After Effects CS6+ Full HD 1920x1080 or GIF Previews",
                "rules": "Provide animated GIF previews showing smart-object updates in action."
            }
        },
        "ranking_tips": [
            "Preview image is EVERYTHING on GraphicRiver: create a killer 590x700px thumbnail showing real mockup context.",
            "Never include copyrighted fonts or stock photos in download files; use free Google Font links and photo placeholders.",
            "Corporate and Church/Gospel flyer templates maintain strong, steady re-sales on Envato.",
            "Packaging mockups (cosmetic bottles, coffee bags, shipping boxes) have great lifetime value."
        ],
                "what_to_create": [
            {
                "concept": "Streetwear Oversized Hoodie & T-Shirt PSD Mockup",
                "asset_type": "Photoshop Mockup (PSD)",
                "suggested_title": "Streetwear Oversized Heavyweight Cotton Hoodie and Vintage T-Shirt PSD Mockup Template",
                "suggested_titles": [
                    "Streetwear Oversized Heavyweight Cotton Hoodie and Vintage T-Shirt PSD Mockup Template",
                    "Urban Streetwear Apparel Mockup Bundle Heavy Cotton Hoodie Smart Object PSD",
                    "Vintage Washed T-Shirt and Drop Shoulder Hoodie Mockup with Realistic Fabric Texture",
                    "Apparel Brand Mockup Kit Male Model Wearing Oversized Hoodie Studio Lighting"
                ],
                "why_it_sells": "Independent streetwear brands and Etsy apparel sellers buy mockups to showcase their collections.",
                "ai_prompts": {
                    "psd_spec": "3000x2000px at 300 DPI layered Photoshop PSD: Smart Object layer with realistic displacement map for natural fabric fold distortion. Highlights on Screen mode, shadows on Multiply mode. Changeable garment colors, heather texture overlay, customizable wall and floor background.",
                    "chatgpt": "Commercial product mockup photograph of a blank heavyweight oversized black streetwear hoodie hanging on an industrial steel rack against a brutalist concrete wall. Dramatic directional spotlight, sharp fabric weave texture, ample copy space for clothing brand logo. No text.",
                    "negative_prompt": "flat 2d look, unnatural warp, pixelated fabric, harsh seams, clipping errors",
                    "reference_guide": {
                        "benchmark": "Fear of God & Represent Clothing Studio Lookbook",
                        "mood": "Moody architectural lighting, tactile heavy cotton weave, displacement map realism."
                    }
                },
                "sample_tags": ["streetwear mockup psd", "oversized hoodie mockup", "vintage tshirt psd", "smart object apparel", "realistic fabric texture", "heavyweight cotton shirt", "clothing brand mockup", "apparel tag mockup"],
                "tag_titles": {
                    "streetwear mockup psd": [
                        "Streetwear Mockup PSD Template with Smart Object Displacement Map",
                        "Urban Streetwear Mockup PSD Bundle for Independent Fashion Brands",
                        "High Resolution Streetwear Mockup PSD with Customizable Color Layers"
                    ],
                    "oversized hoodie mockup": [
                        "Oversized Hoodie Mockup PSD Heavyweight Drop Shoulder Fleece Garment",
                        "Modern Oversized Hoodie Mockup with Front and Back Graphic Placements",
                        "Realistic Oversized Hoodie Mockup Template on Minimalist Model"
                    ],
                    "vintage tshirt psd": [
                        "Vintage TShirt PSD Mockup Washed Acid Wash Cotton Texture Layers",
                        "Retro 90s Vintage TShirt PSD Mockup Template with Realistic Creases",
                        "Heavyweight Vintage TShirt PSD for Direct to Garment Merch Showcase"
                    ],
                    "smart object apparel": [
                        "Smart Object Apparel Mockup Double Click to Insert Your Artwork",
                        "Effortless Smart Object Apparel PSD with Automatic Fabric Distortion",
                        "Professional Smart Object Apparel Presentation File for Clothing Lines"
                    ],
                    "realistic fabric texture": [
                        "Realistic Fabric Texture Details Visible at 100 Percent Zoom in PSD",
                        "Tactile Realistic Fabric Texture Mockup for Premium Merch Portfolios",
                        "Authentic Realistic Fabric Texture with Subtle Heather Grain Overlay"
                    ],
                    "heavyweight cotton shirt": [
                        "Heavyweight Cotton Shirt Mockup PSD Built for High End Fashion Lines",
                        "Thick Heavyweight Cotton Shirt Apparel Template with Ribbed Collar",
                        "Streetwear Heavyweight Cotton Shirt Display File for Online Stores"
                    ],
                    "clothing brand mockup": [
                        "Clothing Brand Mockup Toolkit to Pitch Lookbooks and Retail Buyers",
                        "Complete Clothing Brand Mockup Suite with Apparel Hang Tags and Bags",
                        "All in One Clothing Brand Mockup Bundle for E-Commerce Product Listings"
                    ],
                    "apparel tag mockup": [
                        "Apparel Tag Mockup PSD Woven Neck Label and Cardstock Swing Tag",
                        "Customizable Apparel Tag Mockup with Realistic String and Safety Pin",
                        "Branded Apparel Tag Mockup Template for Garment Packaging Showcase"
                    ]
                }
            },
            {
                "concept": "Modern Corporate Trifold Brochure & A4 Flyer (CMYK 300 DPI)",
                "asset_type": "Photoshop PSD & Illustrator AI",
                "suggested_title": "Corporate Business Annual Report Trifold Brochure and Marketing Flyer Template PSD",
                "suggested_titles": [
                    "Corporate Business Annual Report Trifold Brochure and Marketing Flyer Template PSD",
                    "Modern Corporate Trifold Brochure and A4 Flyer Template Print Ready 300 DPI CMYK",
                    "Clean Annual Report Company Profile Trifold Brochure with Infographic Data Layouts",
                    "Professional Financial Services Marketing Flyer and Brochure Pack PSD and AI"
                ],
                "why_it_sells": "Small business consultants, financial advisors, and agencies download ready-to-print collateral daily.",
                "ai_prompts": {
                    "print_spec": "CMYK 300 DPI with 0.125 inch (3mm) bleed and safety margins. Organized into color-coded layer groups (Text, Shapes, Photo Placeholders). Uses free Google Fonts (Inter & Montserrat). Includes both Photoshop PSD (Smart Objects) and vector Illustrator AI/EPS formats.",
                    "chatgpt": "Professional commercial marketing flatlay showing a trifold corporate brochure and an A4 marketing flyer displayed neatly on a minimalist dark glass boardroom table. Clean corporate layout with subtle geometric teal accents. Soft architectural window lighting, high-end editorial feel.",
                    "negative_prompt": "rgb colors on print file, missing bleed, lowres images, non-commercial licensed fonts",
                    "reference_guide": {
                        "benchmark": "McKinsey & Boston Consulting Group Executive Collateral",
                        "mood": "Executive navy & teal palette, crisp typographic grid, 0.125-inch print bleed accuracy."
                    }
                },
                "sample_tags": ["corporate flyer psd", "trifold brochure template", "business flyer 300dpi", "cmyk print template", "annual report brochure", "company profile template", "marketing leaflet psd"],
                "tag_titles": {
                    "corporate flyer psd": [
                        "Corporate Flyer PSD Template Print Ready CMYK with Free Google Fonts",
                        "Modern Corporate Flyer PSD for Business Consulting and Agency Services",
                        "Elegant Corporate Flyer PSD with Clean Geometric Layout and Photo Slots"
                    ],
                    "trifold brochure template": [
                        "Trifold Brochure Template Double Sided 6 Panel Business Marketing Layout",
                        "Corporate Trifold Brochure Template with Company Overview and Services",
                        "Clean Trifold Brochure Template Print Ready with Standard Bleed Margins"
                    ],
                    "business flyer 300dpi": [
                        "Business Flyer 300DPI High Resolution Template for Professional Printing",
                        "Promotional Business Flyer 300DPI Layout for Conferences and Seminars",
                        "A4 and US Letter Business Flyer 300DPI Pack with Fully Editable Text"
                    ],
                    "cmyk print template": [
                        "CMYK Print Template Calibrated for Commercial Offset and Digital Presses",
                        "Certified CMYK Print Template with Safety Cut Lines and 3mm Bleed",
                        "Clean CMYK Print Template for Small Business Marketing and Direct Mail"
                    ],
                    "annual report brochure": [
                        "Annual Report Brochure Template with Financial Charts and Executive Summary",
                        "Corporate Annual Report Brochure Layout for Stakeholder Presentations",
                        "Modern Annual Report Brochure Template with Clean Multi Page Flow"
                    ],
                    "company profile template": [
                        "Company Profile Template Trifold Flyer Showcasing Mission and Team",
                        "B2B Company Profile Template Brochure for Client Proposals and Pitches",
                        "Professional Company Profile Template with Organized Color Coded Layers"
                    ],
                    "marketing leaflet psd": [
                        "Marketing Leaflet PSD Template for Door to Door and Trade Show Handouts",
                        "Compact Marketing Leaflet PSD Design with Strong Call to Action Slots",
                        "Creative Marketing Leaflet PSD Template Ready to Personalize in Photoshop"
                    ]
                }
            },
            {
                "concept": "Restaurant & Sports Bar Food Menu Poster & Trifold",
                "asset_type": "Photoshop PSD (Print Ready)",
                "suggested_title": "Modern Restaurant and Craft Beer Bar Food Menu Tri-Fold Flyer Template PSD",
                "suggested_titles": [
                    "Modern Restaurant and Craft Beer Bar Food Menu Tri-Fold Flyer Template PSD",
                    "Rustic Chalkboard Restaurant Menu Poster and Trifold Brochure Template 300 DPI",
                    "Gourmet Burger and Craft Beer Bar Table Menu Template PSD Print Ready CMYK",
                    "Elegant Cafe and Bistro Food Drinks Menu Template Package Layered Photoshop"
                ],
                "why_it_sells": "Hospitality venues update menus seasonally and designers rely on pre-formatted templates.",
                "ai_prompts": {
                    "menu_spec": "A4 and US Letter 300 DPI CMYK: Organized layout for Starters, Mains, Desserts, and Drinks with pricing columns and dietary badge icons (Vegan, GF). Uses free commercial fonts. Smart Object food photo slots with realistic appetizing color grading.",
                    "chatgpt": "Editorial food photography mockup of a rustic wooden restaurant clipboard menu resting on a dark slate tabletop next to a gourmet burger and a craft beer glass with condensation droplets. Warm ambient pub lighting, mouth-watering appetizing mood.",
                    "negative_prompt": "unreadable fonts, cluttered spacing, RGB print errors, blurry food images",
                    "reference_guide": {
                        "benchmark": "Bon Appétit & Shake Shack Gourmet Brand Identity",
                        "mood": "Warm ambient restaurant lighting, clean two-column pricing typography, appetizing layout."
                    }
                },
                "sample_tags": ["restaurant menu psd", "cafe food flyer", "bar cocktail menu", "rustic food menu", "burger menu template", "cmyk print menu", "chalkboard restaurant sign"],
                "tag_titles": {
                    "restaurant menu psd": [
                        "Restaurant Menu PSD Template Layered File with Easy Price and Item Editing",
                        "Modern Restaurant Menu PSD Layout for Casual Dining and Fine Bistros",
                        "Complete Restaurant Menu PSD Bundle with Food Category Dividers"
                    ],
                    "cafe food flyer": [
                        "Cafe Food Flyer Template for Coffee Shop Breakfast and Pastry Specials",
                        "Charming Cafe Food Flyer Design Printable Handout with Warm Aesthetic",
                        "Artisan Cafe Food Flyer and Daily Specials Poster Template PSD"
                    ],
                    "bar cocktail menu": [
                        "Bar Cocktail Menu Template PSD for Craft Beer Wine and Spirits List",
                        "Nightclub and Bar Cocktail Menu Card with Signature Drink Descriptions",
                        "Modern Bar Cocktail Menu Template Print Ready CMYK with Bleed"
                    ],
                    "rustic food menu": [
                        "Rustic Food Menu Template with Chalkboard Background and Vintage Type",
                        "Farm to Table Rustic Food Menu Layout for Country Kitchen Restaurant",
                        "Wood Texture Rustic Food Menu Flyer for BBQ Smokehouse and Tavern"
                    ],
                    "burger menu template": [
                        "Burger Menu Template PSD for Fast Casual Gourmet Burger Joint and Fries",
                        "American Diner Burger Menu Template with Appetizing Food Photo Slots",
                        "Street Food Truck Burger Menu Template Printable Poster and Card"
                    ],
                    "cmyk print menu": [
                        "CMYK Print Menu Template Tested for Flawless Color Output on Heavy Stock",
                        "Commercial CMYK Print Menu Document with Standard Trifold Fold Marks",
                        "High Quality CMYK Print Menu Template for Laminated Restaurant Table Cards"
                    ],
                    "chalkboard restaurant sign": [
                        "Chalkboard Restaurant Sign Poster Template for Daily Chef Recommendations",
                        "Vintage Chalkboard Restaurant Sign Layout with Hand Lettered Headings",
                        "Eye Catching Chalkboard Restaurant Sign Design for Sidewalk A-Frame Board"
                    ]
                }
            }
        ]
    }
}
