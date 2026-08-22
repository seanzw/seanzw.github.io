"""Figure: mixed traffic directions.

Grouped bar chart for the two mixed-payload experiments (rank 0 always reads
rank 1). Compares aggregate B/SM-cycle when the second payload (store or TMA
put) travels in the same physical direction as the read response versus the
opposite direction.
"""
import matplotlib.pyplot as plt
import numpy as np

labels = ["load + store", "load + TMA put"]
same_direction = np.array([21.38, 21.45])
opposite_direction = np.array([29.70, 29.26])
gain_pct = (opposite_direction - same_direction) / same_direction * 100

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.bar(x - width / 2, same_direction, width, label="same data direction", color="#84c960")
ax.bar(x + width / 2, opposite_direction, width, label="opposite data directions", color="#416473")

ax.set_ylabel("aggregate bandwidth (B/SM-cycle)")
ax.set_title("Mixed traffic: same vs. opposite data direction")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.16), ncol=2, frameon=False)
ax.set_ylim(0, max(opposite_direction) * 1.3)

for xi, opp, gain in zip(x, opposite_direction, gain_pct):
    ax.annotate(
        f"+{gain:.0f}%",
        xy=(xi + width / 2, opp + 0.4),
        ha="center", va="bottom", fontsize=10, color="#333333",
    )

fig.tight_layout()
fig.savefig("/home/zhengrong/front-cover/static/img/gpu_dsm_bw/fig3_mixed_traffic.png", dpi=150)
print(gain_pct)
