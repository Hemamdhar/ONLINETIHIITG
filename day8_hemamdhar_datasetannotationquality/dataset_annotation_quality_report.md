# Dataset / Annotation Quality Report

## 1. Purpose

This report is the Day 8 quality gate for the underwater visual surveillance datasets. It covers file integrity, image quality, annotation validity, image-label pairing, class and scene coverage, duplicates, and leakage-safe split integrity.

The report is deliberately non-destructive: source files remain unchanged, and any repaired data must be written as a versioned derivative.

## 2. Evidence and limitations

| Evidence source                |                   Current result | Interpretation                             |
| ------------------------------ | -------------------------------: | ------------------------------------------ |
| Day 7 raw archive              |                    Not populated | File-level audit cannot yet be completed   |
| Day 7 `inventory.json`         |                            Empty | No verified file counts                    |
| Day 7 `label_records.json`     |                            Empty | No verified label validity rates           |
| Day 7 `class_counts.json`      |                            Empty | No verified class support                  |
| Day 7 `image_stats.json`       |                            Empty | No verified resolution or corruption rates |
| Day 7 `exact_duplicates.json`  |                            Empty | No verified duplicate result               |
| Existing project documentation | Provisional dataset descriptions | Useful risks, not measured findings        |

### Provisional context from earlier days

- Three exports are expected: `Aquatic Plant.v2i.yolov8`, `DIATAquarium.v4i.yolov8`, and `well.v8i.yolov8`.
- YOLO-style labels are expected, using `class_id x_center y_center width height`.
- The exports have different class vocabularies and must not be merged without an approved mapping.
- Filenames appear to represent frames extracted from video sequences, creating temporal leakage risk.
- Persistent object IDs, raw videos, and environmental metadata are not currently documented as available.

These are hypotheses or documentation-based expectations until reproduced from the archive.

## 3. Audit protocol

### 3.1 File and pair integrity

For each dataset and split, generate a manifest containing relative path, extension, byte size, SHA-256, image dimensions, label path, and source sequence marker.

Flag:

- unreadable or zero-byte images and videos;
- unsupported extensions or unexpected files;
- missing labels where annotations are required;
- labels without a matching image;
- duplicate filenames or path collisions;
- empty label files, distinguishing intentional background images from missing annotations.

### 3.2 Image, resolution, and visibility quality

Measure width, height, aspect ratio, color mode, format, file size, and open/read errors. Summarize minimum, median, maximum, and frequency tables per dataset and split.

Create a review sample for:

- very small images or extreme aspect ratios;
- dark, low-contrast, heavily turbid, blurred, or occluded scenes;
- severe color cast or visibility loss;
- images with unusually high object counts;
- unreadable and truncated files.

Do not remove a difficult underwater scene solely because it is difficult. Record whether it is valid, useful for robustness, or unusable because the target cannot be identified.

### 3.3 Annotation and target validity

Parse each YOLO row and record the exact reason for every failure. A valid row has five numeric fields, an integer class ID present in the approved class map, normalized values in $[0, 1]$, positive width and height, and a box contained within the image after conversion to pixels.

Check:

- malformed rows and non-numeric values;
- unknown or inconsistent class IDs;
- zero or negative box dimensions;
- coordinates outside the normalized range;
- boxes clipped by image boundaries;
- boxes too small to support the declared task;
- duplicate or near-duplicate boxes in one image;
- overlapping boxes with conflicting classes;
- mismatch between visible objects and annotated objects in the review sample.

A clipped box is not automatically invalid: preserve the original row, classify it as `needs_review`, and only repair it after visual confirmation.

### 3.4 Class and scene coverage

Report, per dataset and split:

- class name and ID;
- images containing the class;
- object-instance count;
- median and percentile box area;
- empty-image count;
- missing or uncertain class-map entries.

Also stratify the review by visible scene conditions where labels or manual review permit: clear/turbid water, low/high illumination, vegetation, tank/well environment, occlusion, and object scale. Do not claim scene coverage when the metadata is absent; mark it as `unknown` and use a manual sample review.

### 3.5 Duplicate and split integrity

Compute exact image hashes and, after the archive is available, perceptual hashes for near-duplicate review. Exact or near-duplicate frames must be assigned to one split only.

Infer source sequence/video groups from available folder and filename evidence. Never randomly distribute neighboring frames. Check for:

- identical hashes across splits;
- same source sequence across splits;
- same image stem or adjacent frame ranges across splits;
- class-map differences between train, validation, and test;
- test records reused in tuning or correction decisions.

The split is not ready until group overlap is zero or an approved exception is documented.

## 4. Results register

Populate this table only from generated manifests or reviewed samples.

| Check                                 | Result  | Status  | Evidence / action                            |
| ------------------------------------- | ------- | ------- | -------------------------------------------- |
| Raw archive populated and checksummed | Pending | BLOCKED | Download and preserve source folders         |
| Image/video inventory                 | Pending | BLOCKED | Day 7 `inventory.json`                       |
| Corrupt/unreadable files              | Pending | BLOCKED | Day 7 `image_stats.json` plus review log     |
| Image-label pairing                   | Pending | BLOCKED | Pair manifest and missing/extra-label counts |
| YOLO syntax and coordinate validity   | Pending | BLOCKED | Day 7 `label_records.json`                   |
| Class-map consistency                 | Pending | BLOCKED | Dataset YAML files and approved mapping      |
| Resolution/aspect-ratio coverage      | Pending | BLOCKED | Image statistics summary                     |
| Visibility and scene coverage         | Pending | BLOCKED | Stratified manual review sheet               |
| Exact duplicates                      | Pending | BLOCKED | Day 7 `exact_duplicates.json`                |
| Near duplicates / adjacent frames     | Pending | BLOCKED | Perceptual hash and sequence audit           |
| Split overlap                         | Pending | BLOCKED | Frozen group manifest and overlap report     |
| Annotation-pair consistency           | Pending | BLOCKED | Reviewed image-label sample                  |

## 5. Acceptance criteria

The dataset may proceed to preprocessing and baseline training only when:

- all files have stable manifest IDs and checksums;
- unreadable files are isolated and dispositioned;
- every required image-label pair is accounted for;
- all retained annotations parse and satisfy the approved coordinate rules;
- class IDs and names are frozen per dataset, with any merge approved in writing;
- resolution and visibility limitations are reported, including rare classes and difficult scenes;
- duplicate and sequence overlap across splits is zero or explicitly approved;
- train, validation, and test manifests are frozen and versioned;
- corrected derivatives have provenance and pass the same audit again.

## 6. Current decision

**Decision: BLOCKED pending raw archive population and measured audit results.**

No irreversible preprocessing, annotation repair, class merge, or final model evaluation should be treated as valid until the correction plan is executed and the results register is updated.
