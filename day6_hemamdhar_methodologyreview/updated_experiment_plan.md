# Updated Experiment Plan - Day 6

## 1. Confirmed Constraints

- The project has three exports with different class vocabularies.
- The labels are YOLO-style bounding-box annotations.
- Filenames indicate sequential frames extracted from videos.
- Persistent object IDs are not available in the supplied annotations.
- Raw videos, camera information, water conditions, and exact split counts are not currently available in the documentation.
- Neighboring frames must not be randomly distributed across evaluation splits.

## 2. Experiment Stages

| Stage                | Run | Input and model                                       | Decision or output                        |
| -------------------- | --- | ----------------------------------------------------- | ----------------------------------------- |
| Readiness            | R0  | File, label, class, duplicate, and source-group audit | Frozen manifest and data-readiness report |
| Baseline             | R1  | Raw image -> pretrained YOLO                          | Reference detector result                 |
| Fine-tuned baseline  | R2  | Raw image -> fine-tuned YOLO                          | Primary baseline for enhancement claims   |
| Classical ablation   | R3  | CLAHE image -> same YOLO protocol                     | Tests low-cost enhancement                |
| Learned ablation     | R4  | FUnIE-GAN or WaterNet image -> same YOLO protocol     | Tests selected learned enhancement        |
| Final comparison     | R5  | Best validation-selected raw/enhanced configuration   | One final untouched test evaluation       |
| Tracking feasibility | R6  | Detector -> SORT or ByteTrack                         | Conditional, not formal MOT without IDs   |

## 3. Fixed Controls

For R2-R5, fix:

- the dataset and class mapping;
- the source-group manifests;
- detector architecture and pretrained checkpoint;
- input size, epochs, optimizer, batch size, augmentation, and stopping rule;
- seed schedule;
- confidence and IoU thresholds;
- metric implementation and test manifest.

Use at least three seeds for the primary comparison when resources permit. Do not choose a method using test performance.

## 4. Selection Rules

Select the enhancement method using validation results across:

- mAP@50-95 and recall;
- rare-class AP and false-negative patterns;
- UIQM or another declared quality metric;
- enhancement and detector runtime;
- visual failure cases.

An enhancement is not considered successful solely because its UIQM, PSNR, or SSIM is higher. The preferred method must preserve or improve downstream detection and remain within the approved processing budget.

## 5. Reporting Table

Every completed run should populate the Day 5 CSV log with:

- run, dataset, manifest, and class-map identifiers;
- split leakage result;
- model, enhancement, tracker, and hyperparameters;
- train/validation/test counts;
- precision, recall, mAP@50, mAP@50-95, and per-class AP;
- UIQM, PSNR, SSIM where valid;
- enhancement time, inference time, and FPS;
- tracking metrics only when valid ground truth exists;
- hardware, software, artifacts, status, and notes.

## 6. Constraints and Risk Controls

| Constraint                        | Control                                                                 |
| --------------------------------- | ----------------------------------------------------------------------- |
| Sequential-frame leakage          | Group split by source video or sequence and run an overlap check        |
| Different class vocabularies      | Train separately first; approve any semantic class merge                |
| Unknown image/split counts        | Generate counts from the actual folders during R0                       |
| Missing tracking IDs              | Restrict formal tracking metrics; label proxies as exploratory          |
| No reference-enhanced image pairs | Do not claim PSNR/SSIM reconstruction performance without references    |
| Class imbalance                   | Report per-class support and AP; inspect rare-class failures            |
| Enhancement cost                  | Benchmark preprocessing and end-to-end inference time                   |
| Test contamination                | Freeze test manifest and evaluate only the final selected configuration |

## 7. Mentor Confirmation Gate

R1-R5 can proceed as a detection study after the mentor confirms the dataset-specific split and detector choice. R6 requires an additional decision on whether sequence-level qualitative tracking is sufficient or whether tracking annotations must be obtained before it is included in the project claims.
