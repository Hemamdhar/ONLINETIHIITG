# Day 28: Peer Mock Presentation & Technical Defense Transcript

**Project:** AI-Based Underwater Visual Surveillance  
**Presenter / Author:** Hemamdhar Dakarapu  
**Session Context:** Full Individual Presentation & Mock Defense before Peer Interns (Pre-Mentor Final Trial)  
**Date:** September 16, 2026  
**Session Duration:** 14 minutes 45 seconds (Target: 15 minutes $\pm 1$ min)  
**Overall Peer Evaluation Score:** **9.7 / 10.0 (Unanimous Approval)**

---

## ⏱️ 1. Presentation Timing Breakdown & Delivery Log

| Slide / Section | Target Duration | Actual Time | Delivery Focus & Key Points Covered |
| :--- | :--- | :--- | :--- |
| **1. Title & Executive Vision** | 0:00 - 1:00 (1m) | 0:50 | Project introduction, embedded edge robotics framing, core engineering goals. |
| **2. Problem & Optical Physics** | 1:00 - 3:00 (2m) | 1:55 | Wavelength absorption ($R \gg G > B$), Jaffe-McGlamery optical scattering model. |
| **3. Modular System Pipeline** | 3:00 - 5:30 (2.5m)| 2:20 | 4-stage decoupled architecture (Ingestion $\to$ Preprocessing $\to$ Detection $\to$ Tracking). |
| **4. Preprocessing Optimization** | 5:30 - 8:00 (2.5m)| 2:35 | CIELAB $L^*$ CLAHE rationale, color distortion mitigation, gradient saliency gain. |
| **5. Controlled Benchmark Data** | 8:00 - 10:30 (2.5m)| 2:30 | 5-variant benchmark matrix, Pareto frontier, runtime percentiles ($P_{95}, P_{99}$). |
| **6. Error & Failure Taxonomy** | 10:30 - 12:00 (1.5m)| 1:40 | Turbidity, low-light, occlusion, error propagation audit ($99.2\%$ suppression). |
| **7. Live Inference Demo** | 12:00 - 13:30 (1.5m)| 1:25 | CLI and Python execution demo, latency telemetry, overlay HUD inspection. |
| **8. Future Scope & Conclusion** | 13:30 - 15:00 (1.5m)| 1:30 | TensorRT/CoreML INT8 quantization, ROS2 robotic nodes, multi-frame fusion. |
| **Total Presentation Runtime** | **15:00** | **14:45** | **Pacing verified within optimal window ($15\text{m} \pm 1\text{m}$)**. |

---

## 🥊 2. Technical Defense & Peer Challenge Q&A

During the mock defense, peer interns challenged key engineering decisions. The detailed Q&A and technical justifications are recorded below:

### Challenge 1: Choice of Classical CIELAB CLAHE vs Deep Learning Restorations (GANs / Diffusion Models)
- **Peer Question (Intern A):** *"Why did you choose a classical histogram equalization method like CIELAB CLAHE instead of state-of-the-art deep enhancement models like Water-Net, FUnIE-GAN, or Diffusion-based restoration?"*
- **Technical Defense (Hemamdhar):**
  1. **Strict Real-Time Latency Budget:** Deep enhancement models (e.g., FUnIE-GAN or Water-Net) add between $45\text{ ms}$ to $180\text{ ms}$ of compute latency per frame on edge embedded CPUs (ARM Cortex / Jetson Nano). This alone would exhaust the total system budget of $\le 40\text{ ms}$ ($25\text{ FPS}$).
  2. **Minimal Edge Compute Overhead:** CIELAB CLAHE adds only **$6.21\text{ ms}$** per frame, executing seamlessly in native C++/OpenCV without GPU reliance.
  3. **Zero Hallucination Risk:** Generative deep models risk synthesizing hallucinated artifacts or marine features that corrupt downstream detection fidelity. CLAHE directly operates on measured photon radiance without learned spatial priors.
  4. **Quantified Saliency Boost:** CIELAB CLAHE ($1.5$ clip limit) achieves an **$+88.7\%$ Sobel gradient edge boost**, which matches the feature enhancement required for YOLOv8n to resolve camouflaged boundaries.

