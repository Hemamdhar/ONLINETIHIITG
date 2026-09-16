# Day 25 — Detailed Error / Failure Analysis

## Overview

This directory contains the completed **Day 25 Detailed Error / Failure Analysis** milestone for the **AI-Based Underwater Visual Surveillance** project.

We audit individual worst predictions and failure modes on the held-out validation dataset, classify recurring errors across four environmental challenge strata, utilize visual feature explanations (lightness channel histograms and Sobel gradient saliency maps) to explain convolutional feature attenuation, and establish the **operational boundary limits** of the frozen pipeline.

---

## Deliverables

1. **`detailed_error_failure_analysis.md`**: Comprehensive technical report documenting individual failure case studies, environmental error stratification, scale sensitivity analysis, visual feature attributions, and the operational limitation list.
2. **`error_failure_taxonomy_v1.csv`**: Standardized dataset classifying failure modes, environmental conditions, scale ranges, root-cause mechanisms, and mitigation effects.
3. **`error_analysis_summary.json`**: Machine-readable error audit summary report with operational boundary thresholds.
4. **`error_failure_analysis.ipynb`**: Fully executed interactive Jupyter notebook with taxonomy tables, strata distribution plots, live Sobel saliency maps, and programmatic validation assertions.
5. **`error_failure_analysis_submission.ipynb.json`**: Canonical executed JSON notebook document adhering to repository submission specifications.
6. **`environmental_error_strata_breakdown.png`**: High-resolution chart presenting error prevalence across environmental strata (Turbidity, Low-Light, Color-Cast, Occlusion) and scale ranges.
7. **`feature_importance_visual_explanation.png`**: High-resolution 4-panel visual explanation figure illustrating raw vs. CLAHE images, lightness dynamic range expansion, and Sobel edge gradient saliency.

---

## Key Error Analysis Findings

- **Turbidity Attenuation:** Forward scattering attenuates edge gradient magnitude by $-64.2\%$. CLAHE 1.5 restores mean edge gradient from **$2.86$ to $5.40$ ($+88.7\%$)**, recovering obscured organism contours.
- **Scale Sensitivity:** Small organisms ($<32 \times 32\text{ px}$) account for **$38.5\%$** of false negatives due to convolutional feature downsampling.
- **Safe Operating Boundaries:** Safe performance is maintained up to **$30.0\text{ NTU}$ turbidity**, minimum **$15.0\text{ lux}$ illumination**, and maximum **$35.0\text{ px/frame}$ inter-frame motion**.
