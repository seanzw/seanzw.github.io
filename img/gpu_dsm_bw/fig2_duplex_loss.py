"""Figure: one-way versus bidirectional bandwidth per direction.

Grouped bar chart for load / store / TMA put, comparing fitted one-way
bandwidth (1/beta) against the per-direction bandwidth measured when both
SMs are active simultaneously. Aggregate two-way bandwidth is intentionally
not plotted, since it would hide the per-direction loss being discussed.
"""
import matplotlib.pyplot as plt
import numpy as np

labels = ["load", "store", "TMA put"]
one_way = np.array([19.873848, 18.868462, 21.251327])
two_way = np.array([15.371572, 18.118428, 20.294810])
loss_pct = (one_way - two_way) / one_way * 100

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(6.5, 4.5))
bars1 = ax.bar(x - width / 2, one_way, width, label="one-way", color="#84c960")
bars2 = ax.bar(x + width / 2, two_way, width, label="two-way (per direction)", color="#416473")

ax.set_ylabel("bandwidth per direction (B/SM-cycle)")
ax.set_title("One-way vs. bidirectional DSM bandwidth")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.16), ncol=2, frameon=False)
ax.set_ylim(0, max(one_way) * 1.3)

for xi, tw, loss in zip(x, two_way, loss_pct):
    ax.annotate(
        f"-{loss:.1f}%",
        xy=(xi + width / 2, tw + 0.4),
        ha="center", va="bottom", fontsize=10, color="#333333",
    )

fig.tight_layout()
fig.savefig("/home/zhengrong/front-cover/static/img/gpu_dsm_bw/fig2_duplex_loss.png", dpi=150)
print(loss_pct)
