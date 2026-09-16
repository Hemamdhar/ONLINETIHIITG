# Approved Data-Preparation Plan

## 1. Plan identity

| Field | Value |
|---|---|
| Plan version | D9-v1.0 |
| Scope | Image detection preparation for the three underwater dataset exports |
| Source of controls | Day 8 quality report and correction plan; Day 6 experiment plan |
| Raw-data policy | Read-only; never overwrite or clean in place |
| Current approval state | **Pending mentor sign-off and Day 8 measured audit** |

This document freezes the intended preparation method. It must not be treated as evidence that the data already passed the quality gate.

## 2. Inputs and dataset boundaries

Keep these exports separate during preparation and initial modelling:

- `Aquatic Plant.v2i.yolov8`
- `DIATAquarium.v4i.yolov8`
- `well.v8i.yolov8`

Each export receives its own class map, manifest, audit summary, and split files. A cross-dataset class merge requires a documented semantic comparison and mentor approval.

## 3. Versioned artifacts

```text
raw_data_archive/                 # unchanged source exports
manifests/
  <dataset>_inventory.csv
  <dataset>_pairs.csv
  <dataset>_groups.csv
  <dataset>_split_v1.csv
class_maps/
  <dataset>_class_map_v1.yaml
corrections/
  <dataset>_correction_log.csv
  <dataset>_review_samples.csv
processed/<dataset>/<prep_version>/
reports/
  day8_quality_<dataset>.md
  day9_review_<dataset>.md
```

Every derived record must retain source path, source SHA-256, derivative path, action, reason, reviewer, and status.

## 4. Preparation procedure

### Gate A - Inventory and pairing

- Inventory images, videos, labels, YAML files, extensions, and file sizes.
- Compute SHA-256 checksums.
- Pair images and labels by stable relative stem.
- Account for missing labels, labels without images, empty labels, and unreadable files.

### Gate B - Annotation and visual review

- Parse the YOLO five-field format.
- Reject or quarantine malformed rows, unknown classes, non-positive boxes, and unrecoverable coordinates.
- Review boxes that are clipped, tiny, overlapping, ambiguous, or inconsistent with visible objects.
- Review difficult visibility samples without automatically removing valid hard examples.
- Use a correction log and preserve every before/after label change.

### Gate C - Sequence-safe split

- Infer source groups from source-video metadata where available or defensible filename/frame patterns.
- Keep all members of a duplicate or source-sequence group in one split.
- Check exact hashes, near-duplicate hashes, adjacent frames, and group IDs across splits.
- Freeze train, validation, and test manifests only after cross-split group overlap is zero or explicitly approved.
- Use the mentor-approved split proportions after group assignment; do not force a ratio that fragments a source sequence.

### Gate D - Deterministic preprocessing

- Resize or letterbox with a fixed target input policy.
- Apply the identical geometric transformation to bounding boxes.
- Validate boxes in pixel space and normalized space after transformation.
- Keep validation and test data unaugmented.
- Apply augmentation and enhancement only to training data unless an experiment explicitly defines another controlled protocol.
- Store outputs in versioned derivative folders linked to the raw source.

## 5. Exclusions and claims

- Do not merge classes based only on similar names.
- Do not delete difficult scenes because they reduce a quality score.
- Do not use test data for correction decisions, tuning, or method selection.
- Do not claim PSNR or SSIM improvement without valid reference pairs.
- Do not claim formal tracking performance without persistent object IDs or approved tracking ground truth.
- Do not report final quality rates until the Day 7 archive is populated and the Day 8 audit is rerun.

## 6. Release checklist

- [ ] Raw archive populated, preserved, and checksummed.
- [ ] Inventory and image-label pair manifests generated.
- [ ] Class maps reviewed and versioned per dataset.
- [ ] Corrupt, missing, malformed, and ambiguous records dispositioned.
- [ ] Difficult/inconsistent sample board completed with real thumbnails and reviewer decisions.
- [ ] Correction log complete and derived labels revalidated.
- [ ] Duplicate and source-sequence leakage checks pass.
- [ ] Train/validation/test manifests frozen.
- [ ] Day 8 quality report updated with measured counts and rates.
- [ ] Mentor approval recorded below.

## 7. Approval record

**Decision:** Pending measured Day 8 audit and mentor review.

**Mentor:** ____________________  
**Date:** ____________________  
**Approved plan version:** ____________________  
**Conditions or exceptions:**

```text

```
