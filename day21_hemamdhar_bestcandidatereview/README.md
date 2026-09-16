# Day 21 — Best Candidate Review & Week-4 Direction

## Overview

This directory contains the completed **Day 21 Best Candidate Review** for the **AI-Based Underwater Visual Surveillance** project.

This milestone synthesizes the experimental progress across Weeks 1 to 3 (Days 1–20), evaluates baseline versus tuned results, presents a comprehensive success and failure mode analysis, and establishes the formal **Best-Candidate pipeline architecture** and **Mentor-Approved Roadmap for Week 4**.

---

## Deliverables

1. **`best_candidate_review.md`**: Comprehensive synthesis of baseline vs. tuned results, component trade-off matrix, best-candidate selection rationale, and empirical summary across Days 16–20.
2. **`success_failure_analysis.md`**: Deep-dive qualitative and quantitative audit of pipeline success pillars, bottleneck localizations, unusual errors (over-enhancement artifacts, confidence starvation), and environmental degradation modes.
3. **`week4_direction_and_mentor_approval.md`**: Formal Week-4 proposal and mentor sign-off document featuring key decisions, daily execution timeline (Days 22–28), and acceptance criteria.
4. **`best_candidate_config.json`**: Machine-readable specification of the approved best-candidate pipeline configuration (`CLAHE 1.5, 8x8` + `YOLOv8n 50 epochs` + `raw_v1 control`).
5. **`baseline_vs_tuned_summary.csv`**: Complete multi-stage experimental dataset summarizing metrics, timings, throughput, and outcomes across Days 16–20.
6. **`best_candidate_review.ipynb`**: Fully executed interactive Jupyter notebook with summary tables, latency plots, throughput comparisons, and validation assertions.
7. **`best_candidate_review_submission.ipynb.json`**: Canonical executed JSON notebook document adhering to repository submission requirements.
8. **`baseline_vs_tuned_comparison.png`**: High-resolution chart comparing preprocessing latency, inference latency, and FPS across enhancement variants against real-time operational thresholds.
9. **`success_failure_taxonomy.png`**: Visual diagram categorizing validated pipeline successes, localized bottlenecks, and the Week-4 direction.

---

## Key Review Findings

- **Best-Candidate Enhancement:** **CLAHE ($1.5, 8 \times 8$)** selected due to lowest preprocessing overhead ($+3.76\text{ ms/image}$ over raw), real-time throughput ($33.72\text{ FPS}$ on edge CPU), and suppression of high-frequency noise artifacts.
- **Mandatory Control:** **`raw_v1`** retained in parallel as the scientific reference baseline.
- **Detector Target:** **YOLOv8n** ($3.0\text{M}$ parameters, $5.92\text{ MB}$) to be trained for 50 full epochs on the complete DIATAquarium dataset in Week 4.
- **Split Governance:** The 954-image test split remains strictly frozen until the Day 26 final benchmark.
