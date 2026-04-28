# ============================================================
# Egregious Called Strikes — 2+ inches outside the ABS zone
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

plt.style.use("dark_background")
Path("output").mkdir(exist_ok=True)

df = pd.read_csv("data/pbp.csv", low_memory=False)
df = df[df["plate_x"].between(-3, 3) & df["plate_z"].between(0, 6)].copy()

PLATE_HALF = 0.7083
SZ_TOP     = df["sz_top"].median()
SZ_BOT     = df["sz_bot"].median()

# All called strikes
cs = df[df["description"] == "called_strike"].copy()

# Distance outside zone in inches
cs["dist_x"]    = (cs["plate_x"].abs() - PLATE_HALF).clip(lower=0)
cs["dist_z"]    = pd.concat([
    SZ_BOT - cs["plate_z"],
    cs["plate_z"] - SZ_TOP,
    pd.Series(np.zeros(len(cs)), index=cs.index)
], axis=1).max(axis=1)
cs["dist_in"]   = np.sqrt(cs["dist_x"]**2 + cs["dist_z"]**2) * 12

cs_normal = cs[cs["dist_in"] <= 2]
cs_bad    = cs[cs["dist_in"] >  2]

# All balls for context
ba = df[df["description"] == "ball"]


fig, ax = plt.subplots(figsize=(8, 9))
fig.suptitle(
    "Egregious Missed Calls — Called Strikes 2+ Inches Outside ABS Zone\n"
    "MLB 2026 (ST + Regular Season)",
    fontsize=13, y=1.01
)

# Faint balls for context
ax.scatter(ba["plate_x"], ba["plate_z"],
           c="#4488FF", alpha=0.7, s=3, edgecolors="none")

# Normal called strikes — very dim
ax.scatter(cs_normal["plate_x"], cs_normal["plate_z"],
           c="#FF5500", alpha=0.1, s=4, edgecolors="none")

# Egregious called strikes — colored by distance
sc = ax.scatter(
    cs_bad["plate_x"], cs_bad["plate_z"],
    c=cs_bad["dist_in"],
    cmap="YlOrRd", vmin=2, vmax=8,
    s=22, edgecolors="white", linewidths=0.3,
    zorder=5, alpha=1.0
)

# Zone box
ax.add_patch(patches.Rectangle(
    (-PLATE_HALF, SZ_BOT), PLATE_HALF * 2, SZ_TOP - SZ_BOT,
    linewidth=1.5, edgecolor="white", facecolor="none", linestyle="--"
))

cbar = fig.colorbar(sc, ax=ax, fraction=0.035, pad=0.04)
cbar.set_label("Inches Outside Zone", fontsize=10)
cbar.set_ticks([2, 4, 6, 8])
cbar.set_ticklabels(["2\"", "4\"", "6\"", "8\"+"])

ax.set_xlim(-2.5, 2.5)
ax.set_ylim(0.5, 5.5)
ax.set_xlabel("Horizontal (ft)", fontsize=11)
ax.set_ylabel("Vertical (ft)", fontsize=11)
ax.set_xticks([-2, -1, 0, 1, 2])
ax.set_yticks([1, 2, 3, 4, 5])

ax.text(0.02, 0.98,
        f"n={len(cs_bad):,} egregious calls\n({len(cs_bad)/len(cs)*100:.1f}% of all called strikes)",
        transform=ax.transAxes, fontsize=9,
        va="top", color="white", alpha=0.7)

plt.tight_layout()
plt.savefig("output/egregious_called_strikes.png", dpi=300,
            bbox_inches="tight", facecolor="#111111")
plt.show()
print("Saved: output/egregious_called_strikes.png")