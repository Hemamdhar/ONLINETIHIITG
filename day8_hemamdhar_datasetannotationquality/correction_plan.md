# Dataset / Annotation Correction Plan

## 1. Operating rules

- Keep the Day 7 raw archive read-only and unchanged.
- Make one versioned derivative for each correction stage.
- Preserve the original relative path, SHA-256, and correction reason for every derivative.
- Never silently delete a record; use a disposition such as `retain`, `repair`, `exclude`, `quarantine`, or `needs_review`.
- Re-run the full Day 8 audit after each annotation or split correction.

## 2. Prioritized actions

| Priority | Trigger                                              | Correction                                                                                                                 | Output / evidence                             | Gate                                  |
| -------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------- |
| P0       | Archive unavailable                                  | Download the three exports, preserve folders, record date and SHA-256                                                      | Archive manifest                              | Stop until complete                   |
| P0       | Corrupt or unreadable image/video                    | Quarantine the source path; do not overwrite it; request a clean copy or document exclusion                                | Corruption log and replacement provenance     | No corrupt file in a frozen manifest  |
| P0       | Missing image-label pair                             | Verify whether the image is intentional background; otherwise recover the label or mark image unusable                     | Pair disposition table                        | Every record accounted for            |
| P0       | Invalid YOLO syntax or coordinates                   | Repair only when the intended box is visually unambiguous; otherwise exclude/quarantine for annotation review              | Before/after label diff and reviewer ID       | Zero unexplained invalid rows         |
| P0       | Unknown class ID or class-name mismatch              | Freeze the dataset-specific class map and obtain mentor approval before remapping                                          | Versioned class map                           | No unapproved class merge             |
| P1       | Duplicate or near-duplicate across splits            | Rebuild splits by source sequence; keep duplicate group in one split                                                       | Group-aware split manifest and overlap report | Cross-split overlap is zero           |
| P1       | Duplicate images within a split                      | Retain one canonical record and log the disposition of the others                                                          | Duplicate group report                        | No accidental repeated evidence       |
| P1       | Boxes outside image or clipped                       | Review the image; clip only when the object is genuinely truncated, otherwise correct the box                              | Annotation review record                      | Pixel-space boxes valid and justified |
| P1       | Duplicate/overlapping conflicting boxes              | Compare visible instances and class semantics; merge or relabel only after review                                          | Conflict-resolution log                       | No unexplained conflicts              |
| P1       | Very small or extreme-resolution images              | Preserve valid hard examples; resize only in a derived preprocessing stage with fixed rules                                | Resolution policy and sample report           | Model input policy documented         |
| P1       | Severe blur, turbidity, occlusion, or low visibility | Label as valid difficult sample, unusable sample, or needs review; do not filter by a single automated score               | Visibility review sheet                       | Scene difficulty remains represented  |
| P2       | Class or scene under-coverage                        | Report the gap, seek additional samples or use declared class-aware sampling; do not duplicate data to inflate support     | Coverage report and sampling decision         | Rare classes disclosed                |
| P2       | Missing source video/frame metadata                  | Infer sequence groups only when evidence is defensible; otherwise mark grouping uncertain and avoid strong tracking claims | Metadata limitation note                      | Evaluation claims match metadata      |

## 3. Annotation review protocol

Review a stratified sample from every dataset, split, class, and visibility category. Use two independent reviewers for suspected class ambiguity, missing objects, and box-boundary disputes.

For each reviewed image, record:

- image manifest ID and source checksum;
- annotation version;
- visible object count and annotated object count;
- class agreement;
- box-boundary agreement;
- visibility and occlusion status;
- final disposition and reviewer notes.

Escalate disagreements that change class identity, object presence, or evaluation split. Do not resolve them by majority vote without retaining the disagreement record.

## 4. Preprocessing policy after corrections

1. Split by source sequence before augmentation or enhancement.
2. Freeze the corrected manifest and class map.
3. Apply deterministic resizing/letterboxing with the same box transformation to images and labels.
4. Validate transformed boxes in pixel and normalized coordinates.
5. Keep enhancement outputs in a separate derivative directory and retain a raw-image link.
6. Apply augmentation only to training data; never augment validation or test records.
7. Recompute checksums and rerun pair, label, duplicate, and split audits.

Do not claim PSNR or SSIM improvement unless a valid reference image pair exists. Do not claim formal tracking performance without persistent object IDs or an approved tracking ground truth.

## 5. Required correction log fields

```text
record_id, source_path, source_sha256, derivative_path, action,
reason, old_label, new_label, class_map_version, reviewer,
review_date, confidence, evidence, status
```

## 6. Exit criteria

The correction phase is complete when:

- all P0 findings are closed or explicitly accepted by the mentor;
- no unreadable files or invalid retained labels remain unexplained;
- class mapping and dataset boundaries are frozen;
- corrected image-label pairs pass the Day 8 parser and visual review;
- duplicate and sequence leakage checks pass on frozen manifests;
- the report contains measured counts, rates, and sample evidence;
- downstream experiment logs reference the manifest and correction versions.
