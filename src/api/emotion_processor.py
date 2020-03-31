import os
import sys
import logging

import cv2
from keras.models import load_model
import numpy as np

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.inference import load_image
from utils.preprocessor import preprocess_input

def process_image(image):

    try:
        # parameters for loading data and images
        detection_model_path = './models/haarcascade_frontalface_default.xml'
        emotion_model_path = './models/model.h5'
        emotion_labels = get_labels('fer2013')
        font = cv2.FONT_HERSHEY_SIMPLEX

        # hyper-parameters for bounding boxes shape
        emotion_offsets = (20, 40)
        emotion_offsets = (0, 0)

        # loading models
        face_detection = load_detection_model(detection_model_path)
        emotion_classifier = load_model(emotion_model_path, compile=False)

        # getting input model shapes for inference
        emotion_target_size = emotion_classifier.input_shape[1:3]

        # loading images
        image_array = np.fromstring(image, np.uint8)
        unchanged_image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

        rgb_image = cv2.cvtColor(unchanged_image, cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(unchanged_image, cv2.COLOR_BGR2GRAY)

        faces = detect_faces(face_detection, gray_image)
        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)
            rgb_face = rgb_image[y1:y2, x1:x2]

            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]

            try:
                rgb_face = cv2.resize(rgb_face, (gender_target_size))
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            rgb_face = preprocess_input(rgb_face, False)
            rgb_face = np.expand_dims(rgb_face, 0)

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
            emotion_text = emotion_labels[emotion_label_arg]

            color = (255, 0, 0)

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_text, color, 0, -50, 1, 2)
    except Exception as err:
        logging.error('Erro en procesador de emociones: "{0}"'.format(err))

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

    dirname = 'resultados'
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    cv2.imwrite(os.path.join(dirname, 'resultado.png'), bgr_image)
