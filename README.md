# ASL Sign Recognition System

A final year project demo for isolated American Sign Language recognition using MediaPipe landmarks and a trained Light Transformer model.

The system accepts a short sign video, extracts hand and body pose landmarks, normalizes the sequence, and predicts the performed ASL sign using a trained deep learning model.

## Project Overview

This project focuses on recognizing isolated ASL signs from short video clips. It was developed as a final year AI project to demonstrate the use of computer vision, landmark extraction, deep learning, and web-based deployment.

## Key Features

- Clean project landing page
- Video upload or record option
- MediaPipe hand and pose landmark extraction
- Landmark normalization
- Light Transformer model prediction
- Top 5 predicted signs with confidence percentages
- Flask-based web interface

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

## Developers

- Abdifatah Abdilahi Essa
- Mohamet Muuse Mohamed
- Apdale Omar Ahmed

## Folder Structure

```text
flask_asl_demo/
  app.py
  requirements.txt
  README.md
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

    Important Model File

The trained model file is not included in GitHub by default because it can be large.

Place the model file here:

models/light_transformer_50_words_200.keras

Required model filename:

light_transformer_50_words_200.keras

Also make sure this label map file exists:

label_map_50_words.json
Setup Instructions
1. Clone or download the project
git clone <your-repository-url>
cd flask_asl_demo

Or open the flask_asl_demo folder directly in VS Code.

2. Create a virtual environment

Recommended Python version:

Python 3.12

Create environment:

py -3.12 -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
4. Add the trained model

Place this file:

light_transformer_50_words_200.keras

inside:

models/

Final path should be:

models/light_transformer_50_words_200.keras
5. Run the application
python app.py

Open in browser:

http://127.0.0.1:5000

Recognition demo page:

http://127.0.0.1:5000/demo
How to Use
Open the web application.
Go to the recognition demo page.
Upload or record a short ASL sign video.
Click Classify Sign.
View the predicted sign and the top 5 predictions with confidence percentages.
Best Video Recording Tips

For better prediction:

Use a short 2 to 4 second video.
Show only one isolated sign.
Keep upper body and hands visible.
Use good lighting.
Avoid fast camera movement.
Use a plain background if possible.
Limitations
The system recognizes isolated signs only.
It does not yet perform continuous sentence-level sign language translation.
Real-time camera recognition requires additional segmentation and smoothing.
Some visually similar signs may still be confused by the model.
Future Work
Convert the trained Keras model to TensorFlow Lite.
Build a mobile app version.
Add real-time camera support.
Add sentence-level sign sequence interpretation.
Improve performance using more data and better landmark preprocessing.
Tech Stack
Python
Flask
TensorFlow / Keras
MediaPipe
OpenCV
NumPy
HTML, CSS, JavaScript

---

## Step 5: Check the folder

Your `flask_asl_demo` should now contain:

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
Step 6: Test install command locally

From VS Code terminal, inside:

C:\Users\Moham\sign-language-50\flask_asl_demo

run:

pip install -r requirements.txt

Then run:

python app.py