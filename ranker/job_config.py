"""
Job configuration for the Redrob AI Hackathon challenge.
Role: Senior AI Engineer — Founding Team at Redrob AI
Location: Pune/Noida, India (Hybrid)
Experience: 5-9 years (ideal: 6-8 years)

This module encodes DEEP understanding of the JD —
not just keywords but the actual intent and anti-patterns.
"""

# ============================================================
# JOB DESCRIPTION TEXT (for semantic embedding comparison)
# ============================================================
JOB_DESCRIPTION_TEXT = """
Senior AI Engineer — Founding Team at Redrob AI (Series A AI-native talent intelligence platform).
Pune/Noida India Hybrid. 5-9 years experience.

Core mandate: own the intelligence layer of Redrob's product — ranking, retrieval, and matching systems.
Build v2 ranking system using embeddings, hybrid retrieval, and LLM-based re-ranking.

MUST HAVE:
- Production experience with embeddings-based retrieval systems (sentence-transformers, OpenAI embeddings, BGE, E5)
- Production experience with vector databases or hybrid search (Pinecone, Weaviate, Qdrant, Milvus, OpenSearch, FAISS, Elasticsearch)
- Strong Python — code quality matters
- Hands-on evaluation frameworks for ranking systems: NDCG, MRR, MAP, A/B testing
- LLMs, fine-tuning, transformer architectures, semantic search, NLP

NICE TO HAVE:
- LLM fine-tuning (LoRA, QLoRA, PEFT)
- Learning-to-rank models (XGBoost-based or neural)
- Distributed systems or large-scale inference optimization
- Open-source contributions in AI/ML
- RAG pipeline design

NOT A FIT:
- Pure research without production deployment
- Only recent LangChain/API wrapper experience without pre-LLM ML background
- Consulting-only background (TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini) with no product company
- Pure computer vision/speech without NLP/IR exposure
- Title-chasers with short tenures
- Only worked on closed-source systems with no external validation

IDEAL CANDIDATE:
- 6-8 years total experience, 4-5 in applied ML/AI at PRODUCT companies (not services)
- Shipped at least one ranking/search/recommendation system to real users at scale
- Active on job market (logged in recently, good response rate)
- Located in or willing to relocate to Noida/Pune; Hyderabad, Mumbai, Delhi NCR also ok
- Sub-30-day notice preferred (can buy out up to 30 days)
"""

# ============================================================
# ROLE STRUCTURED REQUIREMENTS
# ============================================================
ROLE = {
    "title": "Senior AI Engineer",
    "company": "Redrob AI",
    "domain": "AI/ML — Embeddings, Retrieval, Ranking, LLMs",
    "locations": ["Pune", "Noida", "Hyderabad", "Mumbai", "Delhi", "Delhi NCR", "Bengaluru", "Bangalore"],
    "country": "India",
    "work_mode": "hybrid",
    "min_exp_years": 5,
    "max_exp_years": 9,
    "ideal_exp_min": 6,
    "ideal_exp_max": 8,
    "salary_min_lpa": 20,   # Not stated explicitly but Series A startup
    "salary_max_lpa": 60,
    "notice_preferred_days": 30,   # Sub-30 day ideal, up to 30 buyout
    "notice_max_days": 90,
    "seniority": "senior",
    # Product company experience is CRITICAL — consulting-only is disqualifying
    "product_company_required": True,
}

# ============================================================
# PURE CONSULTING COMPANIES (signals negative for this role)
# These are explicitly mentioned in the JD as bad fits
# ============================================================
CONSULTING_COMPANY_SIGNALS = {
    "tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini",
    "hcl", "hexaware", "mphasis", "tech mahindra", "l&t infotech",
    "ltimindtree", "mindtree",  # acquired by L&T, still services
    "persistent systems", "coforge",
}

# ============================================================
# PRODUCT COMPANY SIGNALS (positive for this role)
# ============================================================
PRODUCT_COMPANY_SIGNALS = {
    "google", "meta", "amazon", "microsoft", "apple", "netflix", "uber",
    "flipkart", "meesho", "swiggy", "zomato", "razorpay", "cred", "zepto",
    "phonepe", "paytm", "nykaa", "sharechat", "slice", "setu", "khatabook",
    "licious", "dunzo", "ola", "rapido", "dream11", "unacademy", "byju",
    "freshworks", "zoho", "browserstack", "postman", "hasura", "chargebee",
    "startup", "ai", "tech",  # broad positive signals
}

