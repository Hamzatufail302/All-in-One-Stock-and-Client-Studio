"""
Daily Ranked Calendar & Events Engine
Tracks 365-day upcoming holidays, shopping milestones, fashion drops, milestone birthdays,
and life events. Ranks each event by commercial stock demand, calculates precise golden
upload date ranges, deadlines, and flags late windows.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

MASTER_CALENDAR_EVENTS = [
    # =========================================================================
    # Q4: OCTOBER, NOVEMBER, DECEMBER
    # =========================================================================
    {
        "month": 10, "day": 1,
        "name": "Cyber Security Month & Infosec Awareness",
        "category": "Corporate & Tech",
        "impact_score": 92,
        "stars": 5,
        "lead_time_days": 40,
        "what_to_create": {
            "vectors": "Cyber defense shields, biometric fingerprint locks, firewall binary isometric icons.",
            "images": "Photorealistic AI hacker cyber warfare screens, dark glowing neon cybersecurity concept visuals.",
            "videos": "4K loop of digital data encryption, glowing binary numbers matrix, server room status.",
            "templates": "Corporate IT data privacy report Canva, cybersecurity awareness employee training slides."
        },
        "suggested_titles": [
            "Cyber Security Data Protection and Firewall Technology Concept Vector",
            "Biometric Fingerprint Data Privacy Authentication Vector Illustration",
            "Digital Encryption Matrix Data Flow Seamless 4K Stock Video Loop"
        ]
    },
    {
        "month": 10, "day": 10,
        "name": "World Mental Health Day & Wellness",
        "category": "Health & Lifestyle",
        "impact_score": 90,
        "stars": 4,
        "lead_time_days": 35,
        "what_to_create": {
            "vectors": "Brain mental health floral line art, emotional therapy illustrations, self-care badges.",
            "images": "Calming meditation visual, sunrise mindfulness silhouette, psychology consultation scene.",
            "videos": "Gentle ocean waves in slow motion 4k, peaceful nature meditation background.",
            "templates": "Mental health awareness Instagram post kit Canva, therapy clinic brochure."
        },
        "suggested_titles": [
            "Mental Health Awareness Brain Line Art Illustration with Blooming Flowers",
            "Mindfulness Self Care and Emotional Well Being Lifestyle Concept Visual",
            "Therapy Psychology Clinic Medical Brochure Flyer Template PSD"
        ]
    },
    {
        "month": 10, "day": 20,
        "name": "Breast Cancer Awareness & Pink Ribbon Campaign",
        "category": "Health & Lifestyle",
        "impact_score": 89,
        "stars": 4,
        "lead_time_days": 40,
        "what_to_create": {
            "vectors": "Pink ribbon breast cancer vector graphics, female empowerment floral ribbons, fundraising badges.",
            "images": "Diverse women wearing pink ribbons supporting cancer awareness, hopeful smiling survivors.",
            "videos": "Silk pink ribbon gently floating in slow motion 4K, charity marathon crowd.",
            "templates": "Charity 5K run flyers Canva, cancer awareness social media carousel PSD."
        },
        "suggested_titles": [
            "Pink Ribbon Breast Cancer Awareness Symbol Watercolor Vector Graphic",
            "Breast Cancer Awareness Charity Marathon Poster Flyer Template Canva"
        ]
    },
    {
        "month": 10, "day": 31,
        "name": "Halloween Night & Spooky Season",
        "category": "Holidays & Cultural",
        "impact_score": 98,
        "stars": 5,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Jack-o'-lantern pumpkin faces, haunted cemetery silhouette vector, trick or treat badges, spooky ghost SVG.",
            "images": "Atmospheric gothic haunted mansion in moonlight, cinematic AI jack-o-lantern glowing mist.",
            "videos": "Spooky glowing pumpkin candle flicker 4K, dark misty woods drone flight.",
            "templates": "Last minute costume party invitations, trick-or-treat printable signs Canva, party flyer PSD."
        },
        "suggested_titles": [
            "Halloween Spooky Pumpkin Jack O Lantern Glowing Night Aesthetic Visual",
            "Retro Vintage Haunted House and Flying Bats Vector Graphic Illustration",
            "Halloween Party Night Invitation Poster Template Printable Canva"
        ]
    },
    {
        "month": 11, "day": 1,
        "name": "Diwali Festival of Lights & Deepavali",
        "category": "Holidays & Cultural",
        "impact_score": 94,
        "stars": 5,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Ornate golden diya oil lamps, rangoli geometric patterns, Happy Diwali golden typography.",
            "images": "Glowing oil lamps on floral water pool, traditional Indian festive family celebration.",
            "videos": "Cinematic diya lamp candle flicker macro 4K, sparkling fireworks loop.",
            "templates": "Diwali corporate greeting card Canva, luxury festive sale banner PSD."
        },
        "suggested_titles": [
            "Happy Diwali Golden Diya Oil Lamp and Rangoli Floral Pattern Vector",
            "Diwali Festival of Lights Traditional Oil Lamps Floating on Water 4K Stock Image",
            "Happy Diwali Corporate Greeting Card and Social Media Banner Template Canva"
        ]
    },
    {
        "month": 11, "day": 11,
        "name": "Singles' Day (11.11) & Veterans Day",
        "category": "E-Commerce & Retail",
        "impact_score": 91,
        "stars": 4,
        "lead_time_days": 40,
        "what_to_create": {
            "vectors": "11.11 global shopping festival 3D neon badges, American flag soldier silhouette salute vector.",
            "images": "3D golden metallic 11.11 sale ribbons, military hero portrait with US flag.",
            "videos": "Retail shopping cart particle explosion 4K, American flag fluttering slow-mo.",
            "templates": "11.11 flash sale Instagram story Canva, Veterans Day tribute poster PSD."
        },
        "suggested_titles": [
            "11.11 Global Shopping Festival Neon 3D Sale Badge Vector Design",
            "Veterans Day Honor and Remembrance Silhouette Military Vector Graphic"
        ]
    },
    {
        "month": 11, "day": 20,
        "name": "Autumn / Winter Streetwear & Heavy Outerwear Drop",
        "category": "Fashion & Apparel",
        "impact_score": 93,
        "stars": 5,
        "lead_time_days": 50,
        "what_to_create": {
            "vectors": "Heavyweight oversized hoodie mockup vectors, distressed streetwear typography cut files, puffer jacket line art.",
            "images": "Cinematic streetwear model in urban Tokyo alley at night, cozy wool knitwear flatlay aesthetic.",
            "videos": "Streetwear fashion model walking through rainy neon city 4K 60fps slow motion.",
            "templates": "Clothing brand lookbook catalog InDesign, streetwear drop Instagram carousel Canva."
        },
        "suggested_titles": [
            "Oversized Streetwear Hoodie Apparel Mockup PSD Smart Object Realistic Texture",
            "Urban Streetwear Fashion Model in Rainy City Cinematic 4K Stock Video",
            "Cozy Autumn Winter Wool Knitwear and Trench Coat Flatlay Photography"
        ]
    },
    {
        "month": 11, "day": 26,
        "name": "Thanksgiving Day & Autumn Harvest Feast",
        "category": "Holidays & Cultural",
        "impact_score": 96,
        "stars": 5,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Roast turkey vector, cornucopia autumn vegetables, grateful thankful blessed lettering SVG.",
            "images": "Family Thanksgiving dinner table overhead flatlay, cozy autumn harvest aesthetic.",
            "videos": "Slow camera drift over traditional Thanksgiving meal, pouring hot gravy 4K.",
            "templates": "Thanksgiving dinner menu card template Canva, church Thanksgiving worship flyer."
        },
        "suggested_titles": [
            "Grateful Thankful Blessed Autumn Lettering SVG Cut File for Cricut",
            "Thanksgiving Festive Family Dinner Feast Overhead Flatlay Photography",
            "Thanksgiving Dinner Restaurant Food Menu Template Tri-fold PSD"
        ]
    },
    {
        "month": 11, "day": 27,
        "name": "Black Friday & Cyber Monday Mega Weekend",
        "category": "E-Commerce & Retail",
        "impact_score": 100,
        "stars": 5,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Neon Black Friday discount badges, 3D percentage signs, mega sale ribbons, price tags.",
            "images": "Cyberpunk 3D shopping cart with glowing gifts, luxury dark Friday retail background.",
            "videos": "Black Friday particle explosion with glowing 50% off text, retail crowd entering store.",
            "templates": "E-commerce promotional banners Canva, Black Friday weekend sales flyer PSD."
        },
        "suggested_titles": [
            "Black Friday Mega Sale Neon 3D Typography Badge Vector Banner",
            "Black Friday Social Media Promo Discount Template Bundle Canva",
            "Cyber Monday Special Offer 3D Shopping Cart Glowing Tech Background"
        ]
    },
    {
        "month": 12, "day": 10,
        "name": "Hanukkah Menorah Festival",
        "category": "Holidays & Cultural",
        "impact_score": 88,
        "stars": 4,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Golden menorah with nine candles, dreidel spinning vector, Star of David blue-gold patterns.",
            "images": "Lit menorah candles glowing bokeh background, traditional Hanukkah latkes and donuts flatlay.",
            "videos": "Slow motion lighting of Hanukkah menorah candle flame 4K.",
            "templates": "Happy Hanukkah family greeting card Canva, community synagogue festival flyer."
        },
        "suggested_titles": [
            "Happy Hanukkah Golden Menorah and Dreidel Clipart Vector Illustration",
            "Traditional Hanukkah Menorah with Lit Candles Bokeh 4K Stock Image"
        ]
    },
    {
        "month": 12, "day": 25,
        "name": "Christmas Day (Global Top Seller of the Year)",
        "category": "Holidays & Cultural",
        "impact_score": 100,
        "stars": 5,
        "lead_time_days": 60,
        "what_to_create": {
            "vectors": "Christmas tree seamless patterns, retro Santa Claus cliparts, snowflake SVG bundles.",
            "images": "Cozy Scandinavian winter fireplace, glowing bokeh Christmas lights, photorealistic snow cabin.",
            "videos": "Gentle falling snow loop 4K 60fps, glittering Christmas tree branches bokeh b-roll.",
            "templates": "Family photo holiday card Canva, ugly Christmas sweater party flyer PSD."
        },
        "suggested_titles": [
            "Merry Christmas Watercolor Vintage Santa Claus and Reindeer Clipart Bundle",
            "Cozy Winter Holiday Living Room with Decorated Christmas Tree 4K Stock Image",
            "Seamless Loop of Realistic Snow Falling in Forest 4K Stock Video Footage",
            "Family Christmas Photo Holiday Greeting Card Printable Canva Template"
        ]
    },
    {
        "month": 12, "day": 31,
        "name": "New Year's Eve & Global Countdown",
        "category": "Holidays & Cultural",
        "impact_score": 99,
        "stars": 5,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Golden 2027 typography vector logo, champagne toast clinking glasses, fireworks burst.",
            "images": "Luxury New Year golden confetti glitter background, city skyline fireworks celebration.",
            "videos": "Cinematic fireworks countdown 4K, golden confetti explosion slow-motion loop.",
            "templates": "New Year 2027 Eve club party flyer PSD, annual digital life planner GoodNotes."
        },
        "suggested_titles": [
            "Happy New Year 2027 Luxury Golden Typography with Fireworks Vector",
            "New Year 2027 Digital Life and Fitness Planner for iPad GoodNotes",
            "Luxury New Year Eve Nightclub Party Celebration Flyer Template PSD",
            "Golden Confetti and Champagne Glasses Toast Celebration 4K Stock Video"
        ]
    },

    # =========================================================================
    # Q1: JANUARY, FEBRUARY, MARCH
    # =========================================================================
    {
        "month": 1, "day": 1,
        "name": "New Year Resolutions & Fitness Kickoff",
        "category": "Health & Lifestyle",
        "impact_score": 96,
        "stars": 5,
        "lead_time_days": 50,
        "what_to_create": {
            "vectors": "Workout dumbbells and fitness tracker icons, healthy nutrition meal prep infographics.",
            "images": "Athletic fitness runner sunrise workout, modern clean gym equipment aesthetic.",
            "videos": "Gym athlete training slow motion 4k, fresh organic salad prep b-roll.",
            "templates": "Weight loss & workout habit tracker Canva, fitness center promotional flyer PSD."
        },
        "suggested_titles": [
            "New Year Fitness Resolution Workout Habit Tracker Printable Canva PDF",
            "Modern Gym Fitness Center Promotional Marketing Flyer Template PSD",
            "Athletic Woman Running on Track at Sunrise Health Fitness 4K Video"
        ]
    },
    {
        "month": 1, "day": 15,
        "name": "Tax Season & Accounting Planning Wave",
        "category": "Corporate & Tech",
        "impact_score": 89,
        "stars": 4,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Tax calculation charts, IRS tax refund icons, corporate bookkeeping isometric graphics.",
            "images": "Accountant working on laptop with calculator and tax documents, modern office financial meeting.",
            "videos": "Hands calculating numbers on financial calculator macro 4K.",
            "templates": "Tax preparation service brochure Canva, CPA tax deduction checklist PDF."
        },
        "suggested_titles": [
            "Income Tax Return Filing Preparation and Financial Accounting Vector Concept",
            "CPA Accounting Firm Professional Tax Preparation Trifold Brochure Canva"
        ]
    },
    {
        "month": 2, "day": 1,
        "name": "Spring / Summer Fashion Week & Lookbook Launch",
        "category": "Fashion & Apparel",
        "impact_score": 95,
        "stars": 5,
        "lead_time_days": 60,
        "what_to_create": {
            "vectors": "Minimalist haute couture croquis sketches, pastel aesthetic color palette swatches, botanical apparel patterns.",
            "images": "Fashion model in linen dress walking minimalist sunlit studio, high-fashion editorial portrait.",
            "videos": "Catwalk runway model catwalk slow motion 4K 60fps, fabric drapery waving in wind.",
            "templates": "Fashion brand lookbook template InDesign, apparel catalogue Canva mockup."
        },
        "suggested_titles": [
            "Haute Couture Runway Model High Fashion Editorial Studio Photography",
            "Minimalist Linen Dress Apparel Clothing Brand Mockup Template PSD",
            "Fashion Week Runway Show Catwalk Model Slow Motion 4K Stock Video"
        ]
    },
    {
        "month": 2, "day": 10,
        "name": "Super Bowl & Championship Football Sunday",
        "category": "Holidays & Cultural",
        "impact_score": 90,
        "stars": 4,
        "lead_time_days": 40,
        "what_to_create": {
            "vectors": "American football stadium field vector, tailgate BBQ graphics, game day party badges.",
            "images": "Friends cheering watching big game TV in living room with beer and snacks.",
            "videos": "Crowd cheering in sports stadium lights 4K, beer pouring with foam slow motion.",
            "templates": "Game day watch party flyer Canva, sports bar big game drink special menu PSD."
        },
        "suggested_titles": [
            "Game Day Big Football Championship Watch Party Nightclub Flyer PSD",
            "American Football Stadium Field with Dramatic Floodlights Vector Concept"
        ]
    },
    {
        "month": 2, "day": 14,
        "name": "Valentine's Day & Romantic Gifting",
        "category": "Holidays & Cultural",
        "impact_score": 98,
        "stars": 5,
        "lead_time_days": 55,
        "what_to_create": {
            "vectors": "Red glossy 3D hearts, romantic cupid arrows, love typography SVG cut files.",
            "images": "Romantic candlelit fine dining table, red roses bouquet with gift box luxury flatlay.",
            "videos": "Floating 3D heart particles seamless loop 4K, couple holding hands sunset.",
            "templates": "Valentine's dinner menu card PSD, romantic love coupons Canva template."
        },
        "suggested_titles": [
            "Valentine's Day Romantic 3D Glossy Red Hearts Isolated Vector Graphic",
            "Be My Valentine Printable Love Greeting Card Template Editable Canva",
            "Romantic Valentine Special Restaurant Dinner Menu Tri-fold Template PSD"
        ]
    },
    {
        "month": 3, "day": 1,
        "name": "Spring Milestone Birthdays (18th, 21st, 30th & 50th)",
        "category": "Birthdays & Milestones",
        "impact_score": 96,
        "stars": 5,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Dirty Thirty & Death to My 20s retro SVG cut files, Vintage 1976/1986 badges, gold foil cake topper vectors.",
            "images": "Champagne celebration birthday party with 30th golden balloons, laughing friends confetti.",
            "videos": "Birthday cake candles sparkler slow motion 4K, champagne bottle popping cork.",
            "templates": "30th milestone birthday invitation Canva, 21st birthday drink menu card, printable birthday trivia games."
        },
        "suggested_titles": [
            "Dirty Thirty 30th Birthday Retro Groovy SVG Cut File for Cricut",
            "Death to My 20s Gothic Black Theme 30th Birthday Invitation Canva Template",
            "Vintage Made in 1976 50th Birthday Retro Sunset Badge Vector Graphic",
            "Milestone 21st Birthday Celebration Champagne Glass Toast 4K Stock Video"
        ]
    },
    {
        "month": 3, "day": 8,
        "name": "International Women's Day & Female Leadership",
        "category": "Health & Lifestyle",
        "impact_score": 92,
        "stars": 4,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Diverse women empowerment portraits, feminist fist symbol, botanical floral frame.",
            "images": "Inspiring female corporate leadership team, creative artisan woman in studio.",
            "videos": "Confident diverse women walking in office slow motion 4K.",
            "templates": "Women's Day conference flyer PSD, Instagram quote carousel bundle Canva."
        },
        "suggested_titles": [
            "International Women's Day Diverse Female Empowerment Vector Clipart",
            "Women Leadership Conference and Seminar Poster Flyer Template PSD"
        ]
    },
    {
        "month": 3, "day": 17,
        "name": "St. Patrick's Day & Irish Heritage Festival",
        "category": "Holidays & Cultural",
        "impact_score": 93,
        "stars": 4,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Four-leaf clover shamrock vectors, lucky leprechaun hat, Celtic knots.",
            "images": "Pints of Irish green beer pub scene, pot of gold rainbow fantasy render.",
            "videos": "Shamrock green confetti falling loop 4K, frothy stout beer pouring.",
            "templates": "St. Patrick's Day pub crawl flyer PSD, lucky Irish t-shirt SVG cut file."
        },
        "suggested_titles": [
            "Four Leaf Clover Shamrock Lucky Saint Patrick Day Vector Clipart",
            "St. Patrick's Day Beer Party and Pub Crawl Celebration Flyer PSD"
        ]
    },
    {
        "month": 3, "day": 25,
        "name": "Spring Baby Showers & Gender Reveal Season",
        "category": "Birthdays & Milestones",
        "impact_score": 94,
        "stars": 5,
        "lead_time_days": 50,
        "what_to_create": {
            "vectors": "Cute watercolor woodland baby animals (fawn, bear, bunny), greenery eucalyptus wreath, Oh Baby lettering SVG.",
            "images": "Pastel baby shower dessert table with cupcakes and balloons, gender reveal smoke cannon celebration.",
            "videos": "Baby booties next to pregnancy ultrasound flatlay camera drift 4K.",
            "templates": "Safari animal baby shower invitation Canva, gender reveal voting game board printable."
        },
        "suggested_titles": [
            "Watercolor Woodland Baby Animals Nursery Clipart Bundle PNG Vector",
            "Oh Baby Greenery Eucalyptus Baby Shower Invitation Suite Canva Template",
            "Gender Reveal Party He or She Voting Board Game Printable Canva"
        ]
    },

    # =========================================================================
    # Q2: APRIL, MAY, JUNE
    # =========================================================================
    {
        "month": 4, "day": 5,
        "name": "Easter Sunday & Spring Florals",
        "category": "Holidays & Cultural",
        "impact_score": 95,
        "stars": 5,
        "lead_time_days": 55,
        "what_to_create": {
            "vectors": "Pastel watercolor Easter eggs, cute bunny rabbit illustrations, spring floral wreaths.",
            "images": "Easter egg hunt in green garden morning sun, spring flowers bouquet with tulips and daffodils.",
            "videos": "Time-lapse of blooming pink spring flowers 4K, cute bunny eating grass.",
            "templates": "Church Easter worship service flyer PSD, Easter brunch buffet menu Canva."
        },
        "suggested_titles": [
            "Watercolor Easter Bunny Rabbit and Pastel Floral Egg Wreath Clipart",
            "Easter Sunday Church Resurrection Worship Flyer Event Template PSD",
            "Spring Easter Egg Hunt Community Festival Flyer Printable Canva"
        ]
    },
    {
        "month": 4, "day": 15,
        "name": "Music Festival & Desert Boho Chic Fashion",
        "category": "Fashion & Apparel",
        "impact_score": 93,
        "stars": 5,
        "lead_time_days": 50,
        "what_to_create": {
            "vectors": "Boho chic mandala vectors, desert cactus sunset line art, retro hippie floral cut files.",
            "images": "Festival attendees dancing in desert sunset wearing boho outfits and glitter, palm trees silhouette.",
            "videos": "Outdoor music festival crowd cheering with stage lasers and smoke 4K 60fps.",
            "templates": "Indie music festival poster template PSD, festival outfit lookbook social carousel."
        },
        "suggested_titles": [
            "Boho Chic Festival Fashion Model in Desert Sunset Aesthetic Visual",
            "Outdoor Music Festival Concert Poster Flyer Template GraphicRiver PSD",
            "Desert Music Festival Crowd Dancing with Neon Lights 4K Stock Video"
        ]
    },
    {
        "month": 4, "day": 22,
        "name": "Earth Day & Climate ESG Sustainability",
        "category": "Corporate & Tech",
        "impact_score": 91,
        "stars": 4,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Green ecology recycling icons, solar panel wind turbine infographics, zero waste badges.",
            "images": "Hands planting young tree seedling in fertile soil, futuristic eco-friendly green smart city.",
            "videos": "Wind turbines spinning against blue sky aerial drone 4K, ocean plastic clean up.",
            "templates": "Corporate ESG annual sustainability report Canva, school Earth Day science poster."
        },
        "suggested_titles": [
            "Earth Day Eco Friendly Green Energy and Sustainability Concept Vector",
            "Corporate ESG Sustainability Annual Report Presentation Template Canva"
        ]
    },
    {
        "month": 5, "day": 10,
        "name": "Mother's Day & Best Mom Gifting",
        "category": "Holidays & Cultural",
        "impact_score": 98,
        "stars": 5,
        "lead_time_days": 55,
        "what_to_create": {
            "vectors": "Best Mom Ever calligraphy SVG, watercolor peony floral frame, Mama shirt cut file.",
            "images": "Mother hugging her daughter laughing at home golden hour sunlight, breakfast in bed with flowers.",
            "videos": "Mother holding newborn baby close tender moment slow motion 4K.",
            "templates": "Mother's Day restaurant brunch menu PSD, personalized gift card coupon book Canva."
        },
        "suggested_titles": [
            "Best Mom Ever Handwritten Calligraphy SVG Cut File for Cricut",
            "Mother's Day Floral Watercolor Greeting Card Printable Canva Template",
            "Loving Mother Hugging Daughter Golden Hour Portrait Photography"
        ]
    },
    {
        "month": 5, "day": 20,
        "name": "Summer Resort & Swimwear Collection Drop",
        "category": "Fashion & Apparel",
        "impact_score": 94,
        "stars": 5,
        "lead_time_days": 55,
        "what_to_create": {
            "vectors": "Bikini and swimwear flat sketches, tropical palm leaf vector pattern, sunglasses brand logo badge.",
            "images": "Model in stylish luxury swimwear lounging next to infinity pool overlooking Mediterranean ocean.",
            "videos": "Drone aerial tracking boat across turquoise tropical ocean water 4K.",
            "templates": "Summer resort collection lookbook Canva, beach boutique e-commerce discount banner."
        },
        "suggested_titles": [
            "Luxury Resort Swimwear Model by Turquoise Ocean Infinity Pool Photography",
            "Tropical Summer Beach Boutique E-Commerce Sale Banner Set Canva",
            "Aerial Drone View of Luxury Yacht in Tropical Ocean 4K Stock Video"
        ]
    },
    {
        "month": 5, "day": 25,
        "name": "Peak Wedding Season & Bridal Shower Wave",
        "category": "Birthdays & Milestones",
        "impact_score": 99,
        "stars": 5,
        "lead_time_days": 75,
        "what_to_create": {
            "vectors": "Luxury monogram wedding crests, botanical eucalyptus invitation frames, Mr & Mrs SVG cut files.",
            "images": "Bride and groom golden hour portrait in vineyard, luxury wedding banquet table setting with candles.",
            "videos": "Slow motion bride walking down aisle with wedding dress train 4K, clinking champagne glasses.",
            "templates": "Full wedding invitation suite (Invite, RSVP, Details, Menu, Seating Chart) Canva."
        },
        "suggested_titles": [
            "Elegant Botanical Wedding Invitation Suite Printable Editable Canva Template",
            "Luxury Gold Foil Wedding Monogram Crest and Floral Frame Vector Graphic",
            "Romantic Bride and Groom Sunset Vineyard Portrait Photography 4K",
            "Wedding Reception Banquet Table with Candlelight Slow Motion Video"
        ]
    },
    {
        "month": 5, "day": 30,
        "name": "Graduation Season & Class of 2026/2027",
        "category": "Birthdays & Milestones",
        "impact_score": 95,
        "stars": 5,
        "lead_time_days": 50,
        "what_to_create": {
            "vectors": "Graduation cap throwing silhouette, Class of 2026/2027 lettering SVG, diploma scroll badge.",
            "images": "Happy university graduates throwing mortarboards into blue sky, graduate with proud parents.",
            "videos": "Graduation caps flying in slow motion in air 4K 60fps.",
            "templates": "Graduation open house party invitation Canva, graduation photo announcement yard sign."
        },
        "suggested_titles": [
            "Class of 2027 Senior Year Graduation Cap Throwing SVG Cut File",
            "Graduation Open House Celebration Party Announcement Flyer Template Canva",
            "Joyful University Graduates Throwing Caps in Air Celebration 4K Video"
        ]
    },
    {
        "month": 6, "day": 1,
        "name": "Pride Month & Rainbow Diversity Celebrations",
        "category": "Holidays & Cultural",
        "impact_score": 94,
        "stars": 5,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Rainbow pride flag gradients, Love is Love typography, LGBTQ+ community icons.",
            "images": "Diverse friends celebrating at pride parade smiling with rainbow flags, colorful festival confetti.",
            "videos": "Rainbow flag waving proud slow motion 4K against blue sky.",
            "templates": "Pride festival parade flyer PSD, corporate DEI diversity newsletter template Canva."
        },
        "suggested_titles": [
            "Love is Love Rainbow Pride Typography Vector Illustration SVG",
            "Pride Month Community Parade Festival Celebration Poster Template Canva"
        ]
    },
    {
        "month": 6, "day": 15,
        "name": "Quinceañera & Sweet 16 Milestone Celebrations",
        "category": "Birthdays & Milestones",
        "impact_score": 93,
        "stars": 5,
        "lead_time_days": 55,
        "what_to_create": {
            "vectors": "Mis Quince Años calligraphy, sparkling tiara crown SVG, glitter ballroom invitation frames.",
            "images": "Quinceañera in dramatic princess ballgown on grand staircase, sweet 16 birthday celebration.",
            "videos": "Slow motion princess ballgown dress spin on ballroom dance floor 4K.",
            "templates": "Mis Quince Años luxury invitation suite Canva, Sweet Sixteen birthday party ticket flyer PSD."
        },
        "suggested_titles": [
            "Mis Quince Anos Luxury Princess Tiara Gold Foil Invitation Template Canva",
            "Sweet 16 Glamorous Birthday Nightclub Party Ticket Invitation Flyer PSD"
        ]
    },
    {
        "month": 6, "day": 20,
        "name": "Father's Day & Outdoor BBQ Season",
        "category": "Holidays & Cultural",
        "impact_score": 96,
        "stars": 5,
        "lead_time_days": 50,
        "what_to_create": {
            "vectors": "Best Dad Ever vintage retro badge, BBQ smoker grill utensils, fishing silhouette cut file.",
            "images": "Father teaching his young son how to fish at calm lake morning, backyard BBQ family feast.",
            "videos": "Steaks sizzling on hot charcoal grill in slow motion 4K.",
            "templates": "Father's Day restaurant steak dinner menu PSD, printable dad greeting card Canva."
        },
        "suggested_titles": [
            "Best Dad Ever Vintage Retro Badge SVG Cut File for T-Shirt",
            "Father and Son Fishing Together at Calm Lake Sunrise Photography",
            "Father's Day Special Backyard BBQ Steakhouse Menu Flyer Template PSD"
        ]
    },
    {
        "month": 6, "day": 30,
        "name": "Retirement Milestones & Golden Years",
        "category": "Birthdays & Milestones",
        "impact_score": 89,
        "stars": 4,
        "lead_time_days": 40,
        "what_to_create": {
            "vectors": "The Legend Has Retired funny vector badges, golf cart & palm trees clipart, goodbye tension hello pension lettering.",
            "images": "Happy senior retired couple cycling near beach at sunset, relaxed coffee on patio.",
            "videos": "Senior couple walking along beach holding hands sunset slow-mo 4K.",
            "templates": "Retirement farewell party invitation Canva, office memory book album template."
        },
        "suggested_titles": [
            "The Legend Has Retired Funny SVG Cut File for T-Shirt and Mug",
            "Happy Retirement Celebration Farewell Party Invitation Template Canva"
        ]
    },

    # =========================================================================
    # Q3: JULY, AUGUST, SEPTEMBER
    # =========================================================================
    {
        "month": 7, "day": 4,
        "name": "4th of July & USA Independence Day",
        "category": "Holidays & Cultural",
        "impact_score": 97,
        "stars": 5,
        "lead_time_days": 50,
        "what_to_create": {
            "vectors": "American flag red white and blue eagle, vintage 1776 patriotic badges, fireworks SVG.",
            "images": "Spectacular 4th of July fireworks reflecting in city lake, backyard patriotic family BBQ.",
            "videos": "Massive colorful fireworks explosion in night sky 4K 60fps.",
            "templates": "4th of July community festival flyer Canva, American independence party poster PSD."
        },
        "suggested_titles": [
            "4th of July American Independence Day Patriotic Eagle Vector Graphic",
            "Spectacular Fireworks Explosion Over City Skyline 4K Stock Video",
            "4th of July Community Celebration and BBQ Cookout Flyer Template Canva"
        ]
    },
    {
        "month": 7, "day": 15,
        "name": "Amazon Prime Day & Midsummer E-Commerce Rush",
        "category": "E-Commerce & Retail",
        "impact_score": 92,
        "stars": 4,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Mega midsummer sale badges, 3D retail package delivery icons, discount coupons.",
            "images": "Cardboard packages with yellow delivery tape on doorstep, mobile phone online shopping hand flatlay.",
            "videos": "E-commerce automated warehouse conveyor belt with moving packages 4K.",
            "templates": "Midsummer flash sale banner pack Canva, Shopify promotional slider graphic."
        },
        "suggested_titles": [
            "Midsummer Mega Flash Sale 3D Discount Badge and Ribbon Vector",
            "E-Commerce Mobile Shopping and Package Delivery Promo Banner Canva"
        ]
    },
    {
        "month": 8, "day": 15,
        "name": "Back to School & Teacher Prep Season",
        "category": "Corporate & Tech",
        "impact_score": 97,
        "stars": 5,
        "lead_time_days": 55,
        "what_to_create": {
            "vectors": "School bus vector, colorful school supplies icons (backpack, ruler, pencil, apple), Teacher SVG.",
            "images": "Smiling diverse students in modern classroom raising hands, colorful desk with books and laptop.",
            "videos": "Slow motion yellow school bus driving on autumn road 4K.",
            "templates": "Classroom newsletter Canva, first day of school printable sign, lesson plan binder PDF."
        },
        "suggested_titles": [
            "Back to School Supplies Isometric Vector Clipart Set Isolated",
            "First Day of School Editable Photo Sign Template Printable Canva",
            "Modern Classroom Students Learning and Raising Hands Photography"
        ]
    },
    {
        "month": 9, "day": 15,
        "name": "Oktoberfest Beer Festival Season",
        "category": "Holidays & Cultural",
        "impact_score": 91,
        "stars": 4,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Bavarian pretzel vector, beer steins clinking, blue-white Bavarian diamond pattern.",
            "images": "Traditional Oktoberfest beer garden celebration with wooden tables and pretzels.",
            "videos": "Golden beer pouring into glass stein with thick white foam 4K slow motion.",
            "templates": "Oktoberfest beer festival event flyer PSD, Bavarian restaurant food menu Canva."
        },
        "suggested_titles": [
            "Oktoberfest Bavarian Beer Festival Stein and Pretzel Vector Logo",
            "Oktoberfest Celebration Beer Garden Party Event Flyer Template PSD"
        ]
    },
    {
        "month": 4, "day": 15,
        "name": "Music Festival Fashion & Coachella Boho Chic Drop",
        "category": "Fashion & Apparel",
        "impact_score": 93,
        "stars": 5,
        "lead_time_days": 50,
        "what_to_create": {
            "vectors": "Boho celestial sun icons, retro 70s psychedelic festival flowers, crochet texture line art.",
            "images": "Music festival attendee with face glitter in golden hour desert sunset, bohemian crochet outfit.",
            "videos": "Slow motion festival concert crowd dancing with sparkling confetti in lights 4K.",
            "templates": "Music festival event lineup poster Canva, boho fashion boutique Instagram story PSD."
        },
        "suggested_titles": [
            "Bohemian Music Festival Coachella Style Fashion Model Sunset Photography",
            "Retro Groovy 70s Music Festival Lineup Poster Template Editable Canva",
            "Festival Glitter Makeup and Boho Chic Summer Outfit Aesthetic 4K Stock Image"
        ]
    },
    {
        "month": 6, "day": 1,
        "name": "Summer Resort Wear, Swimwear & Vacation Lookbooks",
        "category": "Fashion & Apparel",
        "impact_score": 94,
        "stars": 5,
        "lead_time_days": 60,
        "what_to_create": {
            "vectors": "Tropical monstera leaf seamless patterns, luxury resort hotel logos, sunglasses vector clipart.",
            "images": "High-fashion model in luxury linen resort wear on Mediterranean yacht, sunhat poolside flatlay.",
            "videos": "Turquoise ocean waves gently lapping white sand beach 4K, silk summer dress fluttering in sea breeze.",
            "templates": "Summer swimwear lookbook catalogue InDesign, luxury resort vacation travel guide brochure Canva."
        },
        "suggested_titles": [
            "Luxury Summer Resort Wear Linen Fashion Model on Yacht Deck 4K Stock Visual",
            "Tropical Swimwear and Beach Vacation Lookbook Catalogue Template Canva",
            "Turquoise Ocean Beach Waves and White Sand Resort Vacation 4K Video Loop"
        ]
    },
    {
        "month": 5, "day": 15,
        "name": "Kids & Toddler Birthday Themes (Wild One, Two Groovy, Roar)",
        "category": "Birthdays & Milestones",
        "impact_score": 95,
        "stars": 5,
        "lead_time_days": 45,
        "what_to_create": {
            "vectors": "Safari watercolor baby animals, Wild One safari typography, Two Groovy daisy flower SVG cut files.",
            "images": "First birthday cake smash setup with pastel balloon arch and wooden highchair, joyful celebration.",
            "videos": "Toddler blowing first birthday candle slow motion 4K with sparkles.",
            "templates": "Wild One 1st birthday invitation Canva, editable birthday milestone poster board, party favor tags."
        },
        "suggested_titles": [
            "Wild One Safari Animal First Birthday Invitation Suite Template Canva",
            "Two Groovy Daisy Retro Toddler Second Birthday SVG Cut File for Cricut",
            "First Birthday Cake Smash Setup with Balloon Arch and Highchair 4K Image"
        ]
    },
    {
        "month": 7, "day": 10,
        "name": "Sweet 16 & Quinceañera Regal Celebrations",
        "category": "Birthdays & Milestones",
        "impact_score": 92,
        "stars": 4,
        "lead_time_days": 55,
        "what_to_create": {
            "vectors": "Royal princess tiara crown vectors, Mis Quince ornate flourish calligraphy, glitter floral borders.",
            "images": "Glamorous sweet sixteen debutante in ballroom gown on marble staircase, luxury chandeliers.",
            "videos": "Sparkling crystal chandelier and ballroom dance party slow motion 4K.",
            "templates": "Quinceañera royal court program Canva, Sweet 16 VIP ticket invitation PSD."
        },
        "suggested_titles": [
            "Sweet 16 VIP Pass Event Ticket Invitation Card Template Printable Canva",
            "Mis Quince Anos Royal Princess Tiara and Rose Gold Floral Vector Graphic",
            "Luxury Sweet Sixteen Ballroom Birthday Celebration Gown Photography"
        ]
    },
    {
        "month": 4, "day": 20,
        "name": "Bridal Showers & Bachelorette Party Weekend Decor",
        "category": "Birthdays & Milestones",
        "impact_score": 96,
        "stars": 5,
        "lead_time_days": 50,
        "what_to_create": {
            "vectors": "Last Toast on the Coast champagne vectors, Bride to Be typography, bridal sunglasses SVG.",
            "images": "Chic poolside bachelorette party with pink flamingo floats and matching bride crew hats.",
            "videos": "Champagne flutes clinking at bridal brunch celebration slow motion 4K.",
            "templates": "Bachelorette party weekend itinerary Canva, bridal shower games printable bundle PDF."
        },
        "suggested_titles": [
            "Last Toast on the Coast Bachelorette Party Itinerary Template Editable Canva",
            "Bride to Be Retro Groovy Bridal Shower SVG Cut File Bundle for Cricut",
            "Chic Poolside Bachelorette Party Weekend Celebration Flatlay 4K Visual"
        ]
    }
]

def _next_date(now: datetime, month: int, day: int) -> datetime:
    """Returns the next upcoming date for a given month and day."""
    try:
        candidate = datetime(now.year, month, day)
    except ValueError:
        candidate = datetime(now.year, month, 28)

    # If the date has passed this year by more than 2 days, roll to next year
    if candidate < now - timedelta(days=2):
        try:
            candidate = datetime(now.year + 1, month, day)
        except ValueError:
            candidate = datetime(now.year + 1, month, 28)
    return candidate

def get_upcoming_ranked_events(days_ahead: int = 365, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Scans all master calendar events, computing exact golden upload ranges,
    submission deadlines, lateness flags, and urgency tiers.
    """
    now = datetime.now()
    results = []

    for ev in MASTER_CALENDAR_EVENTS:
        if category and category.lower() != 'all':
            if category.lower() not in ev["category"].lower():
                continue

        target_date = _next_date(now, ev["month"], ev["day"])
        lead_days = ev.get("lead_time_days", 50)

        # Golden upload window: 45 to 90 days before event
        golden_upload_deadline = target_date - timedelta(days=lead_days)
        golden_upload_start = target_date - timedelta(days=lead_days + 45)

        days_until_event = (target_date - now).days
        days_until_deadline = (golden_upload_deadline - now).days
        is_late = now > golden_upload_deadline

        # Compute status and badges
        if is_late:
            days_past = (now - golden_upload_deadline).days
            timing_status = "LATE"
            if days_until_event <= 10:
                status_badge = f"🔴 LATE (Only {days_until_event}d to Event — Final Clearance)"
                urgency_level = "Critical Rush"
            else:
                status_badge = f"🔴 LATE ({days_past}d Past Golden Deadline — Upload ASAP)"
                urgency_level = "Late Window"
            badge_color = "rose"
            action_advice = f"Past optimal {lead_days}-day indexing window. Upload immediately for last-minute buyers (Event is in {days_until_event} days)."
        elif days_until_deadline <= 14:
            timing_status = "CLOSING_SOON"
            status_badge = f"🟡 CLOSING SOON (Golden Window Ends in {days_until_deadline}d)"
            urgency_level = "Urgent Final Call"
            badge_color = "amber"
            action_advice = f"Upload before {golden_upload_deadline.strftime('%b %d')} to index before buyer purchase surges."
        elif golden_upload_start <= now <= golden_upload_deadline:
            timing_status = "PRIME_WINDOW"
            status_badge = f"🟢 PRIME UPLOAD WINDOW (Optimal Rank — Due in {days_until_deadline}d)"
            urgency_level = "Max Priority"
            badge_color = "emerald"
            action_advice = f"In optimal {lead_days}-day production window! Assets uploaded now achieve maximum organic search rank."
        else:
            days_until_start = (golden_upload_start - now).days
            timing_status = "ADVANCE_PREP"
            status_badge = f"🟣 ADVANCE PRODUCTION (Window Opens in {days_until_start}d)"
            urgency_level = "Recommended"
            badge_color = "indigo"
            action_advice = f"Advance planning phase. Upload window formally opens on {golden_upload_start.strftime('%b %d')}."

        if days_until_event <= days_ahead:
            results.append({
                "name": ev["name"],
                "category": ev["category"],
                "target_date_str": target_date.strftime("%B %d, %Y"),
                "target_date_short": target_date.strftime("%b %d"),
                "days_until": days_until_event,
                "golden_upload_start": golden_upload_start.strftime("%b %d, %Y"),
                "golden_upload_deadline": golden_upload_deadline.strftime("%B %d, %Y"),
                "upload_date_range": f"{golden_upload_start.strftime('%b %d')} – {golden_upload_deadline.strftime('%b %d, %Y')}",
                "is_late": is_late,
                "days_past_deadline": (now - golden_upload_deadline).days if is_late else 0,
                "days_until_deadline": days_until_deadline,
                "timing_status": timing_status,
                "timing_badge": status_badge,
                "status": status_badge,
                "urgency_level": urgency_level,
                "badge_color": badge_color,
                "action_advice": action_advice,
                "impact_score": ev["impact_score"],
                "stars": ev["stars"],
                "what_to_create": ev["what_to_create"],
                "suggested_titles": ev["suggested_titles"]
            })

    # Sort primarily by deadline proximity (events whose deadline is closest or recently passed)
    results = sorted(results, key=lambda x: (x["days_until_deadline"] < 0, abs(x["days_until_deadline"]), -x["impact_score"]))
    return results
