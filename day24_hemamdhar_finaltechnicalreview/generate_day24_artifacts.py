import json
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

# ==============================================================
# 1. Generate Input-to-Output Workflow Diagram (input_to_output_workflow.png)
# ==============================================================
fig, ax = plt.subplots(figsize=(14, 6))
ax.axis('off')

ax.text(0.5, 0.96, 'Reproducible Input-to-Output Surveillance Pipeline Workflow',
        ha='center', va='top', fontsize=14, fontweight='bold', color='#0f172a')

box_amber = dict(boxstyle='round,pad=0.6', facecolor='#fffbeb', edgecolor='#f59e0b', linewidth=1.5)
box_blue = dict(boxstyle='round,pad=0.6', facecolor='#eff6ff', edgecolor='#3b82f6', linewidth=1.5)
box_green = dict(boxstyle='round,pad=0.6', facecolor='#ecfdf5', edgecolor='#10b981', linewidth=1.5)
box_purple = dict(boxstyle='round,pad=0.6', facecolor='#f5f3ff', edgecolor='#8b5cf6', linewidth=1.5)

# Step 1: Input
s1 = "STEP 1: INGESTION\n──────────────────────\n• Underwater Video Stream\n• Resolution: 640x640 RGB\n• Paired Annotations\n• Zero-Leakage Val Subset"
ax.text(0.04, 0.72, s1, ha='left', va='top', fontsize=9.5, bbox=box_amber, color='#92400e')

ax.annotate('', xy=(0.27, 0.58), xytext=(0.23, 0.58),
            arrowprops=dict(facecolor='#64748b', shrink=0.05, width=1.5, headwidth=6))

# Step 2: CLAHE Enhancement
s2 = "STEP 2: PREPROCESSING\n──────────────────────\n• CIELAB Color Conversion\n• L* Channel CLAHE\n• Clip: 1.5 | Grid: 8x8\n• Latency: 6.21 ms / img"
ax.text(0.28, 0.72, s2, ha='left', va='top', fontsize=9.5, bbox=box_blue, color='#1e40af')

ax.annotate('', xy=(0.51, 0.58), xytext=(0.47, 0.58),
            arrowprops=dict(facecolor='#64748b', shrink=0.05, width=1.5, headwidth=6))

# Step 3: YOLOv8n Detection
s3 = "STEP 3: INFERENCE\n──────────────────────\n• YOLOv8n (3.0M Params)\n• Letterbox (320x320)\n• Conf: 0.25 | IoU: 0.50\n• Latency: ~29.7 ms / img"
ax.text(0.52, 0.72, s3, ha='left', va='top', fontsize=9.5, bbox=box_green, color='#065f46')

ax.annotate('', xy=(0.75, 0.58), xytext=(0.71, 0.58),
            arrowprops=dict(facecolor='#64748b', shrink=0.05, width=1.5, headwidth=6))

# Step 4: Tracking & Output
s4 = "STEP 4: TRACKING & OUT\n──────────────────────\n• Greedy IoU Spatial Tracker\n• Match Threshold: 0.50\n• Active Tracklet IDs\n• Total Latency: 36.18 ms"
ax.text(0.76, 0.72, s4, ha='left', va='top', fontsize=9.5, bbox=box_purple, color='#5b21b6')

# Footer
footer = (
    "REPRODUCIBILITY & REAL-TIME PERFORMANCE GUARANTEE:\n"
    "• Single Command Execution: python frozen_pipeline.py --input <frame> --method clahe --clip-limit 1.5\n"
    "• Throughput: 33.72 FPS (>30 FPS Target) | Model Footprint: 5.92 MB | Memory Peak: 148.2 MB"
)
ax.text(0.5, 0.18, footer, ha='center', va='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#f8fafc', edgecolor='#64748b', linewidth=1.2),
        color='#334155')

plt.tight_layout()
plt.savefig(DIR / 'input_to_output_workflow.png', dpi=300)
plt.close()
print('Generated input_to_output_workflow.png')

# ==============================================================
# 2. Generate Error Analysis & Reporting Protocol Diagram (error_analysis_reporting_protocol.png)
# ==============================================================
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('off')

ax.text(0.5, 0.96, 'Day 24: Environmental Error Stratification & Reporting Standards',
        ha='center', va='top', fontsize=14, fontweight='bold', color='#0f172a')

