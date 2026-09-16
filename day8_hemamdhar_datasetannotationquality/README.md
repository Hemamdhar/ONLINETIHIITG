# Day 8 - Dataset / Annotation Quality

This folder contains the quality audit and correction plan for the underwater visual surveillance datasets.

## Scope

- Audit image and video files, labels/targets, duplicates, and split integrity.
- Check resolution, class and scene coverage, visibility, and corrupt samples.
- Review image-annotation pairs for consistency.
- Define preprocessing and annotation corrections without modifying the preserved raw archive.

## Evidence status

The Day 7 raw archive is not populated in the current workspace. Its inspection JSON files are empty, so this package records the audit protocol, verified documentation-based risks, and decision gates. It does not invent file counts, defect rates, or split results.

The first execution step is to populate and checksum `day7_hemamdhar_initialinspection/raw_data_archive/`, then run `initial_inspection.ipynb`. Update the measured fields in `dataset_annotation_quality_report.md` and keep repaired derivatives outside the raw archive.

## Files

- `dataset_annotation_quality_report.md` - audit findings, evidence table, acceptance criteria, and readiness decision.
- `correction_plan.md` - prioritized correction actions, owners/evidence, and re-audit gates.

## Required evidence before modelling

1. Complete inventory of images, videos, labels, YAML files, and split folders.
2. Valid image-label pair manifest with missing, empty, malformed, and unreadable records.
3. Class mapping and per-class image/object support for each dataset.
4. Resolution, aspect-ratio, visibility, and corrupt-sample summaries.
5. Exact duplicate and source-sequence overlap results.
6. Frozen group-aware train/validation/test manifests.
7. Correction log linking every changed derivative to its source and reason.
