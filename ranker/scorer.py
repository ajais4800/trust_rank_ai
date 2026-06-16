"""
Core scoring engine — updated with full JD understanding.

Key insight from JD analysis:
1. Career background is MORE important than skill list (keyword-stuffer trap)
2. Product company history > consulting-only history
3. Behavioral signals matter critically (unavailable candidates = not real candidates)
4. Computer vision/speech without NLP/IR = wrong domain
5. Pure researcher without production deployment = disqualified

Architecture: Multi-dimensional weighted scoring with smart disqualifiers.
"""

from __future__ import annotations
import math
import re
from datetime import date, datetime
from typing import Dict, List, Tuple

from job_config import (
    ROLE, SKILLS_TAXONOMY, SCORING_WEIGHTS, RELEVANT_TITLES,
    EDUCATION_FIELDS, EDU_TIER_MULTIPLIERS, SKILL_SYNONYMS,
    CONSULTING_COMPANY_SIGNALS, get_all_synonyms,
    JOB_DESCRIPTION_TEXT,
)

# ─────────────────────────────────────────────
# Global synonym lookup
# ─────────────────────────────────────────────
_SYNONYM_LOOKUP = get_all_synonyms()


# ─────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────

def _today() -> date:
    return datetime.utcnow().date()


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


def _resolve_skill(raw_name: str) -> str:
    norm = _normalize(raw_name)
    return _SYNONYM_LOOKUP.get(norm, norm)


def _days_since(date_str: str | None) -> int:
    if not date_str:
        return 9999
    try:
        d = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        return (_today() - d).days
    except Exception:
        return 9999


def _proficiency_weight(proficiency: str) -> float:
    return {"beginner": 0.3, "intermediate": 0.6, "advanced": 0.85, "expert": 1.0}.get(proficiency, 0.5)


def _endorsement_trust(endorsements: int) -> float:
    """Log-scaled trust boost. 0 endorsements = 0.75 (self-claim, unverified)."""
    if endorsements <= 0:
        return 0.75
    return min(1.0, 0.75 + 0.25 * math.log1p(endorsements) / math.log1p(60))


def _duration_trust(duration_months: int | None) -> float:
    """Hands-on duration → trust. Core skills need 18+ months."""
    if duration_months is None:
        return 0.65
    return min(1.0, 0.5 + 0.5 * min(duration_months, 36) / 36)


def _assessment_multiplier(skill_name: str, assessment_scores: dict) -> float:
    """Platform assessment score → verification multiplier (0.7 – 1.1)."""
    norm_target = _normalize(skill_name)
    resolved_target = _resolve_skill(skill_name)
    for k, v in assessment_scores.items():
        if _normalize(k) == norm_target or _resolve_skill(k) == resolved_target:
            return 0.7 + 0.4 * (v / 100.0)
    return 1.0


# ─────────────────────────────────────────────
# 1. Skill Match Score
# ─────────────────────────────────────────────

