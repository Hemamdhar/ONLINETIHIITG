# Mentor Corrections and Confirmation Record

This document is intentionally prepared for mentor review. The fields below separate the current recommendation from decisions that require confirmation.

## Meeting Details

**Review date:** ********\_\_\_\_********

**Mentor:** ********\_\_\_\_********

**Project:** Underwater Visual Surveillance Using AI

## Proposed Decisions for Confirmation

| Topic                 | Current proposal                                                      | Mentor correction / final decision |
| --------------------- | --------------------------------------------------------------------- | ---------------------------------- |
| Primary task          | Object detection on the three exports                                 |                                    |
| Dataset handling      | Analyze DIAT Aquarium, Well, and Aquatic Plant separately first       |                                    |
| Unified classes       | No merge until semantic mapping is approved                           |                                    |
| Split strategy        | Source-video/sequence-group split; approximately 70/15/15 if feasible |                                    |
| Detector              | Pretrained YOLO fine-tuned per dataset                                |                                    |
| Enhancement role      | Raw versus enhanced ablation, not an assumed requirement              |                                    |
| Classical enhancement | CLAHE                                                                 |                                    |
| Learned enhancement   | Select one of FUnIE-GAN or WaterNet after validation screening        |                                    |
| Detection metrics     | Precision, recall, mAP@50, mAP@50-95, per-class AP                    |                                    |
| Image-quality metrics | UIQM; PSNR/SSIM only with valid references                            |                                    |
| Tracking scope        | Exploratory only until persistent IDs are available                   |                                    |
| Tracking method       | SORT or ByteTrack if approved                                         |                                    |
| Efficiency metrics    | Enhancement time, inference time, FPS, hardware and software record   |                                    |

## Corrections Required From Mentor

1. Confirm whether the three datasets should remain separate for the final report.
2. Confirm whether the supplied Roboflow train/test boundaries are trusted after the source-group overlap check.
3. Confirm the acceptable train/validation/test allocation if a new group split is needed.
4. Confirm the selected YOLO model size, pretrained checkpoint, image size, epoch budget, and seed policy.
5. Confirm whether image enhancement is a required contribution or a comparative experiment.
6. Approve one learned enhancement method or restrict the project to CLAHE.
7. Confirm whether formal tracking metrics are required despite the current absence of persistent IDs.
8. Provide minimum acceptable accuracy and processing-time thresholds, if the project has them.
9. Confirm whether additional metadata, raw videos, or tracking labels can be obtained.

## Current Data-Readiness Status

- [ ] Raw dataset folders received and inventoried
- [ ] Image counts reproduced from folders
- [ ] Label counts and missing pairs checked
- [ ] Class mappings verified against every `data.yaml`
- [ ] Bounding boxes validated
- [ ] Exact and near duplicates checked
- [ ] Source video or sequence IDs parsed
- [ ] No source group crosses train, validation, and test
- [ ] Class distribution and rare classes reported
- [ ] Final manifests frozen

## Mentor Feedback

**Corrections to Methodology V1:**

---

---

---

**Approved scope:**

---

**Approved metrics:**

---

**Approved next actions:**

---

## Post-Review Update Record

| Date | Correction received | File or section updated | Owner | Status |
| ---- | ------------------- | ----------------------- | ----- | ------ |
|      |                     |                         |       |        |
