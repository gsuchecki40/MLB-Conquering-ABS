import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams
from pathlib import Path
 
plt.style.use("dark_background")
rcParams.update({
    "axes.facecolor":   "#111111",
    "figure.facecolor": "#111111",
    "axes.edgecolor":   "#333333",
    "grid.color":       "#222222",
    "text.color":       "white",
    "axes.labelcolor":  "white",
    "xtick.color":      "white",
    "ytick.color":      "white",
    "font.family":      "monospace",
})
 
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)
 
COLORS = {
    "Pitcher": "#FF6B6B",
    "Catcher": "#00BFFF",
    "Batter":  "#98FB98",
    "ST":      "#FFD700",
    "RS":      "#00BFFF",
}
 
 
# ============================================================
# 1. LOAD + STACK
# ============================================================
 
def load(path, role, season):
    df = pd.read_csv(path, low_memory=False)
    df["role"]   = role
    df["season"] = season
    return df
 
lb = pd.concat([
    load("data/abs_pitcher_rs.csv", "Pitcher", "Regular Season"),
    load("data/abs_pitcher_st.csv", "Pitcher", "Spring Training"),
    load("data/abs_catcher_rs.csv", "Catcher", "Regular Season"),
    load("data/abs_catcher_st.csv", "Catcher", "Spring Training"),
    load("data/abs_batter_rs.csv",  "Batter",  "Regular Season"),
    load("data/abs_batter_st.csv",  "Batter",  "Spring Training"),
], ignore_index=True)
 
# Summary by role + season
summary = lb.groupby(["role", "season"]).agg(
    players        = ("entity_name",   "count"),
    total_chal     = ("n_challenges",  "sum"),
    total_overturn = ("n_overturns",   "sum"),
    total_exp      = ("exp_chal",      "sum"),
    total_net_for  = ("net_for",       "sum"),
    total_k_flip   = ("n_strikeouts_flip", "sum"),
    total_bb_flip  = ("n_walks_flip",  "sum"),
).reset_index()
 
summary["overturn_rate"] = summary["total_overturn"] / summary["total_chal"]
summary["chal_vs_exp"]   = summary["total_chal"] - summary["total_exp"]
 
print(summary[[
    "role","season","total_chal","overturn_rate","chal_vs_exp","total_net_for"
]].round(3).to_string(index=False))

# Pitchers