# ============================================================
# SKILLS TAXONOMY
# Levels: core (must-have), secondary (nice-to-have), adjacent (weak signal)
# ============================================================
SKILLS_TAXONOMY = {
    "core": {
        # === Retrieval & Embeddings (PRIMARY FOCUS) ===
        "embeddings": 1.0,
        "semantic search": 1.0,
        "vector search": 1.0,
        "retrieval": 1.0,
        "sentence transformers": 1.0,
        "sentence-transformers": 1.0,
        "faiss": 1.0,
        "milvus": 1.0,
        "pinecone": 1.0,
        "weaviate": 1.0,
        "qdrant": 0.95,
        "opensearch": 0.9,
        "elasticsearch": 0.85,
        "vector databases": 1.0,
        "hybrid search": 1.0,
        "dense retrieval": 0.95,
        "bm25": 0.85,
        "rag": 1.0,

        # === LLMs & NLP (CORE) ===
        "nlp": 1.0,
        "llm": 1.0,
        "large language models": 1.0,
        "transformers": 1.0,
        "bert": 0.9,
        "gpt": 0.9,
        "llama": 0.9,
        "t5": 0.85,
        "fine-tuning llms": 1.0,
        "lora": 0.95,
        "qlora": 0.95,
        "peft": 0.95,
        "fine tuning": 0.9,
        "language models": 0.9,
        "text classification": 0.85,
        "named entity recognition": 0.8,
        "information retrieval": 0.95,

        # === ML Infrastructure / Production (MUST-HAVE) ===
        "python": 1.0,
        "pytorch": 0.95,
        "tensorflow": 0.85,
        "ranking systems": 1.0,
        "recommendation systems": 0.9,
        "learning to rank": 0.95,
        "ndcg": 0.9,
        "mrr": 0.85,
        "map": 0.8,
        "a/b testing": 0.85,
        "model evaluation": 0.9,
        "experiment tracking": 0.8,
        "mlflow": 0.8,
        "weights & biases": 0.8,
        "docker": 0.75,
        "kubernetes": 0.75,
        "fastapi": 0.75,
        "bentoml": 0.8,
        "aws": 0.75,
        "gcp": 0.75,
        "mlops": 0.85,
    },
    "secondary": {
        # Nice-to-haves
        "speech recognition": 0.4,  # NOT primary focus per JD
        "tts": 0.4,
        "image classification": 0.35,
        "object detection": 0.35,
        "gans": 0.4,
        "computer vision": 0.35,
        "deepspeed": 0.75,
        "distributed training": 0.75,
        "apache beam": 0.5,
        "airflow": 0.5,
        "spark": 0.45,
        "feature engineering": 0.6,
        "statistical modeling": 0.55,
        "xgboost": 0.7,
        "statistical analysis": 0.5,
        "databricks": 0.5,
        "kafka": 0.45,
        "dvc": 0.65,
        "kubeflow": 0.65,
        "triton": 0.65,
        "open source": 0.7,
    },
    "adjacent": {
        # Weak or negative signals
        "sql": 0.35,
        "flask": 0.4,
        "react": 0.05,
        "node.js": 0.05,
        "javascript": 0.05,
        "typescript": 0.05,
        "photoshop": 0.0,
        "excel": 0.05,
        "accounting": 0.0,
        "sap": 0.0,
        "six sigma": 0.0,
        "marketing": 0.0,
        "hr": 0.0,
        "content writing": 0.0,
        "seo": 0.0,
        "solidworks": 0.0,
        "ansys": 0.0,
        "cad": 0.0,
    },
}

# ============================================================
# CAREER TITLE RELEVANCE
# Key JD insight: product company ML engineer > keyword-stuffed titles
# ============================================================
RELEVANT_TITLES = {
    # Tier 1: Direct match (1.0)
    "senior ai engineer": 1.0,
    "senior machine learning engineer": 1.0,
    "senior ml engineer": 1.0,
    "ai engineer": 0.95,
    "machine learning engineer": 0.95,
    "ml engineer": 0.95,
    "nlp engineer": 1.0,
    "deep learning engineer": 0.9,
    "search engineer": 0.95,
    "ranking engineer": 1.0,
    "retrieval engineer": 1.0,
    "applied scientist": 0.85,
    "applied ml scientist": 0.9,
    "research engineer": 0.85,
    "ml researcher": 0.85,

    # Tier 2: Adjacent (0.5-0.75)
    "data scientist": 0.7,
    "senior data scientist": 0.75,
    "backend engineer": 0.45,
    "software engineer": 0.4,
    "data engineer": 0.45,
    "platform engineer": 0.4,
    "analytics engineer": 0.35,
    "junior ml engineer": 0.65,

    # Tier 3: Weak signal (0.1-0.2)
    "project manager": 0.08,
    "business analyst": 0.12,
    "product manager": 0.12,
    "full stack": 0.25,
    "devops": 0.2,

    # Tier 4: Disqualifying (<0.1)
    "operations manager": 0.04,
    "hr manager": 0.0,
    "accountant": 0.0,
    "content writer": 0.05,
    "graphic designer": 0.0,
    "marketing manager": 0.03,
    "sales executive": 0.0,
    "civil engineer": 0.08,
    "mechanical engineer": 0.08,
    "customer support": 0.0,
}

