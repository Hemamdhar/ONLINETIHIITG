# Day 4 - Dataset Design

This folder defines the expected dataset structure, annotation schema, metadata, quality requirements, and risk checks for the underwater visual surveillance project.

## Purpose

The dataset must be understood and validated before preprocessing, model training, or evaluation. This design document provides a reference for inspecting the final dataset supplied for the project. The actual dataset format, classes, and available metadata must be confirmed after the dataset is received.

## Expected Data

The project may use:

- Underwater images
- Underwater videos or extracted video frames
- Object annotations and class labels
- Sequence information
- Tracking information, when available

For an image-based object detection dataset, the expected directory layout is:

```text
dataset/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
└── test/
	├── images/
	└── labels/
```

Supported image formats may include JPG, JPEG, and PNG. Each image should have a corresponding annotation file when object-level labels are required.

## Annotation Schema

Each detected object should include an image identifier, class, and bounding box. For YOLO-style labels, the expected format is:

```text
class_id x_center y_center width height
```

Coordinates are generally normalized relative to image dimensions. The annotation format must be verified before it is used for training. Class IDs must also be mapped to confirmed class names rather than assumed categories.

## Targets and Tracking Data

The primary model target is object detection. For each input image, the model should produce an object class, bounding box, and confidence score.

If video or sequence data is available, the dataset may also contain video IDs, frame IDs, timestamps, object IDs, and frame-level bounding boxes. These fields are required to study object identities and trajectories across frames.

## Dataset Splits

- **Training set:** used to learn model parameters.
- **Validation set:** used for model selection, hyperparameter tuning, and monitoring overfitting.
- **Test set:** reserved for final evaluation and kept untouched during training and model development.

Images from the same video or sequence should be assigned carefully so that related frames do not create leakage between splits.

## Quality Checks

Before training, verify:

- Images load successfully and are not corrupted.
- Required annotation files are present and consistently formatted.
- Class IDs and class names are correctly mapped.
- Bounding boxes are positive and remain within image boundaries.
- Image dimensions, formats, and resolutions are valid.
- Class distributions and rare classes are documented.
- Duplicate and near-duplicate images are identified.
- Training, validation, and test sets are independent.
- Video frames are ordered and object IDs are consistent when tracking data is available.
- Underwater conditions such as lighting, haze, blur, color distortion, occlusion, and visibility are recorded where possible.

## Files

- `dataset_schema.md` - Detailed expected inputs, directory structure, annotation fields, metadata, targets, and split definitions.
- `dataset_risk_checklist.md` - Checklist for missing data, annotation errors, image quality, class imbalance, duplicates, leakage, temporal issues, and underwater-specific risks.

## Readiness Gate

The dataset should proceed to preprocessing and model training only after its structure has been verified, annotations have been parsed, bounding boxes and class mappings have been validated, data quality has been reviewed, and train/validation/test leakage has been ruled out. Any unresolved issue should be documented before experimental results are reported.
