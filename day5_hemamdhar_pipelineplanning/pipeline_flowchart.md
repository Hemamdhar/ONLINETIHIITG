# Reproducible Pipeline Flowchart

```mermaid
flowchart TD
    A[Raw Roboflow exports] --> B[Inventory files and read data.yaml]
    B --> C[Validate images and YOLO labels]
    C --> D[Parse dataset name, source video ID, and frame ID]
    D --> E[Remove or record corrupt, missing, duplicate, and invalid files]
    E --> F[Group split by source video or sequence]
    F --> G{Leakage check passes?}
    G -- No --> H[Repair split and repeat checks]
    H --> F
    G -- Yes --> I[Freeze train, validation, and test manifests]
    I --> J[Create raw-image baseline]
    I --> K[Create enhancement variants]
    J --> L[Train fixed YOLO detector]
    K --> M[Train or evaluate the same detector protocol]
    L --> N[Evaluate on untouched test manifest]
    M --> N
    N --> O[Precision, recall, mAP, per-class and error analysis]
    O --> P[Measure image quality and inference time]
    N --> Q{Sequence tracking ground truth available?}
    Q -- Yes --> R[Run tracker and evaluate IDF1, MOTA, ID switches]
    Q -- No --> S[Report tracking as qualitative or proxy consistency only]
    P --> T[Save predictions, metrics, configuration, and environment]
    R --> T
    S --> T
    T --> U[Compare runs and write conclusions]
```

## Workflow Contracts

### Input

- JPG image frames and parallel YOLOv8 label files.
- `data.yaml` class mappings and split paths.
- Filename-derived sequence information where available.

### Frozen artifacts

- `manifests/*.csv` containing image path, label path, dataset, source video ID, frame ID, and split.
- A versioned class mapping for each dataset.
- A run configuration containing model, image size, seed, augmentation, enhancement, and software versions.

### Output

- Model weights and training curves.
- Test predictions and confusion matrices.
- Detection metrics, timing measurements, and image-quality measurements.
- Tracking outputs only when appropriate ground truth exists.
