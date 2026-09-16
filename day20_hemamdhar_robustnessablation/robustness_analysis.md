# Day 20 — Project-Specific Robustness / Ablation Study

## Executive Summary

This study completes the **Day 20 Project-Specific Robustness and Ablation Study** for the underwater visual surveillance system. We systematically compare object detection performance on **raw versus enhanced underwater imagery** across multiple photometric enhancement variants and conduct an **error-propagation audit** across all four stages of the computer vision pipeline.

All experiments were executed on the deterministic 256-image DIAT validation subset established during Day 19 under identical frozen detector hyperparameters (image size 320, confidence threshold 0.25, IoU threshold 0.50, CPU inference). The final 954-image test split remained completely untouched to guarantee zero data leakage.

---

## 1. Research Question & Hypothesis

### Primary Research Question
> **"How does underwater image enhancement affect the performance of deep learning-based object detection, and can an effective computer vision pipeline provide reliable object detection and tracking for underwater visual surveillance?"**

### Sub-Questions Addressed in Day 20
1. **Component Ablation:** What is the precise computational cost (latency and FPS) and detection sensitivity effect of introducing CLAHE enhancement with varying clip limits ($1.5$, $2.0$, $3.0$) relative to the raw image baseline?
2. **Error Propagation:** At which stage in the four-stage pipeline (Data Ingestion $\rightarrow$ Enhancement $\rightarrow$ Detection $\rightarrow$ Tracking) do errors originate, amplify, or bottleneck downstream performance?
3. **Robustness & Degradation:** Does contrast recovery in the luminance channel translate into improved object proposal yield under low-visibility underwater conditions?

---

## 2. Experimental Setup & Protocol

- **Dataset:** `DIATAquarium.v4i.yolov8` (prepared via Day 11 manifest `manifest_v1.json`).
- **Evaluation Split:** Deterministic 256 validation records sorted lexicographically by image path.
- **Model Checkpoint:** Frozen Day 16 YOLOv8n detector (`best.pt`, 3,007,793 parameters, 5.92 MB).
- **Inference Configuration:** `imgsz=320`, `conf=0.25`, `iou=0.50`, `batch=16`, `device='cpu'`.
- **Enhancement Method:** Contrast Limited Adaptive Histogram Equalization (CLAHE) applied to the Lightness ($L$) channel in the CIELAB color space with fixed $8 \times 8$ grid tiles and varying clip limits.
- **Compared Conditions:**
  1. `raw_v1` (Identity control, no enhancement)
  2. `clahe_1.5x8` (Mild contrast enhancement: clip limit 1.5, tile grid 8x8)
  3. `clahe_2.0x8` (Standard baseline enhancement: clip limit 2.0, tile grid 8x8)
  4. `clahe_3.0x8` (Aggressive contrast enhancement: clip limit 3.0, tile grid 8x8)

---

## 3. Ablation Results Table

The quantitative measurements and relative deltas across conditions are summarized below:

| Condition | Variant / Config | Split | Images | Available Labels | Detections | Preprocess (ms/img) | $\Delta$ Prep vs Raw (ms) | Inference (ms/img) | $\Delta$ Inf vs Raw (ms) | Throughput (FPS) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **raw_v1** | Identity (Control) | val | 256 | 256 | 0 | 2.4435 | 0.0000 | 33.5449 | 0.0000 | 29.81 | Reference Baseline |
| **CLAHE 1.5** | Clip=1.5, Grid=8 | val | 256 | 256 | 0 | 6.2065 | **+3.7630** | 29.6594 | -3.8855 | 33.72 | Complete Sweep |
| **CLAHE 2.0** | Clip=2.0, Grid=8 | val | 256 | 256 | 0 | 6.4710 | **+4.0275** | 33.5621 | +0.0173 | 29.80 | Complete Sweep |
| **CLAHE 3.0** | Clip=3.0, Grid=8 | val | 256 | 256 | 0 | 7.6767 | **+5.2331** | 29.7293 | -3.8156 | 33.64 | Complete Sweep |

*Artifact location: `robustness_ablation_table_v1.csv`*

---

## 4. Quantified Effects

### 1. Preprocessing Overhead Effect
- Introducing CLAHE creates a strictly monotonic increase in preprocessing compute overhead:
  - **Clip Limit 1.5:** $+3.7630\text{ ms/image}$ ($+154.0\%$ over raw)
  - **Clip Limit 2.0:** $+4.0275\text{ ms/image}$ ($+164.8\%$ over raw)
  - **Clip Limit 3.0:** $+5.2331\text{ ms/image}$ ($+214.2\%$ over raw)
- Aggressive clipping requires more frequent iterative redistributions of histogram bins in the lightness channel, directly scaling runtime.

### 2. Detection Yield Effect
- All four conditions yielded **0 detections / 256 validation images** at the standard confidence threshold ($\text{conf}=0.25$).
- Consequently, the observed detection count delta across all CLAHE variants is $\Delta \text{Detections} = 0$.

### 3. Inference & Frame Rate Effect
- Model inference latency remained stable within the expected CPU scheduling variance ($29.66 - 33.56\text{ ms/image}$), corresponding to $29.8 - 33.7\text{ FPS}$.
- Because the input tensor dimension ($320 \times 320 \times 3$) is identical for raw and CLAHE images, convolutional FLOPs at the neural network level are unchanged.

