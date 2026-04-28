# ============================================================
# Zone Map by Key Counts — scatter style
# Emphasizes called strikes outside the zone
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
SZ_TOP     = df["sz_top"].median()   # ~3.21
SZ_BOT     = df["sz_bot"].median()   # ~1.62

counts = [(0,0,"0-0"), (0,2,"0-2"), (3,0,"3-0"), (3,2,"3-2")]

fig, axes = plt.subplots(1, 4, figsize=(18, 6), sharey=True)
fig.suptitle("Called Strike vs. Ball by Zone — Key Count States\nMLB 2026 (ST + Regular Season)",
             fontsize=14, y=1.02)

for ax, (b, s, label) in zip(axes, counts):
    sub = df[(df["balls"] == b) & (df["strikes"] == s)]
    ba  = sub[sub["description"] == "ball"]
    cs  = sub[sub["description"] == "called_strike"]

    # Split called strikes into in-zone and out-of-zone
    in_zone = (
        cs["plate_x"].between(-PLATE_HALF, PLATE_HALF) &
        cs["plate_z"].between(SZ_BOT, SZ_TOP)
    )
    cs_in  = cs[in_zone]
    cs_out = cs[~in_zone]

    # Balls — faint blue
    ax.scatter(ba["plate_x"], ba["plate_z"],
               c="#4488FF", alpha=0.2, s=5, edgecolors="none")

    # Called strikes in zone — dim red
    ax.scatter(cs_in["plate_x"], cs_in["plate_z"],
               c="#FF4444", alpha=0.25, s=5, edgecolors="none")

    # Called strikes outside zone — bright, outlined
    ax.scatter(cs_out["plate_x"], cs_out["plate_z"],
               c="#FF4444", alpha=0.9, s=14,
               edgecolors="white", linewidths=0.3, zorder=5)

    # Realistic zone box using actual median sz values
    ax.add_patch(patches.Rectangle(
        (-PLATE_HALF, SZ_BOT),
        PLATE_HALF * 2, SZ_TOP - SZ_BOT,
        linewidth=1.5, edgecolor="white",
        facecolor="none", linestyle="--"
    ))

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(0.5, 5.5)
    ax.set_title(f"{label}\nn={len(sub):,}", fontsize=11, pad=6)
    ax.set_xlabel("Horizontal (ft)", fontsize=9)
    ax.tick_params(labelsize=8)

axes[0].set_ylabel("Vertical (ft)", fontsize=10)

handles = [
    plt.Line2D([0],[0], marker="o", color="w", markerfacecolor="#4488FF",
               markersize=7, alpha=0.6, label="Ball"),
    plt.Line2D([0],[0], marker="o", color="w", markerfacecolor="#FF4444",
               markersize=7, alpha=0.35, label="Called Strike (in zone)"),
    plt.Line2D([0],[0], marker="o", color="w", markerfacecolor="#FF4444",
               markeredgecolor="white", markeredgewidth=0.5,
               markersize=7, alpha=1.0, label="Called Strike (outside zone)"),
]
fig.legend(handles=handles, loc="lower center", ncol=3,
           fontsize=10, framealpha=0.2, bbox_to_anchor=(0.5, -0.05))

plt.tight_layout()
plt.savefig("output/zone_counts_scatter.png", dpi=300,
            bbox_inches="tight", facecolor="#111111")
plt.show()
print("Saved: output/zone_counts_scatter.png")