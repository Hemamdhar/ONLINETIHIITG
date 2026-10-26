# Underwater Vision-Based Surveillance Using Machine Learning and Artificial Intelligence

[![Internship](https://img.shields.io/badge/TIH%20IIT%20Guwahati-4--Week%20Internship-0056b3.svg)](#)
[![Repository](https://img.shields.io/badge/Repository-ONLINETIHIITG-darkblue.svg)](https://github.com/Hemamdhar/ONLINETIHIITG)
[![Tasks](https://img.shields.io/badge/Task--Structure-Day__1__Task__1%20to%20Day__28__Task__3-orange.svg)](TASK_SUBMISSION_INDEX.md)
[![Status](https://img.shields.io/badge/Status-100%25%20Completed-brightgreen.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)](#)
[![YOLOv8](https://img.shields.io/badge/Model-YOLOv8%20Object%20Detection-orange.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](#)

> **Technology Innovation Hub (TIH), IIT Guwahati**  
> **4-Week Daily Internship Project Phase (28 Days) — Cohort 4 (Group O2)**  
> **Author & Intern:** Hemamdhar Dakarapu  
> **Official Repository Name:** `ONLINETIHIITG` ([GitHub Link](https://github.com/Hemamdhar/ONLINETIHIITG))  
> **Master Task Matrix:** See [`TASK_SUBMISSION_INDEX.md`](TASK_SUBMISSION_INDEX.md) for full day-wise and task-wise navigation (`Day_1_Task_1` to `Day_28_Task_3`).  
> **Project Scope:** Software-only, end-to-end underwater image enhancement, robust object detection, multi-object tracking, and edge optimization.

---

## 📌 Executive Summary

Underwater visual surveillance faces severe optical degradation including wavelength-dependent light attenuation, severe backscattering, green/blue color casts, turbidity, and low illumination contrast. 

This repository houses the complete, reproducible **4-Week / 28-Day research & engineering internship workflow** developed according to the official **TIH IIT Guwahati Daily Internship Protocol**. The work establishes an end-to-end pipeline combining:
1. **Adaptive Physics-Inspired & Contrast Enhancement** (CLAHE, Dark Channel Prior, White Balance adjustments).
2. **Transfer-Learning Detection Models** (YOLOv8 nano/small models trained on raw vs. enhanced underwater imagery).
3. **Temporal Multi-Object Tracking** (Kalman-filter/IoU based tracking for continuous subsea surveillance).
4. **Edge Profiling & Error Analysis** (Stratified environmental error analysis, ablation studies, and Pareto latency-quality trade-offs).

---

## 🏛️ Internship Protocol & Structure

| Dimension | Specification |
| :--- | :--- |
| **Institution** | Technology Innovation Hub (TIH), Indian Institute of Technology (IIT) Guwahati |
| **Mode** | Online / Mandatory Individual Execution from scratch |
| **Duration** | 4 Weeks / 28 Days |
| **Intern Discussions** | Every 2 Days (30–45 mins) — Days 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28 |
| **Mentor Reviews** | Every 3 Days (45–60 mins) — Days 3, 6, 9, 12, 15, 18, 21, 24, 27 |
| **Progress Packs** | Maximum 3-slide progress packs prepared before each mentor milestone |
| **Hardware & Dataset Scope** | Software-only execution; raw datasets preserved untouched with versioned derivative splits |

---

## 🗂️ Complete 28-Day Workflow & Repository Structure

```
.
├── day1_hemamdhar_problemunderstanding/
├── day2_hemamdhar_literaturereview/
├── day3_hemamdhar_researchframing/
├── day4_hemamdhar_datasetdesign/
├── day5_hemamdhar_pipelineplanning/
├── day6_hemamdhar_methodologyreview/
├── day7_hemamdhar_initialinspection/
├── day8_hemamdhar_datasetannotationquality/
├── day9_hemamdhar_visiondatapreparationreview/
├── day10_hemamdhar_visualeda/
├── day11_hemamdhar_visionpreprocessing/
├── day12_hemamdhar_visiondatareview/
├── day13_hemamdhar_enhancementdetectionpreparation/
├── day14_hemamdhar_week2peervisualreview/
├── day15_hemamdhar_enhancementbaselinementorreview/
├── day16_hemamdhar_objectdetectionbaseline/
├── day17_hemamdhar_enhanceddetectiontracking/
├── day18_hemamdhar_modelmethodcomparison/
├── day19_hemamdhar_controlledexperiments/
├── day20_hemamdhar_robustnessablation/
├── day21_hemamdhar_bestcandidatereview/
├── day22_hemamdhar_finalpipelinefreeze/
├── day23_hemamdhar_softwareperformancefinalvalidation/
├── day24_hemamdhar_finaltechnicalreview/
├── day25_hemamdhar_detailederrorfailureanalysis/
├── day26_hemamdhar_finalsoftwarepackagereportdraft/
├── day27_hemamdhar_finalreportandpresentation/
└── day28_hemamdhar_peermockpresentationfinalsubmission/
```

---

## 📅 Day-by-Day Detailed Deliverables Matrix

### 🌊 Week 1: Problem Understanding, Research & Dataset Readiness

| Day | Focus Area | Key Tasks & Technical Contributions | Primary Artifacts & Deliverables | Meeting Milestone |
| :-: | :--- | :--- | :--- | :-: |
| **01** | **Problem Understanding & System Definition** | • Problem statement technical rewrite.<br>• Identify underwater optical inputs and surveillance targets.<br>• Draw end-to-end software pipeline diagram.<br>• Formulate $\ge 8$ technical questions/assumptions. | • `problem_understanding.md`<br>• `pipeline.png`<br>• `README.md` | — |
| **02** | **Literature Review – Domain + ML** | • Comprehensive domain review (CV, Underwater Imaging, Deep Learning).<br>• Comparative study of 6–10 methods/datasets.<br>• Shortlist candidate enhancement algorithms and detectors. | • `literature_review.md`<br>• `literature_comparison.csv`<br>• `candidate_methods.md` | **Intern Discussion 1** |
| **03** | **Research Framing & Mentor Review** | • Research hypothesis refinement.<br>• 3-Slide progress pack preparation.<br>• Confirm target definition, dataset structure, metrics with mentor.<br>• Document mentor decisions. | • `progress_pack.pdf`<br>• `research_framing.md`<br>• `mentor_notes.md` | **Mentor Review 1** |
| **04** | **Dataset Design & Quality Expectations** | • Define schema, class balance, and metadata expectations.<br>• Identify data leakage, annotation drift, and temporal split risks.<br>• Formulate dataset risk checklist. | • `dataset_schema.md`<br>• `dataset_risk_checklist.md` | **Intern Discussion 2** |
| **05** | **Pipeline & Experiment Planning** | • Design reproducible end-to-end pipeline.<br>• Define baseline vs. advanced candidate models.<br>• Set evaluation criteria (mAP, Precision, Recall, FPS, Latency).<br>• Establish experiment log template and directory structure. | • `pipeline_flowchart.md`<br>• `experiment_plan.md`<br>• `experiment_log_template.csv`<br>• `folder_structure.md` | — |
| **06** | **Pre-Dataset Readiness + Mentor Review** | • Finalize literature, methodology, and data-readiness package.<br>• Present preprocessing and evaluation methodology.<br>• Update Methodology V1 based on mentor feedback. | • `methodology_v1.md`<br>• `updated_experiment_plan.md`<br>• `mentor_corrections.md` | **Intern Discussion 3 + Mentor Review 2** |
| **07** | **Dataset Receipt & Initial Inspection** | • Archive untouched raw dataset.<br>• Inspect images, annotations, duplicates, class distributions.<br>• Generate preliminary data report and initial visualization notebook. | • `raw_data_archive/`<br>• `initial_inspection.ipynb`<br>• `preliminary_dataset_report.md`<br>• `inspection_outputs/` | — |

---

### 🔬 Week 2: Data Cleaning, EDA & Feature Engineering

| Day | Focus Area | Key Tasks & Technical Contributions | Primary Artifacts & Deliverables | Meeting Milestone |
| :-: | :--- | :--- | :--- | :-: |
| **08** | **Dataset / Annotation Quality Audit** | • Audit resolution, visibility, and corrupt samples.<br>• Check bounding box consistency across underwater sequences.<br>• Propose annotation cleaning and correction plan. | • `dataset_annotation_quality_report.md`<br>• `correction_plan.md` | **Intern Discussion 4** |
| **09** | **Vision Data Preparation Review** | • Present pairing/annotation findings & difficult samples.<br>• Confirm preprocessing and split strategy.<br>• Freeze data-preparation plan. | • `three_slide_progress_pack.md`<br>• `approved_data_plan.md` | **Mentor Review 3** |
| **10** | **Visual EDA** | • Analyze color cast (green/blue dominant histograms) and turbidity.<br>• Generate raw-data grids, class balance charts, and aspect ratio distributions.<br>• Record environmental degradation hypotheses. | • `visual_eda.ipynb` | **Intern Discussion 5** |
| **11** | **Vision Preprocessing Pipeline** | • Build leakage-safe train/val/test splits.<br>• Implement normalization, resizing, and dataset loaders.<br>• Build selective underwater augmentations.<br>• Save versioned `Dataset V1` configuration. | • `preprocess_dataset.py`<br>• `prepared_dataset_v1/`<br>• `preprocessing_config.json` | — |
| **12** | **Vision Data Review** | • Present EDA, augmentations, and split logic.<br>• Defend preprocessing decisions and resolve mentor feedback.<br>• Freeze Dataset V1 record. | • `vision_data_review.md`<br>• `dataset_v1_freeze_record.json` | **Intern Discussion 6 + Mentor Review 4** |
| **13** | **Enhancement / Detection Preparation** | • Implement baseline image enhancements (CLAHE, Dark Channel Prior).<br>• Build YOLOv8 dataset configuration.<br>• Generate sequence metadata for tracking evaluation. | • `enhance_baselines.py`<br>• `detector_dataset.yaml`<br>• `comparison_protocol.md`<br>• `sequence_metadata_v1.csv` | — |
| **14** | **Week-2 Peer Visual Review** | • Compare enhancement outputs without sharing code.<br>• Analyze performance on low-visibility subsea classes.<br>• Prepare Week-2 package and peer observation records. | • `week2_peer_review.md`<br>• `experiment_hypotheses.json`<br>• `peer_observation_form.csv` | **Intern Discussion 7** |

---

### 🚀 Week 3: Model Development & Comparative Experiments

| Day | Focus Area | Key Tasks & Technical Contributions | Primary Artifacts & Deliverables | Meeting Milestone |
| :-: | :--- | :--- | :--- | :-: |
| **15** | **Enhancement Baseline + Mentor Review** | • Quantitative comparison of enhancement techniques (PSNR/UIQM/entropy).<br>• Define detector training protocol on raw vs. enhanced inputs.<br>• Document mentor guidance. | • `enhancement_baseline_results.md`<br>• `mentor_feedback.md`<br>• `detector_training_plan.yaml`<br>• `raw_enhanced_metrics.csv` | **Mentor Review 5** |
| **16** | **Object Detection Baseline** | • Train YOLOv8 transfer-learning detector on raw data.<br>• Evaluate Precision, Recall, mAP@50, mAP@50-95, and class errors.<br>• Record model footprint and inference latency. | • `train_baseline.py`<br>• `baseline_metrics.csv`<br>• `detector_config.yaml`<br>• `outputs/` | **Intern Discussion 8** |
| **17** | **Enhanced Detection & Tracking** | • Train/evaluate detector on enhanced image streams.<br>• Implement multi-object tracking on video sequences.<br>• Compare raw vs. enhanced tracking stability. | • `enhanced_detection_tracking.ipynb`<br>• `enhancement_outputs_v1/`<br>• `day17_outputs/` | — |
| **18** | **Model Comparison & Mentor Review** | • Multi-model comparative analysis (raw vs. enhanced vs. hybrid).<br>• Overfitting, data limitation, and complexity breakdown.<br>• Shortlist best candidates for fine-tuning. | • `method_comparison_v1.csv`<br>• `comparison_and_shortlist.md`<br>• `mentor_review.md`<br>• `progress_pack_3_slides.md` | **Intern Discussion 9 + Mentor Review 6** |
| **19** | **Controlled Hyperparameter Tuning** | • Systematic validation sweep (learning rates, IoU thresholds, batch size).<br>• Held-out test set strictly preserved.<br>• Save best validated configuration (`best_validated_config.json`). | • `run_validation_sweep.py`<br>• `experiment_strategy.md`<br>• `parameter_config_v1.json`<br>• `experiment_log_v1.csv`<br>• `best_validated_config.json` | — |
| **20** | **Robustness & Ablation Study** | • Quantitative ablation on enhancement modules.<br>• Error propagation analysis across the preprocessing-detection cascade.<br>• Subsea turbidity sensitivity analysis. | • `robustness_ablation.ipynb`<br>• `robustness_ablation_table_v1.csv`<br>• `robustness_analysis.md`<br>• `pipeline_error_propagation.png`<br>• `robustness_latency_fps_comparison.png` | **Intern Discussion 10** |
| **21** | **Best Candidate Review** | • Present baseline vs. tuned models.<br>• Analyze failure cases and edge condition taxonomy.<br>• Obtain mentor approval for Week 4 engineering direction. | • `best_candidate_review.ipynb`<br>• `best_candidate_review.md`<br>• `baseline_vs_tuned_comparison.png`<br>• `baseline_vs_tuned_summary.csv`<br>• `success_failure_analysis.md`<br>• `week4_direction_and_mentor_approval.md` | **Mentor Review 7** |

---

### 📦 Week 4: Edge Optimisation, Validation & Final Research Output

| Day | Focus Area | Key Tasks & Technical Contributions | Primary Artifacts & Deliverables | Meeting Milestone |
| :-: | :--- | :--- | :--- | :-: |
| **22** | **Final Pipeline Freeze** | • Select final architecture based on validation evidence & simplicity.<br>• Freeze preprocessing, model weights, and inference configuration.<br>• Save frozen pipeline manifest and architecture diagram. | • `frozen_pipeline.py`<br>• `frozen_pipeline_config.json`<br>• `pipeline_freeze_manifest.json`<br>• `frozen_pipeline_architecture.png`<br>• `technical_selection_rationale.md` | **Intern Discussion 11** |
| **23** | **Software Performance & Final Validation** | • Comprehensive evaluation on held-out test data.<br>• Measure latency breakdown (preprocessing vs. inference vs. NMS).<br>• Plot Pareto accuracy-vs-complexity frontier. | • `final_validation.ipynb`<br>• `final_validation_performance_metrics.csv`<br>• `software_performance_and_final_validation.md`<br>• `accuracy_quality_complexity_pareto.png` | — |
| **24** | **Final Technical Review** | • Present end-to-end reproducible workflow.<br>• 3-Slide technical progress pack.<br>• Action item list addressing mentor corrections. | • `final_technical_review.md`<br>• `progress_pack_3_slides.md`<br>• `input_to_output_workflow.png`<br>• `error_analysis_reporting_protocol.png`<br>• `mentor_corrections_and_action_list.md` | **Intern Discussion 12 + Mentor Review 8** |
| **25** | **Detailed Error & Failure Analysis** | • Analyze worst-case detection errors and false positives.<br>• Environmental stratification (turbidity, extreme depth, color wash).<br>• Feature importance and visual explanation maps. | • `error_failure_analysis.ipynb`<br>• `detailed_error_failure_analysis.md`<br>• `environmental_error_strata_breakdown.png`<br>• `error_failure_taxonomy_v1.csv`<br>• `feature_importance_visual_explanation.png` | — |
| **26** | **Final Software Packaging & Report Draft** | • Package modular codebase into reusable `underwater_surveillance` package.<br>• Write `setup.py`, `pyproject.toml`, and CLI runner `run_inference_demo.py`.<br>• Draft comprehensive research report and slide deck. | • `underwater_surveillance/`<br>• `setup.py`<br>• `pyproject.toml`<br>• `run_inference_demo.py`<br>• `final_research_report_draft.md`<br>• `final_presentation_slides.md` | **Intern Discussion 13** |
| **27** | **Final Mentor Review & Sign-Off** | • Present packaged system, benchmark summary, and report draft.<br>• Resolve final mentor feedback.<br>• Secure formal technical sign-off. | • `final_research_report.md`<br>• `final_presentation_slides.md`<br>• `final_report_and_package_demo.ipynb`<br>• `final_pareto_quality_latency.png` | **Mentor Review 9** |
| **28** | **Peer Mock Defense & Final Submission** | • Conduct mock technical presentation and defense.<br>• Verify repository links, manifests, and reproducible outputs.<br>• Final individual project package submission. | • `final_submission_research_report.md`<br>• `final_submission_presentation_deck.md`<br>• `peer_mock_presentation_and_defense.md`<br>• `future_scope_and_roadmap.md`<br>• `final_submission_and_peer_review_demo.ipynb`<br>• `repository_verification_and_manifest.json` | **Intern Discussion 14 / Mock Presentation** |

---

## 📑 12 Mandatory Final Deliverables (PDF Page 7 Checklist)

All 12 mandatory deliverables listed on **Page 7** of the official TIH IIT Guwahati Internship guidelines are complete and cross-referenced below:

```
[1] Problem Understanding Note & Literature Review ───► Day 1 & Day 2 (problem_understanding.md, literature_review.md)
[2] Dataset Understanding / Quality Report ─────────────► Day 4, 7 & 8 (dataset_schema.md, dataset_annotation_quality_report.md)
[3] Preprocessing / EDA Notebook ──────────────────────► Day 7 & Day 10 (initial_inspection.ipynb, visual_eda.ipynb)
[4] Feature / Representation Preparation Notebook ─────► Day 11 & Day 13 (preprocess_dataset.py, enhance_baselines.py)
[5] Baseline Model / Method Notebook ──────────────────► Day 16 & Day 17 (train_baseline.py, enhanced_detection_tracking.ipynb)
[6] Advanced Model / Method Experiments ───────────────► Day 17 & Day 19 (enhanced_detection_tracking.ipynb, run_validation_sweep.py)
[7] Model / Method Comparison & Experiment Log ────────► Day 18 & Day 19 (method_comparison_v1.csv, experiment_log_v1.csv)
[8] Project-Specific Robustness / Error Analysis ──────► Day 20 & Day 25 (robustness_ablation.ipynb, error_failure_analysis.ipynb)
[9] Final Model / Software Pipeline & Artefacts ───────► Day 22 & Day 23 (frozen_pipeline.py, final_validation.ipynb)
[10] Clean Source-Code Repository with README ──────────► Day 26 & Day 28 (underwater_surveillance package, Root README.md)
[11] Final Individual Project Report ──────────────────► Day 28 (final_submission_research_report.md)
[12] Final Presentation Deck & Future Scope ───────────► Day 28 (final_submission_presentation_deck.md, future_scope_and_roadmap.md)
```

---

## ⚙️ Installation & Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Hemamdhar/ONLINETIHIITG.git
cd ONLINETIHIITG
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies & Package
```bash
pip install --upgrade pip
pip install -e day28_hemamdhar_peermockpresentationfinalsubmission/
pip install ultralytics opencv-python-headless matplotlib pandas pyyaml seaborn jupyter
```

---

## 🚀 Running Inference & Experiments

### Run the Standalone Inference Demo
To test the end-to-end underwater image enhancement + YOLOv8 detection pipeline:
```bash
cd day28_hemamdhar_peermockpresentationfinalsubmission
python3 run_inference_demo.py
```
*Outputs an annotated detection image with enhancement comparison: `demo_submission_inference_output.png`.*

### Run Jupyter Notebooks
Launch any of the research notebooks:
```bash
jupyter notebook day28_hemamdhar_peermockpresentationfinalsubmission/final_submission_and_peer_review_demo.ipynb
```

---

## 📈 Key Findings & Research Conclusions

1. **Impact of Underwater Enhancement:**
   - Applying **CLAHE + Adaptive White Balance** prior to detection improved **mAP@50 by +8.4%** across heavily turbid scenes compared to raw inputs.
2. **Cascade Error Propagation:**
   - Over-enhancing images with aggressive dark channel prior introduced artificial chromatic noise, decreasing recall on distant objects. Tuned CLAHE with clip limit 2.0 provided the optimal Pareto balance.
3. **Real-Time Edge Feasibility:**
   - The frozen **YOLOv8-nano + Optimized Enhancement** pipeline achieves **$\sim 38\text{ FPS}$** on edge GPUs with an end-to-end latency of **$\sim 26.2\text{ ms}$**, satisfying real-time autonomous underwater vehicle (AUV) requirements.

---

## 👨‍💻 Intern & Author Details

- **Intern Name:** Hemamdhar Dakarapu
- **Program:** TIH IIT Guwahati 4-Week Online Internship Project Phase
- **Project Title:** Underwater Vision-Based Surveillance Using Machine Learning and AI
- **Completion Date:** September 2026
- **Status:** **100% Completed & Verified**
