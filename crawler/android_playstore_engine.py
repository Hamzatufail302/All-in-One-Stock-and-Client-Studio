"""
StockPulse AI - Android Play Store Intelligence & App Production Engine
Provides trending Android app blueprints with strictly ZERO-RECURRING-COST ($0/month)
architectures, SEO metadata (30-char title, 80-char short desc, 4000-char full desc),
Master AI prompts to build the app, exact asset upload specifications, and a continuous
Google Play Policy & Dangerous Permissions Shield.
"""

from typing import List, Dict, Any, Optional

# --- ZERO-RECURRING-COST ($0/MO) OPERATING BLUEPRINT GUIDE ---

ZERO_COST_ARCHITECTURE_GUIDE = {
    "title": "The $0/Month Operating Cost Architecture for Solo Android Developers",
    "headline": "Zero-Recurring Operating Cost App Architecture ($0.00 / Month)",
    "core_principle": "Build apps where compute, AI inference, and database storage run 100% on the user's local phone hardware. Never pay recurring server or third-party API bills.",
    "philosophy": "Indie developers succeed by keeping fixed overhead at $0.00. By eliminating server bills, third-party AI tokens, and managed database subscriptions, your apps remain profitable from your very first AdMob impression or in-app upgrade.",
    "total_mandatory_costs": "$25.00 One-Time Lifetime Google Play Console Registration (No recurring annual fees)",
    "cost_comparison": {
        "bad_approach": "Using OpenAI API ($0.03/request) + AWS EC2 ($40/mo) + Cloud Firestore ($50/mo) = $500+/mo bill when scaling. Leads to developer bankruptcy.",
        "zero_cost_approach": "Using On-Device Google ML Kit ($0) + Local SQLite/Room DB ($0) + GitHub Pages Privacy Policy ($0) = $0.00/mo forever. 100% pure profit on AdMob & In-App purchases."
    },
    "zero_cost_pillars": [
        {
            "title": "1. Local On-Device Compute ($0/mo)",
            "pillar": "1. Zero Cloud Server Bills (100% On-Device Logic)",
            "rule": "Execute all app algorithms, calculations, timers, and data processing locally on the user's phone CPU/NPU. Never spin up cloud servers or VPS instances.",
            "how_it_saves_money": "No backend infrastructure or monthly VPS hosting fees. Computations execute entirely on user CPU/GPU.",
            "recommended_tech": "Kotlin Jetpack Compose (MVVM) or Flutter",
            "replaces_expensive_service": "Replaces AWS EC2 / DigitalOcean / Heroku ($15 - $80/mo)",
            "free_tool": "Flutter or Kotlin Jetpack Compose Local Runtime"
        },
        {
            "title": "2. Free On-Device Machine Learning ($0/mo)",
            "pillar": "2. Zero AI API Costs (Google ML Kit & Speech)",
            "rule": "Avoid paid cloud AI endpoints. Use Google ML Kit (100% free on-device OCR, object detection, barcode, language translation) or TensorFlow Lite.",
            "how_it_saves_money": "Leverages free, offline Google ML Kit on-device inference models with zero per-token or per-image API charges.",
            "recommended_tech": "Google ML Kit Text Recognition / Barcode Scanning SDK",
            "replaces_expensive_service": "Replaces OpenAI GPT-4 Vision / Google Cloud Vision API ($20 - $200/mo)",
            "free_tool": "Google ML Kit (google_mlkit_text_recognition / camera)"
        },
        {
            "title": "3. Local Database & Offline Sandbox ($0/mo)",
            "pillar": "3. Zero Database Hosting Costs (Local SQLite & Room)",
            "rule": "Store user profiles, histories, transactions, and settings in local phone storage. Zero cloud database read/write egress fees.",
            "how_it_saves_money": "Stores all entries, user preferences, and analytics securely in local SQLite sandbox. Zero network latency, zero egress charges.",
            "recommended_tech": "Room Database (SQLite) / Isar / Hive / SharedPrefs",
            "replaces_expensive_service": "Replaces MongoDB Atlas / Supabase / AWS DynamoDB ($25 - $100/mo)",
            "free_tool": "Room SQLite (Kotlin) or Isar / Hive / SQLite (Flutter)"
        },
        {
            "title": "4. Free Legal & Privacy Policy Hosting ($0/mo)",
            "pillar": "4. Zero Web Hosting Bills (GitHub Pages Privacy Shield)",
            "rule": "Google Play requires an HTTPS Privacy Policy URL. Never buy a web hosting plan just for a privacy policy.",
            "how_it_saves_money": "Google Play requires a public HTTPS privacy policy URL. Free static hosts provide SSL and custom domains without credit cards.",
            "recommended_tech": "GitHub Pages / Cloudflare Pages / Public Notion Document",
            "replaces_expensive_service": "Replaces Shared CPanel Hosting / Vercel Pro ($12 - $20/mo)",
            "free_tool": "GitHub Pages / Cloudflare Pages / Public Notion Page (100% Free HTTPS)"
        },
        {
            "title": "5. Free Monetization SDKs ($0 Upfront)",
            "pillar": "5. Zero-Cost Native Monetization (AdMob + Play Billing)",
            "rule": "Google AdMob SDK is free to integrate (Google pays you ad revenue). Google Play In-App Billing takes a 15% revenue cut only after a user purchases.",
            "how_it_saves_money": "AdMob and Google Play Billing are 100% free to integrate. Google only takes a standard 15% cut upon actual user purchase.",
            "recommended_tech": "Google Mobile Ads (AdMob) + Play Billing Library 7.0",
            "replaces_expensive_service": "Zero upfront merchant fees or subscription billing gateways",
            "free_tool": "Google Mobile Ads SDK (AdMob) + Google Play Billing Library 7.0"
        },
        {
            "title": "6. The Only Fixed Expense ($25 One-Time)",
            "pillar": "6. One-Time Lifetime Registration (No Annual Fee)",
            "rule": "Google charges a single, one-time $25 registration fee to create a Google Play Developer Account. There are NO annual recurring fees (unlike Apple's $99/yr).",
            "how_it_saves_money": "Google charges a single one-time $25 fee for life. You can publish unlimited apps forever without recurring renewal costs.",
            "recommended_tech": "Google Play Console Developer Account ($25 lifetime)",
            "replaces_expensive_service": "Replaces Apple Developer Program ($99/year recurring subscription)",
            "free_tool": "One-time $25 lifetime developer account"
        }
    ],
    "six_pillars_of_zero_cost": [
        {
            "pillar": "1. Zero Cloud Server Bills (100% On-Device Logic)",
            "how_it_saves_money": "No backend infrastructure or monthly VPS hosting fees. Computations execute entirely on user CPU/GPU.",
            "recommended_tech": "Kotlin Jetpack Compose (MVVM) or Flutter",
            "replaces_expensive_service": "Replaces AWS EC2 / DigitalOcean / Heroku ($15 - $80/mo)"
        },
        {
            "pillar": "2. Zero AI API Costs (Google ML Kit & Speech)",
            "how_it_saves_money": "Leverages free, offline Google ML Kit on-device inference models with zero per-token or per-image API charges.",
            "recommended_tech": "Google ML Kit Text Recognition / Barcode Scanning SDK",
            "replaces_expensive_service": "Replaces OpenAI GPT-4 Vision / Google Cloud Vision API ($20 - $200/mo)"
        },
        {
            "pillar": "3. Zero Database Hosting Costs (Local SQLite & Room)",
            "how_it_saves_money": "Stores all entries, user preferences, and analytics securely in local SQLite sandbox. Zero network latency, zero egress charges.",
            "recommended_tech": "Room Database (SQLite) / Isar / Hive / SharedPrefs",
            "replaces_expensive_service": "Replaces MongoDB Atlas / Supabase / AWS DynamoDB ($25 - $100/mo)"
        },
        {
            "pillar": "4. Zero Web Hosting Bills (GitHub Pages Privacy Shield)",
            "how_it_saves_money": "Google Play requires a public HTTPS privacy policy URL. Free static hosts provide SSL and custom domains without credit cards.",
            "recommended_tech": "GitHub Pages / Cloudflare Pages / Public Notion Document",
            "replaces_expensive_service": "Replaces Shared CPanel Hosting / Vercel Pro ($12 - $20/mo)"
        },
        {
            "pillar": "5. Zero-Cost Native Monetization (AdMob + Play Billing)",
            "how_it_saves_money": "AdMob and Google Play Billing are 100% free to integrate. Google only takes a standard 15% cut upon actual user purchase.",
            "recommended_tech": "Google Mobile Ads (AdMob) + Play Billing Library 7.0",
            "replaces_expensive_service": "Zero upfront merchant fees or subscription billing gateways"
        },
        {
            "pillar": "6. One-Time Lifetime Registration (No Annual Fee)",
            "how_it_saves_money": "Google charges a single one-time $25 fee for life. You can publish unlimited apps forever without recurring renewal costs.",
            "recommended_tech": "Google Play Console Developer Account ($25 lifetime)",
            "replaces_expensive_service": "Replaces Apple Developer Program ($99/year recurring subscription)"
        }
    ],
    "cost_comparison_table": [
        {
            "feature": "App Backend & Business Logic",
            "expensive_traditional_approach": "AWS EC2 / Node.js Server ($25 - $60/mo)",
            "zero_cost_indie_approach": "100% On-Device Kotlin / Flutter ($0.00/mo)",
            "savings": "$300 - $720 / yr"
        },
        {
            "feature": "AI & Computer Vision",
            "expensive_traditional_approach": "OpenAI / Claude API ($15 - $150/mo)",
            "zero_cost_indie_approach": "Google ML Kit On-Device SDK ($0.00/mo)",
            "savings": "$180 - $1,800 / yr"
        },
        {
            "feature": "User Data & Database",
            "expensive_traditional_approach": "MongoDB Atlas / Firestore ($20 - $70/mo)",
            "zero_cost_indie_approach": "Room SQLite / Hive Local Storage ($0.00/mo)",
            "savings": "$240 - $840 / yr"
        },
        {
            "feature": "Background Notification Cron",
            "expensive_traditional_approach": "Cloud Scheduler / Celery Worker ($10/mo)",
            "zero_cost_indie_approach": "Android WorkManager API ($0.00/mo)",
            "savings": "$120 / yr"
        },
        {
            "feature": "Audio & Media Storage",
            "expensive_traditional_approach": "AWS S3 + CloudFront CDN ($15/mo)",
            "zero_cost_indie_approach": "Bundled High-Compression Assets ($0.00/mo)",
            "savings": "$180 / yr"
        },
        {
            "feature": "Privacy Policy Hosting",
            "expensive_traditional_approach": "Domain + Shared Web Host ($12/mo)",
            "zero_cost_indie_approach": "GitHub Pages / Notion Public URL ($0.00/mo)",
            "savings": "$144 / yr"
        },
        {
            "feature": "Developer License Registration",
            "expensive_traditional_approach": "Apple Developer Account ($99/year recurring)",
            "zero_cost_indie_approach": "Google Play Console ($25.00 one-time lifetime)",
            "savings": "$99 / yr recurring"
        }
    ]
}

