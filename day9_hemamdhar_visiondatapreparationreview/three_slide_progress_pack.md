# Day 9 Progress Pack
## Vision Data Preparation Review

> **Evidence note:** Day 8 found that the raw archive is not populated and all generated inspection summaries are empty. The statements below distinguish current evidence from provisional risks. Real sample images and measured counts must be inserted after archive population.

---

## Slide 1 - Dataset and Pairing Findings

### What is established

- Three expected exports: `Aquatic Plant.v2i.yolov8`, `DIATAquarium.v4i.yolov8`, and `well.v8i.yolov8`.
- YOLO-style target format is expected: `class_id x_center y_center width height`.
- Class vocabularies differ; datasets remain separate until a semantic mapping is approved.
- Filenames appear sequence-like, so random frame-level splitting is unsafe.
- Persistent object IDs, raw videos, and environmental metadata are not documented as available.

### What is not yet measured

| Review item | Current result | Decision |
|---|---|---|
| Image/video inventory | Pending | Run Day 7 inventory |
| Image-label pairing | Pending | Build pair manifest; account for missing and extra labels |
| Annotation validity | Pending | Parse every row and record failure reasons |
| Resolution/corruption | Pending | Produce image statistics and quarantine log |
| Class/scene coverage | Pending | Report per-dataset support and manual scene review |
| Duplicates/split overlap | Pending | Hash images and group by source sequence |

**Message:** The data-preparation decision is controlled by the manifest and annotation audit, not by documentation-based counts.

---

## Slide 2 - Difficult and Inconsistent Sample Review

No raw images are currently available in the workspace, so the following are the required representative review slots, not claimed observed samples. Replace each slot with a thumbnail and manifest ID after the archive is populated.

| Sample slot | Required example | Review questions | Allowed disposition |
|---|---|---|---|
| D1 | Dark or low-contrast underwater scene | Is the object identifiable? Is the box complete or legitimately truncated? | `retain-difficult`, `needs_review`, or `exclude-unusable` |
| D2 | Turbid, blurred, or color-cast scene | Does enhancement obscure the target? Is the scene valid for robustness? | `retain-difficult` or `exclude-unusable` |
| D3 | Occluded or partially visible object | Does the annotation cover the visible target consistently? | `retain` or repair after visual confirmation |
| D4 | Missing image-label pair | Is this an intentional background image or a missing annotation? | `background-confirmed`, `recover-label`, or `quarantine` |
| D5 | Malformed, out-of-range, or zero-area label | Can the intended box be determined unambiguously? | repair with before/after diff or quarantine |
| D6 | Duplicate or adjacent frame in another split | Does the source sequence cross a split boundary? | rebuild group split; keep group in one split |
| D7 | Unknown class or conflicting overlapping boxes | Is the class map or object identity ambiguous? | mentor review; no silent remap |

### Sample evidence record

```text
sample_id, manifest_id, source_path, thumbnail_path, issue_type,
visible_objects, annotated_objects, class_decision, box_decision,
visibility, split_group, disposition, reviewer, notes
```

**Review rule:** Include at least one reviewed example for every dataset, split, class, and difficult-scene category once measured data exists. Keep the original source checksum and the correction decision.

---

## Slide 3 - Frozen Data-Preparation Strategy

### Frozen controls

1. Preserve raw exports unchanged and record SHA-256 checksums.
2. Build a versioned manifest with image path, label path, dimensions, checksum, class map, and source-sequence group.
3. Validate YOLO rows before transformation: five fields, approved class ID, normalized coordinates in $[0, 1]$, positive dimensions, and valid pixel-space boxes.
4. Keep dataset-specific class maps; train separately unless a semantic merge is approved.
5. Split by source sequence or defensible filename group, never by neighboring frames. Require zero cross-split group overlap.
6. Apply deterministic resizing/letterboxing with identical box transforms; validate labels after transformation.
7. Apply augmentation only to training data. Keep validation and test images untouched.
8. Store corrected labels, resized images, and enhancement outputs outside the raw archive with provenance.
9. Freeze the manifest, class map, correction log, and split files before baseline training.

### Release gate

**Not released for modelling until:** archive inventory, pair audit, annotation review, duplicate audit, difficult-sample review, and leakage check are complete; all P0 issues are closed or accepted; and the mentor signs the approved data plan.