### 4. Accuracy Metric Estimability
- Formal accuracy metrics (Precision, Recall, mAP@50, mAP@50-95, per-class AP) were not estimable during this sweep due to zero true positives emitted by the abbreviated smoke detector checkpoint.

---

## 5. Pipeline Error Propagation Audit

We analyze the end-to-end computer vision pipeline across four discrete stages to pinpoint error origins and understand how failures cascade:

```
┌────────────────────────────────┐
│   Stage 1: Source & Labels     │  ──► 256/256 Images & Annotations Valid (100% Retained)
└────────────────────────────────┘
               │
               ▼
┌────────────────────────────────┐
│ Stage 2: Photometric Enhance   │  ──► +3.76 to +5.23 ms Preprocessing Overhead; Geometry Preserved
└────────────────────────────────┘
               │
               ▼
┌────────────────────────────────┐
│   Stage 3: Object Detector     │  ──► [BOTTLENECK] 0 Proposals Emitted (Smoke Checkpoint Horizon)
└────────────────────────────────┘
               │
               ▼
┌────────────────────────────────┐
│   Stage 4: Downstream Tracker  │  ──► [BLOCKED] 0 Detections ──► 0 Tracklets Formed (Cascade Failure)
└────────────────────────────────┘
```

### Stage 1: Data Ingestion & Ground Truth Label Stage
- **Input:** 256 paired DIAT validation images and YOLO-formatted label text files.
- **Audit:** 256/256 records possessed valid ground-truth annotations containing bounding boxes for underwater organisms.
- **Error Status:** **Zero upstream data error.** No missing files, corrupted headers, or malformed bounding box formats were identified.

### Stage 2: Photometric Enhancement Preprocessing Stage
- **Transformation:** CIELAB color-space conversion, lightness histogram equalization with clipping, and RGB reconversion.
- **Audit:** The spatial domain is completely invariant under photometric transformation; bounding box coordinates $(x_c, y_c, w, h)$ remain exact and aligned.
- **Error Status:** **Zero geometric error.** The only effect introduced is computational latency ($+3.76\text{ to }+5.23\text{ ms}$).

### Stage 3: Transfer-Learning Object Detection Stage
- **Inference:** Frozen YOLOv8n network executing forward pass on raw and enhanced tensors.
- **Audit:** The network produced 0 bounding box proposals with $\text{confidence} \ge 0.25$.
- **Error Status:** **Primary Bottleneck Identified.** The Day 16 baseline model was trained for only 1 epoch on 2% of the training dataset as an intentionally abbreviated smoke run. Consequently, its convolutional feature extractors have not formed discriminative weights for underwater organisms.

### Stage 4: Downstream Multi-Object Tracking & Association Stage
- **Tracking Algorithm:** Kalman filter motion prediction and Hungarian algorithm association (ByteTrack / SORT paradigm).
- **Audit:** Trackers require detector bounding boxes as inputs to initialize tracks, predict trajectories, and assign IDs.
- **Error Status:** **Downstream Cascade Collapse.** With zero detector proposals, the tracker receives null inputs and cannot initialize tracklets. The tracking stage fails entirely as a downstream consequence of Stage 3 failure.

---

## 6. Research Insights & Interpretation

1. **Photometric Enhancement vs Detector Capacity:**
   - Image enhancement improves visual contrast for human perception, but it **cannot compensate for an under-trained feature extractor**. Neural network backbones require discriminative training to associate enhanced edges and textures with semantic object classes.
2. **Computational Budget Allocation in Underwater Surveillance:**
   - In resource-constrained deployments (such as AUVs or edge marine monitors), adding CLAHE incurs a $+154\%$ to $+214\%$ preprocessing latency penalty. If the downstream detector has not been trained specifically on enhanced distributions, this computational expenditure provides zero return on detection accuracy.
3. **Pipeline Error Containment:**
   - The modular pipeline architecture cleanly contained geometric errors between Stages 1 and 2, but exhibited a total cascade failure between Stages 3 and 4. This underscores that in vision pipelines, **detector recall is the single critical dependency for multi-object tracking stability**.

---

## 7. Limitations & Future Verification Roadmap

- **Full Training Run:** Train the YOLOv8n detector for 50 full epochs on the complete DIATAquarium dataset to obtain non-zero validation detections.
- **Multi-Condition Retraining:** Compare two training paradigms:
  1. Training on raw data and evaluating on enhanced data (cross-domain robustness).
  2. Training directly on CLAHE-enhanced data (matched domain).
- **Degradation Stratification:** Stratify validation evaluation across specific underwater environmental challenges:
  - Low illumination / deep water scenes
  - High turbidity / suspended particle scattering
  - Strong green/blue wavelength absorption
- **Tracking Ground Truth:** Obtain sequential video frames with ground-truth object trajectories to evaluate MOTA, IDF1, and identity switches once non-empty detections are available.

---

## 8. Verification & Reproducibility Deliverables

- `robustness_ablation.ipynb`: Fully executed Jupyter notebook with code, outputs, and matplotlib figures.
- `robustness_ablation_submission.ipynb.json`: Canonical JSON notebook document adhering to repository submission requirements.
- `robustness_ablation_table_v1.csv`: Standardized tabular ablation dataset with quantified deltas.
- `robustness_latency_fps_comparison.png`: Generated latency breakdown and FPS comparison chart.
- `pipeline_error_propagation.png`: Generated stage-by-stage pipeline error propagation audit diagram.
- `README.md`: Deliverable index and summary.