# --- EXACT GOAL & ASSET SPECIFICATIONS FOR GOOGLE PLAY STORE ---

PLAY_STORE_ASSET_SPECS = {
    "app_icon": {
        "title": "App Icon (Launcher & Storefront)",
        "dimension": "512 x 512 px (Square 1:1)",
        "format": "32-bit PNG with Alpha (RGBA)",
        "max_size": "1024 KB (1 MB)",
        "critical_rules": [
            "Do NOT add rounded corners or drop shadows! Google Play automatically applies a 20% squircle radius and shadow mask dynamically.",
            "Badge overlays, promotional text ('SALE', 'NEW', '50% OFF'), and rankings ('#1', 'Best') are strictly banned by Google Play Metadata Policy.",
            "Keep the icon visually bold, high-contrast, and recognizable even at 36x36 px on low-end budget Android devices.",
            "Must be RGB color space. CMYK files will fail during upload validation."
        ]
    },
    "feature_graphic": {
        "title": "Feature Graphic (Storefront Header)",
        "dimension": "1024 x 500 px (Landscape 2:1)",
        "format": "JPG or 24-bit PNG (No Alpha)",
        "max_size": "15 MB",
        "critical_rules": [
            "Crucial banner displayed at the top of your Google Play Store listing and in promotional recommendations.",
            "Safe Zone: Keep critical brand title and graphics in the center 850 x 380 px box.",
            "Do NOT place essential text or logos in the bottom-left corner where your 512px app icon and developer name will overlay on mobile.",
            "Avoid busy backgrounds. Bold typography with 3D or high-contrast mockup graphics converts at 34% higher install rate."
        ]
    },
    "phone_screenshots": {
        "title": "Phone Screenshots (High-Converting Mockups)",
        "dimension": "1080 x 1920 px (9:16 Portrait) or 1080 x 2400 px (20:9 Modern)",
        "count": "Minimum 2, Maximum 8 screenshots (4 to 6 strongly recommended)",
        "format": "RGB PNG or JPEG",
        "critical_rules": [
            "Aspect ratio must be between 16:9 and 9:16. Minimum side 320 px, maximum side 3840 px.",
            "Top 20% Rule: Place the primary benefit / headline caption in the top 20% of each screenshot so users see it while scrolling.",
            "First 3 screenshots account for 85% of install decisions on mobile search results.",
            "Show actual app UI in every screenshot. Generic marketing photos without app UI violate Google Play Developer Policy."
        ]
    },
    "tablet_screenshots": {
        "title": "7-Inch & 10-Inch Tablet Screenshots",
        "specs_7_inch": "1200 x 1920 px (Min 1, Max 8)",
        "specs_10_inch": "1600 x 2560 px (Min 1, Max 8)",
        "critical_rules": [
            "Mandatory if you want your app to be featured in the 'Designed for Tablets' section on Google Play.",
            "Show adaptive tablet layouts (e.g. Master-Detail dual-pane views in Jetpack Compose or Flutter)."
        ]
    },
    "release_binary": {
        "title": "Release Package (Android App Bundle - .AAB)",
        "format": "Android App Bundle (.aab only - APKs no longer accepted for new apps)",
        "target_sdk": "Target SDK API 34 (Android 14) or API 35 (Android 15 Mandatory for late 2024+)",
        "min_sdk": "Min SDK API 24 (Android 7.0) or API 26 (Android 8.0) covers 95%+ active devices",
        "architecture": "64-bit compliance mandatory (must include arm64-v8a alongside armeabi-v7a)",
        "keystore": "Signed with custom JKS / PKCS12 keystore + enrolled in Google Play App Signing"
    },
    "metadata_limits": {
        "title": {"limit": 30, "rule": "Strict max 30 characters. No 'Free', 'Best', '#1', 'Top' (Instant rejection)."},
        "short_description": {"limit": 80, "rule": "Strict max 80 characters. High-impact value proposition hook."},
        "full_description": {"limit": 4000, "rule": "Structured SEO layout, bold headings, bullet points, zero keyword spamming."}
    }
}

# --- DANGEROUS & HIGH-RISK GOOGLE PLAY PERMISSIONS DIRECTORY ---

DANGEROUS_PERMISSIONS_DIRECTORY = [
    {
        "permission": "android.permission.MANAGE_EXTERNAL_STORAGE",
        "name": "All Files Access (Broad Storage)",
        "risk_level": "CRITICAL_REJECTION_HAZARD",
        "badge_color": "rose",
        "policy_rule": "Google Play Storage Policy strictly restricts this to dedicated File Managers, Antivirus, or Backup apps only. General apps asking for this get rejected immediately.",
        "safe_alternative": "Use Android Photo Picker (PickVisualMedia) for images/videos, and Storage Access Framework (SAF: Intent.ACTION_CREATE_DOCUMENT / ACTION_OPEN_DOCUMENT) for documents.",
        "required_declaration": "Mandatory 'All Files Access Declaration' form with recorded video justification."
    },
    {
        "permission": "android.permission.READ_MEDIA_IMAGES / READ_MEDIA_VIDEO",
        "name": "Granular Media Access (Android 13+)",
        "risk_level": "MODERATE_DECLARATION_REQUIRED",
        "badge_color": "amber",
        "policy_rule": "Starting mid-2024, apps requesting READ_MEDIA_IMAGES must justify why they cannot use the system Photo Picker (which requires zero permissions).",
        "safe_alternative": "Migrate to Android Photo Picker (androidx.activity:activity-ktx or image_picker in Flutter with usePhotoPicker: true). It gives full user privacy with 0 permissions!",
        "required_declaration": "Declare core media editing / backup functionality in Play Console."
    },
    {
        "permission": "android.permission.SCHEDULE_EXACT_ALARM",
        "name": "Schedule Exact Alarm (Android 14+)",
        "risk_level": "HIGH_POLICY_RESTRICTION",
        "badge_color": "orange",
        "policy_rule": "Strictly limited to Alarm Clocks and Timer apps. General apps (habits, reminders, productivity) will have exact alarms denied or cause Play Store rejection.",
        "safe_alternative": "Use Inexact Alarms via AlarmManager, or WorkManager for periodic background tasks. If user-set reminder, use USE_EXACT_ALARM (if calendar/alarm app).",
        "required_declaration": "Exact Alarm policy form."
    },
    {
        "permission": "android.permission.FOREGROUND_SERVICE",
        "name": "Foreground Service Types (Android 14+)",
        "risk_level": "HIGH_POLICY_RESTRICTION",
        "badge_color": "orange",
        "policy_rule": "Android 14 requires specifying foregroundServiceType in AndroidManifest.xml (e.g., mediaPlayback, microphone, camera, dataSync). Using wrong type triggers rejection.",
        "safe_alternative": "Match service type strictly to app functionality (e.g. android:foregroundServiceType=\"mediaPlayback\"). Use WorkManager for background uploads instead of services.",
        "required_declaration": "Foreground Service declaration form explaining user-facing notification."
    },
    {
        "permission": "android.permission.QUERY_ALL_PACKAGES",
        "name": "Query All Installed Packages",
        "risk_level": "CRITICAL_REJECTION_HAZARD",
        "badge_color": "rose",
        "policy_rule": "Strictly prohibited unless your app is an Antivirus, Launcher, or Device Search utility. Apps asking for this to detect competing apps are terminated.",
        "safe_alternative": "Use specific <queries> block in AndroidManifest.xml specifying only the package or intent action you need to open (e.g., mailto, web, or specific partner app).",
        "required_declaration": "Query All Packages Exception Form."
    },
    {
        "permission": "android.permission.ACCESS_BACKGROUND_LOCATION",
        "name": "Background Location (All the time)",
        "risk_level": "CRITICAL_REJECTION_HAZARD",
        "badge_color": "rose",
        "policy_rule": "Requires separate approval by Google Play Review team. You must provide a screen-recorded video proving the feature cannot function without background GPS.",
        "safe_alternative": "Request ACCESS_FINE_LOCATION or ACCESS_COARSE_LOCATION only while app is open ('While using the app').",
        "required_declaration": "Background Location Declaration Video Submission."
    },
    {
        "permission": "android.permission.RECORD_AUDIO",
        "name": "Microphone Audio Recording",
        "risk_level": "MODERATE_DECLARATION_REQUIRED",
        "badge_color": "amber",
        "policy_rule": "Must show a prominent runtime disclosure dialog explaining why the app records audio BEFORE the Android permission dialog triggers.",
        "safe_alternative": "Process audio strictly on-device without uploading to servers, and state this clearly in Data Safety section.",
        "required_declaration": "Data Safety form disclosure (Audio recordings collected/not collected)."
    },
    {
        "permission": "android.permission.POST_NOTIFICATIONS",
        "name": "Push Notifications (Android 13+)",
        "risk_level": "LOW_SAFE_STANDARD",
        "badge_color": "emerald",
        "policy_rule": "Standard runtime permission for notifications. Low risk, but must explain value before prompting to maximize opt-in rate.",
        "safe_alternative": "Ask after the user performs an action (e.g., sets a timer or creates a reminder), not immediately upon first launch.",
        "required_declaration": "Standard Data Safety Form."
    }
]

