# TrustRank AI
### Intelligent Candidate Discovery & Ranking Engine

> **Ranks 100,000 candidates in under 23 seconds on CPU. No GPU. No API calls. 100% offline.**

---

## 📌 Project Overview

### The Problem
Traditional Applicant Tracking Systems (ATS) and recruiting software rely heavily on raw keyword matching. This leads to several critical points of failure:
1. **Keyword Stuffing**: Candidates list hundreds of skills (e.g., "Deep Learning", "Generative AI") regardless of their actual expertise. An unqualified candidate with a keyword-optimized resume frequently outranks an actual expert.
2. **Pedigree/Company Trap**: Heavy keyword matching struggles to differentiate between a developer who built high-scale AI systems at a product company versus a developer doing routine maintenance at a traditional consulting giant.
3. **Availability Mismatch**: Perfect-on-paper candidates are often ranked highly even if they are inactive, have a 5% response rate, or demand salaries and locations outside the job profile.
4. **Honeypot/Trap Resumes**: The dataset contains honeypot candidates (subtly impossible profiles, such as 8 years of experience at a company founded 3 years ago) that fool simple embedding models.

### The Solution: TrustRank AI
**TrustRank AI** is an alignment-guided, multi-dimensional candidate discovery and ranking system specifically designed for high-stakes roles like **Senior AI Engineer — Founding Team**. 

Instead of treating resumes as flat text bags, TrustRank AI:
* Evaluates candidates across **6 distinct dimensions** using domain-specific heuristics.
* Applies a **Trust-Multiplier** to every skill based on proficiency level, years of experience, peer endorsements, and assessment scores.
* Analyzes career trajectory to filter out consulting-firm giants, rewarding product-company history and fast promotion cycles.
* Incorporates real-time **behavioral signals** (activity recency, recruiter response rate, assessment completion) directly into the score.
* Programmatically identifies and penalizes **honeypots and skill-stuffers**.

### Technologies Used
* **Python 3.12**: Core programming language.
* **Pandas & NumPy**: For fast array manipulations, candidate streaming, and dataset alignment.
* **scikit-learn**: For robust scaling and distance/alignment math.
* **tqdm**: Memory-efficient streaming CLI progress feedback.
* **python-docx**: For offline parsing of job descriptions and signals.

### Impact Made
* **Throughput**: Processes **4,600+ candidates per second** on a single CPU core.
* **Latency**: Ranks the entire **100,000 candidate pool in 21.7 seconds**, using under **100MB of RAM** (far below the 5-minute, 16GB limit).
* **Accuracy & Safety**: Zero honeypots ranked in the top 100. Accurate top shortlist containing highly qualified Senior AI/ML/NLP engineers with 6–8 years of experience, strong product-company backgrounds, and high engagement rates.

---

## ⚙️ How It Works (Scoring Engine)

```
candidates.jsonl (100K candidates)
        │
        ▼
┌──────────────────────────────────────────────────────┐
│                  TRUST-RANK AI SCORER                │
│                                                      │
│  1. Skill Match (30%)                                │
│     • Semantic synonym resolution (40+ maps)         │
│     • Trust weight: proficiency × endorsement        │
│       × duration × assessment score                  │
│     • Core / secondary / adjacent taxonomy           │
│                                                      │
│  2. Career Trajectory (30%)                          │
│     • Recency-weighted title relevance               │
│     • Consulting-only penalty (0.4x multiplier)      │
│     • Upward-trajectory & tenure checks              │
│                                                      │
│  3. Experience Fit (12%)                             │
│     • Sweet-spot: 6-8 yrs; smooth decay curve        │
│                                                      │
│  4. Education (7%)                                   │
│     • Tier-1/2 school weight + CS/ML degree match    │
│                                                      │
│  5. Behavioral Signals (15%)                         │
│     • Activity recency & recruiter response rates    │
│                                                      │
│  6. GitHub Activity (6%)                             │
│     • Open-source validation signals                 │
└──────────────────────────────────────────────────────┘
        │
        ▼
   submission.csv (Top 100 ranked candidates)
```

