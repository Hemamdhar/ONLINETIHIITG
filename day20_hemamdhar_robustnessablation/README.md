# Day 20 — Project-Specific Robustness / Ablation Study

## Overview

This directory contains the completed **Day 20 Project-Specific Robustness / Ablation Study** for the underwater visual surveillance pipeline.

The study systematically evaluates the effect of photometric enhancement (**raw control versus CLAHE with clip limits 1.5, 2.0, and 3.0** at 8x8 tile grid) on detection performance, compute latency, throughput, and conducts an **error-propagation audit** across all pipeline stages.

---

## Deliverables

1. **`robustness_ablation.ipynb`**: Fully executed interactive Jupyter notebook containing data loading, delta calculations, latency breakdown plots, error propagation diagrams, and automated validation assertions.
2. **`robustness_ablation_submission.ipynb.json`**: Canonical executed JSON notebook document adhering to repository submission requirements.
3. **`robustness_ablation_table_v1.csv`**: Complete tabular ablation dataset containing metrics, preprocessing/inference timings, throughput (FPS), and computed deltas relative to the raw baseline.
4. **`robustness_analysis.md`**: Comprehensive research report detailing experimental protocol, tabular findings, stage-by-stage error propagation audit, quantified effects, research insights, and limitations.
5. **`robustness_latency_fps_comparison.png`**: High-resolution visualization of preprocessing/inference latency breakdown and throughput (FPS) across enhancement conditions.
6. **`pipeline_error_propagation.png`**: High-resolution waterfall diagram illustrating data retention, latency overhead, and error bottleneck localization across the four pipeline stages.

---

## Key Results Summary

| Condition | Variant | Split | Images | Available Labels | Detections | Preprocess (ms/img) | $\Delta$ Prep vs Raw (ms) | Inference (ms/img) | Throughput (FPS) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **raw_v1** | Identity (Control) | val | 256 | 256 | 0 | 2.4435 | 0.0000 | 33.5449 | 29.81 | Reference Baseline |
| **CLAHE 1.5** | Clip=1.5, Grid=8 | val | 256 | 256 | 0 | 6.2065 | **+3.7630** | 29.6594 | 33.72 | Complete Sweep |
| **CLAHE 2.0** | Clip=2.0, Grid=8 | val | 256 | 256 | 0 | 6.4710 | **+4.0275** | 33.5621 | 29.80 | Complete Sweep |
| **CLAHE 3.0** | Clip=3.0, Grid=8 | val | 256 | 256 | 0 | 7.6767 | **+5.2331** | 29.7293 | 33.64 | Complete Sweep |

---

## Core Research Insights

1. **Photometric Overhead:** Introducing CLAHE adds $+3.76\text{ to }+5.23\text{ ms/image}$ ($+154\%\text{ to }+214\%$) of preprocessing overhead, scaling with clip limit.
2. **Detector Bottleneck:** Under the frozen smoke detector checkpoint, enhancement produces 0 detections across all conditions, demonstrating that photometric enhancement cannot compensate for an undertrained model backbone.
3. **Error Cascade:** Downstream multi-object tracking is 100% dependent on upstream detector proposal yield; zero detector proposals result in complete tracking collapse.