# 4 Quadrants for Error Strata
strata_a = (
    "STRATA A: HIGH TURBIDITY & SCATTERING\n"
    "────────────────────────────────────────\n"
    "• Visual Challenge: Milky haze, marine snow\n"
    "• Failure Risk: Edge gradient loss & false textures\n"
    "• Mitigation: CLAHE local contrast normalization\n"
    "• Target Metric: Per-stratum Recall & AP"
)
ax.text(0.05, 0.84, strata_a, ha='left', va='top', fontsize=9.5,
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#fefce8', edgecolor='#eab308', linewidth=1.2),
        color='#713f12')

strata_b = (
    "STRATA B: LOW-LIGHT & DEEP BACKGROUNDS\n"
    "────────────────────────────────────────\n"
    "• Visual Challenge: Severe underexposure\n"
    "• Failure Risk: Low-contrast shadow misdetections\n"
    "• Mitigation: Lightness (L*) adaptive redistribution\n"
    "• Target Metric: Dark scene true-positive yield"
)
ax.text(0.53, 0.84, strata_b, ha='left', va='top', fontsize=9.5,
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#f1f5f9', edgecolor='#64748b', linewidth=1.2),
        color='#1e293b')

strata_c = (
    "STRATA C: SPECTRAL COLOR ABSORPTION\n"
    "────────────────────────────────────────\n"
    "• Visual Challenge: Red-light wavelength loss\n"
    "• Failure Risk: Chrominance feature collapse\n"
    "• Mitigation: Preserved a*, b* chromatic ratios\n"
    "• Target Metric: Color-cast robustness delta"
)
ax.text(0.05, 0.44, strata_c, ha='left', va='top', fontsize=9.5,
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#f0fdf4', edgecolor='#22c55e', linewidth=1.2),
        color='#14532d')

strata_d = (
    "STRATA D: DENSE SCHOOLING & OCCLUSION\n"
    "────────────────────────────────────────\n"
    "• Visual Challenge: Bounding box overlap\n"
    "• Failure Risk: Track fragmentation & NMS merging\n"
    "• Mitigation: IoU NMS (0.50) + Tracklet age buffer\n"
    "• Target Metric: Trajectory continuity & hits"
)
ax.text(0.53, 0.44, strata_d, ha='left', va='top', fontsize=9.5,
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#faf5ff', edgecolor='#a855f7', linewidth=1.2),
        color='#581c87')

# Footer
reporting_footer = (
    "FINAL REPORTING STANDARD (DAYS 25–28):\n"
    "1. Environmental Error Stratification (Day 25) ──► 2. One-Shot Test Evaluation (Day 26) ──► 3. Technical Paper (Day 27)"
)
ax.text(0.5, 0.08, reporting_footer, ha='center', va='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#eff6ff', edgecolor='#3b82f6', linewidth=1.2),
        color='#1e40af')

plt.tight_layout()
plt.savefig(DIR / 'error_analysis_reporting_protocol.png', dpi=300)
plt.close()
print('Generated error_analysis_reporting_protocol.png')

# ==============================================================
# 3. Build & Execute Final Technical Review Notebook
# ==============================================================
nb = nbf.v4.new_notebook()
cells = []

# Cell 1: Markdown Header
md1 = """# Day 24 — Final Technical Review

## Executive Summary
This notebook encapsulates the **Final Technical Review** for the **AI-Based Underwater Visual Surveillance Pipeline**.

We review:
1. **The Frozen Method & Performance Baseline:** End-to-end specifications, real-time throughput ($33.72\\text{ FPS}$), and latency budget ($36.18\\text{ ms}$).
2. **Reproducible Input-to-Output Workflow:** Execution mechanics across ingestion, enhancement, detection, and tracking.
3. **Error-Analysis & Reporting Protocols:** Environmental degradation taxonomy (Turbidity, Low-Light, Color-Cast, Occlusion) and one-shot test split governance.
4. **Mentor Action Items & Corrections:** Sign-off criteria and compliance validation."""
cells.append(nbf.v4.new_markdown_cell(md1))

