# Day 19 - Controlled Hyperparameter / Parameter Experiments

## Deliverables

- `experiment_strategy.md` - documented search space, fixed controls, selection rule, and test-protection policy.
- `run_validation_sweep.py` - reproducible validation-only CLAHE sweep.
- `experiment_log_v1.csv` - one row for every executed candidate.
- `best_validated_config.json` - frozen best configuration from validation selection.
- `validation_derivatives_v1/` - derived validation images only.
- `validation_outputs_v1/` - reserved for validation inference artifacts.

## Candidate and scope

Day 18 shortlisted `clahe_v1` for deeper experiments and retained `raw_v1` as the control. Day 19 varies only the CLAHE clip limit (`1.5`, `2.0`, `3.0`) at a fixed 8x8 grid size, with the raw control included in the same validation sweep.

The sweep uses the frozen Day 16 checkpoint and a deterministic 256-image subset of the DIAT validation split only. It does not read the final test split, and the final test set remains untouched. The bounded subset is documented to keep the CPU experiment executable and reproducible locally; it is not a substitute for final full-validation selection.

## Important limitation

The Day 16 checkpoint is an abbreviated smoke checkpoint trained for 1 epoch on 2% of the training data. Therefore the saved best configuration is the best validated configuration for this smoke sweep, not a final scientific accuracy winner. Precision, recall, and mAP must be recomputed during a properly trained detector experiment before the configuration is promoted to a final test evaluation.
