# 🎯 Job Hunter Agent for Xiao

> **Official Repository**: `job-hunter-agent-for-xiao`  
> **Brand & Dashboard**: **Job Hunter Agent for Xiao**  
> **Challenge Specification**: `Job_Hunter_AI_Agent_Challenge.pdf`

An autonomous, end-to-end recruitment suite and premium dark-theme glassmorphism dashboard built specifically for **Xiao**.

![Dashboard Preview](https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80)

---

## 🌟 Key Features

1. **4x Daily Scheduled Automation**:
   - Executes at **08:00, 12:00, 16:00, and 20:00 CET** (Europe/Paris timezone).
   - Automatically crawls **5 leading job platforms**:
     - 🌴 **Welcome to the Jungle** (French & European tech startups and scale-ups)
     - 🏢 **APEC** (Association Pour l'Emploi des Cadres - Executive & Engineering roles in France)
     - 💼 **LinkedIn Jobs** (Enterprise, remote, and hybrid European tech postings)
     - ⚡ **Indeed France** (Broad cross-industry postings)
     - 🏛️ **France Travail Tech** (French public & private tech ecosystem)
2. **1.0 to 10.0 Compatibility Grading Engine**:
   - Multi-dimensional scoring formula:
     $$\text{Score} = (\text{Tech Stack} \times 0.40) + (\text{Seniority} \times 0.25) + (\text{Domain} \times 0.20) + (\text{Contract/Mode} \times 0.15)$$
   - Color-coded glowing badges (Emerald 9.0+, Cyan 8.0+, Amber 7.0+).
   - Identified strengths and gap highlights.
3. **AI Cover Letter Studio**:
   - Generates custom, tailored cover letters matching the job's stack and company mission.
   - 3 selectable tones: **Dynamic Startup**, **Formal Executive**, and **Deep Technical**.
   - Bilingual support: French (standard for APEC & WTTJ France) and English.
   - One-click copy and live editor.
4. **Targeted CV Tailoring Suggestions**:
   - Actionable recommendations on how Xiao should tweak resume bullet points for each specific job to maximize interview conversion.
5. **Autonomous Gmail Application Dispatch**:
   - Pre-fills recruiter email, custom subject line, and cover letter body.
   - Supports one-click draft creation in Gmail Web or direct API dispatch.
6. **Premium Dark-Theme Glassmorphism UI**:
   - Sleek deep-slate background (`#07090e`) with floating ambient light orbs.
   - Frosted glass cards (`backdrop-filter: blur(20px)`).
   - Real-time search, platform filtering, score sliders, and CDI/Remote toggles.
   - Local persistence via `localStorage`.

---

## 🚀 Quick Start (Local Preview)

To preview the dashboard immediately in your browser:

### Option 1: Double-click to open
Simply open `index.html` directly in Google Chrome, Safari, or Brave:
```bash
open /Users/zhangxiao/.gemini/antigravity/scratch/job-hunter-agent-for-xiao/index.html
```

### Option 2: Run local preview server
```bash
cd /Users/zhangxiao/.gemini/antigravity/scratch/job-hunter-agent-for-xiao
npx serve -l 3000 .
```
Then visit: `http://localhost:3000`

---

## ⏰ Enabling the 4x/Day Scheduled Automation

The automation sidecar definition is stored in `sidecar.json`. To activate it in your Antigravity environment:

```bash
cd /Users/zhangxiao/.gemini/antigravity/scratch/job-hunter-agent-for-xiao
bash scripts/install_sidecar.sh
```

Then open your Automations dashboard to enable it:
👉 [Open Automations Dashboard](sidecar://dashboard)

---

## 🌐 Deploying to Vercel (Live Server)

Deploy your live dashboard to Vercel with zero configuration:

```bash
cd /Users/zhangxiao/.gemini/antigravity/scratch/job-hunter-agent-for-xiao
bash scripts/deploy_vercel.sh
```

Or via direct Vercel CLI:
```bash
npx vercel --prod
```

---

## 🐙 Publishing Code to GitHub (`job-hunter-agent-for-xiao`)

To push the project to your GitHub account under the mandatory repository name `job-hunter-agent-for-xiao`:

```bash
cd /Users/zhangxiao/.gemini/antigravity/scratch/job-hunter-agent-for-xiao
bash scripts/publish_to_github.sh
```

The script will configure remote origin as `https://github.com/<your-username>/job-hunter-agent-for-xiao.git` and push the `main` branch.

---

## 🐍 Python Multi-Site Job Scraping Module (`scraper/`)

The autonomous backend scraper targets 5 leading French employment platforms with anti-bot resilience and rate limiting:

1. **🌴 Welcome to the Jungle** (`wttj`): Queries Algolia / Next.js de-hydrated search state.
2. **⚡ Indeed France** (`indeed`): Powered by `python-jobspy` with automatic fallback to Indeed France public RSS/XML feed.
3. **💼 HelloWork** (`hellowork`): Extracts embedded Schema.org `JobPosting` JSON-LD data.
4. **🏛️ France Travail** (`francetravail`): Candidate portal search & clean text parser.
5. **🏢 APEC** (`apec`): Direct connection to APEC's public single-page-app webservices API (`/cms/webservices/rechercheOffre`).

### Gemini Free Tier Rate-Limiting (15 RPM)
To prevent 403 blocks and respect Gemini's free tier (15 requests per minute limit), the module pauses with an enforced delay:
```python
time.sleep(4)  # 60 seconds / 15 requests = 4.0s interval
```

### Running the Python Scraper

```bash
cd /Users/zhangxiao/.gemini/antigravity/scratch/job-hunter-agent-for-xiao/scraper

# Install dependencies
pip install -r requirements.txt

# Run multi-site search
python job_scraper.py "Senior Full Stack" "Paris"
```

### Clean Standardized JSON Output Schema
```json
[
  {
    "title": "Lead Full Stack Engineer",
    "company": "Doctolib",
    "location": "Paris (Hybrid)",
    "contract": "CDI",
    "description": "Conception et scaling d'architectures web TypeScript / Node.js...",
    "apply_url": "https://www.welcometothejungle.com/fr/companies/doctolib/jobs/lead-full-stack"
  }
]
```

---

## 📄 CV Parsing & Gemini 2.5 Flash Match Engine (`scraper/`)

The agent integrates Xiao ZHANG's verified CV (`cv.pdf`) directly into the evaluation loop:

1. **📄 CV Parser (`cv_parser.py`)**: Uses `pypdf` to extract structured sections:
   - **Candidate Profile**: Xiao ZHANG (Puteaux, Île-de-France)
   - **Target Domains**: Digital Marketing & E-Commerce, International Brand Communication
   - **Key Experience**: LCD Phone Paris (6 mo), Hilton Shanghai (6 mo), Anhui Bai Cai (6 mo)
   - **Education**: MSc Digital Marketing & E-Commerce (INSEEC Paris), Bachelor Economy & Management (Limoges)
   - **Languages**: English (C1), French (B2), Mandarin (Native), Japanese (A1)
   - **IT & Tools**: Google Suite, Office Pack, STATA, Photoshop, CapCut, Social Platforms (WeChat, RED, TikTok)
2. **🧠 Gemini 2.5 Flash Evaluator (`gemini_evaluator.py`)**:
   - Injects Xiao's parsed CV as the ground truth benchmark into `gemini-2.5-flash`.
   - Computes a granular **1.0 to 10.0 score** for each job posting.
   - Extracts exact **matched skills** and **missing skills** along with qualitative strengths and gaps.
3. **⏳ 15 RPM Rate Limiter (`time.sleep(4)`)**:
   - Enforces a 4.0-second pause between each job evaluation to strictly adhere to Gemini's free tier (15 requests per minute limit).
4. **🚀 End-to-End Pipeline (`pipeline.py`)**:
   - Combines scraping across the 5 French portals with Gemini 2.5 Flash scoring in a single execution:
     ```bash
     cd /Users/zhangxiao/.gemini/antigravity/scratch/job-hunter-agent-for-xiao/scraper
     python pipeline.py ../cv.pdf
     ```

---

## 🛠️ Project Structure

```
job-hunter-agent-for-xiao/
├── index.html                   # Complete Glassmorphism Web Dashboard (Branded: Job Hunter Agent for Xiao)
├── cv.pdf                       # Xiao's Master CV (PDF)
├── sidecar.json                 # Antigravity 4x/day scheduled automation config
├── vercel.json                  # Vercel deployment configuration (Project: job-hunter-agent-for-xiao)
├── package.json                 # NPM scripts & project metadata (Package: job-hunter-agent-for-xiao)
├── scraper/                     # Python Multi-Site Scraping & Gemini Evaluation Package
│   ├── __init__.py              # Package init
│   ├── cv_parser.py             # pypdf / python-docx parser for cv.pdf
│   ├── gemini_evaluator.py      # gemini-2.5-flash 1-10 match evaluator
│   ├── job_scraper.py           # Core 5-portal scraper (WTTJ, Indeed, HelloWork, FT, APEC)
│   ├── models.py                # Standardized JobListing dataclass
│   ├── pipeline.py              # End-to-end recruitment pipeline orchestrator
│   ├── requirements.txt         # Python dependencies (pypdf, google-genai, requests, etc.)
│   ├── test_pipeline.py         # Pipeline smoke & schema test
│   └── test_scraper.py          # Scraper unit test
├── scripts/
│   ├── deploy_vercel.sh         # One-click Vercel deployment script
│   ├── publish_to_github.sh     # One-click GitHub publisher script
│   └── install_sidecar.sh       # Antigravity sidecar installation script
└── src/
    └── lib/
        ├── scoring.js           # 1-10 CV compatibility grading algorithm
        ├── scrapers.js          # 5-platform aggregator specs (WTTJ, APEC, etc.)
        └── coverLetter.js       # AI cover letter & CV suggestions generator
```

---

*Crafted for Xiao | Job Hunter Agent for Xiao*
