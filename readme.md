# Redrob Hackathon v4 — Intelligent Candidate Ranking

> **Team:** khikhi
> **Sandbox:** [Run in Colab](https://colab.research.google.com/drive/1gv1xVAySIs5fgwDEPZz2SYXg2jhe5-Ia?usp=sharing)
> **Metadata & AI declarations:** see `submission_metadata.yaml` in repo root

---

## Quickstart (Stage 3 reproduction)

```bash
git clone https://github.com/Miltonbottle/DataLoader.git
cd DataLoader
pip install -r requirements.txt
```

> **Data placement:** Place `candidates.jsonl` (or `candidates.jsonl.gz`) and `job_description.md` inside the `/data` folder before running.

> **Precomputed embeddings are already in the repo via Git LFS** — no need to rerun precomputation. If `precomputed/embeddings.npy` didn't download, run `git lfs pull`.

**Run ranking (~60–130s on CPU):**
```bash
# Uncompressed
python src/rank.py --candidates ./data/candidates.jsonl --jd ./data/job_description.md --precomputed ./precomputed --out ./outputs/submission.csv

# Gzipped
python src/rank.py --candidates ./data/candidates.jsonl.gz --jd ./data/job_description.md --precomputed ./precomputed --out ./outputs/submission.csv
```

**Validate:**
```bash
python validate_submission.py ./outputs/submission.csv
```

**Optional — rerun precomputation from scratch (~25 min, not required):**
```bash
python src/precompute_embeddings.py --candidates ./data/candidates.jsonl --jd ./data/job_description.md --out_dir ./precomputed
```

---

## Architecture tl;dr

- **Precomputation (offline):** All 100K candidates vectorized using `all-MiniLM-L6-v2` and saved to `precomputed/embeddings.npy` — zero encoding overhead at ranking time
- **Pass 1 — Heuristic funnel (~25s):** O(1) string-blob matching drops ~97K candidates instantly via hard gates (honeypots, ghosts, location) and 7 JD trap penalties (LangChain tourist, title chaser, pure consulting, hands-off architect, CV-without-NLP, keyword stuffer, pure research)
- **Pass 2 — Semantic re-ranking (~60s):** Single vectorised NumPy cosine similarity matrix op across all survivors; final score = `semantic×0.45 + heuristic×0.45 + behavioral×0.10` across 9 Redrob platform signals

---

## Repo structure

```
DataLoader/
├── src/
│   ├── rank.py                    # Main pipeline runner
│   ├── feature_extractor.py       # Pass 1 heuristics + JD trap detection
│   ├── composite_scorer.py        # Scoring, blending, reasoning generation
│   ├── semantic_ranker.py         # Pass 2 semantic re-ranker (live mode fallback)
│   └── precompute_embeddings.py   # One-time offline embedding generator
├── data/                          # ← place candidates.jsonl + job_description.md here
│   ├── job_description.md
│   └── sample_candidates.json     # 50-candidate sample for sandbox
├── precomputed/                   # Git LFS — downloads automatically on clone
│   ├── embeddings.npy             # 100K candidate embeddings (~153MB)
│   ├── candidate_ids.json
│   └── jd_embedding.npy
├── outputs/
│   └── khikhi.csv                 # Final submission CSV
├── scripts/
│   └── show_top10.py              # Debug helper — prints top 10 ranked candidates
├── docs/
│   └── EXECUTION_GUIDE.md         # Detailed execution notes
├── README.md
├── requirements.txt
├── submission_metadata.yaml
└── validate_submission.py
```

---

## Compute constraints

| Constraint | Limit | Our usage |
|---|---|---|
| Runtime | ≤5 min | ~60–130s |
| RAM | ≤16GB | ~4–6GB |
| GPU | Not allowed | CPU only |
| Network | Not allowed | No API calls during ranking |
| Disk | ≤5GB | ~153MB (embeddings) |

---

## Dependencies

```
sentence-transformers==2.7.0
numpy>=1.24.0
pandas>=2.0.0
python-docx>=1.1.0
```

---

## AI tools declared

Claude (primary), Gemini (secondary), ChatGPT (minor debugging). Full declaration in `submission_metadata.yaml`. No candidate data sent to any external API.
