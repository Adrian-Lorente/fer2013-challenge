# Main entrypoint to call the facealigner and model
import argparse
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2
from tensorflow import keras
from face_aligner import FaceAligner



EMOTION_LIST =["Enfado", "Asco", "Miedo", "Felicidad", "Neutral", "Tristeza", "Sorpresa"]
MODEL_PATH = "../models/best_basic_final.h5"


parser = argparse.ArgumentParser()
parser.add_argument("--img")
args = parser.parse_args()

aligner = FaceAligner()
raw_face = cv2.imread(args.img)
gray = cv2.cvtColor(raw_face, cv2.COLOR_BGR2GRAY)
aligned_face = aligner.align(gray)
cv2.imwrite("gray_aligned.png", aligned_face)

img = keras.utils.load_img("gray_aligned.png", target_size=(48, 48), color_mode="grayscale")
aligned_face = keras.utils.img_to_array(img)
aligned_face = np.expand_dims(aligned_face, axis=0)

model = keras.models.load_model(MODEL_PATH)
emotion_probabilities = model.predict(aligned_face, verbose=0)
emotion = np.argmax(emotion_probabilities, axis=1)

print(str(EMOTION_LIST[emotion[0]]), flush=True)