# ============================================================
# SCORING WEIGHTS (must sum to 1.0)
# Tuned to match JD priorities:
# 1. Career trajectory is #1 signal (right background > keywords)
# 2. Skill quality with depth matters more than count
# 3. Behavioral signals separate available vs unavailable
# ============================================================
SCORING_WEIGHTS = {
    "skill_match": 0.30,       # Deep technical skills w/ trust multipliers
    "career_trajectory": 0.30, # Role relevance + product vs consulting arc
    "experience_fit": 0.12,    # Years in 5-9 range
    "education": 0.07,         # CS/ML field + tier
    "behavioral_signals": 0.15,# Platform signals — availability is key
    "github_activity": 0.06,   # Open-source validation
}

# ============================================================
# EDUCATION FIELD RELEVANCE
# ============================================================
EDUCATION_FIELDS = {
    "computer science": 1.0,
    "machine learning": 1.0,
    "artificial intelligence": 1.0,
    "data science": 0.95,
    "computational linguistics": 0.95,
    "statistics": 0.85,
    "mathematics": 0.8,
    "information retrieval": 1.0,
    "electronics": 0.65,
    "electrical engineering": 0.6,
    "information technology": 0.7,
    "software engineering": 0.9,
    "physics": 0.55,
    "chemical engineering": 0.15,
    "mechanical engineering": 0.15,
    "civil engineering": 0.08,
    "business": 0.08,
    "commerce": 0.04,
    "accounting": 0.0,
    "marketing": 0.04,
    "human resources": 0.0,
    "electronics and communication": 0.6,
    "electronics and telecommunication": 0.55,
}

EDU_TIER_MULTIPLIERS = {
    "tier_1": 1.0,
    "tier_2": 0.82,
    "tier_3": 0.62,
    "tier_4": 0.42,
    "unknown": 0.5,
}

# ============================================================
# SEMANTIC SYNONYM MAP
# Maps alternate skill names → canonical taxonomy keys
# ============================================================
SKILL_SYNONYMS = {
    "embeddings": ["embedding", "text embeddings", "word embeddings", "sentence embeddings",
                   "dense embeddings", "bi-encoder", "biencoder"],
    "sentence-transformers": ["sbert", "sentence bert", "sentence transformers"],
    "faiss": ["facebook ai similarity search"],
    "rag": ["retrieval augmented generation", "retrieval-augmented generation", "retrieval augmented"],
    "vector databases": ["vector db", "vector store", "vectordb", "vector database"],
    "semantic search": ["semantic retrieval", "dense retrieval", "neural search"],
    "fine-tuning llms": ["llm fine-tuning", "llm finetuning", "fine tuning llm",
                         "fine-tune", "fine tune", "model fine tuning", "sft"],
    "lora": ["low-rank adaptation", "low rank adaptation"],
    "qlora": ["quantized lora", "quantised lora"],
    "peft": ["parameter efficient fine tuning", "parameter-efficient fine-tuning"],
    "pytorch": ["torch", "pytorch lightning", "pl"],
    "tensorflow": ["tf", "keras", "tensorflow 2"],
    "nlp": ["natural language processing", "text processing", "language models", "natural language"],
    "transformers": ["huggingface", "hugging face", "hf transformers", "hf", "huggingface transformers"],
    "bert": ["roberta", "distilbert", "electra", "albert", "xlnet"],
    "gpt": ["gpt-2", "gpt-3", "gpt-4", "chatgpt", "openai"],
    "llama": ["llama 2", "llama2", "mistral", "falcon", "gemma", "phi"],
    "weights & biases": ["wandb", "w&b", "weights and biases"],
    "mlflow": ["ml flow", "ml-flow"],
    "learning to rank": ["ltr", "ranknet", "lambdamart", "listwise", "pairwise ranking"],
    "recommendation systems": ["recommender system", "recsys", "collaborative filtering", "content-based filtering"],
    "ranking systems": ["ranking model", "ranker", "re-ranking", "reranking"],
    "hybrid search": ["hybrid retrieval", "bm25 + dense", "sparse-dense"],
    "distributed training": ["deepspeed", "megatron", "fsdp", "model parallelism", "data parallelism"],
    "speech recognition": ["asr", "automatic speech recognition", "whisper"],
    "tts": ["text to speech", "text-to-speech", "voice synthesis", "speech synthesis"],
    "gans": ["generative adversarial network", "generative adversarial"],
    "a/b testing": ["ab testing", "split testing", "online experiments"],
    "ndcg": ["normalized discounted cumulative gain", "nDCG", "dcg"],
    "mrr": ["mean reciprocal rank"],
    "map": ["mean average precision"],
    "open source": ["opensource", "github", "open-source contributions"],
    "kubernetes": ["k8s", "kube"],
    "docker": ["containerization", "containers"],
    "fastapi": ["fast api"],
    "opensearch": ["open search"],
    "elasticsearch": ["elastic search"],
}

def get_all_synonyms() -> dict:
    """Return lowercase-normalized reverse synonym map."""
    import re
    lookup = {}
    def norm(t):
        return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()
    for canonical, aliases in SKILL_SYNONYMS.items():
        lookup[norm(canonical)] = norm(canonical)
        for alias in aliases:
            lookup[norm(alias)] = norm(canonical)
    return lookup
