# Day 6 - Methodology, Readiness & Mentor Review

This folder consolidates the literature, methodology, data-readiness decisions, updated experiment plan, and mentor-review questions for the underwater visual surveillance project.

## Purpose

Day 6 converts the earlier problem framing, literature review, dataset design, and pipeline plan into a reproducible Methodology V1. It separates:

- **Confirmed:** supported by the available dataset documentation and previous project records.
- **Proposed:** the recommended implementation choice for mentor approval.
- **Blocked:** a result or claim that cannot be validly produced with the current files.

## Files

- `methodology_v1.md` - Complete proposed preprocessing, modelling, evaluation, and reproducibility methodology.
- `updated_experiment_plan.md` - Revised experiment matrix with fixed controls, gates, metrics, and constraints.
- `mentor_corrections.md` - Mentor confirmation form, current assumptions, corrections, and action register.

## Current Decision Summary

| Area              | Day 6 position                                          | Status                                     |
| ----------------- | ------------------------------------------------------- | ------------------------------------------ |
| Primary task      | Single-frame object detection                           | Proposed and aligned with available labels |
| Enhancement study | Raw versus enhanced input ablation                      | Proposed                                   |
| Detector          | Transfer-learning YOLO detector                         | Proposed baseline                          |
| Split             | Source-video/sequence-group split                       | Required constraint                        |
| Tracking          | Exploratory only unless persistent IDs are supplied     | Blocked for formal MOT metrics             |
| Dataset strategy  | Analyze each export separately before any unified model | Recommended                                |
| Test set          | Untouched until the final selected configuration        | Required constraint                        |

## Mentor Review Requirement

The available files do not contain a completed mentor decision record. Therefore this package presents the methodology for confirmation; it does not claim that the mentor has already approved the model, split percentages, enhancement method, or tracking scope.
