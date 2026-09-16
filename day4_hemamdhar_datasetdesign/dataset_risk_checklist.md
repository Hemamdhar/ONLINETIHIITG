# Day 4 — Dataset Risk Checklist

## Project: Underwater Visual Surveillance Using AI

The following risks should be checked before using the dataset for model development.

---

# 1. Missing Data Risks

* [ ] Are any image files missing?
* [ ] Are any annotation files missing?
* [ ] Do all images have corresponding annotations where required?
* [ ] Are there empty annotation files?
* [ ] Are any metadata fields missing?
* [ ] Are image dimensions missing or invalid?
* [ ] Are any video frames missing from a sequence?

---

# 2. Annotation Risks

* [ ] Are annotation files in a consistent format?
* [ ] Are all class IDs valid?
* [ ] Are class names correctly mapped to class IDs?
* [ ] Are bounding box coordinates valid?
* [ ] Are bounding boxes inside image boundaries?
* [ ] Are bounding box widths and heights positive?
* [ ] Are objects incorrectly labeled?
* [ ] Are some objects missing annotations?
* [ ] Are duplicate annotations present?

---

# 3. Image Quality Risks

* [ ] Are any images corrupted?
* [ ] Are image formats consistent?
* [ ] Are image resolutions highly inconsistent?
* [ ] Are some images extremely dark?
* [ ] Are some images heavily blurred?
* [ ] Is underwater visibility significantly different across images?
* [ ] Is there severe color distortion?
* [ ] Are some images too low in quality for reliable annotation?

---

# 4. Class Imbalance Risks

* [ ] How many images belong to each class?
* [ ] How many object instances belong to each class?
* [ ] Are some classes significantly underrepresented?
* [ ] Are rare classes present in validation and test sets?
* [ ] Does the dataset split preserve important classes?

Class imbalance can cause a model to perform well on frequent classes while performing poorly on rare classes.

---

# 5. Duplicate Data Risks

* [ ] Are exact duplicate images present?
* [ ] Are near-duplicate images present?
* [ ] Are highly similar frames present in different splits?
* [ ] Are augmented versions of the same image present in multiple splits?

Duplicate data can create overly optimistic model performance.

---

# 6. Data Leakage Risks

* [ ] Are the training and test sets independent?
* [ ] Are duplicate images shared between splits?
* [ ] Are images from the same video present in multiple splits?
* [ ] Has information from the test set been used during preprocessing?
* [ ] Has the test set been used for model selection?
* [ ] Has normalization information been calculated using the complete dataset?

Data leakage can produce unrealistic evaluation results.

---

# 7. Temporal Risks

This section applies when video or sequence data is available.

* [ ] Are frames correctly ordered?
* [ ] Are frame IDs consistent?
* [ ] Are timestamps available?
* [ ] Are object IDs consistent across frames?
* [ ] Are consecutive frames distributed across different dataset splits?
* [ ] Is temporal information accidentally leaking into training?

---

# 8. Train / Validation / Test Split Risks

* [ ] Is the training set large enough?
* [ ] Is the validation set representative?
* [ ] Is the test set completely independent?
* [ ] Are all important classes represented?
* [ ] Are data distributions significantly different?
* [ ] Are videos or sequences separated correctly?
* [ ] Is the test set untouched during model development?

---

# 9. Underwater Domain-Specific Risks

* [ ] Are different water conditions represented?
* [ ] Are lighting conditions significantly different?
* [ ] Are objects affected by low visibility?
* [ ] Are objects partially occluded?
* [ ] Are objects very small?
* [ ] Is color distortion severe?
* [ ] Is scattering or haze present?
* [ ] Are backgrounds visually complex?

These factors may affect both image enhancement and object detection performance.

---

# 10. Final Dataset Readiness Checklist

Before starting model training:

* [ ] Dataset structure verified
* [ ] Images successfully loaded
* [ ] Annotations successfully parsed
* [ ] Class mapping verified
* [ ] Bounding boxes validated
* [ ] Missing files checked
* [ ] Corrupted files checked
* [ ] Class distribution analyzed
* [ ] Duplicate images checked
* [ ] Train/test leakage checked
* [ ] Temporal leakage checked where applicable
* [ ] Train/validation/test splits verified

---

# Final Decision

The dataset should only proceed to preprocessing and model training after the major data quality and leakage risks have been checked.

Any identified issues should be documented and addressed before experimental results are reported.
