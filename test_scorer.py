import sys, json
sys.path.insert(0, r'D:\H2S\ranker')
from scorer import score_candidate

with open(r'D:\H2S\data\[PUB] India_runs_data_and_ai_challenge\India_runs_data_and_ai_challenge\sample_candidates.json', encoding='utf-8') as f:
    samples = json.load(f)

results = [score_candidate(c) for c in samples[:30]]
results.sort(key=lambda x: (-x['composite'], x['candidate_id']))

print("Top 10 of 30 sample candidates:")
for i, r in enumerate(results[:10], 1):
    dims = r['dimensions']
    print(f"{i:>2}. {r['candidate_id']} | score={r['composite']:.4f} | {r['reasoning'][:75]}")
    print(f"     skill={dims['skill_match']:.3f} career={dims['career_trajectory']:.3f} exp={dims['experience_fit']:.3f} edu={dims['education']:.3f} behav={dims['behavioral_signals']:.3f} gh={dims['github_activity']:.3f}")
print("\nScorer OK!")
