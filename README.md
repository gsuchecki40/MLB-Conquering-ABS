# When to Tap

XGBoost model analyzing the situational factors that drive MLB manager challenge decisions.

---

## Overview

Managers don't challenge calls randomly. Score, inning, count, and pitch context all shape the decision. This project uses XGBoost to surface which situational features most influence whether a manager will ask for a review, framing the problem as a classification task on a heavily imbalanced dataset (~100:1 non-challenge to challenge ratio).

The goal is to teach players when the correct context to challenge is.

---

## Model Performance

| Metric | Value |
|--------|-------|
| AUC | 0.901 |

An AUC of 0.90 means the model correctly ranks a challenged pitch above a non-challenged pitch 90% of the time — solid signal given that manager decisions are inherently noisy human judgments.

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

- **Class imbalance** handled via `scale_pos_weight` tuned to the observed class ratio
- **Eval metric:** `aucpr` (precision-recall AUC) — more informative than standard AUC for imbalanced problems
- **Threshold tuning** applied post-training to optimize the precision/recall tradeoff
- Model built and evaluated in R

---

## Repo Structure

```
check-the-call/
├── data/
├── R/
│   ├── model.R
│   └── features.R
├── outputs/
└── README.md
```

---

## Author

Grant Suchecki — MSBA, University of Notre Dame  
[GitHub](https://github.com/gsuchecki40) · [LinkedIn](https://linkedin.com/in/gsuchecki)
