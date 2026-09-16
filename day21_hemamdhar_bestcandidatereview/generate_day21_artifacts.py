import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient

DIR = Path(__file__).resolve().parent
CSV_PATH = DIR / 'baseline_vs_tuned_summary.csv'
df = pd.read_csv(CSV_PATH)

# ==========================================
# 1. Generate Latency & FPS Comparison Plot
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

val_df = df[df['stage_day'].isin(['Day 19', 'Day 20'])].drop_duplicates(subset=['condition', 'variant'])
variants = val_df['variant'].tolist()
prep = val_df['preprocess_ms'].tolist()
inf = val_df['inference_ms'].tolist()
fps = val_df['fps'].tolist()

x = np.arange(len(variants))
width = 0.35

ax1.bar(x - width/2, prep, width, label='Preprocessing (ms/img)', color='#3b82f6')
ax1.bar(x + width/2, inf, width, label='Inference (ms/img)', color='#10b981')
ax1.set_ylabel('Latency (ms / image)', fontsize=11)
ax1.set_title('Preprocessing & Inference Latency by Variant', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(variants, rotation=15, ha='right')
ax1.legend(loc='upper left')
ax1.grid(True, linestyle='--', alpha=0.5)

# Annotate Best Candidate
ax1.annotate('★ Best Candidate\n(6.21ms Prep)', xy=(1 - width/2, prep[1]), xytext=(1 - width/2, prep[1] + 8),
             arrowprops=dict(facecolor='#1d4ed8', shrink=0.05, width=1.5, headwidth=6),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#dbeafe', edgecolor='#3b82f6'),
             ha='center', fontsize=9, fontweight='bold')

color = '#8b5cf6'
ax2.set_xlabel('Condition Variant', fontsize=11)
ax2.set_ylabel('Throughput (FPS)', color=color, fontsize=11)
bars = ax2.bar(x, fps, width=0.4, color=color, alpha=0.75, label='Throughput (FPS)')
ax2.axhline(30.0, color='#ef4444', linestyle='--', linewidth=1.5, label='Real-Time Target (30 FPS)')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_xticks(x)
ax2.set_xticklabels(variants, rotation=15, ha='right')
ax2.set_title('Throughput vs Real-Time Operational Target', fontsize=12, fontweight='bold')
ax2.legend(loc='lower right')
ax2.grid(True, linestyle='--', alpha=0.5)

for bar, f in zip(bars, fps):
    ax2.text(bar.get_x() + bar.get_width()/2.0, f + 0.6, f'{f:.1f} FPS', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(DIR / 'baseline_vs_tuned_comparison.png', dpi=300)
plt.close()
print('Generated baseline_vs_tuned_comparison.png')

# ==========================================
# 2. Generate Success vs Failure Taxonomy Plot
# ==========================================
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('off')

# Title
ax.text(0.5, 0.95, 'Day 21: Pipeline Successes, Bottlenecks & Weakness Taxonomy',
        ha='center', va='top', fontsize=14, fontweight='bold', color='#1e293b')

# Column 1: Validated Successes
success_text = (
    "★ REPRESENTATIVE SUCCESSES\n"
    "─────────────────────────────────────────\n"
    "• Zero Data Leakage:\n"
    "  954-image test split strictly frozen.\n\n"
    "• Spatial Invariance:\n"
    "  CIELAB L-channel preserves bounding boxes.\n\n"
    "• Real-Time Throughput:\n"
    "  CLAHE 1.5 reaches 33.72 FPS (>30 FPS goal).\n\n"
    "• Upstream Data Integrity:\n"
    "  256/256 paired validation labels verified."
)
ax.text(0.05, 0.85, success_text, ha='left', va='top', fontsize=10.5,
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#ecfdf5', edgecolor='#10b981', linewidth=1.5),
        color='#065f46')

# Column 2: Bottlenecks & Failures
failure_text = (
    "⚠ LOCALIZED BOTTLENECKS\n"
    "─────────────────────────────────────────\n"
    "• Under-Trained Smoke Detector:\n"
    "  1 epoch on 2% data yields 0 proposals.\n\n"
    "• Downstream Tracking Collapse:\n"
    "  Null detector boxes cascade to 0 tracks.\n\n"
    "• Environmental Degradation:\n"
    "  Heavy turbidity & severe color-cast.\n\n"
    "• Static Confidence Starvation:\n"
    "  conf=0.25 on uncalibrated weights."
)
ax.text(0.52, 0.85, failure_text, ha='left', va='top', fontsize=10.5,
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#fef2f2', edgecolor='#ef4444', linewidth=1.5),
        color='#991b1b')

# Bottom Banner: Week 4 Direction
week4_banner = (
    "APPROVED WEEK-4 DIRECTION: YOLOv8n (50 Epochs) + CLAHE (Clip=1.5, Grid=8x8) + raw_v1 Control\n"
    "Action Plan: Full Convergence Training ──► Paired Benchmark ──► Error Stratification ──► One-Shot Test"
)
ax.text(0.5, 0.15, week4_banner, ha='center', va='center', fontsize=10.5, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#eff6ff', edgecolor='#3b82f6', linewidth=1.5),
        color='#1e40af')

plt.tight_layout()
plt.savefig(DIR / 'success_failure_taxonomy.png', dpi=300)
plt.close()
print('Generated success_failure_taxonomy.png')

# ==========================================
# 3. Build & Execute Notebook
# ==========================================
nb = nbf.v4.new_notebook()
cells = []

# Cell 1: Markdown Title & Context
md1 = """# Day 21 — Best Candidate Review & Week-4 Direction

## Overview & Scope
This notebook presents the synthesized experimental outcomes across **Weeks 1–3 (Days 16–20)** for the **AI-Based Underwater Visual Surveillance** pipeline. We evaluate baseline versus tuned enhancement methods, analyze failure modes, inspect representative latency characteristics, and establish the **Best-Candidate configuration** approved for **Week-4 final execution**."""
cells.append(nbf.v4.new_markdown_cell(md1))

# Cell 2: Code Load Data
code1 = """from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

NOTEBOOK_DIR = Path.cwd()
SUMMARY_CSV = NOTEBOOK_DIR / 'baseline_vs_tuned_summary.csv'
CONFIG_JSON = NOTEBOOK_DIR / 'best_candidate_config.json'

summary_df = pd.read_csv(SUMMARY_CSV)
config = json.loads(CONFIG_JSON.read_text(encoding='utf-8'))

print('=== Day 21 Review Pack Status ===')
print(f'Total Evaluated Experimental Runs: {len(summary_df)}')
print(f'Selected Best Candidate: {config[\"approved_week4_direction\"][\"enhancement_pipeline\"][\"selected_method\"]} (clip_limit={config[\"approved_week4_direction\"][\"enhancement_pipeline\"][\"clip_limit\"]})')
print(f'Selected Detector: {config[\"approved_week4_direction\"][\"detection_model\"][\"architecture\"]}')
print(f'Week-4 Status: {config[\"status\"]}')"""
cells.append(nbf.v4.new_code_cell(code1))

# Cell 3: Markdown Section 1
md2 = """## 1. Multi-Day Experimental Progression & Benchmark Summary

Below is the complete multi-stage progression from initial smoke baseline (Day 16) through multi-method comparison (Days 17–18), controlled parameter sweep (Day 19), and robustness ablation (Day 20)."""
cells.append(nbf.v4.new_markdown_cell(md2))

# Cell 4: Code Display Summary Table
code2 = """display_cols = [
    'stage_day', 'phase', 'condition', 'variant', 'split', 'images', 
    'preprocess_ms', 'inference_ms', 'fps', 'detections', 'decision_outcome'
]
summary_df[display_cols]"""
cells.append(nbf.v4.new_code_cell(code2))

# Cell 5: Markdown Section 2
md3 = """## 2. Latency & Throughput Benchmark

We examine the trade-off between preprocessing compute latency, detector forward-pass time, and frames per second (FPS) against the real-time operational target of $30\\text{ FPS}$."""
cells.append(nbf.v4.new_markdown_cell(md3))

# Cell 6: Code Plot Chart
code3 = """fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

val_df = summary_df[summary_df['stage_day'].isin(['Day 19', 'Day 20'])].drop_duplicates(subset=['condition', 'variant'])
variants = val_df['variant'].tolist()
prep = val_df['preprocess_ms'].tolist()
inf = val_df['inference_ms'].tolist()
fps = val_df['fps'].tolist()

x = np.arange(len(variants))
width = 0.35

ax1.bar(x - width/2, prep, width, label='Preprocessing (ms/img)', color='#3b82f6')
ax1.bar(x + width/2, inf, width, label='Inference (ms/img)', color='#10b981')
ax1.set_ylabel('Latency (ms / image)', fontsize=11)
ax1.set_title('Preprocessing & Inference Latency by Variant', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(variants, rotation=15, ha='right')
ax1.legend(loc='upper left')
ax1.grid(True, linestyle='--', alpha=0.5)

# Annotate Best Candidate
ax1.annotate('★ Best Candidate\\n(6.21ms Prep)', xy=(1 - width/2, prep[1]), xytext=(1 - width/2, prep[1] + 8),
             arrowprops=dict(facecolor='#1d4ed8', shrink=0.05, width=1.5, headwidth=6),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#dbeafe', edgecolor='#3b82f6'),
             ha='center', fontsize=9, fontweight='bold')

color = '#8b5cf6'
ax2.set_xlabel('Condition Variant', fontsize=11)
ax2.set_ylabel('Throughput (FPS)', color=color, fontsize=11)
bars = ax2.bar(x, fps, width=0.4, color=color, alpha=0.75, label='Throughput (FPS)')
ax2.axhline(30.0, color='#ef4444', linestyle='--', linewidth=1.5, label='Real-Time Target (30 FPS)')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_xticks(x)
ax2.set_xticklabels(variants, rotation=15, ha='right')
ax2.set_title('Throughput vs Real-Time Operational Target', fontsize=12, fontweight='bold')
ax2.legend(loc='lower right')
ax2.grid(True, linestyle='--', alpha=0.5)

for bar, f in zip(bars, fps):
    ax2.text(bar.get_x() + bar.get_width()/2.0, f + 0.6, f'{f:.1f} FPS', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(code3))

# Cell 7: Markdown Section 3
md4 = """## 3. Best-Candidate Specification & Week-4 Direction

### Approved Best Candidate Configuration
- **Photometric Enhancement:** CLAHE ($L$-channel in CIELAB, $\\text{clip limit}=1.5$, $\\text{grid size}=8 \\times 8$).
- **Mandatory Control Baseline:** `raw_v1` (RGB unenhanced input).
- **Target Object Detector:** YOLOv8n ($3.0\\text{M}$ parameters, $5.92\\text{ MB}$) trained for 50 epochs on full DIAT dataset.
- **Downstream Tracking:** Greedy IoU spatial association with ByteTrack fallback.
- **Split Governance:** 954 test images remain strictly frozen until final Day 26 benchmark."""
cells.append(nbf.v4.new_markdown_cell(md4))

# Cell 8: Code Automated Assertions
code4 = """# Programmatic verification assertions for Day 21
assert len(summary_df) >= 10, 'Expected comprehensive summary records across Days 16-20'
assert config['approved_week4_direction']['enhancement_pipeline']['selected_method'] == 'clahe'
assert config['approved_week4_direction']['enhancement_pipeline']['clip_limit'] == 1.5
assert config['approved_week4_direction']['detection_model']['architecture'] == 'YOLOv8n'
assert config['approved_week4_direction']['acceptance_criteria']['min_fps_target'] == 25.0

print('All Day 21 Best Candidate Review programmatic validation assertions passed successfully.')"""
cells.append(nbf.v4.new_code_cell(code4))

nb['cells'] = cells

client = NotebookClient(nb, timeout=60, kernel_name='python3')
executed_nb = client.execute()

nbf.write(executed_nb, DIR / 'best_candidate_review.ipynb')
nbf.write(executed_nb, DIR / 'best_candidate_review_v1.ipynb')
with open(DIR / 'best_candidate_review_submission.ipynb.json', 'w', encoding='utf-8') as f:
    json.dump(executed_nb, f, indent=2)

print('Executed notebook generated and saved to best_candidate_review.ipynb and best_candidate_review_submission.ipynb.json!')