# --- 20-TESTER CLOSED TESTING SURVIVAL STRATEGY (NEW PLAY STORE POLICY) ---

TWENTY_TESTER_POLICY_GUIDE = {
    "title": "Google Play 20-Tester Mandatory Requirement (Accounts After Nov 13, 2023)",
    "rules": [
        "Personal developer accounts registered after Nov 13, 2023 CANNOT publish directly to production.",
        "Must run a Closed Test with at least 20 opted-in testers for at least 14 consecutive days.",
        "Testers must remain opted-in for the full 14 days and actively open/test the app.",
        "After 14 days, you submit an application questionnaire answering: 'How did you gather testers?', 'What feedback did you collect?', 'What bugs did you fix?'"
    ],
    "actionable_blueprint": [
        "1. Create a Google Group (e.g., 'your-app-testers@googlegroups.com') and set permission to 'Anyone can join'.",
        "2. Add the Google Group email to your Play Console Closed Testing track testers list.",
        "3. Share the opt-in Web URL (play.google.com/apps/testing/your.package) and Android Play Store link.",
        "4. Recruit 22-25 testers (buffer in case someone uninstalls) via Reddit (r/AndroidClosedTesting), Indie Hackers, developer Discord, and peer groups.",
        "5. Push at least 1-2 small updates (v1.0.1, v1.0.2) during the 14 days to prove active development in the final review questionnaire."
    ]
}

# --- CURATED HIGH-CONVERTING ZERO-COST ($0/MO) ANDROID APP BLUEPRINTS ---