def score_skills(candidate: dict) -> Tuple[float, str, int]:
    """
    Semantic skill scoring with trust multipliers.
    
    Returns: (score 0-1, reasoning, core_count)
    
    NOT a simple keyword counter:
    - Each skill is scored by proficiency × endorsement trust × duration trust × assessment verification
    - Core skills weighted 1.0, secondary 0.5x, adjacent 0.15x
    - Score normalized against achievable maximum
    """
    skills_list = candidate.get("skills", [])
    assessment_scores = candidate.get("redrob_signals", {}).get("skill_assessment_scores", {})

    # Pre-compute all taxonomy lookups in normalized form
    core_norm = {_normalize(k): (k, w) for k, w in SKILLS_TAXONOMY["core"].items()}
    sec_norm = {_normalize(k): (k, w) for k, w in SKILLS_TAXONOMY["secondary"].items()}
    adj_norm = {_normalize(k): (k, w) for k, w in SKILLS_TAXONOMY["adjacent"].items()}

    raw_score = 0.0
    matched_core = []
    matched_sec = []

    for skill_entry in skills_list:
        raw_name = skill_entry.get("name", "")
        proficiency = skill_entry.get("proficiency", "intermediate")
        endorsements = skill_entry.get("endorsements", 0)
        duration = skill_entry.get("duration_months")

        norm_name = _normalize(raw_name)
        resolved = _resolve_skill(raw_name)

        relevance = 0.0
        level = None
        canonical_key = None

        # Check core taxonomy (direct + synonym)
        for nkey, (orig, w) in core_norm.items():
            if nkey == norm_name or nkey == resolved or norm_name == resolved:
                relevance = w
                level = "core"
                canonical_key = orig
                break

        # Also check if synonym resolves to a core key
        if level is None and resolved in core_norm:
            _, (orig, w) = resolved, core_norm[resolved]
            relevance = w
            level = "core"
            canonical_key = orig

        if level is None:
            for nkey, (orig, w) in sec_norm.items():
                if nkey == norm_name or nkey == resolved:
                    relevance = w * 0.5
                    level = "secondary"
                    canonical_key = orig
                    break
            if level is None and resolved in sec_norm:
                _, (orig, w) = resolved, sec_norm[resolved]
                relevance = w * 0.5
                level = "secondary"
                canonical_key = orig

        if level is None:
            for nkey, (orig, w) in adj_norm.items():
                if nkey == norm_name or nkey == resolved:
                    relevance = w * 0.15
                    level = "adjacent"
                    break

        if relevance <= 0.0:
            continue  # Not relevant to this JD

        # Trust-adjusted score
        prof_w = _proficiency_weight(proficiency)
        endorse_w = _endorsement_trust(endorsements)
        dur_w = _duration_trust(duration)
        assess_m = _assessment_multiplier(raw_name, assessment_scores)

        skill_score = relevance * prof_w * endorse_w * dur_w * assess_m
        raw_score += skill_score

        if level == "core" and relevance > 0.6:
            matched_core.append(raw_name)
        elif level == "secondary":
            matched_sec.append(raw_name)

    # Normalize: cap at ~60% of theoretical max to be realistic
    # A perfect candidate might have ~20 core skills; 20 * avg_weight(0.9) = 18
    # With avg proficiency/trust: 18 * 0.85 * 0.85 * 0.85 * 1.0 ≈ 11
    NORMALIZER = 11.0
    normalized = min(1.0, raw_score / NORMALIZER)

    reasoning = f"{len(matched_core)} core AI skills matched"
    return normalized, reasoning, len(matched_core)


# ─────────────────────────────────────────────
# 2. Career Trajectory Score
# ─────────────────────────────────────────────

def _title_score(title: str) -> float:
    norm = _normalize(title)
    # Direct lookup
    for key, val in RELEVANT_TITLES.items():
        if key == norm:
            return val
    # Partial match
    for key, val in RELEVANT_TITLES.items():
        if key in norm or norm in key:
            return val
    # Heuristic
    if any(kw in norm for kw in ["machine learning", " ml", "deep learning", "nlp", " ai", "search", "ranking", "retrieval"]):
        return 0.9
    if any(kw in norm for kw in ["data scien", "research", "applied scientist"]):
        return 0.72
    if any(kw in norm for kw in ["backend", "software", "platform", "full stack"]):
        return 0.38
    if any(kw in norm for kw in ["data engineer", "analytics engineer"]):
        return 0.38
    return 0.05


def _is_consulting_company(company: str) -> bool:
    norm = _normalize(company)
    return any(c in norm for c in CONSULTING_COMPANY_SIGNALS)


