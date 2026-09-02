#  Invisibility Cloak

> **Real-time invisibility using Computer Vision, OpenCV, and MediaPipe**

The **Invisibility Cloak** is a real-time computer vision project that creates an invisibility effect using a webcam. The system detects the user's body, separates it from the background, and replaces the detected body pixels with a previously captured clean background.

The effect can be controlled using **custom hand gestures**, making the project an interactive demonstration of real-time **semantic segmentation, hand tracking, image masking, and alpha compositing**.

---

## ✨ Features

* 🎥 Real-time webcam processing
* 🧍 Human/background separation using MediaPipe Selfie Segmentation
* ✋ Real-time hand tracking using MediaPipe Hands
* 🤏 Gesture-based invisibility toggle
* 🎭 Automatic body masking
* 🖼️ Static background frame capture
* 🔲 Morphological mask smoothing
* ⚡ NumPy-based high-speed pixel operations
* 🧩 Modular and clean project architecture
* 💻 Designed for real-time CPU execution

---

## 🧠 How It Works

The system follows a simple computer vision pipeline:

```text
             Webcam
                │
                ▼
        ┌─────────────────┐
        │ Capture Frames  │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │ Human Detection │
        │   MediaPipe     │
        └────────┬────────┘
                 │
                 ▼
          Human Mask
                 │
       ┌─────────┴─────────┐
       │                   │
       ▼                   ▼
 Background Frame     Live Webcam
       │                   │
       └─────────┬─────────┘
                 │
                 ▼
          Mask Processing
                 │
                 ▼
          Image Compositing
                 │
                 ▼
        Invisibility Effect
```

When the invisibility effect is enabled, pixels corresponding to the detected human are replaced with pixels from the previously captured background.

---

## 🛠️ Technologies Used

| Technology    | Purpose                                                                 |
| ------------- | ----------------------------------------------------------------------- |
| **Python**    | Main programming language                                               |
| **OpenCV**    | Webcam capture, image processing, display, and morphological operations |
| **MediaPipe** | Human segmentation and hand landmark detection                          |
| **NumPy**     | Fast vectorized pixel and matrix operations                             |

---

## 🤖 Pre-Trained ML Models

### MediaPipe Selfie Segmentation

MediaPipe Selfie Segmentation is used to separate the human subject from the background.

**Input:**

* Webcam frame

**Output:**

* Pixel-level segmentation probability map

The probability map is converted into a binary mask using a confidence threshold.

```text
Probability > 0.5
        │
        ▼
     Human
        │
        ▼
      Mask
```

---

### MediaPipe Hands

MediaPipe Hands detects and tracks the user's hand.

It uses:

* **Palm Detection Model (BlazePalm)**
* **Hand Landmark Model**

The hand model provides **21 3D landmarks**, including:

* Wrist
* Thumb joints
* Index finger joints
* Middle finger joints
* Ring finger joints
* Pinky finger joints

These landmarks are used to recognize gestures.

---

## ✋ Gesture Detection

The project uses spatial distances between hand landmarks to identify gestures.

For example, the distance between the **thumb tip** and **index finger tip** can be calculated using Euclidean distance:

$$
d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}
$$

Where:

* $P_1(x_1,y_1)$ = first landmark
* $P_2(x_2,y_2)$ = second landmark
* $d$ = distance between the landmarks

If the calculated distance satisfies the defined threshold, the corresponding gesture is triggered.

Example:

```text
Thumb Tip ●
          \
           \  small distance
            \
Index Tip ●

       ↓

   Gesture Trigger
       ↓
Invisibility ON/OFF
```

---

## 🎭 Invisibility Effect

The invisibility effect works by combining:

1. Live webcam frame
2. Human segmentation mask
3. Captured background frame

The mask determines which pixels should come from the live frame and which pixels should come from the background.

### Frame Compositing

The final image can be represented as:

$$
\mathbf{I}_{out}
=
\mathbf{I}_{live}\odot(1-\mathbf{M})
+
\mathbf{I}_{bg}\odot\mathbf{M}
$$

Where:

* $\mathbf{I}_{out}$ = final output image
* $\mathbf{I}_{live}$ = current webcam frame
* $\mathbf{I}_{bg}$ = captured background
* $\mathbf{M}$ = processed mask
* $\odot$ = element-wise multiplication

The mask is normalized between:

```text
0.0 ─────────────── 1.0
Background          Human
```

---

## 🧹 Mask Smoothing

Raw segmentation masks can contain noisy edges around the body.

To improve the visual quality, image-processing techniques such as:

* Gaussian Blur
* Dilation
* Erosion

can be applied to the mask.

This helps produce smoother transitions between the person and background.

---

## 📸 Background Calibration

Before the invisibility effect is activated, the system captures a clean background frame.

```text
Step 1
   ↓
User is outside the camera view
   ↓
Capture background
   ↓
Store frame in RAM
   ↓
User enters the scene
   ↓
Apply invisibility effect
```

The captured frame acts as the replacement image for the user's body.

---

# 📁 Project Structure

```text
invisibility-cloak/
│
├── main.py
├── requirements.txt
│
├── core/
│   ├── segmenter.py
│   ├── gesture_tracker.py
│   └── blender.py
│
├── utils/
│   └── camera.py
│
└── assets/
    ├── background.jpg
    └── screenshots/
```

---

## 📂 Directory Description

### `main.py`

The main entry point of the application.

Responsibilities:

* Initialize webcam
* Initialize computer vision modules
* Capture frames
* Manage processing loop
* Coordinate segmentation
* Track gestures
* Apply invisibility effect
* Display output

---

### `core/segmenter.py`

Handles **MediaPipe Selfie Segmentation**.

Responsibilities:

* Process webcam frames
* Generate segmentation probabilities
* Create human/background masks
* Apply thresholding
* Smooth the generated mask

---

### `core/gesture_tracker.py`

Handles **MediaPipe Hands** and gesture recognition.

Responsibilities:

* Detect hands
* Extract 21 hand landmarks
* Calculate landmark distances
* Recognize predefined gestures
* Trigger invisibility state changes

---

### `core/blender.py`

Handles image compositing.

Responsibilities:

* Process the segmentation mask
* Combine live frame and background
* Perform NumPy-based pixel operations
* Generate final invisibility frame

---

### `utils/camera.py`

Contains camera-related helper functions.

Responsibilities:

* Initialize webcam
* Configure resolution
* Capture frames
* Capture the initial background
* Handle camera-related utilities

---

### `assets/`

Stores project assets such as:

```text
background.jpg
screenshots/
```

The `background.jpg` file contains the clean scene captured before the user enters the camera view.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/invisibility-cloak.git
```

Navigate into the project:

```bash
cd invisibility-cloak
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
opencv-python
mediapipe
numpy
```

---

# ▶️ Running the Project

Start the application with:

```bash
python main.py
```

The webcam should open and begin processing frames in real time.

---

# 🎮 Usage

1. Start the application.
2. Allow access to your webcam.
3. Keep the scene clear while the initial background is captured.
4. Enter the camera view.
5. Perform the configured hand gesture.
6. The invisibility effect will activate.
7. Perform the gesture again to toggle the effect.
8. Press the configured exit key to close the application.

---

# 🔬 Computer Vision Techniques

This project demonstrates several important computer vision concepts:

### 1. Semantic Segmentation

Separates the human subject from the background.

### 2. Hand Landmark Detection

Tracks 21 hand keypoints in real time.

### 3. Spatial Distance Calculation

Uses Euclidean distance between landmarks to recognize gestures.

### 4. Binary Masking

Converts segmentation probabilities into a human/background mask.

### 5. Morphological Processing

Improves mask quality using operations such as erosion and dilation.

### 6. Alpha Compositing

Combines the live frame and captured background.

### 7. Real-Time Video Processing

Processes webcam frames continuously while maintaining interactive performance.

---

# 🚀 Performance

The project is designed around lightweight computer vision models and vectorized NumPy operations.

Performance depends on:

* Webcam resolution
* CPU performance
* MediaPipe inference speed
* Number of image-processing operations
* OpenCV configuration

Reducing the webcam resolution can improve real-time FPS on lower-end systems.

---

# 🧩 Architecture

The project separates different responsibilities into independent modules:

```text
main.py
   │
   ├── Camera
   │      └── utils/camera.py
   │
   ├── Segmentation
   │      └── core/segmenter.py
   │
   ├── Gesture Tracking
   │      └── core/gesture_tracker.py
   │
   └── Image Blending
          └── core/blender.py
```

This modular design makes the project easier to:

* Maintain
* Debug
* Extend
* Test
* Reuse

---

🔮 Future Improvements

The project can be extended into a more advanced real-time AI vision system.

🎥 Dynamic Backgrounds

Support videos or dynamically changing backgrounds instead of a single static frame.

👥 Multi-Person Segmentation

Extend the system to handle multiple people simultaneously.

🧠 Advanced Gesture Recognition

Train a custom gesture classification model instead of relying only on landmark distances.

⚡ GPU Acceleration

Use GPU-based inference to improve FPS at higher resolutions.

🌐 Web Application

Build a browser-based interface using:

FastAPI
Streamlit
WebSockets
📱 Mobile Deployment

Convert the computer vision pipeline for mobile devices.

🎨 Advanced Segmentation

Use more sophisticated segmentation models for improved boundary accuracy.

🎬 Video Recording

Add the ability to record and export the final invisibility effect.

🏆 Why This Project Matters

Although the final effect looks like a visual trick, the project demonstrates a complete real-time AI pipeline:

Machine Learning
       +
Computer Vision
       +
Image Processing
       +
Human-Computer Interaction
       +
Real-Time Systems

It provides practical experience with how machine learning models can be integrated into real-world interactive applications.

📚 Learning Outcomes

Through this project, you can demonstrate experience with:

Real-time Computer Vision
Semantic Segmentation
MediaPipe
OpenCV
Hand Landmark Detection
Gesture Recognition
NumPy Optimization
Image Masking
Alpha Compositing
Morphological Image Processing
Modular Python Development
Real-Time AI Applications

## ⭐ Acknowledgements

This project uses the following open-source technologies:

* OpenCV
* MediaPipe
* NumPy

Special thanks to the open-source computer vision community for providing the tools and pre-trained models that make real-time vision applications possible.

---
🤝 Contributing

Contributions are welcome!

# Fork the repository

# Create a feature branch
git checkout -b feature/new-feature

# Commit your changes
git commit -m "Add new feature"

# Push the branch
git push origin feature/new-feature

Then open a Pull Request.

📄 License

This project is available under the MIT License.


## 👨‍💻 Author

**Qamar Abbas**

Artificial Intelligence Student & AI/ML Developer

---
⭐ Support

If you found this project interesting or useful:

⭐ Star the repository

🍴 Fork the project

🐛 Report issues

💡 Suggest improvements