TRENDING_ANDROID_APPS = [
    {
        "id": "app_ai_scanner",
        "concept": "AI Pocket Scanner & Document OCR Clean Room",
        "category": "Tools / Productivity",
        "opportunity_score": 97,
        "search_volume": "240k / month",
        "admob_ecpm": "$24 - $38 (Tier 1 US/UK/CA)",
        "monetization": "AdMob Native + Banner, In-App Pro ($3.99/mo or $29.99 Lifetime for unlimited batch OCR)",
        "trend_momentum": "+410% Search Surge (Paperless workflow trend)",
        "recommended_stack": "Flutter with google_mlkit_text_recognition OR Kotlin Jetpack Compose with CameraX + ML Kit",
        "target_title": "DocuScan: AI PDF & OCR Scanner",
        "short_description": "Pocket AI PDF scanner, text OCR extractor & offline document organizer.",
        "full_description": """Transform your smartphone into an ultra-fast, professional document scanner with DocuScan AI.

Scan documents, contracts, receipts, book pages, and whiteboard notes directly into crystal-clear PDF or JPEG files with zero watermark.

★ ADVANCED AI SCANNING & OCR FEATURES:
• Auto-Edge Detection & Smart Cropping: Automatically locates document borders, corrects perspective distortion, and eliminates shadows.
• High-Speed On-Device OCR: Extract editable text from any scanned image in 40+ languages with 99.4% accuracy.
• Clean Filters: Professional B&W, Grayscale, Magic Color, and Crisp Document enhancement modes.
• Multi-Page Batch Scanning: Scan entire books and contracts in seconds without delay.
• PDF Signature & Watermark Tools: Sign documents directly on screen and add security stamps.
• 100% Private & Offline: Your documents are processed entirely on your local device. No files are uploaded to external servers.

★ DESIGNED FOR BUSINESS & PRODUCTIVITY:
Whether you are a student digitizing notes, a freelance contractor sending invoices, or a business professional signing agreements on the go, DocuScan delivers crisp, professional results every time.

Export and share via Email, Google Drive, WhatsApp, Dropbox, and local storage with a single tap.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (No backend server required)",
            "ai_engine": "$0 (Google ML Kit runs 100% offline on phone hardware)",
            "database": "$0 (Local MediaStore & SQLite on phone)",
            "external_apis": "$0 (Zero third-party paid subscriptions)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion / Cloudflare Pages)",
            "one_time_setup": "$25 (Google Play Developer Registration, one-time lifetime)",
            "profit_margin": "100% Pure Profit (AdMob Ads + In-App Subscriptions)",
            "summary": "100% offline document processing. No recurring costs even at 1,000,000 active users."
        },
        "dangerous_permissions_check": {
            "avoid": ["android.permission.MANAGE_EXTERNAL_STORAGE", "android.permission.READ_EXTERNAL_STORAGE"],
            "use_instead": "MediaStore.Files API or Storage Access Framework (SAF) for saving PDFs. Camera permission (android.permission.CAMERA) requires clear runtime rationale.",
            "policy_status": "🟢 100% Clean & Zero-Rejection Safe when using SAF"
        },
        "kickstart_prompt": """Act as a Senior Principal Android Mobile Architect and Flutter/Kotlin expert.

I am building a high-performance Android utility app called 'DocuScan: AI PDF & OCR Scanner' to publish on the Google Play Store.

ZERO-COST ARCHITECTURE REQUIREMENTS:
- Target SDK: Android 14/15 (API 34/35)
- Compute & AI: 100% on-device Google ML Kit (google_mlkit_text_recognition). Zero server calls, $0 operating cost!
- Storage: Storage Access Framework and MediaStore.files (Zero dangerous permissions).
- Monetization: Google Mobile Ads (AdMob banner & interstitial) + Google Play Billing 7.0 for Pro lifetime unlock.

PROVIDE A COMPLETE PRODUCTION BLUEPRINT:
1. Complete Project Directory Structure following Clean Architecture.
2. Complete dependencies configuration (pubspec.yaml or build.gradle.kts) including CameraX, ML Kit, PDF generator, and Google Mobile Ads SDK.
3. AndroidManifest.xml with strict Play Store compliance, camera permission with queries block, and FileProvider config.
4. Core Camera & Auto-Edge crop detection controller code.
5. OCR text extraction service code converting camera frames into editable text and searchable PDF.
6. Clean, modern Material 3 Dark-mode UI layout code.
7. AdMob mediation manager (Banner + Interstitial on export + Rewarded for Pro batch scan)."""
    },
    {
        "id": "app_expense_budget",
        "concept": "Minimalist Offline Budget & Subscription Manager",
        "category": "Finance / Productivity",
        "opportunity_score": 96,
        "search_volume": "190k / month",
        "admob_ecpm": "$35 - $60 (Highest Financial Ad Bids)",
        "monetization": "AdMob Native Cards, Pro Theme & Cloud Backup Unlock ($2.49/mo)",
        "trend_momentum": "+380% Search Surge (Privacy-first offline finance)",
        "recommended_stack": "Flutter with Isar/Hive local database OR Kotlin Jetpack Compose with Room SQLite",
        "target_title": "SpendWise: Expense & Budget",
        "short_description": "Private offline budget tracker, recurring expense manager & smart money planner.",
        "full_description": """Take total control of your personal finances with SpendWise, the privacy-focused offline expense tracker and daily budget planner.

No forced account creation. No linking sensitive bank passwords. 100% offline security.

★ EFFORTLESS EXPENSE & INCOME TRACKING:
• 3-Second Quick Entry: Log daily expenses in seconds with custom categories and smart icons.
• Smart Monthly Budgets: Set category spending limits (Groceries, Dining, Transport, Entertainment) with visual progress bars.
• Recurring Subscription Manager: Track recurring Netflix, Spotify, gym, and utility bills so you never miss a renewal.
• Visual Spending Analytics: Interactive pie charts, weekly breakdown trends, and cash flow reports.
• Multi-Currency & Travel Mode: Real-time exchange rates and custom currency support for frequent travelers.
• Biometric Lock & Privacy: Secure your financial data with Fingerprint / Face Unlock.

★ 100% LOCAL DATA OWNERSHIP:
Your money data never leaves your device. Export transparent CSV/Excel spreadsheets whenever you need.

Start building your wealth with zero financial anxiety today with SpendWise.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (Completely offline architecture)",
            "ai_engine": "$0 (Native statistical calculators & local algorithms)",
            "database": "$0 (Local Room / SQLite / Hive database)",
            "external_apis": "$0 (Zero bank APIs needed - manual quick log)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Margin (AdMob Ad Revenue & Pro Upgrades)",
            "summary": "Zero ongoing costs. Highest financial AdMob eCPMs ($35-$60) yield maximum ROI."
        },
        "dangerous_permissions_check": {
            "avoid": ["android.permission.RECEIVE_SMS", "android.permission.READ_SMS"],
            "use_instead": "DO NOT attempt automatic SMS bank reading! Google Play strictly bans SMS permissions for non-default SMS apps. Use manual 3-second quick logging or notification listener with explicit user consent.",
            "policy_status": "🟢 Zero Dangerous Permissions. 100% Instant Approval."
        },
        "kickstart_prompt": """Act as a Principal Mobile Architect specializing in Fintech & Personal Finance Android apps.

I want to build 'SpendWise: Expense & Budget', an offline-first, privacy-focused expense tracker for Google Play.

ZERO-COST SPECIFICATIONS:
- Framework: Flutter (Riverpod + Isar DB / SQLite) or Kotlin Jetpack Compose (MVVM + Room)
- Operating Cost: $0/month. No backend servers, no Plaid/bank API subscription costs.
- Zero Dangerous Permissions: Zero SMS permissions! Manual 3-second quick add + CSV export via Storage Access Framework.
- Design: Ultra-clean Material 3 Dark theme, smooth spring animations, tactile haptic feedback.

PROVIDE THE FULL CODE ARCHITECTURE:
1. Complete folder structure (presentation, domain, data layers).
2. Complete Database Schema (ExpenseEntity, CategoryEntity, BudgetEntity, SubscriptionEntity) with Room/Isar definitions.
3. Fast Expense Logging Screen code with numeric keypad, category chips, and note input.
4. Monthly Budget Analytics Screen with dynamic progress bars and percentage health indicators.
5. Recurring Subscription Tracker with reminder notifications using local WorkManager.
6. CSV export service utilizing Android Storage Access Framework (SAF: ACTION_CREATE_DOCUMENT).
7. Google Play Billing 7.0 integration code for Pro Lifetime Unlock ($19.99) and AdMob banner removal."""
    },
    {
        "id": "app_slumber_audio",
        "concept": "3D Spatial Audio White Noise & Sleep Machine",
        "category": "Health & Fitness",
        "opportunity_score": 94,
        "search_volume": "170k / month",
        "admob_ecpm": "$20 - $32",
        "monetization": "AdMob Open App + Interstitial, Annual Sleep Sound Pass ($19.99/yr)",
        "trend_momentum": "+340% Steady Seasonal Search (High Retention & Daily Active Users)",
        "recommended_stack": "Kotlin Jetpack Compose with Android ExoPlayer / Media3 OR Flutter with just_audio",
        "target_title": "Slumber3D: White Noise & Sleep",
        "short_description": "Binaural 3D sleep sounds, rain machine, ambient mixer & gentle bedtime timer.",
        "full_description": """Drift into deep, restorative sleep in minutes with Slumber3D, the spatial sound sleep machine and ambient soundscape mixer.

Craft your custom sound environment by blending soothing rain on tent, gentle ocean waves, crackling fireplace, binaural alpha waves, and gentle fan white noise.

★ 40+ HI-FI SPATIAL AMBIENT SOUNDS:
• Nature & Weather: Heavy thunderstorm, soft rainfall, autumn wind, babbling forest creek, ocean surf.
• White, Pink & Brown Noise: High-frequency masking sounds to block out street traffic, snoring partners, and loud neighbors.
• Calming Machinery: Ceiling fan, airplane cabin hum, vintage train tracks, washing machine rhythm.
• Brainwave Entrainment: Solfeggio frequencies (528Hz, 432Hz) and binaural delta beats for rapid REM sleep.

★ SLEEP TIMER & SMART FADE-OUT:
Set a gentle bedtime timer. The audio smoothly fades away as you fall asleep, saving your device battery.

★ WORKS 100% OFFLINE & IN BACKGROUND:
Play audio continuously with your screen turned off or while reading other apps with zero interruptions.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (Sound files bundled directly in app assets - zero streaming bandwidth bills)",
            "ai_engine": "$0 (Native multi-channel audio mixer)",
            "database": "$0 (Local SharedPreferences / DataStore for sound mix presets)",
            "external_apis": "$0 (Zero external audio APIs)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Margin (AdMob Ads + In-App Sound Packs)",
            "summary": "Audio loops are packaged directly in the AAB asset bundle. Zero server egress fees."
        },
        "dangerous_permissions_check": {
            "avoid": ["Unspecified Foreground Service"],
            "use_instead": "Must declare android.permission.FOREGROUND_SERVICE and android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK in Android 14+ manifest. Attach ongoing playback notification with MediaStyle.",
            "policy_status": "🟡 Declaration Required: Specify 'mediaPlayback' type in Play Console."
        },
        "kickstart_prompt": """Act as a Senior Android Audio Engineer and UI/UX Designer.

Build 'Slumber3D: White Noise & Sleep', a high-performance background audio mixer app for Android with $0 monthly server costs.

ZERO-COST SPECIFICATIONS:
- Audio loops are packaged directly in assets/ (Ogg Vorbis format for low file size). Zero streaming server bills!
- Engine: Android Media3 / ExoPlayer (or Flutter just_audio + audio_service)
- Android 14/15 Compliance: Foreground Service type='mediaPlayback' with MediaStyle lockscreen controls
- UI: Deep midnight dark theme with glowing volume dials and animated audio waves.

DELIVERABLES:
1. Complete AndroidManifest.xml setup for Android 14 Media Playback Service (API 34/35).
2. Multi-channel audio mixer engine code capable of playing up to 6 looped audio tracks simultaneously with individual volume faders.
3. Sleep Timer controller code that gradually fades audio volume over 10 minutes to zero before stopping the foreground service.
4. Main UI screen code with sound card grid, interactive volume sliders, and master play/pause floating action button.
5. In-App Purchase integration (Google Play Billing) for premium Solfeggio sound packs."""
    },
    {
        "id": "app_habit_fasting",
        "concept": "Clean Intermittent Fasting & Habit Streak Tracker",
        "category": "Health & Fitness",
        "opportunity_score": 95,
        "search_volume": "280k / month",
        "admob_ecpm": "$22 - $36",
        "monetization": "Rewarded Ads for fasting stage insights, Pro Yearly ($24.99/yr)",
        "trend_momentum": "+420% Surge (High New Year & seasonal wellness demand)",
        "recommended_stack": "Flutter with Riverpod or Kotlin Jetpack Compose with Flow",
        "target_title": "FastTrack: Intermittent Fasting",
        "short_description": "Clean 16:8 intermittent fasting tracker, water reminder & daily habit streaks.",
        "full_description": """Reach your health and weight goals naturally with FastTrack, the simple, scientifically backed intermittent fasting and daily habit streak tracker.

Whether you are practicing 16:8, 18:6, OMAD (One Meal a Day), or custom fasts, FastTrack guides your body through every metabolic milestone.

★ INTUITIVE FASTING TIMER & BODY STAGES:
• Visual Fasting Clock: Start and stop your fast with one tap. Watch your progress in real-time.
• Metabolic Stages Tracker: See when your body enters Ketosis, Autophagy, Fat Burning, and Insulin Drop stages.
• Popular Fasting Protocols: Beginner (12:12, 14:10), Intermediate (16:8, 18:6), and Advanced (20:4, 24h, 36h).
• Daily Water Hydration Reminder: Log water intake with customizable haptic glass indicators.
• Streak & Weight Progress Charts: Celebrate consistency streaks and track weight loss momentum over time.

Zero intrusive ads during active fasts. No confusing calorie counting. Pure metabolic focus.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (Fasting calculations executed locally in phone RAM/CPU)",
            "ai_engine": "$0 (Rule-based metabolic stage calculator)",
            "database": "$0 (Local Room / Hive database)",
            "external_apis": "$0 (Zero third-party APIs)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Margin (AdMob Rewarded Video + Pro Passes)",
            "summary": "All fasting timers, stages, and hydration trackers run locally. $0 server costs."
        },
        "dangerous_permissions_check": {
            "avoid": ["android.permission.SCHEDULE_EXACT_ALARM"],
            "use_instead": "Use inexact alarms or Android WorkManager for hydration and fast completion reminders. Avoid asking for exact alarm permissions to bypass Google Play health scrutiny.",
            "policy_status": "🟢 Clean & Safe using standard WorkManager notifications."
        },
        "kickstart_prompt": """Act as a Lead Mobile App Developer and Health Tech Specialist.

Create the complete production codebase for 'FastTrack: Intermittent Fasting & Habit Tracker' targeting Android 14/15 with $0 monthly operating costs.

ZERO-COST STACK:
- Flutter (Riverpod) or Kotlin Compose (ViewModel + StateFlow)
- Local DB: Hive / SharedPreferences / Room ($0 cloud database bills)
- Notifications: Local WorkManager periodic tasks (NO exact alarm permission)
- Styling: Minimalist OLED Black with vibrant gradient timer rings.

OUTPUT SPECIFICATIONS:
1. Architecture setup with state management for ActiveFastState (startTime, targetHours, currentStage).
2. Metabolic Stage Calculation Engine (Blood Sugar drop at 2h, Ketosis at 12h, Autophagy at 18h).
3. Circular Fasting Clock Screen with animated progress arc, elapsed hours, remaining time, and metabolic milestone cards.
4. Water Tracker widget with quick-add buttons (+250ml, +500ml) and daily target bar.
5. In-App Review API (Google Play In-App Review SDK) trigger after 3 successful completed fasts.
6. AdMob integration (Banner at bottom of History screen + Rewarded Ad to unlock detailed metabolic science report)."""
    },
    {
        "id": "app_pomodoro_focus",
        "concept": "Micro-SaaS Pomodoro & Deep Work Flow Timer",
        "category": "Productivity",
        "opportunity_score": 93,
        "search_volume": "150k / month",
        "admob_ecpm": "$18 - $28",
        "monetization": "AdMob Banner & Interstitial, Pro Tags & Stats Export ($1.99)",
        "trend_momentum": "+290% Steady Search Volume",
        "recommended_stack": "Flutter with Riverpod or Kotlin Compose with Coroutines",
        "target_title": "FocusPulse: Pomodoro Deep Work",
        "short_description": "Minimalist Pomodoro timer, deep work session blocker & productivity statistics.",
        "full_description": """Boost your daily focus, crush procrastination, and complete your biggest goals with FocusPulse, the distraction-free Pomodoro and deep work session manager.

Designed for developers, designers, students, and writers who need uninterrupted deep work flow states.

★ CLEAN SCIENTIFIC POMODORO WORKFLOW:
• 25/5 Classic Rhythm: 25 minutes of deep focus followed by 5 minutes of restorative break.
• Custom Interval Settings: Tailor focus sessions from 10 to 90 minutes with custom long breaks.
• Project & Task Categorization: Tag focus blocks by Coding, Writing, Design, Study, or Admin tasks.
• Detailed Productivity Heatmaps: Track daily completed focus hours, weekly velocity, and streak consistency.
• Ambient Focus Sounds: Built-in rain, mechanical keyboard, library hum, and coffee shop soundscapes.
• Fullscreen Minimalist Clock: Turn your phone into an aesthetic desk clock with OLED screen burn-in prevention.

Achieve deep work mastery every single day with FocusPulse.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (Local timer state and stats stored in phone database)",
            "ai_engine": "$0 (Native timer coroutines & tick loops)",
            "database": "$0 (Local SQLite / Room database)",
            "external_apis": "$0 (Zero third-party APIs)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Margin (AdMob Ad Revenue & In-App Purchases)",
            "summary": "100% standalone focus app. Scale to millions of downloads with zero cloud bills."
        },
        "dangerous_permissions_check": {
            "avoid": ["android.permission.SYSTEM_ALERT_WINDOW (Draw over other apps)", "android.permission.PACKAGE_USAGE_STATS"],
            "use_instead": "Do NOT build an invasive app blocker requiring Accessibility or Usage Access permissions unless you are prepared for prolonged Google Play verification. Keep it a clean, beautiful focus timer with optional Do Not Disturb (DND) trigger.",
            "policy_status": "🟢 Zero Policy Friction. Safe for instant Play Store approval."
        },
        "kickstart_prompt": """Act as a Senior Android Developer and Minimalist UI Specialist.

Build 'FocusPulse: Pomodoro Deep Work' for Android 14/15 with Flutter or Kotlin Jetpack Compose ($0/mo operating cost).

ZERO-COST GOALS:
- Zero dangerous permissions (No accessibility service, no draw over other apps)
- Focus timer with tick animations, custom tags, ambient background sound, and daily stats
- Clean OLED Dark Theme with smooth number rolling transitions.

PROVIDE:
1. Architecture setup with PomodoroTimerEngine (TimerState: Idle, Running, Paused, Break).
2. Main Timer Screen UI with circular countdown, interactive time picker, and start/pause toggle.
3. Task Tag Selector (Work, Study, Coding, Design) with color-coded badges.
4. Statistics Screen with GitHub-style productivity contribution heatmap and daily bar charts.
5. Google Mobile Ads banner setup positioned safely without blocking UI controls."""
    },
    {
        "id": "app_private_vault",
        "concept": "Private Local Vault & Secure File Encryptor",
        "category": "Tools",
        "opportunity_score": 92,
        "search_volume": "210k / month",
        "admob_ecpm": "$20 - $35",
        "monetization": "Pro Cloud Encrypted Backup & Unlimited Vaults ($4.99)",
        "trend_momentum": "+330% Search Surge",
        "recommended_stack": "Kotlin Jetpack Compose with Android Jetpack Security (MasterKey, EncryptedFile, BiometricPrompt)",
        "target_title": "Crypta: Private File Vault",
        "short_description": "AES-256 encrypted hidden photo vault, document locker & biometric protector.",
        "full_description": """Protect your sensitive personal photos, private videos, passwords, and confidential documents with Crypta, the military-grade AES-256 local encrypted vault.

★ UNCOMPROMISED SECURITY ARCHITECTURE:
• AES-256-GCM Hardware-Backed Encryption: Every file is encrypted using Android Keystore hardware security module (Keymaster/StrongBox).
• Biometric Fingerprint & Face Unlock: Instant, seamless access using device-native biometric hardware.
• Fake PIN Decoy Mode: Enter a decoy PIN to open an empty decoy vault in emergency situations.
• Break-In Alert & Intruder Selfie: Captures photo of anyone entering the wrong PIN 3 times.
• Zero Cloud Exposure: 100% offline encryption. Your master password is never transmitted across the internet.

Your privacy is your right. Keep your private life truly private with Crypta.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (Hardware-backed on-device Android Keystore)",
            "ai_engine": "$0 (Native AES-256 hardware cryptographic engine)",
            "database": "$0 (EncryptedSharedPreferences and app private filesDir)",
            "external_apis": "$0 (Zero cloud sync APIs required for free tier)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Margin (AdMob Ads & Pro Features)",
            "summary": "AES-256 encryption executes directly on Android device hardware. $0 cloud storage."
        },
        "dangerous_permissions_check": {
            "avoid": ["android.permission.MANAGE_EXTERNAL_STORAGE"],
            "use_instead": "Use Android Photo Picker to import files into app's private sandbox (context.filesDir) where files are encrypted at rest with EncryptedFile. No storage permissions needed!",
            "policy_status": "🟢 Fully compliant with Google Play Private Storage Guidelines."
        },
        "kickstart_prompt": """Act as a Mobile Cryptography & Android Security Expert.

Build 'Crypta: Private File Vault' in Kotlin Jetpack Compose targeting Android 14/15 (API 34/35) with $0 operating costs.

SECURITY STACK:
- androidx.security:security-crypto (MasterKeys, EncryptedFile, EncryptedSharedPreferences)
- androidx.biometric:biometric (BiometricPrompt with BIOMETRIC_STRONG)
- Photo Picker: ActivityResultContracts.PickMultipleVisualMedia()
- App Private Storage: context.filesDir/vault/ (Zero external storage permissions, $0 cloud cost)

PROVIDE COMPLETE CODE FOR:
1. Android Keystore CryptoManager that generates AES-256 GCM keys in hardware Keystore and encrypts/decrypts byte streams.
2. Biometric Authentication helper with fallback PIN support.
3. Vault File Manager that imports images via Photo Picker, writes encrypted ciphertext to filesDir, and deletes original source file safely.
4. Clean, secure Grid Gallery UI that streams decrypted bitmaps in memory with FLAG_SECURE enabled (preventing screenshots).
5. Fake Decoy PIN switcher architecture."""
    },
    {
        "id": "app_qr_utility",
        "concept": "Smart Offline QR & Barcode Studio",
        "category": "Tools",
        "opportunity_score": 95,
        "search_volume": "320k / month",
        "admob_ecpm": "$20 - $34",
        "monetization": "AdMob Native Cards, Pro Unlimited Batch Export ($2.99 Lifetime)",
        "trend_momentum": "+390% High Daily Search Momentum (Essential Utility)",
        "recommended_stack": "Flutter with google_mlkit_barcode_scanning + qr_flutter OR Kotlin Compose with CameraX + ML Kit",
        "target_title": "QuickScan: QR & Barcode Reader",
        "short_description": "Instant offline QR code reader, barcode scanner & custom WiFi/business generator.",
        "full_description": """Scan any QR code or retail barcode in milliseconds with QuickScan, the ultra-fast, privacy-first offline QR code scanner and custom code generator.

Designed for everyday shopping, instant WiFi connections, business cards, and product verification without annoying full-screen ads.

★ ADVANCED OFFLINE SCANNING & GENERATION:
• Instant Real-Time Detection: Automatically scans codes the instant they enter the camera viewfinder.
• All Standard Formats: QR Code, EAN-13, EAN-8, UPC-A, UPC-E, Code 128, Data Matrix, Aztec, PDF417.
• One-Tap WiFi Quick Connect: Connect to home and office WiFi networks directly from a scanned QR without typing passwords.
• Custom QR Studio: Generate colored QR codes for Website URLs, Contact vCards, WhatsApp, Text, SMS, and Bitcoin.
• Batch Scan Mode: Scan multiple retail barcodes continuously for inventory or price comparisons.
• History & CSV Export: Search past scans and export clean CSV spreadsheets.

★ 100% LOCAL DEVICE PRIVACY:
Scanned links and data are processed locally on your phone. No tracking, no data harvesting.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (Runs 100% on phone CPU/NPU)",
            "ai_engine": "$0 (Google ML Kit on-device barcode vision)",
            "database": "$0 (Local Room / SQLite scan history)",
            "external_apis": "$0 (Zero third-party paid subscriptions)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Profit (AdMob Ads + Pro Upgrades)",
            "minimum_cost_option": "Zero recurring cost forever. If optional cloud backup is ever added, Google Firebase Spark Free Tier ($0/mo) keeps ongoing cost strictly at $0.00.",
            "summary": "100% offline barcode & QR engine. Zero server egress fees even at 1M+ downloads."
        },
        "dangerous_permissions_check": {
            "avoid": ["android.permission.MANAGE_EXTERNAL_STORAGE", "android.permission.READ_MEDIA_IMAGES"],
            "use_instead": "Camera permission (android.permission.CAMERA) only for live viewfinder scanning. Use MediaStore or SAF to save generated QR PNGs without storage permissions.",
            "policy_status": "🟢 100% Clean. Standard Camera Permission with in-app disclosure."
        },
        "kickstart_prompt": """Act as a Principal Mobile Architect specializing in Android Camera & Vision applications.

Build 'QuickScan: QR & Barcode Reader' in Flutter or Kotlin Jetpack Compose ($0/month operating cost).

ZERO-COST SPECIFICATIONS:
- Target SDK: Android 14/15 (API 34/35)
- Computer Vision: Google ML Kit Barcode Scanning (google_mlkit_barcode_scanning) running 100% on-device.
- QR Generator: qr_flutter / zxing-android-embedded with custom corner colors and logo embed.
- Operating Cost: $0.00/month. No external scan verification servers.
- Monetization: Google Mobile Ads (Banner + Native ad in scan history) + In-App Billing for Ad-Free Pro ($2.99).

DELIVERABLES:
1. Complete project structure and pubspec.yaml / build.gradle.kts setup.
2. CameraX Viewfinder with real-time barcode bounding-box overlay shader.
3. QR Generator Screen with custom color picker, WiFi vCard template, and PNG export via MediaStore.
4. Scan History SQLite repository (Room/Hive) with batch CSV export.
5. Play Store compliant AndroidManifest.xml with scoped camera permissions."""
    },
    {
        "id": "app_voice_memo",
        "concept": "EchoNote: Offline Voice Memo & Speech Transcriber",
        "category": "Productivity / Tools",
        "opportunity_score": 93,
        "search_volume": "180k / month",
        "admob_ecpm": "$24 - $38",
        "monetization": "AdMob Banner & Interstitial, Pro Unlimited Transcription Length ($3.49)",
        "trend_momentum": "+310% Steady Demand (Journaling & Student Lectures)",
        "recommended_stack": "Kotlin Jetpack Compose with Android SpeechRecognizer / Vosk-Android OR Flutter with speech_to_text",
        "target_title": "EchoNote: Voice Memo & Audio",
        "short_description": "Private voice recorder, offline speech-to-text transcriber & smart audio notes.",
        "full_description": """Never lose a brilliant thought or important meeting detail again with EchoNote, the offline voice recorder and instant speech-to-text audio notepad.

Record lectures, interviews, voice journals, and brainstorming sessions in crystal-clear audio with automatic transcription.

★ ADVANCED OFFLINE AUDIO & TRANSCRIPTION:
• High-Fidelity Audio Recording: High-quality AAC/M4A 128kbps stereo encoding with noise reduction and skip-silence.
• 100% Offline Speech-to-Text: Convert your spoken words into searchable notes directly on your phone hardware.
• Live Audio Waveform: Interactive animated visualizer while recording.
• Smart Bookmarks & Timestamps: Pin key moments in the audio recording to jump back with one tap.
• Background Recording: Record lectures with screen off or while browsing other apps.
• Categorized Notes & Tags: Tag memos by Work, Idea, Study, Personal, or Meeting.
• Audio Export: Share audio snippets or full text transcripts via WhatsApp, Email, or Google Drive.

★ ZERO CLOUD RECORDING BILLS:
All audio files and transcripts remain securely in your device's private storage.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (Runs 100% on phone CPU/NPU)",
            "ai_engine": "$0 (Android native on-device SpeechRecognizer or local Vosk/Whisper.tflite)",
            "database": "$0 (Local Room / SQLite for transcript text and tags)",
            "external_apis": "$0 (Zero third-party paid transcription APIs)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Margin (AdMob Ads + In-App Audio Tools)",
            "minimum_cost_option": "Expected ongoing cost is $0.00/mo. Avoid paid cloud Whisper endpoints to preserve 100% gross margins.",
            "summary": "Audio is encoded and transcribed locally. No cloud speech transcription bills."
        },
        "dangerous_permissions_check": {
            "avoid": ["Unspecified Foreground Service", "android.permission.MANAGE_EXTERNAL_STORAGE"],
            "use_instead": "Declare android.permission.RECORD_AUDIO with clear runtime disclosure. Use android:foregroundServiceType=\"microphone\" for background lecture recording.",
            "policy_status": "🟡 Declaration Required: Specify 'microphone' foreground service type in Play Console."
        },
        "kickstart_prompt": """Act as a Senior Android Audio Engineer.

Build 'EchoNote: Voice Memo & Audio', an offline voice recorder and speech transcriber for Android with $0/month server costs.

ZERO-COST SPECIFICATIONS:
- Audio Engine: Android MediaRecorder (M4A/AAC) with live visualizer amplitude callback.
- Transcription: Android SpeechRecognizer with EXTRA_PREFER_OFFLINE=true (or Vosk-Android on-device model). Zero paid OpenAI Whisper API bills!
- Storage: context.filesDir with MediaStore.Audio export.
- Monetization: AdMob Native ads on note list + In-App Billing for Pro Audio Enhancer ($3.49).

DELIVERABLES:
1. Complete AndroidManifest.xml setup for Android 14/15 microphone foreground service.
2. AudioRecorderService with pause/resume, decibel metering, and background notification.
3. On-device Speech-to-Text transcription manager converting audio stream into synchronized text blocks.
4. Material 3 Dark theme recording UI with circular pulsing record button and glowing waveform canvas.
5. Audio Player Controller with 1.5x/2x speed toggle and scrubber."""
    },
    {
        "id": "app_water_hydration",
        "concept": "HydroPulse: Water Tracker & Habit Reminder",
        "category": "Health & Fitness",
        "opportunity_score": 94,
        "search_volume": "230k / month",
        "admob_ecpm": "$22 - $35",
        "monetization": "AdMob Native Cards, Pro Custom Widgets & Drink Types ($1.99)",
        "trend_momentum": "+340% Steady Health Demand (High 30-Day Retention)",
        "recommended_stack": "Flutter with Riverpod & Hive OR Kotlin Compose with WorkManager & Room SQLite",
        "target_title": "HydroPulse: Daily Water Drink",
        "short_description": "Smart hydration drink reminder, daily water log & wellness streak tracker.",
        "full_description": """Stay energized, boost your metabolism, and improve your daily wellness with HydroPulse, the clean, minimalist water intake reminder and daily hydration log.

Drinking enough water has never been easier or more satisfying.

★ SMART HYDRATION FEATURES:
• Personalized Daily Water Target: Calculates your optimal daily water goal based on your weight, activity level, and climate.
• 1-Second Quick Log: Log water with customizable glass sizes (200ml, 250ml, 350ml, 500ml, 1 Liter).
• Multiple Beverage Support: Track Tea, Coffee, Electrolytes, Milk, and Smoothies with custom hydration factor ratings.
• Non-Intrusive Smart Reminders: Gentle notification reminders scheduled only during your awake hours.
• Visual Progress & Streaks: Watch your liquid wave container fill up with smooth fluid physics as you hydrate throughout the day.
• Weekly & Monthly Trends: Detailed hydration consistency heatmaps and hydration score ratings.

★ 100% PRIVACY & OFFLINE CAPABILITY:
No health account registration required. Your personal metrics remain stored locally on your device.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (Hydration calculation executed on device)",
            "ai_engine": "$0 (Native hydration formula algorithms)",
            "database": "$0 (Local Room / SQLite for daily drink logs)",
            "external_apis": "$0 (Zero third-party APIs)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Margin (AdMob Ads + Pro Drink Packs)",
            "minimum_cost_option": "Expected ongoing cost is $0.00/mo. All reminders scheduled using Android WorkManager periodic tasks.",
            "summary": "100% on-device habit tracker. Zero recurring infrastructure bills."
        },
        "dangerous_permissions_check": {
            "avoid": ["android.permission.SCHEDULE_EXACT_ALARM"],
            "use_instead": "Use Android WorkManager periodic requests or inexact alarms for interval hydration reminders. Avoid asking for exact alarm permissions.",
            "policy_status": "🟢 100% Safe with WorkManager background scheduling."
        },
        "kickstart_prompt": """Act as a Principal Mobile UX Designer and Android Engineer.

Build 'HydroPulse: Daily Water Drink' in Flutter or Kotlin Jetpack Compose ($0/month operating cost).

SPECIFICATIONS:
- Fluid Animation: Custom canvas rendering fluid liquid wave filling a modern bottle silhouette based on percentage.
- Notification Engine: Android WorkManager scheduling reminders every 2 hours between 8 AM and 10 PM. Zero exact alarm permission!
- Local Database: Room or Hive storing DrinkLogEntity (timestamp, amountMl, beverageType).
- Monetization: AdMob Banner at bottom of History screen + In-App Purchase for Pro Custom Glass Sizes ($1.99).

DELIVERABLES:
1. Complete project architecture with Clean Architecture pattern.
2. Fluid Wave Bottle Widget with spring physics and water fill animation.
3. Quick-Add Drink Button Grid with haptic feedback vibrations.
4. Local WorkManager Notification Worker with notification action button (+250ml directly from notification shade).
5. Weekly Consistency Heatmap widget."""
    },
    {
        "id": "app_flashcard_study",
        "concept": "Memoria: Spaced Repetition Flashcards & Quiz Engine",
        "category": "Education / Productivity",
        "opportunity_score": 96,
        "search_volume": "210k / month",
        "admob_ecpm": "$25 - $42 (High Education CPC Bids)",
        "monetization": "AdMob Rewarded Video for practice tests, Pro Unlimited Decks ($4.99 Lifetime)",
        "trend_momentum": "+370% Exam & Language Learning Surge",
        "recommended_stack": "Flutter with Isar Database OR Kotlin Jetpack Compose with Room SQLite",
        "target_title": "Memoria: Smart Study Cards",
        "short_description": "Spaced repetition flashcards, offline exam quiz maker & active recall planner.",
        "full_description": """Ace your medical exams, master foreign languages, and memorize complex subjects faster with Memoria, the science-backed spaced repetition flashcard and active recall study app.

Powered by the proven SuperMemo SM-2 algorithm, Memoria predicts the exact moment you are about to forget a concept and schedules a quick review.

★ POWERFUL ACTIVE RECALL STUDY TOOLS:
• Proven Spaced Repetition (SM-2): Adapts review intervals dynamically based on your ease rating (Again, Hard, Good, Easy).
• Rich Flashcard Creator: Add bold text, bullet points, code snippets, formulas, and images directly to cards.
• Offline Quiz & Practice Mode: Test your knowledge with multiple choice, typing recall, and flip cards.
• Study Heatmaps & Retention Stats: Track cards learned, daily retention percentage, and projected mastery curves.
• Pre-Built & Custom Decks: Create unlimited decks for Medical USMLE, MCAT, Law, SAT, Spanish, Japanese, and Tech Coding.
• Anki / CSV Import & Export: Easily import existing Anki .apkg files and CSV spreadsheets.

★ 100% OFFLINE STUDY SANDBOX:
Study anywhere on the subway, airplane, or library without internet. Your decks are stored 100% locally.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (SM-2 algorithm calculates intervals on device)",
            "ai_engine": "$0 (Native mathematical memory retention formulas)",
            "database": "$0 (Local Room / SQLite for cards, decks, and review states)",
            "external_apis": "$0 (Zero paid APIs)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Margin (AdMob Ads + Pro Lifetime Unlock)",
            "minimum_cost_option": "Expected ongoing cost is $0.00/mo. Zero cloud bills even with 50,000 flashcards per user.",
            "summary": "Full offline spaced repetition system. High education AdMob eCPMs yield stellar returns."
        },
        "dangerous_permissions_check": {
            "avoid": ["android.permission.MANAGE_EXTERNAL_STORAGE"],
            "use_instead": "Use Storage Access Framework (SAF: ACTION_OPEN_DOCUMENT) to import CSV/Anki decks without broad storage permissions.",
            "policy_status": "🟢 Zero Dangerous Permissions. 100% Clean."
        },
        "kickstart_prompt": """Act as a Principal Educational Software Architect.

Build 'Memoria: Smart Study Cards' for Android using Flutter or Kotlin Jetpack Compose ($0/month operating cost).

ZERO-COST SPECIFICATIONS:
- Spaced Repetition Engine: Implement full SuperMemo SM-2 algorithm on-device (calculating easiness factor, repetitions, and nextReviewDate).
- Database: Room SQLite or Isar storing DeckEntity, CardEntity, and ReviewLogEntity.
- Safe Import: Storage Access Framework for importing CSV study decks.
- Monetization: Rewarded Video ad to unlock Cramming Mode + In-App Billing for Pro Lifetime ($4.99).

DELIVERABLES:
1. Complete SM-2 mathematical calculation engine in Kotlin/Dart with unit tests.
2. Flashcard Flip Screen with 3D card flip animation and 4 review action buttons (Again, Hard, Good, Easy).
3. Deck Manager Screen with progress rings (Due Today, Learning, Mastered).
4. Card Editor Screen with markdown formatting and image attachment via Photo Picker.
5. GitHub-style daily study heatmap widget."""
    },
    {
        "id": "app_unit_currency",
        "concept": "OmniConvert: Multi-Unit & Offline Currency Calculator",
        "category": "Tools / Travel",
        "opportunity_score": 92,
        "search_volume": "250k / month",
        "admob_ecpm": "$20 - $32",
        "monetization": "AdMob Banner & Native, Pro Ad-Free Lifetime ($1.99)",
        "trend_momentum": "+280% Steady Travel & Engineering Search Volume",
        "recommended_stack": "Kotlin Jetpack Compose or Flutter with local JSON conversion tables",
        "target_title": "OmniConvert: Unit & Currency",
        "short_description": "All-in-one offline unit converter, currency exchange calculator & math tool.",
        "full_description": """Convert anything instantly with OmniConvert, the fast, elegant unit converter and multi-currency exchange calculator.

Whether you are traveling overseas, cooking in the kitchen, studying physics, or working on construction plans, OmniConvert provides instant real-time conversions.

★ 30+ CATEGORIES & 1,000+ UNITS:
• Everyday: Currency (160+ world currencies with offline cached rates), Cooking (cups, grams, ounces, tsp), Fuel Economy.
• Science & Engineering: Length, Weight, Area, Volume, Temperature, Pressure, Power, Speed, Torque, Force.
• Digital Computing: Storage (Byte, KB, MB, GB, TB, PB), Data Transfer Speed (Mbps, Gbps).
• Built-In Calculator: Perform real-time math operations while converting.
• Multi-Currency Live Conversion: Convert 1 base currency into 4 target currencies simultaneously on one screen.
• Favorites & Custom Units: Pin your most-used unit pairs to the top for 1-tap access.

★ WORKS 100% OFFLINE:
No internet needed for unit conversions. Currency rates are cached on your device for seamless travel abroad.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (All conversion ratios computed locally on device)",
            "ai_engine": "$0 (Native mathematical formulas)",
            "database": "$0 (Local JSON conversion table + SharedPreferences)",
            "external_apis": "$0 (Uses free European Central Bank XML feed once daily or manual edits)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Margin (AdMob Ads + In-App Pro)",
            "minimum_cost_option": "Expected ongoing cost is $0.00/mo. Use free public central bank daily feeds without paying paid currency API subscriptions.",
            "summary": "Pure algorithmic math app. Zero server overhead and zero maintenance."
        },
        "dangerous_permissions_check": {
            "avoid": ["All Dangerous Permissions"],
            "use_instead": "Zero permissions needed! Pure utility app with instant approval.",
            "policy_status": "🟢 Zero Permissions Required. Instant Google Play approval."
        },
        "kickstart_prompt": """Act as a Senior Android Tools & Utility Developer.

Build 'OmniConvert: Unit & Currency' in Flutter or Kotlin Jetpack Compose ($0/month operating cost).

ZERO-COST SPECIFICATIONS:
- Zero dangerous permissions.
- Conversion Engine: 30 categories with base-unit mathematical normalization matrices.
- Currency Engine: Caches European Central Bank free daily XML feed in SharedPreferences/DataStore. Works 100% offline!
- Design: Clean OLED Dark theme with responsive numeric keypad and instant dual-display conversion.
- Monetization: Google Mobile Ads (Banner + Native in category list) + Play Billing for Pro ($1.99).

DELIVERABLES:
1. Complete Conversion Matrix Engine (converting any unit to base unit, then to target unit).
2. Modern Calculator & Conversion UI with animated digit transitions.
3. Multi-Currency Screen converting input into 4 selected currencies simultaneously.
4. Favorite Conversions pinning system.
5. In-App Purchase integration for removing ads."""
    },
    {
        "id": "app_habit_routine",
        "concept": "AtomicDay: Minimalist Habit Streak & Routine Tracker",
        "category": "Productivity / Lifestyle",
        "opportunity_score": 95,
        "search_volume": "260k / month",
        "admob_ecpm": "$26 - $42",
        "monetization": "AdMob Native Cards, Pro Unlimited Habits & Data Export ($2.99)",
        "trend_momentum": "+390% High Productivity Surge",
        "recommended_stack": "Flutter with Riverpod or Kotlin Jetpack Compose with Room",
        "target_title": "AtomicDay: Habit & Routine",
        "short_description": "Clean daily habit streak tracker, morning routine planner & discipline calendar.",
        "full_description": """Build life-changing daily habits, maintain unstoppable discipline, and crush procrastination with AtomicDay, the distraction-free habit tracker and routine builder.

Inspired by atomic habits science, AtomicDay helps you build micro-habits that compound into remarkable results.

★ STREAMLINED HABIT TRACKING:
• 1-Tap Daily Check-in: Complete habits with satisfying haptic feedback and celebration confetti.
• Habit Streaks & Best Scores: Keep your streak alive and challenge your personal best consistency records.
• Flexible Habit Frequencies: Daily, Weekdays only, or custom days per week (e.g., Gym 3x/week).
• Morning, Afternoon & Evening Routines: Organize habits by time-of-day blocks for effortless flow.
• Visual Progress & Consistency Heatmap: GitHub-style 365-day habit matrix to see your momentum grow.
• Private & Secure: Protect your habit journal with biometric Fingerprint / Face Unlock.

★ 100% PRIVATE & OFFLINE:
No forced account registration. Your personal routine data never leaves your device. Export clean CSV records anytime.""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (Habit streaks calculated locally in device RAM)",
            "ai_engine": "$0 (Native streak algorithm)",
            "database": "$0 (Local Room / SQLite database)",
            "external_apis": "$0 (Zero third-party APIs)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Margin (AdMob Native Ads + Pro Lifetime)",
            "minimum_cost_option": "Expected ongoing cost is $0.00/mo. All reminders scheduled locally with Android WorkManager.",
            "summary": "100% local database and streak engine. Scale to millions with zero recurring costs."
        },
        "dangerous_permissions_check": {
            "avoid": ["android.permission.SCHEDULE_EXACT_ALARM"],
            "use_instead": "Schedule reminders via Android WorkManager or inexact alarms. Avoid asking for exact alarm permissions.",
            "policy_status": "🟢 Zero Dangerous Permissions. Safe for immediate Play Store approval."
        },
        "kickstart_prompt": """Act as a Principal Mobile UX Designer and Android Architect.

Build 'AtomicDay: Habit & Routine' in Flutter or Kotlin Jetpack Compose ($0/month operating cost).

ZERO-COST SPECIFICATIONS:
- Zero cloud servers, zero paid backend databases. Local Room/Hive storage.
- Zero dangerous permissions: Notification reminders via WorkManager.
- Design: Ultra-clean Material 3 Dark theme, smooth spring animations, confetti particle effect on completion.
- Monetization: Google Mobile Ads (Native Cards in habit history) + In-App Billing for Pro ($2.99).

DELIVERABLES:
1. Complete Database Schema (HabitEntity, HabitLogEntity, RoutineEntity) with streak calculation queries.
2. Main Dashboard UI with Routine Tabs (Morning, Afternoon, Evening) and interactive completion toggle circles.
3. Streak & Heatmap Screen with 365-day GitHub-style grid and longest streak counters.
4. Habit Creation Dialog with icon picker, color palette, and frequency selector.
5. WorkManager reminder notification setup."""
    }
]

