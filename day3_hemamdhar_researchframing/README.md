# Day 3 - Research Framing

This folder defines the research question, project scope, measurable outputs, and mentor-review items for the underwater visual surveillance project.

## Project Focus

The project investigates an AI-based computer vision pipeline for underwater imagery. The pipeline is designed to handle common underwater challenges such as poor visibility, color distortion, low contrast, scattering, haze, and blur.

The main goal is to determine whether image enhancement improves deep learning-based object detection. Object tracking will also be explored when suitable video or sequence data and tracking annotations are available.

## Research Question

**How does underwater image enhancement affect the performance of deep learning-based object detection, and can an effective computer vision pipeline provide reliable object detection and tracking for underwater visual surveillance?**

## Experimental Comparison

The initial experiment compares two pipelines using the same evaluation data:

1. **Baseline:** raw underwater image -> object detector -> detection evaluation
2. **Enhanced:** raw underwater image -> image enhancement -> object detector -> detection evaluation

This comparison will show whether improved visual quality produces a measurable improvement in downstream detection performance.

## Planned Outputs and Metrics

### Image Enhancement

- Visual quality comparison
- PSNR and SSIM when reference images are available
- UIQM or another suitable underwater image quality metric

### Object Detection

- Precision
- Recall
- mAP@50
- mAP@50-95

### Object Tracking

When sequence data supports tracking evaluation:

- Tracking consistency
- Identity switches
- MOTA
- IDF1

## Current Scope

The primary target is object detection in underwater images or video frames. Each detection should provide an object class, bounding box, and confidence score. If tracking is supported, the system may additionally produce object identities, trajectories, and identity consistency measurements.

The final dataset and some implementation decisions are still pending mentor confirmation. These include the dataset name, class distribution, annotation format, data split, availability of sequence data, detection model, enhancement methods, and tracking method.

## Files

- `research_framing.md` - Full research question, sub-questions, target definition, experimental scope, dataset requirements, and success criteria.
- `mentor_notes.md` - Template for recording mentor decisions, assumptions, feedback, and next actions.
- `progress_pack.pdf` - Project progress-pack document.

## Immediate Next Actions

1. Obtain and inspect the final dataset.
2. Validate annotations and confirm the train, validation, and test split.
3. Perform exploratory data analysis.
4. Create a baseline object detection model.
5. Confirm the evaluation metrics and project scope with the mentor.
6. Compare raw-image and enhanced-image pipelines.
7. Explore tracking if sequence data and annotations are available.

## Success Criteria

The project should produce a reproducible preprocessing and detection pipeline, a clear comparison between raw and enhanced inputs, appropriate quantitative evaluation, and a documented analysis of the strengths and limitations of the selected methods.
