# Day 5 - Pipeline & Experiment Planning

This folder defines the reproducible workflow, experiment matrix, evaluation criteria, experiment log, and repository structure for the underwater visual surveillance project.

## Dataset Basis

The current project data consists of three Roboflow YOLOv8 exports:

| Dataset       | Images | Classes | Known split structure  |
| ------------- | -----: | ------: | ---------------------- |
| DIAT Aquarium |  9,281 |      11 | train and test         |
| Well          |  4,155 |       4 | train and test         |
| Aquatic Plant |  2,147 |       1 | train, valid, and test |

The image totals and class mappings come from the available dataset documentation. Split-level counts, raw video files, camera metadata, and tracking IDs still need to be verified from the downloaded folders.

## Critical Split Rule

The filenames indicate sequential frames extracted from videos. Randomly splitting frames can place near-identical neighboring frames in training and test sets and produce misleading results. The pipeline must therefore:

1. Extract a source video or sequence ID from each filename.
2. Assign complete source-video groups to train, validation, or test.
3. Check that no source-video ID appears in more than one split.
4. Perform preprocessing and augmentation only after the split has been fixed.

## Deliverables

- `pipeline_flowchart.md` - End-to-end reproducible workflow and Mermaid flowchart.
- `experiment_plan.md` - Baseline, advanced methods, project-specific ablation, metrics, and run protocol.
- `experiment_log_template.csv` - One-row-per-run experiment recording template.
- `folder_structure.md` - Proposed repository and artifact layout.

## Planned Research Comparison

The primary comparison is:

1. Raw image -> YOLO detector -> detection evaluation.
2. Enhanced image -> the same YOLO detector -> detection evaluation.

The detector, split, image size, training budget, and evaluation code must remain fixed when comparing raw and enhanced inputs. Enhancement quality is useful context, but the main decision criterion is its effect on downstream detection.

## Readiness Gate

No final result should be reported until image-label pairs, YOLO labels, class mappings, source-video grouping, duplicate risk, and split leakage have been checked and recorded in the experiment log.