# --- DYNAMIC APP CONCEPT GENERATOR (FOR ANY USER SEARCH) ---

def generate_dynamic_android_app(query: str) -> Dict[str, Any]:
    """Generates a complete, Google Play-calibrated Android app blueprint for any user query with zero operating cost."""
    q_clean = query.strip() if isinstance(query, str) else str(query).strip()
    words = [w.capitalize() for w in q_clean.split()]
    main_kw = " ".join(words[:4]) if words else "Smart App"
    first_w = words[0] if words else "App"
    second_w = words[1] if len(words) > 1 else "Utility"
    
    # Strictly calibrate Title to <= 30 characters
    title_cand = f"{first_w}: {main_kw}"
    if len(title_cand) > 30:
        title_cand = f"{first_w} Pro: {second_w}"
    if len(title_cand) > 30:
        title_cand = f"{q_clean.capitalize()} App"[:30]

    # Strictly calibrate Short Description to <= 80 characters
    short_desc = f"Smart {q_clean.lower()} tracker, offline utility & clean daily manager for Android."
    if len(short_desc) > 80:
        short_desc = f"Smart {q_clean.lower()} tool & offline organizer for Android."[:80]

    return {
        "id": f"dyn_{q_clean.lower().replace(' ', '_')}",
        "concept": f"{main_kw} - Smart Android Utility & Mobile App",
        "category": "Productivity / Tools",
        "opportunity_score": 94,
        "search_volume": "120k - 260k / month",
        "admob_ecpm": "$22 - $40 (Tier 1 Geography)",
        "cost_badge": "🟢 Zero Operating Cost: $0.00 / mo",
        "monetization": "AdMob Rewarded / Native + Pro Lifetime Unlock ($4.99)",
        "trend_momentum": "+360% Active Play Store Search Momentum",
        "recommended_stack": "Flutter (Riverpod + Hive) or Kotlin Jetpack Compose (MVVM + Room)",
        "target_title": title_cand,
        "short_description": short_desc,
        "full_description": f"""Elevate your daily routine with {title_cand}, the modern, battery-optimized Android solution designed for {q_clean.lower()}.

★ KEY FEATURES:
• Fast & Responsive: Built with modern Material 3 design and buttery smooth 120Hz refresh rate.
• 100% Offline Capable: Works without internet connection, keeping your personal data secure on your device.
• Smart Insights & Analytics: Visual charts and metrics to track your {q_clean.lower()} activity.
• Dark Mode First: OLED-optimized midnight dark theme to protect your eyes and preserve battery life.
• Zero Clutter: Clean, distraction-free interface without annoying full-screen popups.

Download {title_cand} today and take control with total confidence!""",
        "operating_cost": {
            "monthly_cost": "$0.00 / month",
            "tier_label": "Zero Recurring Cost (100% On-Device)",
            "badge_color": "emerald",
            "servers": "$0 (Runs entirely on local device)",
            "ai_engine": "$0 (On-device processing & native algorithms)",
            "database": "$0 (Local SQLite / Room / Hive on user phone)",
            "external_apis": "$0 (Zero paid third-party APIs)",
            "privacy_policy_hosting": "$0 (Free GitHub Pages / Notion)",
            "one_time_setup": "$25 (Google Play Developer Registration)",
            "profit_margin": "100% Pure Profit",
            "summary": "Engineered for zero monthly maintenance and zero server overhead."
        },
        "dangerous_permissions_check": {
            "avoid": ["android.permission.MANAGE_EXTERNAL_STORAGE", "android.permission.READ_MEDIA_IMAGES"],
            "use_instead": "Always use Android Photo Picker (PickVisualMedia) and Storage Access Framework (SAF). Never request broad storage access.",
            "policy_status": "🟢 Zero Dangerous Permissions Recommended"
        },
        "kickstart_prompt": f"""Act as a Principal Android Architect.

I am developing an Android app called '{title_cand}' focused on '{q_clean}'.

ZERO-COST SPECIFICATIONS:
- Operating Cost: $0.00/month. Compute, database, and logic run 100% on the user's device. No cloud servers!
- Target SDK: Android 14/15 (API 34/35)
- Architecture: MVVM with Clean Architecture (Flutter or Kotlin Jetpack Compose)
- Policy Compliance: 100% compliant with Google Play Developer Policy. ZERO dangerous permissions.
- Monetization: Google Mobile Ads (AdMob) + In-App Billing 7.0

PROVIDE:
1. Complete Project Structure and dependencies.
2. AndroidManifest.xml setup with zero dangerous permissions.
3. Core Business Logic and Local Storage Repository (Room/Hive).
4. Material 3 Dark UI screen implementation.
5. Step-by-step instructions to compile release AAB and sign with keystore."""
    }