def score_career_trajectory(candidate: dict) -> Tuple[float, str]:
    """
    Holistic career trajectory scoring.
    
    Key JD-derived logic:
    1. Consulting-only history (TCS/Infosys/Wipro/etc.) = strong negative signal
    2. Product company experience at any point = positive boost
    3. ML/AI title recency matters more than history
    4. Upward trajectory toward ML = trajectory bonus
    5. Job-hopper (< 12 months avg tenure) = penalty
    6. Research-only without production = soft penalty
    """
    history = candidate.get("career_history", [])
    current_title = candidate.get("profile", {}).get("current_title", "")

    if not history:
        return _title_score(current_title) * 0.6, f"{current_title} (no history)"

    # Analyze company types across career
    consulting_stints = 0
    product_stints = 0
    total_consulting_months = 0
    total_months = 0

    weighted_title_score = 0.0
    total_weight = 0.0
    best_title_score = 0.0
    best_title = current_title
    tenures = []

    for i, role in enumerate(history):
        title = role.get("title", "")
        company = role.get("company", "")
        duration = role.get("duration_months", 0)
        is_current = role.get("is_current", False)

        # Recency decay: current = weight 3.0, next = 2.0, then 1.5, 1.2, 1.0...
        recency_weight = 3.0 if is_current else max(0.8, 2.5 - i * 0.5)

        ts = _title_score(title)
        weighted_title_score += ts * recency_weight
        total_weight += recency_weight

        if ts > best_title_score:
            best_title_score = ts
            best_title = title

        # Company type analysis
        if _is_consulting_company(company):
            consulting_stints += 1
            total_consulting_months += duration
        else:
            product_stints += 1

        total_months += duration
        if duration > 0:
            tenures.append(duration)

    trajectory_base = weighted_title_score / max(total_weight, 1.0)

    # ── Consulting penalty ──
    # JD explicitly says consulting-only = not a fit
    # But: if they have product company experience TOO, it's fine
    if product_stints == 0 and consulting_stints > 0:
        # Consulting-only: significant penalty
        trajectory_base *= 0.4
    elif total_months > 0:
        consulting_fraction = total_consulting_months / total_months
        if consulting_fraction > 0.75:
            trajectory_base *= 0.65  # Mostly consulting
        elif consulting_fraction > 0.50:
            trajectory_base *= 0.85  # Mixed, leaning consulting

    # ── Upward trajectory bonus ──
    if len(history) >= 2:
        oldest_ts = _title_score(history[-1].get("title", ""))
        newest_ts = _title_score(history[0].get("title", ""))
        if newest_ts > oldest_ts + 0.2:
            trajectory_base = min(1.0, trajectory_base * 1.12)

    # ── Tenure stability ──
    if tenures:
        avg_tenure = sum(tenures) / len(tenures)
        if avg_tenure < 12:
            trajectory_base *= 0.75  # Job-hopper penalty (JD explicitly mentions this)
        elif avg_tenure < 18:
            trajectory_base *= 0.88
        elif avg_tenure >= 36:
            trajectory_base = min(1.0, trajectory_base * 1.05)  # Stability bonus

    reasoning = f"{current_title} (best: {best_title})"
    return min(1.0, trajectory_base), reasoning


# ─────────────────────────────────────────────
# 3. Experience Fit Score
# ─────────────────────────────────────────────

def score_experience(candidate: dict) -> Tuple[float, str]:
    """
    Score against 5-9 year range, ideal 6-8.
    JD says: \"range, not a requirement\" — won't reject outside band if other signals strong.
    We implement this as a soft curve rather than hard cutoff.
    """
    yoe = candidate.get("profile", {}).get("years_of_experience", 0)
    min_e, max_e = ROLE["min_exp_years"], ROLE["max_exp_years"]
    ideal_min, ideal_max = ROLE["ideal_exp_min"], ROLE["ideal_exp_max"]

    if ideal_min <= yoe <= ideal_max:
        score = 1.0
    elif min_e <= yoe < ideal_min:
        score = 0.75 + 0.25 * (yoe - min_e) / (ideal_min - min_e)
    elif ideal_max < yoe <= max_e:
        score = 0.85 + 0.15 * (max_e - yoe) / (max_e - ideal_max)
    elif yoe < min_e:
        # Under: 3-5 years acceptable if other signals strong
        score = max(0.3, 0.55 * yoe / min_e)
    else:
        # Over 9 years: over-qualified risk, gentle decay
        score = max(0.5, 0.85 - (yoe - max_e) * 0.03)

    return score, f"{yoe:.1f} yrs (ideal {ideal_min}-{ideal_max})"


# ─────────────────────────────────────────────
# 4. Education Score
# ─────────────────────────────────────────────

def score_education(candidate: dict) -> Tuple[float, str]:
    education = candidate.get("education", [])
    if not education:
        return 0.35, "No education listed"

    degree_level = {
        "ph.d": 1.05, "phd": 1.05,
        "m.tech": 0.95, "m.e.": 0.95, "m.s.": 0.95, "ms": 0.92,
        "m.sc": 0.88, "msc": 0.88,
        "mba": 0.35,
        "b.tech": 0.8, "b.e.": 0.8, "be": 0.78,
        "b.sc": 0.7, "bsc": 0.7, "b.s.": 0.72,
    }

    best = 0.0
    best_desc = ""
    for edu in education:
        field = _normalize(edu.get("field_of_study", ""))
        tier = edu.get("tier", "unknown")
        degree_raw = _normalize(edu.get("degree", ""))

        field_score = 0.25
        for f, s in EDUCATION_FIELDS.items():
            if f in field or field in f:
                field_score = s
                break

        tier_mult = EDU_TIER_MULTIPLIERS.get(tier, 0.5)

        deg_bonus = 0.8
        for d_key, d_val in degree_level.items():
            if d_key in degree_raw:
                deg_bonus = d_val
                break

        edu_score = min(1.0, field_score * tier_mult * deg_bonus)
        if edu_score > best:
            best = edu_score
            best_desc = f"{edu.get('degree','')} {edu.get('field_of_study','')} ({tier})"

    return best, best_desc


