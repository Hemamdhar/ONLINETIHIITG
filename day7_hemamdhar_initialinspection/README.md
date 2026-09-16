# Day 7 - Initial Dataset Inspection

This folder contains the non-destructive first inspection package for the underwater visual surveillance datasets.

## Files

- `initial_inspection.ipynb` - Notebook that inventories files, image properties, YOLO labels, sequence-like filenames, metadata, duplicates, class coverage, and obvious inconsistencies without modifying source data.
- `preliminary_dataset_report.md` - Initial findings, data-readiness status, limitations, and next actions.
- `raw_data_archive/README.md` - Preservation rules and expected raw archive layout.
- `raw_data_archive/SOURCE_LINK.txt` - Original Google Drive source link.

## Raw Archive Status

The Drive folder is visible, but file-level download access requires authentication in the current environment. Therefore `raw_data_archive/` is prepared but does not claim to contain the supplied dataset yet. Place the three downloaded dataset folders there unchanged before running the notebook:

```text
raw_data_archive/
├── Aquatic Plant.v2i.yolov8/
├── DIATAquarium.v4i.yolov8/
└── well.v8i.yolov8/
```

The notebook reads from the archive and writes only reports or inspection tables outside the raw folders. It does not rename, resize, relabel, deduplicate, or delete source files.

## Run Order

1. Download the three folders from the supplied Drive link.
2. Copy them unchanged into `raw_data_archive/`.
3. Record archive checksums and download date in `raw_data_archive/README.md`.
4. Run `initial_inspection.ipynb` from this folder.
5. Review the generated inventory, label checks, duplicate checks, and visual samples before any preprocessing.
