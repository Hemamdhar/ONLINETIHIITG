# Week-2 Peer Visual Review Package

## 1. Purpose and independence

The review compares enhancement and data findings without sharing implementation code. Each reviewer receives only:

- matched raw/enhanced image grids;
- stable sample IDs and dataset names;
- annotation overlays or label summaries;
- class, visibility, and sequence-group metadata needed for interpretation;
- the fixed review questions below.

Reviewers do not receive source code, training scripts, hidden test results, or parameter-search history.

**Current status:** The package is prepared, but peer observations are pending because the raw archive and enhancement outputs are not available in this workspace.

## 2. Comparison board

| Board item | Raw V1 | CLAHE V1 | Gamma/contrast V1 | Peer decision |
|---|---|---|---|---|
| Dark/low-contrast samples | Pending grid | Pending grid | Pending grid | Pending independent ratings |
| Turbid/color-cast samples | Pending grid | Pending grid | Pending grid | Pending artifacts and failure notes |
| Blurred/occluded samples | Pending grid | Pending grid | Pending grid | Pending visibility judgment |
| Small/rare-class objects | Pending grid | Pending grid | Pending grid | Pending localization judgment |
| Annotation readability | Same labels expected | Same labels expected | Same labels expected | Check target visibility and boundary clarity |
| Sequence-adjacent frames | Group metadata pending | Same source records | Same source records | Check temporal redundancy, not object identity |

Enhancement must not be judged by visual brightness alone. Record whether a transformation makes object boundaries, class cues, or annotation interpretation better, unchanged, or worse.

## 3. Difficult-condition discussion

### Visibility

Discuss darkness, turbidity, blur, occlusion, color cast, low contrast, and extreme aspect ratio separately. A difficult but valid scene should remain represented for robustness; an unusable scene requires a documented exclusion reason.

### Classes

Keep the three exports separate. Discuss rare classes, visually similar classes, ambiguous class names, and class-specific enhancement failures. Do not infer a unified class mapping from appearance alone.

### Sequences

Use source groups to identify adjacent frames and leakage risk. A group ID is not a persistent object ID. Do not turn visual continuity into formal tracking evidence.

## 4. Independent review questions

For each matched sample, each reviewer records:

1. Which condition gives the clearest evidence for the annotated object?
2. Does enhancement reveal useful structure or create artifacts that could mislead the detector?
3. Is the class still visually defensible after enhancement?
4. Is the bounding box consistent with the visible object?
5. Is the sample valid, difficult-but-valid, ambiguous, or unusable?
6. Does the sample appear sequence-adjacent or duplicated across a split?
7. What follow-up experiment would distinguish the proposed explanation?

Use `peer_observation_form.csv`; do not overwrite the raw sample or label.

## 5. Peer synthesis template

Complete this section after independent forms are returned.

| Topic | Reviewer A | Reviewer B | Agreement | Resolution |
|---|---|---|---|---|
| Best condition for dark scenes | Pending | Pending | Pending | Pending |
| Best condition for turbidity/color cast | Pending | Pending | Pending | Pending |
| Enhancement artifacts | Pending | Pending | Pending | Pending |
| Difficult class or scene | Pending | Pending | Pending | Pending |
| Annotation inconsistency | Pending | Pending | Pending | Pending |
| Sequence/leakage concern | Pending | Pending | Pending | Pending |

Disagreements that affect class identity, object presence, or split assignment require adjudication and a retained disagreement record.

## 6. Week-2 package contents

- [ ] Independent peer observation forms completed.
- [ ] Matched raw/CLAHE/gamma grids attached or linked by stable sample ID.
- [ ] Day 10 EDA statistics and class support tables attached.
- [ ] Annotation/pair exceptions linked to Day 8 correction records.
- [ ] Sequence-group overlap result attached.
- [ ] Reviewer agreement and unresolved disagreements recorded.
- [ ] Experiment hypotheses selected for validation.
- [ ] No code shared as part of peer review.

## 7. Package decision

**Decision:** Review package ready; peer evidence pending.  
**Week-2 conclusion:** Keep raw V1 as the reference condition. Treat enhancement as a validation-controlled ablation, and treat sequence groups as leakage controls rather than tracking ground truth.