### 1. Skill Trust Multiplier
Raw skills are unreliable. TrustRank AI calculates a custom trust score for each skill:
$$\text{Trust Score} = \text{Relevance} \times \text{Proficiency} \times \text{Endorsement Factor} \times \text{Duration Factor} \times \text{Assessment Score}$$
This separates a candidate who actually worked with SBERT/LLMs for 3 years from one who merely added it as a tag yesterday.

### 2. Career Trajectory Analysis
* **The Consulting Penalty**: Candidates whose entire history lies at outsourcing giants (e.g., TCS, Infosys, Wipro, Cognizant) receive a `0.4` multiplier on their career score. The penalty scales down proportionally if they have any product company experience.
* **Job Hopper Penalty**: If the average job tenure is under 12 months, the candidate's trajectory score is penalized by `30%`.
* **Title Relevance**: Recency-weighted matching of past titles to "Founding Engineer", "Lead AI Engineer", "Senior NLP Engineer", etc.

### 3. Trap & Honeypot Detection
* **Temporal Integrity Check**: Flags candidates claiming experience durations longer than the target company has existed (e.g., worked 5 years at a startup founded in 2024).
* **Experience Check**: Flags candidates with skill durations exceeding their total professional experience years.
* Identified anomalies are penalized with a composite score cap of `0.0`, excluding them from the top shortlist.

---

## 🗂️ Repository Structure

```
├── rank.py                  # Main CLI entry point
├── ranker/
│   ├── job_config.py        # Configures weights, skills taxonomy, and synonym maps
│   └── scorer.py            # Multi-dimensional candidate scoring engine
├── requirements.txt         # Required Python packages
├── submission.csv           # Top 100 candidate shortlist (output of run)
├── submission_metadata.yaml # Metadata details for reproduction validation
├── .gitignore               # Excludes large data files from version control
└── README.md                # Documentation & Setup guide
```

---

## 📊 Key Anti-Patterns Handled

| Anti-Pattern | How We Handle It |
|---|---|
| **Keyword Stuffers** (Marketing Manager with every AI skill) | Title & career checks override skill weight; composite score capped at `0.0`. |
| **Consulting-Only Background** | Career trajectory score multiplied by `0.4` (released proportionally for product experience). |
| **Inactive Candidates** (6+ months) | Behavioral score decay; drops behavioral dimension score to near `0`. |
| **Low Response Rates** | Recruiter response rate below `5%` yields `0` behavioral score. |
| **Honeypot Resumes** (Impossible dates) | Temporal analysis instantly caps composite score at `0.0`. |

---

## 🚀 How to Run the Project

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Clone the Repository
```bash
git clone https://github.com/ajais4800/trust_rank_ai.git
cd trust_rank_ai
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Candidate Ranking
To run the ranker on your candidates JSONL file:
```bash
python rank.py --candidates ./path/to/candidates.jsonl --out ./submission.csv
```

*To run on a sample JSON array format (e.g., `sample_candidates.json`):*
```bash
python rank.py --candidates ./path/to/sample_candidates.json --out ./submission.csv --json-array
```

### 5. Validate the Output
Run the official challenge validator to verify the output constraints:
```bash
python path/to/validate_submission.py submission.csv
```

---

## 🏆 Top Shortlisted Candidates (Sample Output)

| Rank | Score | Candidate ID | Reasoning |
| :---: | :---: | :---: | :--- |
| 1 | 0.9796 | CAND_0002025 | Senior AI Engineer with 5.9 yrs; 20 AI core skills; response rate 0.80. |
| 2 | 0.9782 | CAND_0011687 | Senior NLP Engineer with 7.8 yrs; 13 AI core skills; response rate 0.89. |
| 3 | 0.9732 | CAND_0018499 | Senior Machine Learning Engineer with 7.2 yrs; 17 AI core skills; response rate 0.61. |
| 4 | 0.9688 | CAND_0052682 | NLP Engineer with 6.6 yrs; 15 AI core skills; response rate 0.88. |
| 5 | 0.9657 | CAND_0098846 | AI Engineer with 7.6 yrs; 18 AI core skills; response rate 0.62. |
