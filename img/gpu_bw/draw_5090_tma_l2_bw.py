import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

# Data from the benchmark
chunk_sizes = [256, 512, 1024, 2048, 4096, 8192, 16384]  # in bytes
stages = [1, 2, 4, 8, 16, 32]

# Bandwidth matrix (GB/s)
bw_matrix = np.array([
    [209.09, 197.27, 375.16, 443.94, 442.25, 441.13],    # 256B
    [407.85, 393.76, 742.35, 880.42, 881.16, 860.90],    # 512B
    [783.98, 758.74, 1421.80, 1651.30, 1705.00, 1623.18], # 1024B
    [1469.62, 1402.78, 2548.18, 3261.51, 3048.19, 2920.82], # 2048B
    [2496.61, 2496.61, 3898.05, 5165.40, 5533.38, np.nan], # 4096B
    [3942.02, 3591.01, 5461.33, 5041.23, np.nan, np.nan], # 8192B
    [5533.38, 5065.58, 5504.34, np.nan, np.nan, np.nan]   # 16384B
])

# Convert to TB/s for utilization calculation
peak_bw_tb = 5.6  # 5.6 TB/s
bw_util_matrix = bw_matrix / 1000 / peak_bw_tb  # Convert GB/s to TB/s and divide by peak

# In-flight bytes matrix
inflight_matrix = np.zeros_like(bw_matrix)
for i, chunk in enumerate(chunk_sizes):
    for j, stage in enumerate(stages):
        if not np.isnan(bw_matrix[i, j]):
            inflight_matrix[i, j] = chunk * stage

# Create the visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Bandwidth heatmap
im1 = ax1.imshow(bw_matrix, cmap='viridis', aspect='auto')
ax1.set_xticks(range(len(stages)))
ax1.set_xticklabels(stages)
ax1.set_yticks(range(len(chunk_sizes)))
ax1.set_yticklabels([f'{cs}B' for cs in chunk_sizes])
ax1.set_xlabel('Number of Stages')
ax1.set_ylabel('Chunk Size')
ax1.set_title('Bandwidth (GB/s) - Hopper TMA Bulk Transfer')

# Add text annotations for bandwidth
for i in range(len(chunk_sizes)):
    for j in range(len(stages)):
        if not np.isnan(bw_matrix[i, j]):
            ax1.text(j, i, f'{bw_matrix[i, j]:.0f}', 
                    ha='center', va='center', fontweight='bold',
                    fontsize=16,
                    color='white' if bw_matrix[i, j] > 2000 else 'black')

# Plot 2: Bandwidth utilization heatmap
im2 = ax2.imshow(bw_util_matrix, cmap='plasma', aspect='auto', vmin=0, vmax=1)
ax2.set_xticks(range(len(stages)))
ax2.set_xticklabels(stages)
ax2.set_yticks(range(len(chunk_sizes)))
ax2.set_yticklabels([f'{cs}B' for cs in chunk_sizes])
ax2.set_xlabel('Number of Stages')
ax2.set_ylabel('Chunk Size')
ax2.set_title('Bandwidth Utilization (Fraction of 5.6 TB/s)')

# Add text annotations for utilization and in-flight bytes
for i in range(len(chunk_sizes)):
    for j in range(len(stages)):
        if not np.isnan(bw_util_matrix[i, j]):
            util_percent = bw_util_matrix[i, j] * 100
            inflight_kb = inflight_matrix[i, j] / 1024
            text = f'{util_percent:.1f}%\n({inflight_kb:.0f}KB)'
            ax2.text(j, i, text, 
                    ha='center', va='center', fontsize=12, fontweight='bold',
                    color='white' if bw_util_matrix[i, j] > 0.5 else 'black')

# Add colorbars
plt.colorbar(im1, ax=ax1, label='Bandwidth (GB/s)')
plt.colorbar(im2, ax=ax2, label='Utilization Fraction')

plt.tight_layout()
# plt.show()
plt.savefig("5090_tma_l2_bw.png")

# Print summary statistics
print("Performance Summary:")
print(f"Peak bandwidth achieved: {np.nanmax(bw_matrix):.2f} GB/s")
print(f"Peak utilization: {np.nanmax(bw_util_matrix)*100:.1f}% of 5.6 TB/s")
print(f"Best configuration: {chunk_sizes[np.nanargmax(bw_matrix) // len(stages)]}B chunk, "
      f"{stages[np.nanargmax(bw_matrix) % len(stages)]} stages")
