# ASL Sign Recognition System

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black?logo=flask)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-orange?logo=tensorflow)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Landmarks-red)
![Status](https://img.shields.io/badge/Status-Final%20Year%20Project-success)

A final year project demo for **isolated American Sign Language recognition** using MediaPipe landmarks and a trained **Light Transformer** model.

The system accepts a short sign video, extracts hand and body pose landmarks, normalizes the sequence, and predicts the performed ASL sign using a trained deep learning model.

---

## Project Overview

This project focuses on recognizing isolated ASL signs from short video clips. It was developed as a final year AI project to demonstrate the use of:

- Computer vision
- Landmark extraction
- Deep learning
- Model evaluation
- Flask-based web deployment

The application includes a clean landing page and a recognition demo page where users can upload or record a short sign video and view the predicted sign with top 5 confidence scores.

---

## Key Features

- Clean final year project landing page
- Video upload or record option
- MediaPipe hand and pose landmark extraction
- Landmark normalization
- Light Transformer model prediction
- Top 5 predicted signs with confidence percentages
- Flask-based web interface
- Included trained model file

---

## Model Summary

| Item | Value |
|---|---|
| Task | Isolated ASL sign recognition |
| Number of signs | 50 |
| Dataset size | 10,000 samples |
| Samples per sign | 200 |
| Input shape | 64 x 225 |
| Best model | Light Transformer |
| Test accuracy | 78% |

---

## Developers / Co-authors

- [Abdifatah Abdilahi Essa](https://github.com/Cabdifatahtoni)
- Mohamed Muse Mohamed
- Abdalle Omar Ahmed
---

## Folder Structure

```text
asl-sign-recognition-flask-demo/
  app.py
  requirements.txt
  README.md
  .gitignore
  label_map_50_words.json

  models/
    light_transformer_50_words_200.keras

  templates/
    index.html
    demo.html

  static/
    css/
      style.css
    js/
      app.js
    images/
      person1.jpg
      person2.jpg
      person3.jpg
      university.jpg

  uploads/
    .gitkeep
```

---

## Model File

The trained model is included in this repository.

Required model path:

```text
models/light_transformer_50_words_200.keras
```

Required label map path:

```text
label_map_50_words.json
```

Do not rename these files unless you also update the paths inside `app.py`.

---

## Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/6302Mohamed/asl-sign-recognition-flask-demo.git
cd asl-sign-recognition-flask-demo
```

Or download the ZIP from GitHub:

```text
Code → Download ZIP
```

Then extract it and open the folder in VS Code.

---

### 2. Create a virtual environment

Recommended Python version:

```text
Python 3.12
```

Create the environment:

```bash
py -3.12 -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Run the application

```bash
python app.py
```

Open the home page in your browser:

```text
http://127.0.0.1:5000
```

Open the recognition demo page directly:

```text
http://127.0.0.1:5000/demo
```

---

## How to Use

1. Open the web application.
2. Go to the recognition demo page.
3. Upload or record a short ASL sign video.
4. Click **Classify Sign**.
5. View the predicted sign and the top 5 predictions with confidence percentages.

---

## Best Video Recording Tips

For better prediction:

- Use a short 2 to 4 second video.
- Show only one isolated sign.
- Keep upper body and hands visible.
- Use good lighting.
- Avoid fast camera movement.
- Use a plain background if possible.

---

## Limitations

- The system recognizes isolated signs only.
- It does not yet perform continuous sentence-level sign language translation.
- Real-time camera recognition requires additional segmentation and smoothing.
- Some visually similar signs may still be confused by the model.
- Prediction quality depends on video clarity and how similar the sign performance is to the training data.

---

## Future Work

- Convert the trained Keras model to TensorFlow Lite.
- Build a mobile app version.
- Add real-time camera support.
- Add sentence-level sign sequence interpretation.
- Improve performance using more data and stronger landmark preprocessing.
- Add support for more ASL signs.

---

## Tech Stack

| Area | Tools |
|---|---|
| Programming | Python |
| Web framework | Flask |
| Deep learning | TensorFlow / Keras |
| Computer vision | OpenCV |
| Landmark extraction | MediaPipe |
| Frontend | HTML, CSS, JavaScript |
| Model type | Light Transformer |

---

## Local Test Checklist

Before sharing or presenting, confirm that the folder contains:

```text
app.py
README.md
requirements.txt
.gitignore
label_map_50_words.json
models/
templates/
static/
uploads/
```

Then run:

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

If the page loads and `/demo` classifies a short video, the project is ready for demonstration.
