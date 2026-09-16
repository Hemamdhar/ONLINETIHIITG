# Day 21 — Week-4 Final Direction & Mentor Approval Record

## Review Record & Status

- **Project:** AI-Based Underwater Visual Surveillance
- **Milestone:** Day 21 — Best Candidate Review & Week-4 Direction Sign-Off
- **Status:** **SUBMITTED FOR MENTOR APPROVAL**
- **Evidence Basis:** 
  - Day 16: Raw YOLOv8n object detection baseline
  - Day 17: Matched test inference (Raw, CLAHE, Gamma) and exploratory tracker interface
  - Day 18: Model/method trade-off comparison matrix and shortlist
  - Day 19: Controlled validation parameter sweep (CLAHE clip limits 1.5, 2.0, 3.0)
  - Day 20: Project-specific robustness ablation and 4-stage pipeline error propagation audit
  - Day 21: Quantitative synthesis, failure taxonomy, and best-candidate specification

---

## 1. Approved Best-Candidate Configuration

```json
{
  "enhancement": {
    "method": "CLAHE (CIELAB L-channel)",
    "clip_limit": 1.5,
    "tile_grid": [8, 8],
    "preprocess_latency": "6.21 ms / image",
    "throughput": "33.72 FPS"
  },
  "detector": {
    "architecture": "YOLOv8n (Compact 3.0M params)",
    "training_budget": "50 epochs on full DIAT dataset",
    "image_size": 320,
    "confidence_threshold": 0.25,
    "iou_threshold": 0.50
  },
  "control": {
    "method": "raw_v1 (Mandatory unenhanced reference baseline)"
  }
}
```

---

## 2. Proposed Key Decisions for Week-4

| Strategic Topic | Proposed Recommendation | Rationale & Evidence | Mentor Approval Status |
| :--- | :--- | :--- | :---: |
| **1. Primary Enhancement Candidate** | **Approve CLAHE (Clip=1.5, Grid=8)** | Lowest preprocessing overhead ($+3.76\text{ ms}$), highest throughput ($33.72\text{ FPS}$), and suppression of noise artifacts. | **[PENDING MENTOR SIGN-OFF]** |
| **2. Mandatory Control Pipeline** | **Retain `raw_v1` in parallel** | Ensures scientific validity by isolating the exact performance delta attributable to photometric preprocessing. | **[PENDING MENTOR SIGN-OFF]** |
| **3. Detector Training Horizon** | **Train YOLOv8n for 50 full epochs** | Overcomes the smoke-run underfitting bottleneck to generate converged feature extractors for underwater marine life. | **[PENDING MENTOR SIGN-OFF]** |
| **4. Multi-Dataset Policy** | **Focus exclusively on DIATAquarium** | `Aquatic Plant` and `Well` lack sequence-independent partitions and risk data leakage; keeping them isolated protects scientific integrity. | **[PENDING MENTOR SIGN-OFF]** |
| **5. Test Split Governance** | **Strictly freeze 954 test images** | No test images will be evaluated until the trained model weights and preprocessing parameters are frozen on Day 26. | **[PENDING MENTOR SIGN-OFF]** |
| **6. Tracking Scope** | **Exploratory Greedy IoU + ByteTrack** | Formal MOTA/IDF1 metrics deferred due to lack of ground-truth persistent IDs; evaluate trajectory continuity and hit consistency. | **[PENDING MENTOR SIGN-OFF]** |

---

## 3. Detailed Week-4 Daily Execution Roadmap (Days 22–28)

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                               WEEK-4 EXECUTION TIMELINE                               │
├──────────────┬────────────────────────────────────────────────────────────────────────┤
│ Day 22       │ Full Detector Training (50 Epochs, complete DIAT training split)       │
│ Day 23       │ Paired Validation Benchmark (Raw vs CLAHE 1.5 on Precision/Recall/mAP)│
│ Day 24       │ Stratified Error Analysis (Turbidity, low light, rare-class recall)    │
│ Day 25       │ Sequence Tracking Evaluation & Trajectory Consistency Audit           │
│ Day 26       │ One-Shot Final Test Evaluation (Frozen winning pipeline)               │
│ Day 27       │ Comprehensive Technical Paper / Final Project Report & Presentation    │
│ Day 28       │ Final Review, Packaging, Artifact Archival, and Release                │
└──────────────┴────────────────────────────────────────────────────────────────────────┘
```

- **Day 22 — Full Model Convergence & Training:** Train YOLOv8n for 50 epochs on the complete `DIATAquarium.v4i.yolov8` training split under controlled seeds.
- **Day 23 — Paired Validation Benchmark:** Evaluate the converged detector on raw vs. CLAHE 1.5 validation data; compute Precision, Recall, mAP@50, mAP@50-95, and per-class AP.
- **Day 24 — Environmental Stratification & Robustness:** Measure detection robustness across stratified underwater degradation categories (low illumination, heavy turbidity, blue/green color cast).
- **Day 25 — Sequence Tracking & Association:** Execute the greedy IoU and ByteTrack tracker modules on ordered validation sequences; evaluate tracklet fragmentation and trajectory smoothness.
- **Day 26 — One-Shot Test Split Evaluation:** Unfreeze the 954-image test split and execute a single, final evaluation run to establish unbiased generalization metrics.
- **Day 27 — Comprehensive Technical Report & Slides:** Author the final end-to-end research report and 10-slide executive presentation pack.
- **Day 28 — Peer Review, Release Packaging, and Archival:** Conduct final code refactoring, verify reproducibility scripts, and package the complete repository.

---

## 4. Specific Mentor Review Questions

1. **Enhancement Parameter Freezing:** Is **CLAHE ($1.5, 8 \times 8$)** approved as the definitive enhancement candidate for the 50-epoch training and validation benchmark?
2. **Computational Target:** Is an inference throughput target of **$\ge 30\text{ FPS}$** on edge CPU acceptable for real-time marine monitoring?
3. **Acceptance Thresholds:** Are minimum validation targets of **$\text{mAP@50} \ge 0.40$** and **$\text{mAP@50-95} \ge 0.25$** approved as acceptance criteria?
4. **Tracking Deliverable:** Is reporting **trajectory continuity, ID count, and fragmentation rate** acceptable given the lack of ground-truth sequence tracking IDs?

---

## 5. Mentor Sign-Off Section

**Mentor Name / Title:** _____________________________________________

**Review Date:** _____________________________________________

**Decision:** `[ ] APPROVED FOR WEEK 4` &nbsp;&nbsp;&nbsp;&nbsp; `[ ] APPROVED WITH CONDITIONS` &nbsp;&nbsp;&nbsp;&nbsp; `[ ] REVISION REQUIRED`

**Mentor Notes & Guidance:**
```text


```
