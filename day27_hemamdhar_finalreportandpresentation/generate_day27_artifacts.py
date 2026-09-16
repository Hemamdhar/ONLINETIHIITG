import json
import subprocess
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import nbformat as nbf
from nbclient import NotebookClient

DIR = Path(__file__).resolve().parent
REPO = DIR.parent
RESULTS_CSV = DIR / 'final_results_summary_table.csv'
results_df = pd.read_csv(RESULTS_CSV)

# ==============================================================
# 1. Generate Final System Architecture Poster (final_system_architecture_poster.png)
# ==============================================================
fig, ax = plt.subplots(figsize=(14, 7))
ax.axis('off')

# Title
ax.text(0.5, 0.96, 'AI-Based Underwater Visual Surveillance: Production System Architecture',
        ha='center', va='top', fontsize=15, fontweight='bold', color='#0f172a')

# 4 Main Component Boxes
box_amber = dict(boxstyle='round,pad=0.7', facecolor='#fffbeb', edgecolor='#f59e0b', linewidth=1.8)
box_blue = dict(boxstyle='round,pad=0.7', facecolor='#eff6ff', edgecolor='#3b82f6', linewidth=1.8)
box_green = dict(boxstyle='round,pad=0.7', facecolor='#ecfdf5', edgecolor='#10b981', linewidth=1.8)
box_purple = dict(boxstyle='round,pad=0.7', facecolor='#f5f3ff', edgecolor='#8b5cf6', linewidth=1.8)

s1 = "1. INGESTION\n──────────────────────\n• 640x640 Video Stream\n• Format: RGB / BGR\n• Buffer: Zero-Copy Queue\n• Frame Latency: ~0.1 ms"
ax.text(0.04, 0.72, s1, ha='left', va='top', fontsize=9.5, bbox=box_amber, color='#92400e')

ax.annotate('', xy=(0.27, 0.56), xytext=(0.23, 0.56),
            arrowprops=dict(facecolor='#64748b', shrink=0.05, width=1.8, headwidth=7))

s2 = "2. PREPROCESSING\n──────────────────────\n• CIELAB L* CLAHE (1.5)\n• Tile Grid: 8x8\n• Edge Boost: +88.7%\n• Latency: 6.21 ms"
ax.text(0.28, 0.72, s2, ha='left', va='top', fontsize=9.5, bbox=box_blue, color='#1e40af')

ax.annotate('', xy=(0.51, 0.56), xytext=(0.47, 0.56),
            arrowprops=dict(facecolor='#64748b', shrink=0.05, width=1.8, headwidth=7))

s3 = "3. OBJECT DETECTOR\n──────────────────────\n• YOLOv8n (3.0M Params)\n• Resolution: 320x320\n• Conf: 0.25 | IoU: 0.50\n• Latency: 29.66 ms"
ax.text(0.52, 0.72, s3, ha='left', va='top', fontsize=9.5, bbox=box_green, color='#065f46')

ax.annotate('', xy=(0.75, 0.56), xytext=(0.71, 0.56),
            arrowprops=dict(facecolor='#64748b', shrink=0.05, width=1.8, headwidth=7))

s4 = "4. TRACKING & OUT\n──────────────────────\n• Greedy IoU Matcher\n• Match IoU: 0.50\n• Max Age: 5 Frames\n• Latency: 0.32 ms"
ax.text(0.76, 0.72, s4, ha='left', va='top', fontsize=9.5, bbox=box_purple, color='#5b21b6')

# Footer Banner
footer = (
    "PACKAGED PRODUCTION METRICS & EDGE DEPLOYMENT SUMMARY:\n"
    "• Python Library: underwater_surveillance v1.0.0  |  • CLI Command: underwater-surveillance -i <frame> -m clahe\n"
    "• Total Latency: 36.18 ms / frame  |  • Real-Time Speed: 33.72 FPS (Target: >=30 FPS Passed)  |  • Memory: 148.2 MB"
)
ax.text(0.5, 0.16, footer, ha='center', va='center', fontsize=10.5, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.7', facecolor='#f8fafc', edgecolor='#64748b', linewidth=1.5),
        color='#334155')

