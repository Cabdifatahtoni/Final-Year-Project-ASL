import json
import uuid
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "light_transformer_50_words_200.keras"
LABEL_MAP_PATH = BASE_DIR / "label_map_50_words.json"
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FRAMES = 64
FEATURES_PER_FRAME = 225


class PositionalEmbedding(tf.keras.layers.Layer):
    def __init__(self, sequence_length, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.sequence_length = sequence_length
        self.embed_dim = embed_dim
        self.position_embedding = tf.keras.layers.Embedding(
            input_dim=sequence_length,
            output_dim=embed_dim,
        )

    def call(self, inputs):
        positions = tf.range(start=0, limit=self.sequence_length, delta=1)
        positions = self.position_embedding(positions)
        return inputs + positions

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "sequence_length": self.sequence_length,
                "embed_dim": self.embed_dim,
            }
        )
        return config


print("Loading ASL model...")
model = tf.keras.models.load_model(
    MODEL_PATH,
    custom_objects={"PositionalEmbedding": PositionalEmbedding},
)
print("Model loaded successfully.")


with open(LABEL_MAP_PATH, "r", encoding="utf-8") as f:
    label_map = json.load(f)

id_to_label = {int(v): k for k, v in label_map.items()}

mp_holistic = mp.solutions.holistic

app = Flask(__name__)


def resize_sequence(sequence: np.ndarray, max_frames: int = MAX_FRAMES) -> np.ndarray:
    num_frames = sequence.shape[0]

    if num_frames == max_frames:
        return sequence

    if num_frames > max_frames:
        indices = np.linspace(0, num_frames - 1, max_frames).astype(int)
        return sequence[indices]

    padded = np.zeros((max_frames, sequence.shape[1]), dtype=np.float32)
    padded[:num_frames] = sequence
    return padded


def normalize_frame(left_hand: np.ndarray, right_hand: np.ndarray, pose: np.ndarray):
    left_shoulder = pose[11]
    right_shoulder = pose[12]

    if np.all(left_shoulder == 0) or np.all(right_shoulder == 0):
        non_zero_pose = pose[np.any(pose != 0, axis=1)]

        if len(non_zero_pose) == 0:
            return left_hand, right_hand, pose

        center = non_zero_pose.mean(axis=0)
        scale = np.std(non_zero_pose[:, :2])
    else:
        center = (left_shoulder + right_shoulder) / 2.0
        scale = np.linalg.norm(left_shoulder[:2] - right_shoulder[:2])

    if scale < 1e-6:
        scale = 1.0

    def normalize_block(block):
        output = block.copy()
        mask = np.any(output != 0, axis=1)
        output[mask] = (output[mask] - center) / scale
        return output

    return normalize_block(left_hand), normalize_block(right_hand), normalize_block(pose)


def extract_landmarks_from_video(video_path: Path) -> np.ndarray:
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError("Could not open uploaded video. Try another MP4, MOV, AVI, MKV, or WEBM video.")

    sequence_rows = []
    total_frames = 0
    frames_with_pose_or_hands = 0

    with mp_holistic.Holistic(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        enable_segmentation=False,
        refine_face_landmarks=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as holistic:
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            total_frames += 1

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(rgb)

            left_hand = np.zeros((21, 3), dtype=np.float32)
            right_hand = np.zeros((21, 3), dtype=np.float32)
            pose = np.zeros((33, 3), dtype=np.float32)

            detected_anything = False

            if results.left_hand_landmarks:
                detected_anything = True
                for i, lm in enumerate(results.left_hand_landmarks.landmark):
                    left_hand[i] = [lm.x, lm.y, lm.z]

            if results.right_hand_landmarks:
                detected_anything = True
                for i, lm in enumerate(results.right_hand_landmarks.landmark):
                    right_hand[i] = [lm.x, lm.y, lm.z]

            if results.pose_landmarks:
                detected_anything = True
                for i, lm in enumerate(results.pose_landmarks.landmark):
                    pose[i] = [lm.x, lm.y, lm.z]

            if detected_anything:
                frames_with_pose_or_hands += 1

            left_hand, right_hand, pose = normalize_frame(left_hand, right_hand, pose)

            frame_vector = np.concatenate(
                [
                    left_hand.reshape(-1),
                    right_hand.reshape(-1),
                    pose.reshape(-1),
                ]
            ).astype(np.float32)

            sequence_rows.append(frame_vector)

    cap.release()

    if total_frames == 0:
        raise RuntimeError("The uploaded video has no readable frames.")

    if frames_with_pose_or_hands < 3:
        raise RuntimeError(
            "The system could not detect enough body or hand landmarks. "
            "Record again with your upper body and hands clearly visible."
        )

    sequence = np.stack(sequence_rows).astype(np.float32)
    sequence = resize_sequence(sequence)

    if sequence.shape != (MAX_FRAMES, FEATURES_PER_FRAME):
        raise RuntimeError(f"Unexpected model input shape: {sequence.shape}")

    return sequence


def predict_video(video_path: Path):
    sequence = extract_landmarks_from_video(video_path)
    x_input = np.expand_dims(sequence, axis=0)

    probs = model.predict(x_input, verbose=0)[0]
    top_indices = np.argsort(probs)[-5:][::-1]

    top5 = []
    for idx in top_indices:
        word = id_to_label[int(idx)]
        confidence = round(float(probs[idx]) * 100, 2)
        top5.append({"word": word, "confidence": confidence})

    return top5[0], top5


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/demo", methods=["GET", "POST"])
def demo():
    prediction = None
    top5 = None
    error = None
    uploaded_filename = None

    if request.method == "POST":
        uploaded_file = request.files.get("video")

        if not uploaded_file or uploaded_file.filename == "":
            error = "Please upload or record a short sign video first."
        else:
            file_ext = Path(uploaded_file.filename).suffix.lower()

            if file_ext not in [".mp4", ".mov", ".avi", ".mkv", ".webm"]:
                error = "Unsupported video format. Please use MP4, MOV, AVI, MKV, or WEBM."
            else:
                safe_name = f"{uuid.uuid4().hex}{file_ext}"
                video_path = UPLOAD_DIR / safe_name
                uploaded_file.save(video_path)
                uploaded_filename = safe_name

                try:
                    prediction, top5 = predict_video(video_path)
                except Exception as exc:
                    error = str(exc)

    return render_template(
        "demo.html",
        prediction=prediction,
        top5=top5,
        error=error,
        uploaded_filename=uploaded_filename,
    )


if __name__ == "__main__":
    app.run(debug=True)