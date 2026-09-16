# Candidate Methods

## 1. Image Enhancement

### Classical Baseline: CLAHE

CLAHE will be considered as a simple baseline for improving local contrast in underwater images. It is computationally efficient and does not require model training.

### Learning-Based Method: FUnIE-GAN

FUnIE-GAN will be considered as a deep learning-based underwater image enhancement method. It is designed for enhancing underwater imagery and provides a useful comparison against a classical enhancement baseline.

### Alternative Learning-Based Method: WaterNet

WaterNet can be considered as an additional learning-based enhancement method because it uses a fusion-based approach for improving underwater image quality.

---

## 2. Object Detection

### Primary Candidate: YOLO with Transfer Learning

A pretrained YOLO model will be fine-tuned on the provided underwater dataset. Transfer learning is suitable because pretrained models already contain useful visual features and can be adapted to a new object detection dataset with less training data than training from scratch.

Evaluation metrics will include:

* Precision
* Recall
* mAP@50
* mAP@50–95

---

## 3. Object Tracking

### Baseline Tracker: SORT

SORT will be considered when video or sequence data is available. It is simple, fast and suitable as an initial tracking baseline.

### Advanced Candidate: DeepSORT or ByteTrack

If the dataset contains sufficient sequence information, DeepSORT or ByteTrack can be evaluated to improve object identity consistency and tracking stability.

---

## Proposed Initial Pipeline

Underwater Input

↓

Image Quality Analysis

↓

CLAHE / Learning-Based Enhancement

↓

YOLO Object Detection

↓

SORT / DeepSORT / ByteTrack

↓

Performance Evaluation and Failure Analysis

---

## Initial Method Selection

The initial experimental setup will compare:

**Baseline Pipeline:**

Raw Underwater Image → YOLO Detection

**Enhanced Pipeline:**

Underwater Image → Image Enhancement → YOLO Detection

This comparison will help determine whether image enhancement improves downstream object detection rather than assuming that visually enhanced images automatically produce better detection performance.
