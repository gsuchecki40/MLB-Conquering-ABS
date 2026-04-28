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

cs = df[df["description"] == "called_strike"].copy()
ba = df[df["description"] == "ball"].copy()

# Called strikes — distance outside zone in inches
cs["dist_x"] = (cs["plate_x"].abs() - PLATE_HALF).clip(lower=0)
cs["dist_z"] = pd.concat([
    SZ_BOT - cs["plate_z"],
    cs["plate_z"] - SZ_TOP,
    pd.Series(np.zeros(len(cs)), index=cs.index)
], axis=1).max(axis=1)
cs["dist_in"] = np.sqrt(cs["dist_x"]**2 + cs["dist_z"]**2) * 12
cs_normal = cs[cs["dist_in"] <= 2]
cs_bad    = cs[cs["dist_in"] >  2]

# Called balls inside zone — colored by distance from edge
ba_in_zone = ba[
    ba["plate_x"].between(-PLATE_HALF, PLATE_HALF) &
    ba["plate_z"].between(SZ_BOT, SZ_TOP)
].copy()
ba_in_zone["dist_from_edge"] = pd.concat([
    PLATE_HALF - ba_in_zone["plate_x"].abs(),
    ba_in_zone["plate_z"] - SZ_BOT,
    SZ_TOP - ba_in_zone["plate_z"]
], axis=1).min(axis=1) * 12

ba_outside = ba[~(
    ba["plate_x"].between(-PLATE_HALF, PLATE_HALF) &
    ba["plate_z"].between(SZ_BOT, SZ_TOP)
)]


def add_zone(ax):
    ax.add_patch(patches.Rectangle(
        (-PLATE_HALF, SZ_BOT), PLATE_HALF * 2, SZ_TOP - SZ_BOT,
        linewidth=1.5, edgecolor="white", facecolor="none", linestyle="--"
    ))
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(0.5, 5.5)
    ax.set_xlabel("Horizontal (ft)", fontsize=11)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([1, 2, 3, 4, 5])


fig, axes = plt.subplots(1, 2, figsize=(16, 9), sharey=True)
fig.suptitle("Egregious Missed Calls — MLB 2026 (ST + Regular Season)",
             fontsize=14, y=1.01)

# Left: called strikes outside zone
ax = axes[0]
ax.scatter(ba["plate_x"], ba["plate_z"],
           c="#4488FF", alpha=0.3, s=3, edgecolors="none")
ax.scatter(cs_normal["plate_x"], cs_normal["plate_z"],
           c="#FF5500", alpha=0.4, s=4, edgecolors="none")
sc1 = ax.scatter(
    cs_bad["plate_x"], cs_bad["plate_z"],
    c=cs_bad["dist_in"], cmap="YlOrRd", vmin=2, vmax=8,
    s=22, edgecolors="white", linewidths=0.3, zorder=5, alpha=0.9
)
add_zone(ax)
ax.set_ylabel("Vertical (ft)", fontsize=11)
ax.set_title('Called Strikes 2"+ Outside Zone', fontsize=12, pad=8)
cbar1 = fig.colorbar(sc1, ax=ax, fraction=0.035, pad=0.04)
cbar1.set_label("Inches Outside Zone", fontsize=9)
cbar1.set_ticks([2, 4, 6, 8])
cbar1.set_ticklabels(['2"', '4"', '6"', '8"+'])
ax.text(0.02, 0.98,
        f"n={len(cs_bad):,} egregious calls\n({len(cs_bad)/len(cs)*100:.1f}% of all called strikes)",
        transform=ax.transAxes, fontsize=9, va="top", color="white", alpha=0.7)

# Right: called balls inside zone
ax = axes[1]
ax.scatter(ba_outside["plate_x"], ba_outside["plate_z"],
           c="#4488FF", alpha=0.4, s=3, edgecolors="none")
ax.scatter(cs["plate_x"], cs["plate_z"],
           c="#FF5E00", alpha=0.25, s=3, edgecolors="none")
sc2 = ax.scatter(
    ba_in_zone["plate_x"], ba_in_zone["plate_z"],
    c=ba_in_zone["dist_from_edge"], cmap="YlGnBu", vmin=0, vmax=4,
    s=22, edgecolors="white", linewidths=0.3, zorder=5, alpha=1.0
)
add_zone(ax)
ax.set_title("Called Balls Inside Zone", fontsize=12, pad=8)
cbar2 = fig.colorbar(sc2, ax=ax, fraction=0.035, pad=0.04)
cbar2.set_label("Inches from Zone Edge", fontsize=9)
cbar2.set_ticks([0, 1, 2, 3, 4])
cbar2.set_ticklabels(['0"', '1"', '2"', '3"', '4"+'])
ax.text(0.02, 0.98,
        f"n={len(ba_in_zone):,} balls called in zone\n({len(ba_in_zone)/len(ba)*100:.1f}% of all called balls)",
        transform=ax.transAxes, fontsize=9, va="top", color="white", alpha=0.7)

plt.tight_layout()
plt.savefig("output/egregious_missed_calls.png", dpi=300,
            bbox_inches="tight", facecolor="#111111")
plt.show()
print("Saved: output/egregious_missed_calls.png")