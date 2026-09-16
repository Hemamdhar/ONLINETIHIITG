# Experiment Plan

## 1. Objective

Measure whether underwater image enhancement improves object detection over raw images, while keeping the comparison reproducible and protecting the evaluation from sequential-frame leakage.

## 2. Dataset Protocol

The three exports should first be analyzed separately because their class vocabularies differ. A unified model should only be trained after an explicit class mapping and a decision about whether same-named classes such as `fish`, `fishes`, and `school-of-fish` are semantically compatible.

For every image, create a manifest with:

- dataset name and class-map version;
- image and label paths;
- source video or sequence ID parsed from the filename;
- frame ID when it can be parsed;
- split and validation status.

Use group-aware splitting by source video or sequence. The original Roboflow split may be retained only after verifying that no source group crosses its boundaries. If the source ID cannot be parsed reliably, mark tracking and leakage-sensitive results as blocked until the ambiguity is resolved.

## 3. Controlled Variables

Keep these fixed across comparable runs:

- dataset and class mapping;
- leakage-safe manifests;
- detector architecture and pretrained checkpoint;
- input image size, epochs, batch size, optimizer, and seed;
- augmentation policy;
- confidence and IoU thresholds used for reporting;
- evaluation script and test manifest.

Run each important configuration with at least three seeds when compute permits. Report mean and standard deviation rather than selecting the best seed only.

## 4. Experiment Matrix

| ID  | Pipeline                                                          | Purpose                          | Required comparison                                     |
| --- | ----------------------------------------------------------------- | -------------------------------- | ------------------------------------------------------- |
| E0  | Dataset validation only                                           | Establish data readiness         | No model result; record failures and counts             |
| E1  | Raw image -> pretrained YOLO detector                             | Primary baseline                 | Per-dataset and aggregate detection metrics             |
| E2  | Raw image -> YOLO fine-tuning                                     | Stronger detector baseline       | Compare against E1 using the same split                 |
| E3  | CLAHE or a documented classical enhancement -> YOLO               | Low-cost enhancement baseline    | Compare visual quality and downstream detection with E2 |
| E4  | FUnIE-GAN, WaterNet, or another selected learned enhancer -> YOLO | Advanced enhancement             | Compare against E2 with the same detector protocol      |
| E5  | Best enhancement + detector                                       | Project-specific final candidate | Confirm on untouched test data only once                |
| E6  | Detector -> SORT or ByteTrack on ordered frames                   | Tracking feasibility study       | Run only with sequence-level evaluation support         |

E3 and E4 should be selected after a small validation-only screening. Do not use test results to choose the enhancement method.

## 5. Baseline Method

The baseline is a pretrained YOLO object detector fine-tuned on the raw underwater images. It provides the reference point for all enhancement claims. Training should use the official class mapping for one dataset at a time initially, because the three exports do not share the same label space.

## 6. Advanced Methods

Candidate methods from the literature review are:

- CLAHE as a transparent classical baseline.
- FUnIE-GAN or WaterNet as a learned enhancement method.
- ByteTrack or SORT for detection-based temporal association.

The advanced enhancement method must be selected using validation results and practical processing cost. Tracking is not a primary accuracy experiment because the supplied annotations have no persistent object IDs.

## 7. Project-Specific Experiment

The main ablation compares raw and enhanced inputs while holding the detector and training protocol constant:

```text
Same leakage-safe split + same YOLO protocol
        raw images       -> detection metrics
        enhanced images  -> detection metrics
```

The enhancement is considered useful only if it produces a meaningful downstream improvement without an unacceptable increase in inference time or failure on rare classes. A higher UIQM score alone is not sufficient evidence.

## 8. Evaluation Criteria

### Detection

- Precision, recall, mAP@50, and mAP@50-95.
- Per-class precision, recall, AP, and support.
- Confusion matrix and false-positive/false-negative examples.
- Results separately for each dataset and, only when justified, for an explicitly mapped unified dataset.

### Image quality

- UIQM or a comparable underwater quality metric for every image variant.
- PSNR and SSIM only where a trustworthy reference image exists; generated enhanced images without a reference should not be assigned reconstruction scores.
- Human visual examples covering haze, blur, low light, color distortion, and occlusion.

### Tracking

- IDF1, MOTA, identity switches, and track fragmentation only if persistent ground-truth IDs are obtained.
- Otherwise report track continuity, lost tracks, and identity-switch proxies as exploratory observations, clearly labeled as non-ground-truth measures.

### Efficiency and reproducibility

- Preprocessing/enhancement time per image.
- Detector inference time per image and frames per second.
- End-to-end time per frame, peak memory where available, hardware, software versions, model size, and parameter count.

## 9. Run Procedure

1. Run E0 and save the validated manifest and data report.
2. Train E1 or E2 using only the training manifest.
3. Select configurations using validation metrics and validation-side timing.
4. Evaluate the selected configuration once on the untouched test manifest.
5. Repeat the identical protocol for enhancement variants.
6. Run tracking only on ordered sequences that remain independent of training and have suitable annotations.
7. Save predictions, metrics, configuration, logs, and environment details for every run.

## 10. Decision Rules

The preferred pipeline should:

- improve or preserve mAP@50-95 and recall relative to the raw baseline;
- avoid a severe drop in rare-class AP;
- show a defensible image-quality improvement where quality is measured;
- satisfy the project processing-time requirement;
- reproduce within an acceptable range across seeds;
- have no unresolved split or annotation leakage.
