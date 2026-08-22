"""Figure: extracting bandwidth from a size slope.

Uses the one-way remote-load size sweep (load_size_uni) as the worked
example: payload per active SM (bytes) on the x-axis, median elapsed SM
cycles on the y-axis, with the affine fit T(B) = alpha + beta*B overlaid
and a residual sub-panel below.
"""
import matplotlib.pyplot as plt
import numpy as np

# median_cycles vs payload (KiB) for load_size_uni, from the Plot Data section
payload_kib = np.array([16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96], dtype=float)
median_cycles = np.array([
    1405.0, 1745.5, 2147.5, 2502.5, 2914.5, 3296.0,
    3706.0, 4254.5, 4691.0, 5052.0, 5443.0,
])

payload_bytes = payload_kib * 1024.0

# Fitted coefficients from the fitted-coefficients table (load_size_uni)
alpha = 492.554545
beta = 0.050317383
bw = 1.0 / beta

fitted = alpha + beta * payload_bytes
residuals = median_cycles - fitted

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(7, 5), sharex=True,
    gridspec_kw={"height_ratios": [4, 1]},
)

ax1.plot(payload_kib, median_cycles, "o", color="#84c960",
         label="measured (median of 30 samples)", zorder=3)
xs_kib = np.linspace(0, payload_kib.max() * 1.05, 100)
ax1.plot(xs_kib, alpha + beta * xs_kib * 1024.0, "-", color="#416473",
         label=r"fit: $T(B)=\alpha+\beta B$", zorder=2)

ax1.set_ylabel("median elapsed SM cycles")
ax1.set_title("Remote load, one way: extracting bandwidth from a size slope")
ax1.legend(loc="upper left", frameon=False)

ax1.annotate(
    rf"$\alpha$ = {alpha:.0f} cycles" "\n"
    rf"$\beta$ = {beta:.5f} cycles/byte" "\n"
    rf"$1/\beta$ = {bw:.2f} B/cycle",
    xy=(0.98, 0.05), xycoords="axes fraction",
    ha="right", va="bottom", fontsize=10,
    bbox=dict(boxstyle="round", fc="white", ec="gray"),
)

ax2.axhline(0, color="gray", linewidth=0.8)
ax2.plot(payload_kib, residuals, "o", color="#e7bc58")
ax2.set_ylabel("residual\n(cycles)")
ax2.set_xlabel("payload per active SM (KiB)")
ax2.set_xticks(payload_kib)

fig.tight_layout()
fig.savefig("/home/zhengrong/front-cover/static/img/gpu_dsm_bw/fig1_slope_fit.png", dpi=150)
print("alpha", alpha, "beta", beta, "1/beta", bw)
