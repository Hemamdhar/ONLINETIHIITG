# Day 2 — Literature Review: Domain + Machine Learning

## Introduction

Underwater visual surveillance is a challenging computer vision problem because underwater images and videos often suffer from color distortion, low contrast, scattering, haze, blur and poor illumination. These issues reduce the visibility of objects and can negatively affect object detection and tracking.

A typical underwater surveillance system can be divided into three major stages:

1. Underwater image enhancement
2. Object detection
3. Object tracking

Image enhancement aims to improve the visual quality of underwater imagery before further analysis. Traditional methods such as CLAHE and color correction can improve contrast and visibility. Deep learning-based approaches such as WaterNet and FUnIE-GAN attempt to learn more complex transformations from degraded underwater images to visually improved images.

For object detection, transfer learning is useful because training a deep detection model from scratch requires large amounts of labeled data and computational resources. A pretrained detector such as YOLO can be fine-tuned on underwater objects and evaluated using Precision, Recall and mean Average Precision (mAP).

When video or sequence data is available, object tracking can be used to maintain the identity of detected objects across consecutive frames. Methods such as SORT, DeepSORT and ByteTrack combine object detections with motion or appearance information to associate objects over time.

The literature indicates that underwater surveillance should not only focus on visual enhancement. An enhanced image that appears visually better may not necessarily produce better object detection. Therefore, the proposed project will evaluate the complete pipeline and analyze how image enhancement affects downstream detection and tracking performance.
