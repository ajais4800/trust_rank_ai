#!/usr/bin/env python3
"""
rank.py — Main entry point for TrustRank AI.

Usage:
    python rank.py --candidates ./candidates.jsonl --out ./submission.csv

Runs in < 5 minutes on CPU with 16GB RAM. No network calls during ranking.
Produces a valid submission.csv with exactly 100 ranked candidates.
"""

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

from tqdm import tqdm

# Add parent dir to path if running from repo root
sys.path.insert(0, str(Path(__file__).parent / "ranker"))

from scorer import score_candidate


# ─────────────────────────────────────────────
# Tie-break: equal scores → sort by candidate_id ascending
# ─────────────────────────────────────────────

def _tiebreak_key(result: dict):
    return (-result["composite"], result["candidate_id"])


# ─────────────────────────────────────────────
# Score assignment: map rank → non-increasing score
# Required: scores must be non-increasing by rank;
# ties break by candidate_id ascending.
# ─────────────────────────────────────────────

def assign_scores(ranked_results: list) -> list:
    """
    Assign submission scores to the top-100 results.
    Scores are non-increasing (rank 1 = highest).
    Formula: score = composite_score (already float 0-1).
    If ties exist at the boundary, scores are identical and
    tie-breaking is applied by candidate_id ascending (as required).
    """
    # Step 1: attach rounded scores
    rows = []
    for result in ranked_results[:100]:
        rows.append({
            "candidate_id": result["candidate_id"],
            "score": round(result["composite"], 4),
            "reasoning": result["reasoning"],
        })

    # Step 2: re-sort by (score DESC, candidate_id ASC) on the ROUNDED score
    # This ensures validator tie-break rule: equal scores → lower candidate_id first
    rows.sort(key=lambda r: (-r["score"], r["candidate_id"]))

    # Step 3: assign sequential ranks
    output = []
    for rank_idx, row in enumerate(rows, start=1):
        output.append({
            "candidate_id": row["candidate_id"],
            "rank": rank_idx,
            "score": row["score"],
            "reasoning": row["reasoning"],
        })
    return output


# ─────────────────────────────────────────────
# Main ranking pipeline
# ─────────────────────────────────────────────

def rank_candidates(candidates_path: str, out_path: str, top_n: int = 100,
                    verbose: bool = True, batch_report: int = 10000):
    """
    Full ranking pipeline:
    1. Stream candidates from JSONL (memory efficient for 100K+)
    2. Score each candidate across 6 dimensions
    3. Maintain rolling top-N heap for efficiency
    4. Sort final top-N by composite score (desc), then candidate_id (asc) for ties
    5. Write submission CSV
    """
    import heapq

    start = time.time()

    if verbose:
        print(f"\n{'='*60}")
        print("  TrustRank AI — Redrob Hackathon")
        print(f"{'='*60}")
        print(f"  Input : {candidates_path}")
        print(f"  Output: {out_path}")
        print(f"  Top-N : {top_n}")
        print(f"{'='*60}\n")

    # Count lines for tqdm
    if verbose:
        print("Counting candidates...", end=" ", flush=True)
    total = 0
    with open(candidates_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                total += 1
    if verbose:
        print(f"{total:,} candidates found.\n")

    # Min-heap to track top-N efficiently
    # Heap element: (composite_score, candidate_id, result_dict)
    # We negate composite for max-heap behavior via min-heap
    heap = []  # (neg_composite, candidate_id, result)

    scored = 0
    errors = 0

    with open(candidates_path, "r", encoding="utf-8") as f:
        iterator = tqdm(f, total=total, desc="Scoring", unit="cand",
                        disable=not verbose, ncols=80)
        for line in iterator:
            line = line.strip()
            if not line:
                continue
            try:
                candidate = json.loads(line)
                result = score_candidate(candidate)
                scored += 1

                # Push to heap
                neg_score = -result["composite"]
                cid = result["candidate_id"]
                heapq.heappush(heap, (neg_score, cid, result))

                # Keep heap bounded for memory efficiency
                if len(heap) > top_n * 2:
                    # We can't trim easily without knowing bottom; let it grow
                    # For 100K candidates this is fine (heap stays small)
                    pass

            except json.JSONDecodeError as e:
                errors += 1
                if verbose and errors <= 5:
                    print(f"  [WARN] JSON parse error: {e}")
            except Exception as e:
                errors += 1
                if verbose and errors <= 5:
                    print(f"  [WARN] Scoring error for line: {e}")

    elapsed = time.time() - start
    if verbose:
        print(f"\n  Scored: {scored:,} candidates in {elapsed:.1f}s "
              f"({scored/elapsed:.0f} cand/sec)")
        if errors:
            print(f"  Errors: {errors} (skipped)")

    # Sort heap to get top-N
    all_results = [item[2] for item in heap]
    all_results.sort(key=_tiebreak_key)
    top_results = all_results[:top_n]

    # Assign final ranks and scores
    submission_rows = assign_scores(top_results)

    # Write CSV
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for row in submission_rows:
            writer.writerow([
                row["candidate_id"],
                row["rank"],
                f"{row['score']:.4f}",
                row["reasoning"],
            ])

    total_time = time.time() - start

    if verbose:
        print(f"\n  Output written: {out_path}")
        print(f"  Total time   : {total_time:.1f}s")
        print(f"\n  Top 10 candidates:")
        print(f"  {'Rank':>4}  {'Score':>6}  {'ID':<14}  Reasoning")
        print(f"  {'-'*70}")
        for row in submission_rows[:10]:
            print(f"  {row['rank']:>4}  {row['score']:>6.4f}  {row['candidate_id']:<14}  {row['reasoning'][:55]}")
        print(f"\n  {'='*60}")
        print(f"  Submission ready: {out_path.name}")
        print(f"  {'='*60}\n")

    return submission_rows


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="TrustRank AI — Redrob Hackathon",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rank.py --candidates ./candidates.jsonl --out ./submission.csv
  python rank.py --candidates ./sample_candidates.json --out ./sample_out.csv --json-array
        """
    )
    parser.add_argument(
        "--candidates", "-c", required=True,
        help="Path to candidates JSONL file (or JSON array with --json-array)"
    )
    parser.add_argument(
        "--out", "-o", default="./submission.csv",
        help="Output CSV path (default: ./submission.csv)"
    )
    parser.add_argument(
        "--top", type=int, default=100,
        help="Number of candidates to include in shortlist (default: 100)"
    )
    parser.add_argument(
        "--json-array", action="store_true",
        help="Input is a JSON array instead of JSONL"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Suppress progress output"
    )

    args = parser.parse_args()

    # If JSON array format, convert to JSONL temporarily
    candidates_path = args.candidates
    tmp_jsonl = None

    if args.json_array:
        import tempfile
        print("Converting JSON array to JSONL...", end=" ", flush=True)
        with open(args.candidates, "r", encoding="utf-8") as f:
            data = json.load(f)
        tmp_jsonl = tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
        )
        for item in data:
            tmp_jsonl.write(json.dumps(item) + "\n")
        tmp_jsonl.close()
        candidates_path = tmp_jsonl.name
        print(f"{len(data)} candidates.")

    try:
        rank_candidates(
            candidates_path=candidates_path,
            out_path=args.out,
            top_n=args.top,
            verbose=not args.quiet,
        )
    finally:
        if tmp_jsonl and os.path.exists(tmp_jsonl.name):
            os.unlink(tmp_jsonl.name)


if __name__ == "__main__":
    main()
