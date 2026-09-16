# Day 18 - Model / Method Comparison + Mentor Review

## Deliverables

- `method_comparison_v1.csv` - one comparison table covering the built raw, CLAHE, gamma, and tracking methods.
- `comparison_and_shortlist.md` - measured results, evidence boundaries, limitations, failure risks, and shortlisted candidates.
- `mentor_review.md` - proposed decisions and mentor questions/sign-off fields.
- `progress_pack_3_slides.md` - the expected three-slide progress pack.

## Current conclusion

The current evidence supports a method shortlist, not a final winner. `clahe_v1` is recommended for the next properly trained validation experiment, while `raw_v1` remains the mandatory control. `gamma_v1` is deferred because its current parameters are identity settings and its measured processing time is highest.

All unavailable metrics are explicitly marked as not measured or not applicable. The DIAT detection values are smoke-run outputs from the abbreviated Day 16 checkpoint and must not be interpreted as final detector performance. Formal tracking metrics are unavailable because persistent object IDs and approved tracking ground truth do not exist.

## Evidence sources

- Day 13 enhancement comparison protocol and baseline implementation.
- Day 15 enhancement/detector plan, metrics schema, and mentor prompts.
- Day 16 detector smoke metrics and completion status.
- Day 17 enhanced inference summary, tracking status, and notebook.
