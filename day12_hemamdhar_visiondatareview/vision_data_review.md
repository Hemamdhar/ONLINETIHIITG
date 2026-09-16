# Day 12 - Vision Data Review

## 1. Review decision

**Preparation specification:** Frozen as `prepared_dataset_v1`.  
**Release state:** **Pending raw archive audit and mentor sign-off.**

The implementation and controls are frozen, but the dataset itself cannot be certified until the source archive is available and the Day 8 and Day 10 checks produce measured evidence.

## 2. Evidence reviewed

| Area                | Current evidence                                                          | Review decision                                                    |
| ------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Visual EDA          | Day 10 notebook exists; archive has no image records                      | Keep EDA outputs conditional; do not invent distributions          |
| Image-label pairs   | Day 8 pair audit is pending                                               | Require complete pair manifest and disposition for every exception |
| Annotation validity | YOLO parser and correction plan exist                                     | Retain only parsed, approved labels; quarantine unexplained errors |
| Augmentation        | Day 11 config has train-only policy and flip probability `0.0`            | Keep augmentation disabled in V1 until EDA supports it             |
| Split logic         | Day 9 requires source-group isolation                                     | Use deterministic group assignment and zero cross-split overlap    |
| Preprocessing       | Day 11 implements RGB conversion, `640x640` letterbox, and box transforms | Approve as the fixed V1 preprocessing contract                     |
| Raw-data integrity  | Archive is absent                                                         | No release; preserve raw source once received                      |

## 3. EDA and annotation review summary

### EDA findings currently defensible

- The three expected exports have different class vocabularies and remain separate.
- Filename-derived sequential frames create a credible leakage risk.
- Brightness, resolution, aspect ratio, blur/turbidity, occlusion, and color cast are valid candidate difficulty factors, but none has a measured rate in the current workspace.
- Day 10 is prepared to generate raw grids, darkest-sample grids, resolution/brightness distributions, class counts, and degradation hypotheses once images are present.

### Pair and annotation release checks

Before release, confirm for every retained image:

- exactly one intended image-label relationship, or an explicitly reviewed background-image disposition;
- readable image and label files;
- five-field YOLO rows with approved class IDs;
- normalized coordinates in `[0, 1]` and positive width/height;
- transformed boxes still valid after letterboxing;
- source checksum and correction provenance;
- no unexplained malformed, unknown-class, or conflicting records.

## 4. Preprocessing choices and defense

| Choice          | Frozen V1 setting                                                                        | Defense                                                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Image size      | `640x640`                                                                                | Fixed detector input size gives consistent tensor dimensions and is compatible with the planned YOLO baseline                |
| Resize method   | Aspect-preserving letterbox with gray padding                                            | Avoids geometric distortion; applies the same scale and padding to boxes                                                     |
| Color           | Convert to RGB                                                                           | Removes source-mode differences while preserving the three-channel detector input contract                                   |
| Normalization   | Float image values divided by `255`                                                      | Stable, explicit loader behavior; model-specific mean/std can be added only as a controlled experiment                       |
| Augmentation    | Training-only; horizontal flip probability `0.0` in V1; no vertical flip or color jitter | Underwater orientation and color may carry scene information; do not add transformations without EDA and validation evidence |
| Validation/test | No augmentation                                                                          | Keeps evaluation comparable and prevents altered test evidence                                                               |
| Enhancement     | Not part of Dataset V1                                                                   | Raw versus CLAHE/learned enhancement remains a later controlled ablation                                                     |
| Labels          | Transform with image geometry and revalidate                                             | Prevents image-target misalignment after resizing                                                                            |

## 5. Resolved mentor corrections

| Mentor question              | Day 12 resolution                                                                                             | Evidence needed to close                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Keep datasets separate?      | Yes. Train and report each export separately first; no semantic class merge by name alone.                    | Approved class maps from each `data.yaml`  |
| Trust supplied boundaries?   | No automatic trust. Recheck exact hashes, near duplicates, adjacent frames, and source groups.                | Zero cross-split overlap report            |
| Split allocation?            | Target approximately `70/15/15`, but group integrity overrides exact ratios.                                  | Frozen group-aware manifest                |
| Model/input controls?        | Dataset V1 fixes `640x640`; model/checkpoint, epochs, seeds, and thresholds remain experiment-level controls. | Mentor confirmation in experiment protocol |
| Enhancement required?        | No. V1 is raw prepared data; enhancement is a later validation-selected ablation.                             | Experiment decision record                 |
| Learned enhancement?         | Not included in V1. Select only after validation evidence and mentor approval.                                | Later ablation approval                    |
| Formal tracking metrics?     | No. Tracking remains exploratory until persistent IDs or approved ground truth exist.                         | Tracking annotation decision               |
| Accuracy/runtime thresholds? | Not invented. Record thresholds when mentor supplies them.                                                    | Mentor feedback entry                      |
| Additional metadata/videos?  | Useful but not required for V1 detection preparation; missing metadata remains a limitation.                  | Archive and metadata inventory             |

## 6. Dataset V1 freeze contract

The following controls are frozen and must not change between preparation runs:

1. Raw exports remain read-only and retain source checksums.
2. Dataset-specific class maps are versioned independently.
3. Image-label pairs are validated before processing.
4. Source-sequence and exact-duplicate groups stay within one split.
5. Split assignment uses the configured deterministic seed `20260914`; target ratios are `70/15/15` where group sizes allow.
6. Images are converted to RGB and aspect-preserving letterboxed to `640x640`.
7. YOLO boxes receive the same scale/padding transform and are revalidated.
8. Loader values are float RGB arrays scaled to `[0, 1]`.
9. Training augmentation is disabled by default (`horizontal_flip_probability: 0.0`); validation and test are unchanged.
10. All derived images, labels, manifests, and logs carry the `prepared_dataset_v1` version.

## 7. Release checklist

- [ ] Raw archive populated and checksummed.
- [ ] Day 8 inventory, pair, annotation, duplicate, and visibility results updated with measured values.
- [ ] Day 10 grids and statistics reviewed for each dataset and difficult condition.
- [ ] Class maps verified and frozen.
- [ ] All retained labels pass pre- and post-letterbox validation.
- [ ] Every source group appears in exactly one split.
- [ ] Exact and near-duplicate cross-split overlap is zero or explicitly approved.
- [ ] Prepared images and labels generated under `prepared_dataset_v1/`.
- [ ] Manifest and split summary reviewed.
- [ ] Mentor approval recorded.

**Final status:** Dataset V1 specification frozen; data release pending evidence gates.
