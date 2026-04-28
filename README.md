# MLB-Conquering-ABS

XGBoost model analyzing the situational factors that drive MLB manager challenge decisions under the new Automated Ball-Strike (ABS) system.

---

## Overview

The ABS challenge system is new to MLB full-time in 2026. Players get two challenges per game — lose one, it's gone. Teams cannot signal to players when to challenge (the Milwaukee Brewers were warned to stop doing exactly that), meaning players need to understand the right game context on their own.

This project doesn't try to predict whether a call will be overturned. It analyzes what game context warrants burning a challenge in the first place, using XGBoost and logistic regression on Statcast pitch-by-pitch data.

---

## Data

- Source: sabRmetrics R package (Powers, 2024)
- Coverage: 2026 MLB season through April 20th
- Size: 100,000+ pitches, ~993 challenged
- Class imbalance: ~100:1 non-challenge to challenge ratio
- Features: pre-pitch balls, strikes, outs, inning, score differential, pitch number

---

## Methods

**Logistic Regression** — established the linear pattern. Inning was the most significant variable, confirming that smarter teams hold challenges for late-game, high-leverage situations. Balls, outs, and pitch number also showed significance.

**XGBoost** — captured full game context. `scale_pos_weight` was tuned to the observed ~100:1 class ratio to correct for imbalance. `aucpr` used as the eval metric — more informative than standard AUC on heavily skewed data. SHAP values used for interpretability.

---

## Model Performance

| Metric | Value |
|--------|-------|
| AUC-PR | 0.901 |
| Accuracy | ~73% |

An AUC-PR of 0.90 means the model correctly ranks a challenged pitch above a non-challenged pitch 90% of the time. The 10% it misses represents challenges made in genuinely unusual game contexts.

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

Game context dominates. The model leans on the full game state before considering pitch-level detail.

---

## Actionable Lessons for Players

**1. Be patient.** Save challenges for late innings. High-leverage, high-pressure situations are where a blown call actually costs you.

**2. Read the score.** Score differential is the #1 feature. Tight games warrant more challenges. Don't burn one in a blowout — unless you're mounting a comeback.

**3. Flip walks, not strikeouts.** Players challenge most to flip strikes into walks. A 3-2 count flipped to a walk is productive. Extending an at-bat only to strike out on the next pitch is not.

---

## Future Work

- Incorporate pitch location data — perceived distance from the strike zone is a natural next feature. Raw coordinates alone aren't enough; batters can't perceive the zone the way ABS cameras can.
- Analyze challenge rates by pitch type — breaking balls on corners may be challenged differently than fastballs, and umpires may be less accurate on certain pitch shapes.
- Expand the dataset as the 2026 season progresses. Early-season behavior may shift as players grow familiar with the system.

---

## Repo Structure

```
MLB-Conquering-ABS/
├── data/
├── output/
├── DataPull.py                        # Statcast data ingestion
├── PitchPlots.py                      # Pitch visualization
├── Baseball.Rmd                       # Main modeling notebook
├── Sabermetrics.Rmd                   # Supporting sabermetric analysis
├── download_abs_challenge_data.R
├── Baseball.Rproj
└── README.md
```

---

## References

- Powers, S. (2024). sabRmetrics. https://saberpowers.github.io/sabRmetrics/
- Castrovince, A. (2025). ABS Challenge System coming to MLB full time in '26. MLB.com.
- Lee, K., Han, K., & Ko, J. (2025). Analyzing the impact of the automatic ball strike system in professional baseball. *Scientific Reports*, 15(1).

---

## Author

Grant Suchecki — MSBA Candidate, University of Notre Dame  
[GitHub](https://github.com/gsuchecki40) · [LinkedIn](https://linkedin.com/in/grantsuchecki)
