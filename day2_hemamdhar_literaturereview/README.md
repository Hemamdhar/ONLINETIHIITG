# Day 2 - Literature Review

This folder contains the literature review for an underwater visual surveillance project. The review examines methods for improving underwater images, detecting objects, and tracking objects across video frames.

## Project Context

Underwater imagery commonly suffers from color distortion, low contrast, scattering, haze, blur, and poor illumination. These problems can reduce the performance of later computer vision tasks. The proposed surveillance pipeline therefore consists of three stages:

1. Image enhancement
2. Object detection
3. Object tracking

The literature review considers both classical computer vision methods and deep learning approaches. It also emphasizes that visual enhancement should be evaluated by its effect on downstream detection and tracking, not only by how an image looks.

## Files

- `literature_review.md` - Summary of the underwater surveillance problem, relevant machine learning methods, and the proposed evaluation perspective.
- `literature_comparison.csv` - Structured comparison of enhancement, detection, and tracking methods, including datasets, approaches, metrics, results, and limitations.

## Methods Reviewed

### Image Enhancement

- CLAHE: classical local contrast enhancement method.
- WaterNet: CNN-based multi-image fusion approach.
- FUnIE-GAN: lightweight GAN-based enhancement method.
- Shallow-UWnet: lightweight deep neural network.
- Deep learning color-feature fusion: multi-feature enhancement approach.

### Object Detection

- YOLO with transfer learning: pretrained one-stage detector fine-tuned for underwater objects.

### Object Tracking

- SORT: Kalman filtering with Hungarian-algorithm data association.
- DeepSORT and ByteTrack: detection-based tracking methods designed to improve object association across frames.

## Evaluation Metrics

The reviewed studies use different metrics according to the task:

- **PSNR and SSIM:** quantitative measures of image reconstruction and structural similarity.
- **UIQM:** underwater image quality metric.
- **Precision and Recall:** object detection accuracy measures.
- **mAP:** mean Average Precision for object detection performance.
- **MOTA and IDF1:** multi-object tracking and identity-association measures.

## Main Finding

No single enhancement method can be assumed to be the best for every underwater dataset. Published comparisons report different PSNR, SSIM, and UIQM results for methods such as WaterNet, FUnIE-GAN, and Shallow-UWnet. The project should therefore test candidate enhancement methods on its own dataset and measure both image quality and downstream detection and tracking performance.
