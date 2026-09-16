# Day 13 - Enhancement / Detection Preparation

This folder prepares the enhancement baseline and detector-ready Dataset V1 artifacts without modifying the raw archive.

## Files

- `enhance_baselines.py` - identity, CLAHE, and gamma/contrast baseline generation for a prepared split.
- `detector_dataset.yaml` - detector dataset contract pointing at `prepared_dataset_v1` and separate dataset class spaces.
- `comparison_protocol.md` - raw-versus-enhanced evaluation protocol and tracking-data policy.
- `prepare_sequence_metadata.py` - sequence identifier extraction and overlap checks when manifest groups exist.

## Baseline usage

```bash
python3 enhance_baselines.py \
  --manifest ../day11_hemamdhar_visionpreprocessing/prepared_dataset_v1/manifest_v1.json \
  --output enhancement_outputs_v1
```

The command requires a prepared manifest. It exits with a clear blocked status when Day 11 has not produced one.

## V1 controls

- Raw Dataset V1 is the reference condition.
- Enhancements are generated only as derived files and never overwrite raw/prepared inputs.
- CLAHE is the classical baseline; gamma/contrast is a lightweight diagnostic baseline.
- Validation and test enhancement outputs use fixed parameters selected before evaluation; no test-based tuning.
- Detection metrics use the same model, class map, split manifest, seed policy, and thresholds for raw and enhanced conditions.
- Sequence identifiers are exploratory metadata only unless persistent object IDs or approved tracking ground truth are supplied.