### Challenge 2: Detector Sizing and Resolution Compromise (YOLOv8n @ 320x320 vs YOLOv8s @ 640x640)
- **Peer Question (Intern B):** *"Why did you downsample the input resolution to $320 \times 320$ with YOLOv8n rather than retaining native $640 \times 640$ with YOLOv8s to capture small marine organisms?"*
- **Technical Defense (Hemamdhar):**
  1. **Quadratic Scaling of Convolutional FLOPs:** Scaling from $320 \times 320$ to $640 \times 640$ quadruples the feature map activations ($4\times$ FLOPs). On CPU, YOLOv8n @ $640 \times 640$ takes $58.4\text{ ms}$, dropping frame rate to $17.1\text{ FPS}$.
  2. **Model Footprint & Cache Locality:** YOLOv8n has only **$3.0\text{M}$ parameters** ($5.92\text{ MB}$ weights file), allowing the entire model weight graph to reside in L3 CPU cache, eliminating memory bandwidth bottlenecks.
  3. **Empirical Verification:** The $320 \times 320$ pipeline achieves **$33.72\text{ FPS}$** ($36.18\text{ ms}$ total latency) with high bounding box localization accuracy across macro and meso marine targets.

### Challenge 3: Multi-Object Tracker Selection (Greedy IoU vs DeepSORT / ByteTrack)
- **Peer Question (Intern C):** *"Why implement a zero-parameter Greedy IoU tracker instead of feature-based ReID trackers like DeepSORT or ByteTrack?"*
- **Technical Defense (Hemamdhar):**
  1. **Zero Feature-Extraction Overhead:** DeepSORT requires a secondary ReID embedding network per detected bounding box, adding $15\text{–}30\text{ ms}$ per frame depending on object count.
  2. **Real-Time Association:** Greedy IoU computes bounding box spatial overlap in **$0.32\text{ ms}$** ($<1\%$ of frame budget).
  3. **High Inter-Frame Overlap:** Because the camera operates at $33.72\text{ FPS}$, inter-frame target displacements are small ($<15\text{ px}$ per frame), making spatial IoU association highly robust without complex Kalman filtering.

### Challenge 4: Mitigation of Error Propagation
- **Peer Question (Intern D):** *"In your error propagation study, what happens when CLAHE amplifies high-frequency turbidity noise into false positives?"*
- **Technical Defense (Hemamdhar):**
  1. **Controlled Clip Limit ($1.5$):** We specifically rejected aggressive clip limits ($\ge 3.0$) because they amplified suspension speckle noise. Clip limit $1.5$ restricts histogram slope, preventing localized contrast blowouts.
  2. **Lightness Isolation:** Operating exclusively on the $L^*$ channel in CIELAB space prevents chromatic artifact generation.
  3. **Detector Confidence Filtering ($0.25$) & Tracking Persistence ($5\text{ frames}$):** Transient floating particulate reflections rarely persist across consecutive frames, enabling the tracker to suppress $99.2\%$ of upstream optical noise spikes.

---

## 📋 3. Peer Evaluation Rubric & Feedback Matrix

| Evaluation Criterion | Weight | Score (1-10) | Peer Feedback / Observations |
| :--- | :--- | :--- | :--- |
| **1. Technical Rigor & Depth** | 25% | **9.8 / 10** | Comprehensive optical physics formulation and empirical ablation evidence. |
| **2. Pacing & Time Management** | 20% | **9.8 / 10** | Completed at 14m45s within the 15m limit without rushing. |
| **3. Clarity of Visualizations** | 20% | **9.5 / 10** | High-contrast posters, Pareto frontier, and visual side-by-side comparisons. |
| **4. Ability to Defend Choices** | 20% | **10.0 / 10** | Clear, quantitative, hardware-justified defenses against all challenger questions. |
| **5. Packaging & Reproducibility** | 15% | **9.6 / 10** | Installable Python package, clean CLI, and cryptographic audit manifest. |
| **Weighted Total** | **100%** | **9.74 / 10.0** | **Outstanding / Ready for Final Mentor & Leadership Submission** |

---

## 🎯 4. Rehearsal Action Items & Final Polish
- [x] Confirmed all repository links use proper GitHub Markdown structure.
- [x] Verified zero-dependency execution of standalone CLI (`underwater-surveillance`).
- [x] Validated that all Pareto frontier plots and system diagrams are 300 DPI high resolution.
- [x] Consolidated full 12-section technical research report for final project archiving.
