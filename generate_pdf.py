#!/usr/bin/env python3
import sys
from fpdf import FPDF

class SlideDeck(FPDF):
    def __init__(self):
        # Landscape A4 (297mm x 210mm)
        super().__init__(orientation="L", unit="mm", format="A4")
        self.set_margins(20, 15, 20)
        self.alias_nb_pages()
        self.set_auto_page_break(auto=False)

    def draw_bg(self):
        # Draw dark premium slate background: rgb(15, 23, 42)
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 297, 210, "F")

    def slide_header(self, title):
        self.draw_bg()
        # Draw top accent bar (Cyan-400: rgb(34, 211, 238))
        self.set_fill_color(34, 211, 238)
        self.rect(0, 0, 297, 5, "F")

        # Slide Title
        self.set_y(15)
        self.set_font("helvetica", "B", 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT", align="L")
        
        # Underline accent line
        self.set_draw_color(34, 211, 238)
        self.set_line_width(0.8)
        self.line(20, 28, 277, 28)
        self.set_y(32)

    def slide_footer(self):
        # Slide number
        self.set_y(195)
        self.set_font("helvetica", "I", 9)
        self.set_text_color(148, 163, 184) # slate-400
        self.cell(0, 10, f"Page {self.page_no()} of {self.alias_nb_pages()}", align="R")
        # Brand logo / team name
        self.set_x(20)
        self.cell(0, 10, "TrustRank AI  |  Redrob Candidate Discovery & Ranking Challenge", align="L")

    def draw_card(self, x, y, w, h, title="", fill_color=(30, 41, 59), border_color=(51, 65, 85)):
        # Slate-800 card
        self.set_fill_color(*fill_color)
        self.set_draw_color(*border_color)
        self.set_line_width(0.4)
        self.rect(x, y, w, h, "DF")
        
        if title:
            self.set_xy(x + 5, y + 4)
            self.set_font("helvetica", "B", 12)
            self.set_text_color(34, 211, 238) # Cyan accent
            self.cell(w - 10, 6, title, align="L")
            return y + 12
        return y + 4

def create_deck(output_path):
    pdf = SlideDeck()
    
    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Cover)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_bg()
    
    # Gold top accent bar
    pdf.set_fill_color(251, 191, 36) # Amber-400
    pdf.rect(0, 0, 297, 6, "F")
    
    pdf.set_y(65)
    pdf.set_font("helvetica", "B", 40)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "TrustRank AI", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_y(85)
    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(34, 211, 238) # Cyan-400
    pdf.cell(0, 10, "Intelligent Candidate Discovery & Ranking Engine", align="C", new_x="LMARGIN", new_y="NEXT")
    
    # Line divider
    pdf.set_draw_color(34, 211, 238)
    pdf.set_line_width(1)
    pdf.line(70, 100, 227, 100)
    
    pdf.set_y(115)
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(203, 213, 225) # Slate-300
    pdf.cell(0, 8, "Redrob Intelligent Candidate Discovery & Ranking Hackathon", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "A Multi-Dimensional Scoring Engine and Trap Filter", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_y(155)
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(251, 191, 36) # Amber-400
    pdf.cell(0, 8, "Author: Team TrustRank AI (Ajai)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "I", 10)
    pdf.set_text_color(148, 163, 184) # Slate-400
    pdf.cell(0, 6, "Platform: 8-Core CPU (16GB RAM) | Runtime: ~22s for 100K candidates", align="C")
    
    # -------------------------------------------------------------
    # SLIDE 2: The Core Problem
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.slide_header("The Core Recruiting Problem")
    
    # Left Card: ATS Limitations
    card1_y = pdf.draw_card(20, 38, 120, 145, "Limitations of Keyword-Based ATS")
    pdf.set_xy(25, card1_y)
    pdf.set_font("helvetica", "", 10.5)
    pdf.set_text_color(203, 213, 225)
    
    bullets_left = [
        "Keyword Stuffing: Candidates list hundreds of AI keywords (LLM, NLP, PyTorch) without real expertise.",
        "Outsourcing / Consulting Trap: Heavy keyword matching ranks outsourced maintenance roles above product-focused R&D profiles.",
        "Candidate Availability: Traditional systems ignore critical behavioral signals (activity recency, recruiter response rates).",
        "Resume Honeypots: Embedded 'trap' profiles with impossible experience data (e.g. 5 yrs skill use in a 3 yr career)."
    ]
    for b in bullets_left:
        pdf.multi_cell(110, 6, f"- {b}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(pdf.get_y() + 3)
        
    # Right Card: The Startup Profile
    card2_y = pdf.draw_card(150, 38, 127, 145, "Finding a Founding AI Engineer")
    pdf.set_xy(155, card2_y)
    
    bullets_right = [
        "Product over Research: Focus on candidates with practical shipping experience rather than academic publications.",
        "Fast Trajectory: Spot candidates with rapid growth (promotions, leadership) within small-to-medium product companies.",
        "Active Engagement: High login activity, high recruiter response rate (>50%), and quick assessment completions.",
        "Location & Setting: Finding talent aligned with Bangalore/hybrid and ready to work in high-speed settings."
    ]
    for b in bullets_right:
        pdf.multi_cell(117, 6, f"- {b}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(pdf.get_y() + 3)

    pdf.slide_footer()

    # -------------------------------------------------------------
    # SLIDE 3: Architecture & 6-Dimensional Scorer
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.slide_header("TrustRank AI Architecture")
    
    # Introduction text
    pdf.set_y(35)
    pdf.set_font("helvetica", "", 11)
    pdf.set_text_color(226, 232, 240)
    pdf.multi_cell(0, 6, "We built a multi-dimensional heuristic scoring pipeline that evaluates candidates across 6 distinct weighted dimensions. Raw JSONL profiles are streamed and scored on-the-fly, generating a composite alignment index in sub-minute speeds.", new_x="LMARGIN", new_y="NEXT")
    
    # 6 Grid Cards
    dimensions = [
        ("1. Skill Match (30%)", "Evaluates canonical AI skills mapped from 40+ synonyms, weighted by proficiency, duration, endorsements, and tests."),
        ("2. Career Trajectory (30%)", "Measures title relevance, company pedigree, tenure stability, and applies a 0.4x consulting-firm penalty."),
        ("3. Experience Fit (12%)", "Uses a Gaussian-like bell curve centered at the ideal 6-8 year sweet-spot, avoiding binary dropoffs."),
        ("4. Education (7%)", "Scores field relevance (CS/ML/Stats) and matches against Tier-1/Tier-2 engineering institution databases."),
        ("5. Behavioral Signals (15%)", "Decays score based on login inactivity, recruiter response rate, assessment completion, and notice period."),
        ("6. GitHub Activity (6%)", "Validates candidate quality using open-source contribution metrics (commits, stars, and PRs).")
    ]
    
    positions = [
        (20, 58), (105, 58), (190, 58),
        (20, 122), (105, 122), (190, 122)
    ]
    
    for i, (title, desc) in enumerate(dimensions):
        x, y = positions[i]
        card_y = pdf.draw_card(x, y, 80, 58, title)
        pdf.set_xy(x + 5, card_y)
        pdf.set_font("helvetica", "", 9.5)
        pdf.set_text_color(203, 213, 225)
        pdf.multi_cell(70, 5, desc)
        
    pdf.slide_footer()

    # -------------------------------------------------------------
    # SLIDE 4: Trust-Weighted Skill Match
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.slide_header("Dimension Focus: Trust-Weighted Skills")
    
    # Left Card: Semantic Maps
    card1_y = pdf.draw_card(20, 38, 120, 145, "Semantic Synonym Mapping")
    pdf.set_xy(25, card1_y)
    pdf.set_font("helvetica", "", 10.5)
    pdf.set_text_color(203, 213, 225)
    
    pdf.multi_cell(110, 6, "Skill lists are noisy and unstandardized. We implemented a 40+ synonym map resolving terms to clean taxonomic buckets:")
    pdf.set_y(pdf.get_y() + 3)
    
    synonyms = [
        "NLP: sentence-transformers, BERT, SBERT, NLTK, spaCy",
        "GenAI: LLMs, LangChain, RAG, prompt-engineering",
        "Deep Learning: PyTorch, TensorFlow, keras, neural-networks",
        "Core vs Secondary: NLP and Information Retrieval are weighted heavily (1.0). CV and Audio are secondary (0.35)."
    ]
    for syn in synonyms:
        pdf.multi_cell(110, 5.5, f"- {syn}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(pdf.get_y() + 2)
        
    # Right Card: Trust Formula
    card2_y = pdf.draw_card(150, 38, 127, 145, "The Skill-Trust Formula")
    pdf.set_xy(155, card2_y)
    
    pdf.multi_cell(117, 6, "Instead of counting skills, we compute a Trust Score for each skill entry. Candidates who keyword-stuff with zero duration/endorsements receive negligible scores:")
    pdf.set_y(pdf.get_y() + 4)
    
    formula_desc = [
        "Proficiency Weight: Beginner = 0.25, Intermediate = 0.5, Advanced = 0.8, Expert = 1.0.",
        "Endorsement Trust: Logarithmic scaling based on peer endorsements: log(1 + endorsements) / log(50).",
        "Duration Trust: Linear scaling up to 5 years (60 months) of hands-on experience.",
        "Assessment Multiplier: Candidates who passed platform assessments receive a 1.25x trust boost."
    ]
    for f in formula_desc:
        pdf.multi_cell(117, 5.5, f"- {f}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(pdf.get_y() + 2)

    pdf.slide_footer()

    # -------------------------------------------------------------
    # SLIDE 5: Trajectories, Penalties & Traps
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.slide_header("Dimension Focus: Trajectory & Trap Protection")
    
    # Left Card: Career Trajectory
    card1_y = pdf.draw_card(20, 38, 120, 145, "Career Trajectory & Pedigree")
    pdf.set_xy(25, card1_y)
    pdf.set_font("helvetica", "", 10.5)
    pdf.set_text_color(203, 213, 225)
    
    trajectories = [
        "Title Relevance: Recency-weighted parsing matches roles like 'Senior AI Engineer' (1.0) down to 'HR Manager' (0.0).",
        "The Consulting Penalty: Entire careers spent at IT services/outsourcing firms (TCS, Infosys, Wipro, Accenture) trigger a severe 0.4x penalty.",
        "Product Rebound: The consulting penalty is released proportionally if the candidate transitioned into a product company.",
        "Job-Hopper Check: Average tenure under 12 months triggers a 0.7x penalty on the career score."
    ]
    for t in trajectories:
        pdf.multi_cell(110, 5.5, f"- {t}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(pdf.get_y() + 2.5)
        
    # Right Card: Honeypot & Skill-Stuffer Checks
    card2_y = pdf.draw_card(150, 38, 127, 145, "Trap & Honeypot Protection")
    pdf.set_xy(155, card2_y)
    
    traps = [
        "Honeypot Profiles: The dataset contains ~80 impossible resumes. We inspect dates to find impossible tenure timelines.",
        "Temporal Validation: If a candidate has worked at a company longer than it has existed, their profile is flagged.",
        "Skill-Stuffer Validation: If a candidate's skill duration exceeds their total professional experience, they are flagged.",
        "Hard Disqualification: All flagged profiles receive a hard cap of 0.0 composite score, keeping them out of the top-100 entirely."
    ]
    for t in traps:
        pdf.multi_cell(117, 5.5, f"- {t}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(pdf.get_y() + 2.5)

    pdf.slide_footer()

    # -------------------------------------------------------------
    # SLIDE 6: Performance, Verification & Impact
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.slide_header("Performance & Verification Results")
    
    # Left Card: Compute Metrics
    card1_y = pdf.draw_card(20, 38, 120, 145, "Compute & Efficiency Metrics")
    pdf.set_xy(25, card1_y)
    pdf.set_font("helvetica", "", 10.5)
    pdf.set_text_color(203, 213, 225)
    
    metrics = [
        "Throughput: Processed 100,000 candidates in 21.7 seconds (4,600+ candidates/second).",
        "RAM Usage: Under 100MB of RAM, utilizing memory-efficient JSONL line streaming.",
        "Zero GPU / Network: Ranks candidates completely offline without API dependencies or GPU hardware.",
        "Scalability: Designed to scale to million-row databases with ease on standard CPU instances."
    ]
    for m in metrics:
        pdf.multi_cell(110, 6, f"- {m}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(pdf.get_y() + 3)
        
    # Right Card: Compliance & Quality
    card2_y = pdf.draw_card(150, 38, 127, 145, "Compliance & shortlisting")
    pdf.set_xy(155, card2_y)
    
    compliance = [
        "Submission Validity: 100% compliant with the challenge rules (unique ranks 1-100, unique candidate IDs, non-increasing scores).",
        "Deterministic Tie-Breaking: In case of identical rounded scores, candidate IDs are sorted in ascending order.",
        "Honeypot Rate: 0.0% honeypots in the top-100 shortlist (disqualification rate is >10%).",
        "AI Reasoning: Shortlist includes a non-templated, factual, profile-derived rationale for every ranked row."
    ]
    for c in compliance:
        pdf.multi_cell(117, 6, f"- {c}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(pdf.get_y() + 3)

    pdf.slide_footer()

    # Write PDF
    pdf.output(output_path)
    print(f"Presentation PDF successfully created at: {output_path}")

if __name__ == "__main__":
    out_file = "D:\\H2S\\TrustRank_AI_Approach.pdf"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    create_deck(out_file)