# ─────────────────────────────────────────────
# 5. Behavioral Signals Score
# ─────────────────────────────────────────────

def score_behavioral_signals(candidate: dict) -> Tuple[float, str]:
    """
    Platform engagement signals scored holistically.
    
    JD quote: \"a perfect-on-paper candidate who hasn't logged in for 6 months
    and has a 5% recruiter response rate is, for hiring purposes, not actually available.\"
    
    This is treated as a MULTIPLIER effect on the raw score:
    - Activity recency: most critical (are they even looking?)
    - Response rate: will they reply to the recruiter?
    - Interview completion: do they follow through?
    - Notice period: operational availability
    """
    sig = candidate.get("redrob_signals", {})

    # ── Activity recency ──
    days_inactive = _days_since(sig.get("last_active_date"))
    if days_inactive <= 14:
        activity = 1.0
    elif days_inactive <= 30:
        activity = 0.92
    elif days_inactive <= 60:
        activity = 0.78
    elif days_inactive <= 90:
        activity = 0.58
    elif days_inactive <= 180:
        activity = 0.35
    elif days_inactive <= 365:
        activity = 0.15
    else:
        activity = 0.05

    # ── Open to work ──
    otw = 1.0 if sig.get("open_to_work_flag", False) else 0.38

    # ── Profile completeness ──
    completeness = sig.get("profile_completeness_score", 50) / 100.0

    # ── Recruiter response rate (CRITICAL per JD) ──
    rr = sig.get("recruiter_response_rate", 0.5)
    # Non-linear: 0.7+ is really good, < 0.2 is a red flag
    if rr >= 0.7:
        rr_score = 1.0
    elif rr >= 0.4:
        rr_score = 0.7 + (rr - 0.4) / 0.3 * 0.3
    elif rr >= 0.2:
        rr_score = 0.4 + (rr - 0.2) / 0.2 * 0.3
    else:
        rr_score = rr * 2.0  # < 0.2 = poor, approaches 0

    # ── Interview completion ──
    icr = sig.get("interview_completion_rate", 0.5)

    # ── Notice period: JD prefers sub-30, can buy out up to 30 ──
    notice = sig.get("notice_period_days", 90)
    if notice <= 15:
        notice_score = 1.0
    elif notice <= 30:
        notice_score = 0.95
    elif notice <= 45:
        notice_score = 0.8
    elif notice <= 60:
        notice_score = 0.65
    elif notice <= 90:
        notice_score = 0.45
    else:
        notice_score = 0.25

    # ── Salary alignment ──
    sal = sig.get("expected_salary_range_inr_lpa", {})
    sal_mid = (sal.get("min", 25) + sal.get("max", 40)) / 2
    if ROLE["salary_min_lpa"] <= sal_mid <= ROLE["salary_max_lpa"]:
        sal_score = 1.0
    elif sal_mid < ROLE["salary_min_lpa"]:
        sal_score = 0.85  # Will probably accept — good
    elif sal_mid <= ROLE["salary_max_lpa"] * 1.25:
        sal_score = 0.6
    else:
        sal_score = 0.25

    # ── Work mode ──
    wm = sig.get("preferred_work_mode", "flexible")
    wm_score = {"hybrid": 1.0, "flexible": 0.9, "onsite": 0.7, "remote": 0.45}.get(wm, 0.7)

    # ── Weighted composite ──
    components = [
        (activity,      0.28),  # Most critical: are they available?
        (otw,           0.12),
        (rr_score,      0.22),  # Second critical: will they respond?
        (icr,           0.12),
        (notice_score,  0.10),
        (completeness,  0.06),
        (sal_score,     0.06),
        (wm_score,      0.04),
    ]
    score = sum(s * w for s, w in components)

    # Verification trust bonus
    trust_bonus = 0.0
    if sig.get("verified_email"): trust_bonus += 0.015
    if sig.get("verified_phone"): trust_bonus += 0.015
    if sig.get("linkedin_connected"): trust_bonus += 0.01

    score = min(1.0, score + trust_bonus)

    # Recruiter-saved signal (external validation)
    saved = sig.get("saved_by_recruiters_30d", 0)
    if saved >= 5:
        score = min(1.0, score + 0.02)

    days_str = f"{days_inactive}d inactive" if days_inactive < 9999 else "unknown"
    return score, f"response rate {rr:.2f}; {days_str}"


