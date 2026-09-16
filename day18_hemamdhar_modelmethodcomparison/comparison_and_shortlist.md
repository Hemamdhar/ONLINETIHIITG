# Day 18 - Model / Method Comparison and Shortlist

## Scope and evidence boundary

This comparison covers the methods actually built and measured through Day 17. The only completed comparable detector evaluation is the DIAT Aquarium smoke run using the same frozen Day 16 YOLOv8n checkpoint on 954 test images. The checkpoint was trained for 1 epoch on 2% of the training data, so its zero detection metrics are valid pipeline outputs but not evidence that the method is scientifically ineffective.

The comparison table is in `method_comparison_v1.csv`. Blank metrics mean not measured; they are not zero. The measured zero values belong only to the abbreviated detector smoke run.

## Comparison summary

| Method             | Precision / Recall | mAP50 / mAP50-95 |                       Runtime | Tracking     | Current interpretation                                                        |
| ------------------ | -----------------: | ---------------: | ----------------------------: | ------------ | ----------------------------------------------------------------------------- |
| raw_v1             |          0.0 / 0.0 |        0.0 / 0.0 | 42.9064 ms/image, 23.3065 FPS | Not measured | Reference control; fastest condition                                          |
| clahe_v1           |          0.0 / 0.0 |        0.0 / 0.0 | 50.0835 ms/image, 19.9667 FPS | Not measured | Classical enhancement candidate; no smoke-run accuracy gain shown             |
| gamma_v1           |          0.0 / 0.0 |        0.0 / 0.0 | 63.8674 ms/image, 15.6574 FPS | Not measured | Current gamma=1.0 is identity; slowest condition without demonstrated benefit |
| greedy IoU tracker |     Not applicable |   Not applicable |                  Not measured | Not measured | Code exists, but no tracking assignment output was produced                   |

## Image quality and tracking

UIQM, PSNR, and SSIM are not available in the current artifacts. PSNR and SSIM should remain unreported until valid reference image pairs and a defined protocol exist. UIQM may be added as a descriptive enhancement measure, but it cannot select a method by itself.

The manifest contains 1,576 sequence groups, including a largest group of 1,721 frames, but these are sequence proxies. There are no approved persistent object IDs. Therefore IDF1, MOTA, MOTP, identity switches, and formal tracking consistency are unavailable. Day 17 includes a greedy IoU tracker function, but it was not called and no track output was generated.

## Overfitting, data limitations, and complexity

- The detector evidence is underpowered: 1 training epoch and 2% of the training data create a strong underfitting risk.
- Aquatic Plant and Well detector baselines remain blocked because the available source groups do not support a leakage-safe three-way split.
- The smoke checkpoint produced zero detections for all three conditions. This prevents claims about enhancement improving or harming precision, recall, mAP, rare classes, or failure cases.
- CLAHE is deterministic and has modest processing overhead relative to raw inference. Its benefit must be tested on a properly trained detector and validation split.
- Gamma is currently configured as gamma=1.0 and contrast=1.0, so it is effectively an identity diagnostic while still adding processing overhead. It should not be treated as a meaningful enhancement until validation selects non-identity parameters.
- Expected detector failure strata requiring review are small, dark, turbid, blurred, occluded, visually similar, duplicate-detection, and background-false-positive cases.
- The simple greedy IoU tracker is low complexity, but it is sensitive to missed detections, occlusion, fast motion, and crowded scenes. Those risks cannot be quantified from the current zero-detection smoke output.

## Shortlisted candidates

### 1. CLAHE + fully trained frozen-or-comparable detector

Shortlist as the strongest enhancement candidate for the next experiment. It is the only classical enhancement with a non-identity transformation, has modest measured overhead, and matches the approved Day 13 comparison protocol. It remains conditional: select it only if validation preserves or improves detector metrics, rare-class recall, difficult-scene behavior, and the agreed runtime budget.

### 2. raw_v1 control + same detector

Retain as the mandatory control and likely operational fallback. It is the fastest condition and provides the reference needed to attribute any change to enhancement. It is not a winner based on the smoke metrics because all three methods scored zero.

### Deferred: gamma_v1

Keep for reproducibility and diagnostic comparison, but defer as a deeper candidate. Current gamma and contrast values are identity settings, and the measured runtime is the slowest of the three conditions. Reconsider only after validation-selected non-identity parameters show a measurable benefit.

### Deferred: formal tracking method

Do not claim a tracking winner yet. First obtain persistent object IDs or approved tracking ground truth, execute the existing tracker on non-empty detector predictions, and then compare greedy IoU with an approved SORT or ByteTrack baseline if required.

## Required next experiment before final selection

1. Train the detector beyond the smoke budget on a complete group-safe Dataset V1 split.
2. Evaluate raw, CLAHE, and a validation-selected gamma setting on validation data with identical model, seeds, thresholds, and augmentation.
3. Record precision, recall, mAP50, mAP50-95, per-class AP, rare-class recall, false-negative examples, preprocessing time, inference time, FPS, hardware, and software.
4. Run the tracker on ordered sequence predictions and save track assignments or a rendered sample; report formal metrics only if persistent IDs become available.
5. Freeze the selected condition, then evaluate the untouched test split once.
