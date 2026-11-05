# Universality of Spectral Bias in Deep Learning: Identifying High-Frequency Vulnerability Signatures Across Architectures, Scales, and Modalities

**Preliminary Research Report**  
*Apart Research Style Report*

---

## 1. Introduction

### 1.1 Motivation & The Spectral Vulnerability Problem

Deep neural networks (DNNs) have achieved parity with—and in many domains surpassed—human perceptual accuracy across computer vision and multimodal tasks. However, their real-world deployment in safety-critical systems remains fundamentally constrained by an acute sensitivity to **adversarial perturbations**: tiny, worst-case input shifts that are imperceptible to human observers yet reliably induce catastrophic classification failures ([Szegedy et al., 2013](file:///); [Goodfellow et al., 2014](file:///)). 

A prominent explanation for this vulnerability is the **"Features, Not Bugs" hypothesis** ([Ilyas et al., 2019](file:///)), which posits that adversarial vulnerability is not an incidental flaw of optimization or architecture, but a direct consequence of standard empirical risk minimization (ERM). Models maximize predictive accuracy by latching onto any statistically reliable pattern in the training distribution—including "non-robust features" that correlate with the target label but are orthogonal to human semantic perception.

```
+----------------------------------------------------------------------------------------------------+
|                                    THE SPECTRAL DIVERGENCE                                         |
|                                                                                                    |
|  Natural Image Statistics                                      Adversarial Perturbations          |
|  Power Law Decay: S(f) ~ 1 / f^a (a ~ 2)                       Concentrated in High Frequencies    |
|                                                                                                    |
|  Power ^                                                       Power ^                             |
|        | *                                                           |                        * *  |
|        |   *                                                         |                     * *     |
|        |     *                                                       |                  * *        |
|        |        * *                                                  |             * * *           |
|        |             * * * *                                         |       * * *                 |
|        +-----------------------> Frequency                           +----------------------->     |
|        0.0 (DC)        1.0 (Nyquist)                                 0.0 (DC)        1.0 (Nyquist) |
|        [Human Perception Focus: Shape, Geometry]                     [Model Vulnerability Focus]   |
+----------------------------------------------------------------------------------------------------+
```

In this work, we operationalize the non-robust feature hypothesis through the mathematical lens of **Fourier analysis and signal processing**. Natural visual environments exhibit scale-invariant statistics: their power spectral density follows a power-law decay $S(f) \propto 1/f^\alpha$ (with $\alpha \approx 2$), where low spatial frequencies dominate and encode global geometric structure, object boundaries, and holistic semantics ([Field, 1987](file:///); [Torralba & Oliva, 2003](file:///)). Human visual cognition relies heavily on these low-to-mid spatial frequency envelopes. Conversely, high spatial frequencies correspond to fine-grained textures, rapid pixel transitions, and imperceptible micro-patterns. 

When deep networks are optimized, do they develop a pathological **spectral bias**—preferentially exploiting high-frequency statistical artifacts over robust low-frequency geometry? More critically, is this high-frequency reliance an isolated byproduct of specific architectures, or is it a **universal property** governing modern representation learning?

---

### 1.2 Core Research Questions

While prior investigations have examined spectral bias in narrow contexts (such as spectral neural tangents in MLPs ([Rahaman et al., 2019](file:///)) or frequency shortcuts in standard CNNs ([Wang et al., 2020](file:///))), whether this phenomenon constitutes a universal failure mode remains an open and urgent question. We frame this inquiry around three primary research questions:

* **RQ1 (Architectural Inductive Bias):** *Does the strong spatial inductive bias of Convolutional Neural Networks (local connectivity, weight sharing, translation equivariance) provide spectral protection compared to the weak inductive bias of Vision Transformers (patch-level linear projections, global multi-head self-attention)?*
* **RQ2 (Scale and Resolution Invariance):** *Does scaling the data domain and input resolution (from low-resolution $32 \times 32$ CIFAR-10 images to high-resolution $224 \times 224$ ImageNet-1k images) mitigate high-frequency shortcuts by providing richer multiscale semantic context?*
* **RQ3 (Multimodal Semantic Anchoring):** *Does joint vision-language contrastive supervision (e.g., CLIP's text-image alignment) force visual representations to adopt human-aligned semantic shape priors, or does the vision encoder inherit identical high-frequency vulnerabilities?*

---

### 1.3 Analytical Framework: Dual Signal & Mechanistic Approach

To answer these questions, we deploy a dual-perspective analytical framework combining frequency-domain signal processing with mechanistic interpretability:

1. **Normalized Power Spectrum (NPS) Profiling:**  
   We calculate the 2D Discrete Fourier Transform ($\mathcal{F}$) of minimum-norm and iterative adversarial perturbations generated by standard attack suites (DeepFool, Projected Gradient Descent (PGD), and AutoAttack). By computing the radially integrated (azimuthally averaged) Normalized Power Spectrum over the discrete spatial frequency interval $[0, f_{\text{Nyquist}}]$, we quantify the exact spectral distribution of the signals required to fool each model.
   
2. **Mechanistic Drift Tracking:**  
   To understand not only *where* models are vulnerable at the input layer, but *how* spectral bias propagates internally, we leverage layer-wise activation tracking (via NNsight). This traces how high-frequency perturbation energy triggers internal latent representations to drift away from their true class manifolds across successive network depths.

---

### 1.4 Summary of Contributions

Through systematic experimentation across three distinct operational regimes—(1) Small-scale vision, (2) Large-scale vision, and (3) Multimodal foundation models—this report makes four key contributions:

* **Universal High-Frequency Backdoor Across Diverse Modalities:**  
  We demonstrate that high-frequency spectral vulnerability is universal. Regardless of whether models employ localized convolutions (ResNet-18, ResNet-50), global self-attention (ViT-B/16), or contrastive cross-modal supervision (CLIP ViT-B/32), adversarial perturbations universally concentrate their power in the high-frequency spectrum ($f > 0.5 \cdot f_{\text{Nyquist}}$), in sharp contrast to the low-frequency dominance of natural images.
  
* **Invariance to Resolution and Scale:**  
  Scaling input resolution by an order of magnitude (from CIFAR-10 to ImageNet-1k) does not attenuate spectral bias. Both ResNet-50 and ViT-B/16 exhibit Normalized Power Spectra with spectral centroids consistently centered around $f \approx 0.5$, indicating a persistent near-white or high-pass noise vulnerability.

* **Absence of "Semantic Immunity" in Vision-Language Models:**  
  We show that language supervision fails to eliminate spectral vulnerabilities. Even though CLIP's training aligns images with high-level linguistic concepts, high-frequency noise decouples the visual embedding from its textual anchor in the terminal Transformer blocks, demonstrating that semantic alignment at the loss level does not guarantee spectral robustness in representation space.

* **Architectural Divergence in Internal Error Propagation:**  
  While the input-level spectral signatures are virtually indistinguishable across CNNs and Transformers, mechanistic analysis reveals a marked architectural divergence in latent propagation: CNNs undergo a structured, stage-by-stage drift, whereas Vision Transformers suffer a creeping, distributed representation collapse across attention blocks.

---

### 1.5 Organization of the Report

The remainder of this report is organized as follows:
* **Section 2 (Theoretical Foundations & Background):** Formulates the Fourier analysis methodology, defines the Normalized Power Spectrum (NPS), and reviews the foundational literature on spectral bias, inductive biases, and adversarial feature learning.
* **Section 3 (Experimental Methodology & Setup):** Details the benchmark architectures, datasets (CIFAR-10, ImageNet-1k, COCO-Captions), attack formulations (DeepFool, PGD, AutoAttack), and metric definitions.
* **Section 4 (Empirical Results & Comparative Analysis):** Presents our empirical findings across the three regimes (Study 1: CIFAR-10 Baseline; Study 2: ImageNet Scaling; Study 3: CLIP Multimodal Robustness) with visual NPS curves and spectral centroid metrics.
* **Section 5 (Mechanistic Interpretability & Latent Propagation):** Analyzes layer-wise activation drift, contrasting the localized breakdown in CNNs against the global decoupling in ViTs and CLIP.
* **Section 6 (Discussion, Safety Implications & Future Work):** Discusses the implications for AI safety and robustness, and outlines future avenues for spectrally regularized objective functions designed to penalize high-frequency exploitation.
