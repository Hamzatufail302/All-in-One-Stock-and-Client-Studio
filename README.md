# StockPulse AI 🚀
### Local Keywords & Trends Intelligence Platform for Stock & Digital Asset Creators

**StockPulse AI** is an advanced local web application built specifically for creators selling on **Adobe Stock, Shutterstock, Etsy, IconScout, and GraphicRiver**. It automatically crawls live search demand, analyzes keyword competition, forecasts seasonal trends, tracks daily production goals, and provides production specifications tailored to your skills in **Adobe Illustrator, Adobe Photoshop, Canva, and Generative AI Images & Video**.

---

## 🌟 Key Features & Updates

### 1. 🌐 Combined vs. Platform-Isolated Sections
- **Combined Search & Trends Hub**: Unified search across all marketplaces simultaneously with cross-platform comparison and calculated Opportunity Scores.
- **Isolated Platform Sections**: Dedicated individual tabs for **Adobe Stock, Shutterstock, Etsy, IconScout, and GraphicRiver**.
  - **In-Tab Search Engine**: Search exclusively within that marketplace's buyer index.
  - **Strictly Separated Technical Requirements**: Separate tabs for 📐 **Vectors**, 📸 **Images / Photos / AI**, and 🎬 **4K Stock Video**.
  - **AI Acceptance Policy Callouts**: Real-world legal policies (e.g. Adobe Stock 100% accepts AI images & video; Shutterstock restricts external third-party AI; Etsy has huge demand for AI clipart and wall art).
  - **"What to Create" with Ready SEO Titles**: Actionable asset concepts with pre-formatted titles and tags ready to upload.

### 2. ⚡ Daily Progress Tracker & Goal Manager (Persistent in SQLite)
- **Daily Target Quotas**: Set daily targets for Vectors, AI Images, AI Videos, and Canva/PSD Templates.
- **One-Click Asset Logging**: Click "+ Log Done" from any search result, AI prompt card, or event to add to today's count.
- **Persistent Local Database**: All logged assets, completion percentages, notes, and targets are saved permanently in [`stock_crawler.db`](file:///C:/Users/Hamza%20Tufail/Documents/keyword%20cwarler%20for%20stock/data/stock_crawler.db).
- **Streak & Consistency Radar**: 14-day consistency tracker with fire streak badge (`🔥 X Day Streak`).
- **Status Toggle**: Toggle between `Created` and `Uploaded` for complete pipeline tracking.

### 3. 🤖 AI Daily Quota Generator (15–20 Prompts per Day)
- Tailored for **Google Flow, Midjourney v6, Flux.1, Runway Gen-3, Luma Dream Machine, and Sora**.
- Generates batches of **20 ready-to-run commercial prompts**:
  - **10 Commercial AI Stock Photos / Backgrounds** with lighting, camera lenses (e.g. Hasselblad H6D-100c, 85mm f/1.8), color grading, and negative copy space.
  - **10 4K Stock Video B-Roll Loops** with camera movement (gimbal dolly, aerial drone descent, 60fps slow-motion loops, ProRes 422).
- Each prompt includes: Ready Stock Title, ready copy tags, aspect ratio, and "+ Log to Today" button.

### 4. 📅 365-Day Daily Ranked Events & Calendar
- Dynamically scans global holidays, shopping milestones, and cultural dates starting from today forward.
- **5-Star Commercial Ranking (⭐⭐⭐⭐⭐)**: Ranked by earning potential and lead time.
- **60–90 Day Production Lead Times**: Alerts you when to create assets (e.g. Christmas, New Year 2027, Black Friday, Valentine's Day) well ahead of peak buying surges.
- Separated asset recommendations for **Illustrator Vectors, AI Images, 4K Videos, and Canva/PSD Templates** for every single holiday.

### 5. 🔍 Multi-Engine Trend Crawler & Alphabet Soup
- **Direct Adobe Stock Weights**: Real-time integration with Adobe's Fotolia autocomplete backend for exact search popularity scores (`0.0 - 1.0`).
- **Alphabet-Soup Deep Digger (A–Z)**: Automatically cycles seed keywords through 26 letters (`seed + a`, `seed + b`, ...) to uncover **100 to 250+** high-converting long-tail buyer queries in seconds.
- **Tag Generators**: Ready-to-copy tags formatted for Adobe Stock (49 tags) and Etsy (13 tags).

### 6. 📋 Production Kanban Queue
- Organize ideas and design roadmaps across 4 stages: `Idea` ➔ `Designing` ➔ `Ready` ➔ `Uploaded`.
- Export your production roadmap or Alphabet Soup keywords to CSV.

---

## 🚀 How to Run Locally

### Option 1: One-Click Launch (Windows)
Double-click the **[`run.bat`](file:///C:/Users/Hamza%20Tufail/Documents/keyword%20cwarler%20for%20stock/run.bat)** file. It launches the server and opens `http://localhost:8000` in your web browser.

### Option 2: Terminal / Command Line
```powershell
python app.py
```
Open:
```
http://localhost:8000
```