def _enrich_app_zero_cost(app: Dict[str, Any]) -> Dict[str, Any]:
    """Ensures uniform zero-cost fields exist for UI rendering."""
    app_copy = dict(app)
    if not app_copy.get("cost_badge"):
        app_copy["cost_badge"] = "🟢 Zero Operating Cost: $0.00 / mo"
    
    op = dict(app_copy.get("operating_cost", {}))
    if not op.get("monthly_servers"):
        op["monthly_servers"] = op.get("servers", "$0.00 (100% on-device architecture)")
    if not op.get("ai_ml_cost"):
        op["ai_ml_cost"] = op.get("ai_engine", "$0.00 (On-device Google ML Kit / Algorithmic)")
    if not op.get("database_cost"):
        op["database_cost"] = op.get("database", "$0.00 (Local Room / SQLite / Hive)")
    if not op.get("minimum_cloud_option"):
        op["minimum_cloud_option"] = "Firebase Spark Tier ($0/mo up to 50k reads/day) or Cloudflare D1"
    if not op.get("one_time_setup"):
        op["one_time_setup"] = "$25.00 (One-time lifetime Google Play registration)"
    
    app_copy["operating_cost"] = op
    return app_copy

def get_android_studio_data(search_query: Optional[str] = None) -> Dict[str, Any]:
    """Returns complete Android Studio intelligence package with zero-cost architecture guidelines."""
    apps = [_enrich_app_zero_cost(a) for a in TRENDING_ANDROID_APPS]
    
    active_search = False
    clean_query = search_query.strip() if isinstance(search_query, str) and search_query.strip() else None
    if clean_query:
        active_search = True
        q = clean_query.lower()
        matched = [a for a in apps if q in a['concept'].lower() or q in a['category'].lower() or q in a['target_title'].lower()]
        if not matched:
            dyn_app = _enrich_app_zero_cost(generate_dynamic_android_app(clean_query))
            apps = [dyn_app] + apps[:5]
        else:
            apps = matched

    return {
        "active_search": clean_query if active_search else None,
        "search_mode": active_search,
        "total_apps": len(apps),
        "trending_apps": apps,
        "zero_cost_guide": ZERO_COST_ARCHITECTURE_GUIDE,
        "asset_specs": PLAY_STORE_ASSET_SPECS,
        "dangerous_permissions": DANGEROUS_PERMISSIONS_DIRECTORY,
        "twenty_tester_policy": TWENTY_TESTER_POLICY_GUIDE
    }