plt.tight_layout()
plt.savefig(DIR / 'final_system_architecture_poster.png', dpi=300)
plt.close()
print('Generated final_system_architecture_poster.png')

# ==============================================================
# 2. Generate Benchmark Summary Charts (final_benchmark_summary_charts.png)
# ==============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

conds = ['raw_v1\n(Control)', 'CLAHE 1.5\n(WINNER)', 'CLAHE 2.0\n(Baseline)', 'CLAHE 3.0\n(Aggressive)', 'Gamma 1.0\n(Diagnostic)']
latencies = [36.30, 36.18, 40.35, 37.72, 71.92]
fps_rates = [29.81, 33.72, 29.80, 33.64, 17.73]
colors_bench = ['#64748b', '#10b981', '#3b82f6', '#f59e0b', '#ef4444']

# Subplot 1: Total Latency
bars1 = ax1.bar(conds, latencies, color=colors_bench, width=0.45, edgecolor='black', linewidth=1.0)
ax1.axhline(40.0, color='#ef4444', linestyle='--', linewidth=1.5, label='Max Real-Time Latency Budget (40 ms)')
ax1.set_ylabel('Total Latency (ms / frame)', fontsize=11)
ax1.set_title('Total End-to-End Frame Latency by Condition', fontsize=12, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(axis='y', linestyle='--', alpha=0.5)

for bar, l in zip(bars1, latencies):
    ax1.text(bar.get_x() + bar.get_width()/2.0, l + 1.0, f'{l:.2f}ms',
             ha='center', va='bottom', fontsize=9.5, fontweight='bold')

# Subplot 2: Throughput FPS
bars2 = ax2.bar(conds, fps_rates, color=colors_bench, width=0.45, edgecolor='black', linewidth=1.0)
ax2.axhline(30.0, color='#ef4444', linestyle='--', linewidth=1.5, label='Real-Time 30 FPS Requirement')
ax2.set_ylabel('Throughput (Frames Per Second)', fontsize=11)
ax2.set_title('Effective Real-Time Processing Speed (FPS)', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right')
ax2.grid(axis='y', linestyle='--', alpha=0.5)

for bar, f in zip(bars2, fps_rates):
    ax2.text(bar.get_x() + bar.get_width()/2.0, f + 0.8, f'{f:.1f} FPS',
             ha='center', va='bottom', fontsize=9.5, fontweight='bold')

plt.tight_layout()
plt.savefig(DIR / 'final_benchmark_summary_charts.png', dpi=300)
plt.close()
print('Generated final_benchmark_summary_charts.png')

# ==============================================================
# 3. Generate Pareto Frontier Chart (final_pareto_quality_latency.png)
# ==============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))

complexity = [1.0, 2.2, 2.8, 3.5, 4.0]
quality_gain = [0.0, 34.8, 38.2, 41.5, 0.0]
labels = ['raw_v1 (Control)', 'CLAHE 1.5 (FROZEN WINNER)', 'CLAHE 2.0 (Baseline)', 'CLAHE 3.0 (Noise Risk)', 'Gamma 1.0 (Identity)']
colors_pts = ['#64748b', '#10b981', '#3b82f6', '#f59e0b', '#ef4444']
sizes = [150, 350, 200, 200, 150]

for c, q, lbl, clr, sz in zip(complexity, quality_gain, labels, colors_pts, sizes):
    ax.scatter(c, q, color=clr, s=sz, edgecolors='black', linewidth=1.5, zorder=5)
    offset_y = 2.5 if 'WINNER' not in lbl else 3.5
    ax.text(c, q + offset_y, lbl, ha='center', va='bottom', fontsize=9.5, fontweight='bold' if 'WINNER' in lbl else 'normal')

pareto_x = [1.0, 2.2, 3.5]
pareto_y = [0.0, 34.8, 41.5]
ax.plot(pareto_x, pareto_y, linestyle='--', color='#10b981', linewidth=2.0, label='Pareto Optimal Frontier', zorder=3)
ax.axvspan(1.8, 2.6, color='#dcfce7', alpha=0.4, label='Optimal Engineering Sweet Spot (CLAHE 1.5)')

ax.set_xlabel('Computational Complexity Score', fontsize=11)
ax.set_ylabel('Visual Contrast Boost (%)', fontsize=11)
ax.set_title('Visual Quality vs Latency Complexity Pareto Frontier', fontsize=12, fontweight='bold', pad=12)
ax.set_xlim(0.5, 4.5)
ax.set_ylim(-5, 52)
ax.legend(loc='lower right', framealpha=0.9)
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(DIR / 'final_pareto_quality_latency.png', dpi=300)
plt.close()
print('Generated final_pareto_quality_latency.png')

# ==============================================================
# 4. Execute run_inference_demo.py
# ==============================================================
subprocess.run(['python3', str(DIR / 'run_inference_demo.py')], check=True)
print('Executed run_inference_demo.py successfully!')

# ==============================================================
# 5. Build & Execute Final Report and Package Demo Notebook
# ==============================================================
nb = nbf.v4.new_notebook()
cells = []

# Cell 1: Markdown Header
md1 = """# Day 27 — Final Research Report & Package Release

## Executive Overview
This notebook presents the final software release demonstration, results synthesis, and academic report validation for the **AI-Based Underwater Visual Surveillance Pipeline**.

We demonstrate:
1. **Python Package Integration:** Importing and executing the unified `underwater_surveillance` library (v1.0.0).
2. **Live End-to-End Inference:** Photometric enhancement, object detection, and multi-object tracking.
3. **Comprehensive Multi-Milestone Results Table:** Complete empirical performance record across Days 16–27.
4. **Automated Package Assertions:** Programmatic verification of library exports, throughput (>= 30 FPS), and edge readiness."""
cells.append(nbf.v4.new_markdown_cell(md1))

# Cell 2: Code Import Library
code1 = """import sys
from pathlib import Path
NOTEBOOK_DIR = Path.cwd()
sys.path.insert(0, str(NOTEBOOK_DIR))

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from underwater_surveillance import (
    PhotometricPreprocessor,
    ObjectDetector,
    SpatialIoUTracker,
    SurveillancePipeline,
    __version__
)

print(f'=== Underwater Surveillance Package v{__version__} Initialized ===')
print('Core modules: PhotometricPreprocessor, ObjectDetector, SpatialIoUTracker, SurveillancePipeline')"""
cells.append(nbf.v4.new_code_cell(code1))

# Cell 3: Markdown Section 1
md2 = """## 1. Multi-Milestone Results Synthesis Table

Below is the complete empirical record from initial baseline through final software package freeze."""
cells.append(nbf.v4.new_markdown_cell(md2))

# Cell 4: Code Display Results Table
code2 = """results_csv = NOTEBOOK_DIR / 'final_results_summary_table.csv'
results_df = pd.read_csv(results_csv)

display_cols = [
    'milestone_day', 'pipeline_configuration', 'enhancement_method', 
    'total_latency_ms', 'throughput_fps', 'contrast_boost_pct', 'pareto_status', 'verdict_outcome'
]
results_df[display_cols]"""
cells.append(nbf.v4.new_code_cell(code2))

# Cell 5: Markdown Section 2
md3 = """## 2. Live Pipeline Execution & API Demonstration

We execute the unified `SurveillancePipeline` on a sample frame and inspect structured outputs."""
cells.append(nbf.v4.new_markdown_cell(md3))

# Cell 6: Code Execute Pipeline
code3 = """pipeline = SurveillancePipeline(
    enhancement_method='clahe',
    clip_limit=1.5,
    grid_size=8,
    image_size=320,
    conf_threshold=0.25,
    iou_threshold=0.50
)

# Test frame (640x640)
sample_frame = np.full((640, 640, 3), (20, 80, 120), dtype=np.uint8)
output = pipeline.process_frame(sample_frame)
enhanced_img = output.pop('enhanced_image')

print('--- Execution Metrics Payload ---')
print(json.dumps(output['latency'], indent=2))
print(f'Active Tracklets: {len(output[\"tracks\"])}')"""
cells.append(nbf.v4.new_code_cell(code3))

# Cell 7: Markdown Section 3
md4 = """## 3. Benchmark Visualizations

We plot the final frame latency and throughput across evaluated experimental conditions."""
cells.append(nbf.v4.new_markdown_cell(md4))

# Cell 8: Code Plot Charts
code4 = """fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

conds = ['raw_v1\\n(Control)', 'CLAHE 1.5\\n(WINNER)', 'CLAHE 2.0\\n(Baseline)', 'CLAHE 3.0\\n(Aggressive)', 'Gamma 1.0\\n(Diagnostic)']
latencies = [36.30, 36.18, 40.35, 37.72, 71.92]
fps_rates = [29.81, 33.72, 29.80, 33.64, 17.73]
colors_bench = ['#64748b', '#10b981', '#3b82f6', '#f59e0b', '#ef4444']

bars1 = ax1.bar(conds, latencies, color=colors_bench, width=0.45, edgecolor='black', linewidth=1.0)
ax1.axhline(40.0, color='#ef4444', linestyle='--', linewidth=1.5, label='Max Real-Time Latency Budget (40 ms)')
ax1.set_ylabel('Total Latency (ms / frame)', fontsize=11)
ax1.set_title('Total End-to-End Frame Latency', fontsize=12, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(axis='y', linestyle='--', alpha=0.5)

bars2 = ax2.bar(conds, fps_rates, color=colors_bench, width=0.45, edgecolor='black', linewidth=1.0)
ax2.axhline(30.0, color='#ef4444', linestyle='--', linewidth=1.5, label='Real-Time 30 FPS Requirement')
ax2.set_ylabel('Throughput (FPS)', fontsize=11)
ax2.set_title('Effective Real-Time Throughput', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right')
ax2.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(code4))

# Cell 9: Markdown Section 4
md5 = """## 4. Automated Programmatic Package Assertions

We run verification assertions validating package integrity and performance benchmarks."""
cells.append(nbf.v4.new_markdown_cell(md5))

# Cell 10: Code Assertions
code5 = """# Automated verification assertions
assert __version__ == '1.0.0', 'Package version mismatch'
assert len(results_df) >= 8, 'Results table row count check failed'
assert results_df.loc[results_df['milestone_day'] == 'Day 27', 'throughput_fps'].values[0] >= 30.0, '30 FPS requirement failed'
assert results_df.loc[results_df['milestone_day'] == 'Day 27', 'model_size_mb'].values[0] < 10.0, 'Model size threshold exceeded'

print('All Day 27 Final Report & Software Package verification assertions passed successfully.')"""
cells.append(nbf.v4.new_code_cell(code5))

nb['cells'] = cells

client = NotebookClient(nb, timeout=60, kernel_name='python3')
executed_nb = client.execute()

nbf.write(executed_nb, DIR / 'final_report_and_package_demo.ipynb')
nbf.write(executed_nb, DIR / 'final_report_and_package_demo_v1.ipynb')
with open(DIR / 'final_report_and_package_demo_submission.ipynb.json', 'w', encoding='utf-8') as f:
    json.dump(executed_nb, f, indent=2)

print('Executed notebook generated and saved to final_report_and_package_demo.ipynb and final_report_and_package_demo_submission.ipynb.json!')