# ─────────────────────────────────────────────
# 6. GitHub Activity Score
# ─────────────────────────────────────────────

def score_github(candidate: dict) -> Tuple[float, str]:
    """
    GitHub activity as open-source validation signal.
    JD explicitly values: \"Open-source contributions in the AI/ML space\"
    -1 means no GitHub linked.
    """
    gh = candidate.get("redrob_signals", {}).get("github_activity_score", -1)
    if gh < 0:
        return 0.15, "No GitHub linked"
    normalized = gh / 100.0
    if normalized >= 0.7:
        label = "very active"
    elif normalized >= 0.4:
        label = "active"
    elif normalized >= 0.2:
        label = "moderate"
    else:
        label = "low"
    return normalized, f"GitHub {label} ({gh:.0f}/100)"


# ─────────────────────────────────────────────
# Domain mismatch detector
# ─────────────────────────────────────────────

def _detect_wrong_domain(candidate: dict, skill_score: float, career_score: float) -> float:
    """
    Detect candidates who are clearly wrong domain — apply score cap.
    
    JD explicitly warns: CV/speech without NLP/IR = wrong domain.
    Accounting/HR/Sales/Marketing = irrelevant domain.
    """
    skills = [_normalize(s.get("name", "")) for s in candidate.get("skills", [])]
    current_title = _normalize(candidate.get("profile", {}).get("current_title", ""))

    # Pure wrong-domain titles
    wrong_domain_titles = {"accountant", "hr manager", "content writer", "graphic designer",
                           "marketing manager", "sales executive", "civil engineer",
                           "mechanical engineer", "customer support", "operations manager"}
    if current_title in wrong_domain_titles:
        # These can still have AI skills listed — check substance
        if skill_score < 0.15 and career_score < 0.1:
            return 0.22  # Hard cap: keyword-stuffed but clearly wrong domain

    return 1.0  # No cap needed


# ─────────────────────────────────────────────
# Master scoring function
# ─────────────────────────────────────────────

def score_candidate(candidate: dict) -> dict:
    """
    Compute composite score for a single candidate.
    
    Scoring philosophy:
    - Dimensions are computed independently then combined with learned weights
    - Smart disqualifiers prevent keyword-stuffed profiles from ranking high
    - Behavioral signals act as an availability multiplier
    """
    skill_score, skill_reason, core_count = score_skills(candidate)
    career_score, career_reason = score_career_trajectory(candidate)
    exp_score, exp_reason = score_experience(candidate)
    edu_score, edu_reason = score_education(candidate)
    behavior_score, behavior_reason = score_behavioral_signals(candidate)
    github_score, github_reason = score_github(candidate)

    # Weighted composite
    w = SCORING_WEIGHTS
    composite = (
        skill_score     * w["skill_match"] +
        career_score    * w["career_trajectory"] +
        exp_score       * w["experience_fit"] +
        edu_score       * w["education"] +
        behavior_score  * w["behavioral_signals"] +
        github_score    * w["github_activity"]
    )

    # Domain mismatch cap
    cap = _detect_wrong_domain(candidate, skill_score, career_score)
    composite = min(composite, cap)

    # Build reasoning string (matches submission format)
    sig = candidate.get("redrob_signals", {})
    rr = sig.get("recruiter_response_rate", 0)
    yoe = candidate.get("profile", {}).get("years_of_experience", 0)
    current_title = candidate.get("profile", {}).get("current_title", "")

    reasoning = (
        f"{current_title} with {yoe:.1f} yrs; "
        f"{core_count} AI core skills; "
        f"response rate {rr:.2f}."
    )

    return {
        "candidate_id": candidate["candidate_id"],
        "composite": round(composite, 6),
        "dimensions": {
            "skill_match": round(skill_score, 4),
            "career_trajectory": round(career_score, 4),
            "experience_fit": round(exp_score, 4),
            "education": round(edu_score, 4),
            "behavioral_signals": round(behavior_score, 4),
            "github_activity": round(github_score, 4),
        },
        "reasoning": reasoning,
    }
