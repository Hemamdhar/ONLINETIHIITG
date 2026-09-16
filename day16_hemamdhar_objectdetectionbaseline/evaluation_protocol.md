# Object Detection Baseline Evaluation Protocol

## Scope

Train a transfer-learning detector on raw `prepared_dataset_v1` images for each dataset export separately. Do not merge class spaces without an approved semantic mapping.

## Training controls

- Use the same frozen Dataset V1 manifest and group-safe train/validation/test assignment.
- Start from the configured pretrained checkpoint and record its exact name/version.
- Keep image size, epochs, batch size, optimizer, seed, confidence threshold, and IoU threshold in the run record.
- Keep augmentation disabled for this first raw baseline, matching Day 12 V1 controls.
- Tune or select on validation only. Do not inspect test metrics until the final baseline protocol is frozen.

## Required metrics

- Precision and recall at the declared confidence/IoU settings.
- mAP@50 and mAP@50-95.
- Per-class AP, support, true positives, false positives, and false negatives.
- Confusion matrix and representative false-negative/false-positive examples.
- Model parameter count and checkpoint size in MB.
- Inference latency in milliseconds per image and FPS, with hardware, batch size, and warm-up policy.

## Class-wise error review

For each class, inspect:

- missed small, dark, turbid, blurred, or occluded objects;
- confusion with visually similar classes;
- duplicate detections and background false positives;
- errors concentrated in a source sequence or scene condition;
- annotation ambiguity before assigning blame to the detector.

Use the same class map and manifest IDs when saving predictions. Preserve prediction files, confusion matrices, plots, and checkpoint metadata.

## Release rule

A baseline result is reportable only when the pair audit, label validation, group-overlap check, and Dataset V1 manifest are complete. A missing archive or missing dependency produces `blocked`, not zero-valued metrics.
