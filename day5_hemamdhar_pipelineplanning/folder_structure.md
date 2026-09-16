# Proposed Repository and Artifact Structure

```text
underwater-visual-surveillance/
├── README.md
├── configs/
│   ├── datasets/
│   │   ├── diat_aquarium.yaml
│   │   ├── well.yaml
│   │   └── aquatic_plant.yaml
│   ├── experiments/
│   │   ├── baseline_raw.yaml
│   │   ├── clahe.yaml
│   │   └── learned_enhancement.yaml
│   └── class_maps/
├── data/
│   ├── raw/                    # Original exports; read-only
│   ├── manifests/              # Versioned leakage-safe CSV manifests
│   ├── interim/                # Validated or converted copies
│   └── processed/              # Enhancement outputs, never mixed with raw data
├── src/
│   ├── data/                   # Inventory, parsing, validation, group splitting
│   ├── enhancement/            # CLAHE and learned enhancement adapters
│   ├── detection/              # Training, prediction, and evaluation
│   ├── tracking/               # SORT/ByteTrack experiments
│   └── utils/                  # Seeds, timing, configuration, reporting
├── scripts/
│   ├── build_manifest.py
│   ├── validate_dataset.py
│   ├── train_detector.py
│   ├── evaluate_detector.py
│   └── benchmark_pipeline.py
├── experiments/
│   ├── logs/                   # experiment_log.csv and machine-readable run logs
│   ├── predictions/
│   ├── metrics/
│   └── figures/
├── models/                     # Checkpoints and model metadata
├── reports/                    # Data reports, tables, and final comparisons
├── environment/
│   ├── requirements.txt
│   └── README.md               # Python, CUDA, GPU, and package versions
└── docs/
    ├── data_card.md
    └── experiment_protocol.md
```

## Reproducibility Rules

- Keep raw exports unchanged and record their source and checksum.
- Version manifests separately from model outputs.
- Store the exact configuration and random seed with every run.
- Save the code revision, package versions, hardware, and command used.
- Never overwrite a completed run; create a new `run_id`.
- Keep test predictions and metrics separate from validation artifacts.
- Record unresolved assumptions, especially ambiguous source-video IDs and absent tracking IDs.
