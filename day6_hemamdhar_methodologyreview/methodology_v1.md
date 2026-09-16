# Methodology V1

## 1. Study Objective

This study evaluates whether underwater image enhancement improves downstream object detection for AI-based underwater visual surveillance. The primary comparison is between a raw-image pipeline and an enhanced-image pipeline using the same leakage-safe data split, detector protocol, and evaluation code.

The project has three related components:

1. Image quality analysis and optional enhancement.
2. Object detection as the primary measurable task.
3. Temporal tracking as a conditional extension when sequence metadata and persistent object identities are available.

## 2. Literature-to-Method Rationale

The literature review identified three relevant method families:

| Component   | Candidate                   | Role in this project        | Rationale                                                                        |
| ----------- | --------------------------- | --------------------------- | -------------------------------------------------------------------------------- |
| Enhancement | CLAHE                       | Classical reference         | Fast, transparent, and does not require enhancement-model training               |
| Enhancement | FUnIE-GAN or WaterNet       | Learning-based comparison   | Tests whether a learned underwater enhancer provides useful downstream changes   |
| Detection   | YOLO with transfer learning | Primary detector            | One-stage detection, practical inference speed, and suitable pretrained features |
| Tracking    | SORT                        | Simple feasibility baseline | Lightweight association using detector outputs                                   |
| Tracking    | ByteTrack or DeepSORT       | Optional advanced tracker   | Tests stronger temporal association if valid tracking evaluation data exists     |

The central methodological principle is task-based evaluation: a visually improved image is not automatically a better input. Enhancement must be judged by its effect on precision, recall, mAP, error patterns, and processing cost.

## 3. Dataset and Unit of Analysis

The available exports are:

- DIAT Aquarium v4: 9,281 documented images and 11 classes.
- Well v8: 4,155 documented images and 4 classes.
- Aquatic Plant v2: 2,147 documented images and 1 class.

All three use YOLO-style object-detection labels. The class vocabularies differ, so each export will first be treated as an independent dataset. A combined model requires a documented semantic class mapping and mentor approval; labels such as `fishes` and `school-of-fish` must not be merged by name alone.

The unit of analysis for detection is an image frame and its object annotations. The unit of split assignment is a source video or sequence group, not an individual frame, because filenames indicate sequential frames from continuous recordings.

## 4. Data-Readiness Procedure

Before modelling, create a versioned manifest containing:

- dataset name and dataset version;
- image path and matching label path;
- image dimensions and file format;
- class IDs and class names;
- number of objects per image;
- source video or sequence ID parsed from the filename;
- frame ID where available;
- proposed split and validation status;
- corruption, duplicate, and annotation-check flags.

Run these checks:

1. Confirm that every required image and label file can be opened.
2. Parse every label as `class_id x_center y_center width height`.
3. Confirm valid class IDs, positive box dimensions, and normalized coordinates in the range 0 to 1.
4. Count images, instances, empty labels, and instances per class for every export.
5. Check exact and near duplicates.
6. Parse source sequence IDs and confirm that no group crosses train, validation, and test.
7. Freeze the manifest before preprocessing or model selection.

The exact split counts, source-group parsing reliability, corruption rate, duplicate rate, and class distribution remain data-readiness outputs rather than assumptions.

## 5. Split Strategy

Use group-aware splitting at source-video or sequence level. The preferred allocation is approximately 70% training, 15% validation, and 15% test by source groups, subject to mentor approval and sufficient representation of important classes. If the supplied Roboflow folders already satisfy group separation, retain them and record the verification rather than reshuffling frames.

If a source group cannot be identified reliably, do not report a leakage-sensitive final result. Record the affected files and resolve the metadata or treat the affected sequence as excluded from the formal test claim.

The test split is read only for the final selected configuration. Validation data is used for model choice, enhancement selection, threshold selection, and early stopping.

## 6. Preprocessing Plan

### Common preprocessing

- Convert images using a consistent decoder and color-channel convention.
- Resize to the detector's fixed input size, initially 640 x 640 to match the documented exports where applicable.
- Preserve YOLO normalized coordinates correctly during any geometric transformation.
- Apply training augmentation only to training images.
- Do not compute data-dependent preprocessing statistics using the test set.

### Enhancement variants

- `RAW`: original image after only required detector resizing.
- `CLAHE`: documented color-space and clip-limit configuration selected on validation data.
- `LEARNED`: one selected learned enhancer, either FUnIE-GAN or WaterNet, chosen using validation-side quality, detection, and runtime results.

Save enhancement configuration, output paths, processing time, and model version. Do not overwrite raw images or mix enhanced outputs across splits.

## 7. Modelling Plan

### Detection baseline

Fine-tune a pretrained YOLO detector independently on each dataset using its confirmed class mapping. The baseline uses raw images and establishes precision, recall, mAP@50, mAP@50-95, per-class AP, and runtime.

### Enhancement ablation

Repeat the same detector training protocol with CLAHE and, if approved, the selected learned enhancer. Detector architecture, image size, seed policy, epochs, optimizer, augmentation, confidence threshold, IoU threshold, and evaluation script must remain fixed for a fair comparison.

### Tracking extension

Run SORT or ByteTrack only on ordered sequences. Formal IDF1, MOTA, identity-switch, and fragmentation claims require persistent ground-truth object IDs. The current YOLO exports do not provide those IDs, so tracking is currently a feasibility or qualitative extension, not a primary success criterion.

## 8. Evaluation Plan

### Detection metrics

- Precision and recall at the declared operating threshold.
- mAP@50 and mAP@50-95.
- Per-class AP, precision, recall, and support.
- Confusion matrix and representative false-positive/false-negative cases.

Report results separately per dataset before any aggregate result. For repeated runs, report mean and standard deviation across seeds.

### Image-quality metrics

- UIQM or another documented underwater image-quality metric for raw and enhanced images.
- PSNR and SSIM only when a trustworthy reference image exists.
- Qualitative examples covering haze, blur, low illumination, color distortion, and occlusion.

### Tracking metrics

When valid tracking ground truth becomes available: IDF1, MOTA, identity switches, and track fragmentation. Without it: report only clearly labelled exploratory measures such as track continuity and lost-track counts.

### Efficiency metrics

- Enhancement time per image.
- Detector inference time per image and frames per second.
- End-to-end time per frame.
- Model size, parameter count, hardware, memory where available, and software versions.

## 9. Reproducibility and Reporting

Each run must record the dataset version, manifest version, class-map version, source-group split result, model and checkpoint, enhancement settings, seed, hyperparameters, software environment, hardware, command, metrics, predictions, and artifact path.

The final report must distinguish measured results from assumptions. It must also state the limitations caused by missing raw videos, unavailable camera and water-condition metadata, unknown split-level counts, and absent persistent tracking IDs.

## 10. Methodology V1 Approval Points

The mentor should confirm:

1. Whether the three exports remain separate or are combined.
2. The detector checkpoint and training budget.
3. Whether enhancement is mandatory or an ablation.
4. The approved enhancement method or screening budget.
5. The group split allocation after source IDs are parsed.
6. The minimum acceptable detection and processing-time criteria.
7. Whether tracking is required despite absent tracking IDs.
