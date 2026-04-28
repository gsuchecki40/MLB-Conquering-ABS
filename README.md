# Conquering ABS

XGBoost model analyzing the situational factors that drive MLB manager challenge decisions.

---

## Overview

Since MLB introduced the Automated Ball-Strike challenge system, managers have had to make real-time decisions: tap your wrist or let the call stand. Score, inning, count, and pitch context all shape that decision — and the data shows it.

This project uses XGBoost to surface which situational features most influence whether a manager will challenge a call, framing it as a classification task on a heavily imbalanced dataset (~100:1 non-challenge to challenge ratio).



---

## Model Performance

| Metric | Value |
|--------|-------|
| AUC | 0.901 |

An AUC of 0.90 means the model correctly ranks a challenged pitch above a non-challenged pitch 90% of the time — solid signal given that manager decisions are inherently noisy human judgments made in seconds.

---

## Key Features (by XGBoost Gain)

| Feature | Importance |
|---------|------------|
| Score Differential | 27.8% |
| Inning | 23.7% |
| Pre-Strikes | 14.7% |
| Pitch Number | 12.3% |
| Pre-Outs | 11.4% |
| Pre-Balls | 10.3% |

---

## Technical Notes

- **Class imbalance** handled via `scale_pos_weight` tuned to the observed ~100:1 class ratio
- **Eval metric:** `aucpr` (precision-recall AUC) — more informative than standard AUC for heavily imbalanced problems
- **Threshold tuning** applied post-training to find the precision/recall sweet spot
- Data pulled via Python (Statcast / pybaseball), model built and evaluated in R

---

## Repo Structure

```
MLB-Conquering-ABS/
├── data/
├── output/
├── DataPull.py               # Statcast data ingestion
├── PitchPlots.py             # Pitch visualization
├── Baseball.Rmd              # Main modeling notebook
├── Sabermetrics.Rmd          # Supporting sabermetric analysis
├── download_abs_challenge_data.R
├── Baseball.Rproj
└── README.md
```

---

## Author

Grant Suchecki — MSBA Candidate, University of Notre Dame  
[GitHub](https://github.com/gsuchecki40) · [LinkedIn](https://linkedin.com/in/grantsuchecki)
