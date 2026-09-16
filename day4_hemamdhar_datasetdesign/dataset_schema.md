# Day 4 — Dataset Design & Quality Expectations

## Project

**Underwater Visual Surveillance Using AI**

## Dataset Design Objective

Before using the final dataset, it is important to define the expected dataset structure, input files, annotations, labels, targets and metadata.

The purpose of this step is to ensure that the dataset is properly understood before preprocessing, model training or evaluation.

The final dataset will be inspected and compared against the expected structure defined below.

---

# 1. Expected Dataset Inputs

The system may receive one or more of the following data types:

* Underwater images
* Underwater video files
* Extracted video frames
* Object annotations
* Object class labels
* Sequence information
* Tracking information, if available

The exact structure will depend on the dataset provided by the mentor.

---

# 2. Expected Image Structure

For an image-based object detection dataset, the expected structure may be:

```text
dataset/
│
├── train/
│   ├── images/
│   └── labels/
│
├── val/
│   ├── images/
│   └── labels/
│
└── test/
    ├── images/
    └── labels/
```

Each image should have a corresponding annotation file where object-level annotations are required.

Expected image formats may include:

* JPG
* JPEG
* PNG

Important image metadata to inspect:

* Image filename
* Image width
* Image height
* Image resolution
* File format
* File size

---

# 3. Expected Annotation Structure

For object detection, each object should have the following information:

* Image identifier
* Object class
* Bounding box coordinates

Depending on the annotation format, bounding boxes may contain:

* Class ID
* x-coordinate
* y-coordinate
* Width
* Height

For YOLO-style annotations, the expected format is:

```text
class_id x_center y_center width height
```

The coordinates are generally normalized relative to image width and height.

The actual annotation format must be confirmed after receiving the final dataset.

---

# 4. Expected Labels

The dataset is expected to contain one or more object classes.

For each class, the following information should be verified:

* Class name
* Class ID
* Number of instances
* Number of images containing the class

A class mapping should be created after inspecting the dataset:

```text
Class ID → Class Name
```

Example:

```text
0 → Object Class A
1 → Object Class B
2 → Object Class C
```

The actual class names should not be assumed until the dataset is inspected.

---

# 5. Expected Target

The primary target of the project is object detection.

For each input image, the model should predict:

* Object class
* Bounding box
* Confidence score

The expected output can be represented as:

```text
Input Image

        ↓

Object Detection Model

        ↓

Class + Bounding Box + Confidence Score
```

Example:

```text
Object: Fish
Confidence: 0.92
Bounding Box: [x_min, y_min, x_max, y_max]
```

The actual object categories will depend on the final dataset.

---

# 6. Expected Video / Sequence Structure

If the dataset contains videos or sequential frames, additional metadata may be required.

Expected information may include:

* Video ID
* Frame ID
* Frame order
* Timestamp
* Object ID
* Object class
* Bounding box

Example:

```text
Video ID → Frame ID → Object ID → Bounding Box
```

This information is important for object tracking because the system must associate the same object across multiple frames.

---

# 7. Important Metadata

The following metadata should be collected and analyzed where available:

| Metadata          | Purpose                           |
| ----------------- | --------------------------------- |
| Image ID          | Unique identification of an image |
| Image Size        | Understand image resolution       |
| Class Label       | Identify object category          |
| Bounding Box      | Object localization               |
| Number of Objects | Analyze image complexity          |
| Video ID          | Identify video sequence           |
| Frame ID          | Preserve temporal order           |
| Object ID         | Support object tracking           |
| Timestamp         | Analyze temporal information      |
| Camera / Location | Identify environmental variation  |
| Water Condition   | Analyze visual degradation        |

Not all metadata may be available in the final dataset.

---

# 8. Dataset Quality Expectations

A high-quality dataset should have:

* Correct image files
* Valid annotations
* Consistent class labels
* Valid bounding boxes
* No corrupted files
* Clear train/validation/test separation
* Minimal duplicate images
* No information leakage between splits

The dataset should be inspected before model training.

---

# 9. Expected Train / Validation / Test Split

The dataset should be divided into three independent subsets.

## Training Set

The training set will be used to train the model.

The model learns patterns and features from this data.

---

## Validation Set

The validation set will be used during model development.

It can be used for:

* Hyperparameter tuning
* Model selection
* Monitoring training performance
* Detecting overfitting

---

## Test Set

The test set should only be used for final evaluation.

It should not be used during:

* Model training
* Hyperparameter tuning
* Model selection

---

# 10. What the Dataset Split Should Preserve

A correct dataset split should preserve:

* Class representation across splits
* Independence between training and testing data
* Similar data distribution where appropriate
* Temporal order when sequence data exists
* Separation of related video frames
* Prevention of duplicate or near-duplicate images across splits

If the dataset contains videos, randomly splitting individual frames may cause information leakage.

Frames from the same video or sequence should ideally remain within the same dataset split.

For example:

```text
Video A → Training Set

Video B → Validation Set

Video C → Test Set
```

This is preferable to:

```text
Frame 1 from Video A → Training

Frame 2 from Video A → Validation

Frame 3 from Video A → Test
```

The second approach may cause temporal data leakage because highly similar frames can appear in multiple splits.

---

# 11. Dataset Verification Plan

After receiving the final dataset, the following checks will be performed:

1. Inspect the directory structure.
2. Count the total number of files.
3. Identify image and annotation formats.
4. Verify class labels.
5. Check image dimensions.
6. Validate bounding box coordinates.
7. Check for missing annotations.
8. Check for corrupted files.
9. Analyze class distribution.
10. Check for duplicate images.
11. Check for possible train/test leakage.
12. Verify temporal or sequence relationships.

---

# Conclusion

The dataset will not be used directly without validation. The expected structure and quality requirements defined in this document will be compared with the actual dataset after it is received.

This will help identify data quality issues before model development and reduce the risk of invalid experimental results.