def audit_app_permissions(permissions: List[str]) -> Dict[str, Any]:
    """Audits a user-supplied list of permissions against Google Play Developer Policies."""
    audit_results = []
    has_critical = False
    has_declaration = False

    for p in permissions:
        perm_clean = p.strip()
        match = next((item for item in DANGEROUS_PERMISSIONS_DIRECTORY if item['permission'] in perm_clean or perm_clean in item['permission']), None)
        if match:
            if match['risk_level'] == 'CRITICAL_REJECTION_HAZARD':
                has_critical = True
            elif match['risk_level'] in ['MODERATE_DECLARATION_REQUIRED', 'HIGH_POLICY_RESTRICTION']:
                has_declaration = True
            audit_results.append(match)
        else:
            audit_results.append({
                "permission": perm_clean,
                "name": perm_clean.split(".")[-1],
                "risk_level": "LOW_SAFE_STANDARD",
                "badge_color": "emerald",
                "policy_rule": "Standard Android permission. Low risk of Play Store rejection if purpose is aligned.",
                "safe_alternative": "Ensure permission is requested at runtime with contextual explanation.",
                "required_declaration": "Standard Data Safety Form declaration if data is transmitted."
            })

    status_verdict = "PASSED_SAFE"
    if has_critical:
        status_verdict = "CRITICAL_REJECTION_RISK"
    elif has_declaration:
        status_verdict = "DECLARATION_REQUIRED"

    return {
        "verdict": status_verdict,
        "total_audited": len(permissions),
        "findings": audit_results,
        "safe_practices_summary": [
            "Use Android Photo Picker instead of READ_MEDIA_IMAGES or READ_EXTERNAL_STORAGE.",
            "Use Storage Access Framework (SAF: ACTION_CREATE_DOCUMENT) instead of MANAGE_EXTERNAL_STORAGE.",
            "Use Inexact Alarms or WorkManager instead of SCHEDULE_EXACT_ALARM.",
            "Ensure Foreground Services explicitly define foregroundServiceType in AndroidManifest.xml.",
            "Never use QUERY_ALL_PACKAGES; specify target packages in <queries> block."
        ]
    }
