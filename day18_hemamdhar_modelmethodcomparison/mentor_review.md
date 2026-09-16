# Day 18 Mentor Review Record

## Review status

**Status:** Prepared for mentor review; final approval is pending.

**Evidence basis:** Day 13 comparison protocol, Day 15 detector/enhancement plan and mentor prompts, Day 16 DIAT smoke baseline, and Day 17 matched raw/CLAHE/gamma inference outputs.

## Proposed decisions

| Topic | Proposed decision | Mentor decision |
|---|---|---|
| Dataset handling | Keep DIAT Aquarium, Aquatic Plant, and Well separate until semantic mapping and leakage-safe splits are approved | Pending |
| Detector | Continue with YOLOv8n or mentor-approved equivalent, using the same model and checkpoint policy for all conditions | Pending |
| Primary comparison | raw_v1 control versus CLAHE_v1; retain gamma_v1 as a diagnostic condition | Pending |
| Enhancement selection | Select using validation detector metrics, rare-class recall, difficult-scene failures, and runtime together | Pending |
| Gamma parameters | Do not call gamma a meaningful enhancement while gamma=1.0 and contrast=1.0; select parameters on validation only | Pending |
| Tracking scope | Exploratory until persistent object IDs or approved tracking ground truth are available | Pending |
| Tracking implementation | Execute the existing greedy IoU tracker on ordered predictions; consider SORT or ByteTrack only after approval | Pending |
| Test policy | Keep the test split untouched until the condition and parameters are frozen; evaluate selected condition once | Pending |

## Current recommendation

Shortlist `clahe_v1` for the next properly trained validation experiment and retain `raw_v1` as the mandatory control. Defer `gamma_v1` as a deeper candidate because the current setting is identity and has the highest measured inference time. Do not select a tracking method from the present evidence.

## Mentor questions requiring answers

1. Is CLAHE the approved enhancement candidate for the next validation run?
2. Is YOLOv8n and the proposed training budget adequate, or should the model size and epochs change?
3. What minimum precision, recall, mAP, rare-class recall, and FPS thresholds define acceptance?
4. Should the three source datasets remain separate in the final report?
5. Can persistent tracking IDs, raw videos, or approved tracking annotations be obtained?
6. Is exploratory tracking output sufficient for the current project, or are formal MOT metrics required?
7. Should a learned enhancement remain out of scope until the classical comparison is complete?

## Required mentor sign-off

**Mentor:** ____________________

**Review date:** ____________________

**Decision:** `pending` / `approved with conditions` / `revise`

**Corrections:**

```text

```