# Cell 2: Code Load Configuration & Metrics
code1 = """from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

NOTEBOOK_DIR = Path.cwd()
DAY23_METRICS = NOTEBOOK_DIR.parent / 'day23_hemamdhar_softwareperformancefinalvalidation' / 'final_validation_performance_metrics.csv'
DAY22_CONFIG = NOTEBOOK_DIR.parent / 'day22_hemamdhar_finalpipelinefreeze' / 'frozen_pipeline_config.json'

metrics_df = pd.read_csv(DAY23_METRICS)
config = json.loads(DAY22_CONFIG.read_text(encoding='utf-8'))

print('=== Day 24 Final Technical Review Pack ===')
print(f'Pipeline Name: {config[\"pipeline_name\"]}')
print(f'Pipeline Status: {config[\"status\"]}')
print(f'Frozen Preprocessing: {config[\"frozen_components\"][\"preprocessing\"][\"method\"]} (Clip: {config[\"frozen_components\"][\"preprocessing\"][\"clip_limit\"]}, Grid: {config[\"frozen_components\"][\"preprocessing\"][\"tile_grid_size\"]})')
print(f'Frozen Detector: {config[\"frozen_components\"][\"detection_model\"][\"architecture\"]} ({config[\"frozen_components\"][\"detection_model\"][\"parameter_count\"]:,} params)')
print(f'Real-Time Throughput: {metrics_df.loc[metrics_df[\"variant\"] == \"CLAHE 1.5 (Frozen)\", \"fps\"].values[0]:.2f} FPS')"""
cells.append(nbf.v4.new_code_cell(code1))

# Cell 3: Markdown Section 1
md2 = """## 1. 3-Slide Progress Pack Summary

Below is the comparative performance data synthesized for the technical review board."""
cells.append(nbf.v4.new_markdown_cell(md2))

# Cell 4: Code Display Table
code2 = """display_cols = [
    'variant', 'preprocess_mean_ms', 'inference_mean_ms', 'total_latency_mean_ms', 
    'fps', 'quality_contrast_gain', 'pareto_optimal_status'
]
metrics_df[display_cols]"""
cells.append(nbf.v4.new_code_cell(code2))

# Cell 5: Markdown Section 2
md3 = """## 2. End-to-End Workflow Execution Test

We verify the reproducible execution of the frozen pipeline on synthetic / sample frame input."""
cells.append(nbf.v4.new_markdown_cell(md3))

# Cell 6: Code Execute Pipeline
code3 = """import sys
sys.path.insert(0, str(NOTEBOOK_DIR.parent / 'day22_hemamdhar_finalpipelinefreeze'))
from frozen_pipeline import FrozenPipeline
import numpy as np

pipeline = FrozenPipeline(
    enhancement_method='clahe',
    clip_limit=1.5,
    grid_size=8,
    image_size=320,
    conf_threshold=0.25,
    iou_threshold=0.50
)

test_frame = np.full((640, 640, 3), (15, 65, 110), dtype=np.uint8)
res = pipeline.process_frame(test_frame)

print('=== Live Workflow Verification ===')
print(f'Status: {res[\"status\"]}')
print(f'Preprocessing: {res[\"preprocessing_ms\"]:.3f} ms')
print(f'Inference: {res[\"inference_ms\"]:.3f} ms')
print(f'Tracking: {res[\"tracking_ms\"]:.3f} ms')
print(f'Total Latency: {res[\"total_latency_ms\"]:.3f} ms ({res[\"throughput_fps\"]:.1f} FPS)')"""
cells.append(nbf.v4.new_code_cell(code3))

# Cell 7: Markdown Section 3
md4 = """## 3. Programmatic Technical Review Assertions

We execute automated assertions verifying that all technical review constraints, latency limits, and split governance policies are satisfied."""
cells.append(nbf.v4.new_markdown_cell(md4))

# Cell 8: Code Assertions
code4 = """# Programmatic technical review assertions
assert config['status'] == 'FROZEN_IMMUTABLE', 'Pipeline freeze status mismatch'
assert config['frozen_components']['split_policy']['test_split_size'] == 954, 'Test split size check failed'
assert metrics_df.loc[metrics_df['variant'] == 'CLAHE 1.5 (Frozen)', 'fps'].values[0] >= 30.0, '30 FPS requirement failed'
assert config['frozen_components']['preprocessing']['clip_limit'] == 1.5, 'Clip limit mismatch'
assert config['frozen_components']['detection_model']['architecture'] == 'YOLOv8n', 'Detector architecture mismatch'

print('All Day 24 Final Technical Review verification assertions passed successfully.')"""
cells.append(nbf.v4.new_code_cell(code4))

nb['cells'] = cells

client = NotebookClient(nb, timeout=60, kernel_name='python3')
executed_nb = client.execute()

nbf.write(executed_nb, DIR / 'final_technical_review.ipynb')
nbf.write(executed_nb, DIR / 'final_technical_review_v1.ipynb')
with open(DIR / 'final_technical_review_submission.ipynb.json', 'w', encoding='utf-8') as f:
    json.dump(executed_nb, f, indent=2)

print('Executed notebook generated and saved to final_technical_review.ipynb and final_technical_review_submission.ipynb.json!')
