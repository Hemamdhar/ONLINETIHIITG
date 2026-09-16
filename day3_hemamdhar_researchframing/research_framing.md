# Day 3 — Research Framing 

## Project Research Framing

### Project Domain

The project focuses on AI-based underwater visual surveillance using computer vision and deep learning techniques.

Underwater images and videos often suffer from poor visibility, color distortion, low contrast, scattering and other environmental challenges. These conditions can affect the performance of downstream computer vision tasks such as object detection and tracking.

The project aims to investigate an end-to-end computer vision pipeline for processing underwater visual data and performing reliable object detection and, where applicable, object tracking.

---

## Revised Research Question

**How does underwater image enhancement affect the performance of deep learning-based object detection, and can an effective computer vision pipeline provide reliable object detection and tracking for underwater visual surveillance?**

---

## Research Sub-Questions

1. What are the major visual challenges present in the provided underwater dataset?

2. Can classical or learning-based image enhancement improve the visual quality of underwater images?

3. Does image enhancement improve downstream object detection performance compared with using raw underwater images?

4. How effectively can a transfer-learning-based object detector identify underwater objects?

5. If sequence data is available, how stable can object tracking be across consecutive frames?

---

## Target Definition

The primary target of the project is to develop and evaluate a computer vision pipeline capable of detecting objects in underwater imagery.

The system will take underwater images or video frames as input and produce object detections containing:

* Object class
* Bounding box location
* Detection confidence

If video or sequential data is available, the system may additionally produce:

* Object identities
* Object trajectories
* Tracking consistency across frames

---

## Measurable Outputs

The project will measure the following outputs.

### Image Enhancement

Where enhancement methods are evaluated:

* Visual quality comparison
* PSNR, where reference images are available
* SSIM, where reference images are available
* UIQM or other suitable underwater image quality measures

### Object Detection

The detection model will be evaluated using:

* Precision
* Recall
* mAP@50
* mAP@50–95

### Object Tracking

If sequence data is available, tracking may be evaluated using:

* Tracking consistency
* Number of identity switches
* MOTA
* IDF1

The final tracking metrics will depend on the dataset annotations and available ground-truth sequence information.

---

## Experimental Scope

The initial experiments will focus on comparing two pipelines.

### Pipeline 1 — Baseline

Raw Underwater Image

↓

Object Detector

↓

Detection Evaluation

### Pipeline 2 — Enhanced Pipeline

Raw Underwater Image

↓

Image Enhancement

↓

Object Detector

↓

Detection Evaluation

The performance of both pipelines will be compared using the same evaluation dataset.

This experimental design will help determine whether image enhancement provides an actual improvement in object detection performance.

---

## Dataset Scope

The final dataset has not yet been confirmed.

Therefore, the following dataset characteristics must be verified with the mentor:

* Dataset name
* Number of images
* Number of object classes
* Class distribution
* Annotation format
* Train/validation/test split
* Availability of video or sequence data
* Availability of tracking annotations
* Image resolution and quality

---

## Success Criteria

The project will be considered successful if:

1. The dataset is correctly understood and processed.

2. A reproducible preprocessing pipeline is developed.

3. A baseline object detection model is successfully implemented.

4. The enhanced-image pipeline is compared with the raw-image pipeline.

5. Object detection performance is evaluated using appropriate metrics.

6. The advantages and limitations of the selected approaches are analyzed.

7. Object tracking is explored if the dataset supports sequence-based analysis.

8. Experimental results are clearly documented and reproducible.
