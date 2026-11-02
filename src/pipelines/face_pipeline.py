import dlib
import numpy as np
#import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students
from pathlib import Path
import sys
from pathlib import Path    

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "models"

def get_safe_path(file_path):
    path_str = str(file_path)
    # Convert non-ASCII path (like ドキュメント) to Windows 8.3 short ASCII path
    if sys.platform == 'win32':
        import ctypes
        buf = ctypes.create_unicode_buffer(500)
        ctypes.windll.kernel32.GetShortPathNameW(path_str, buf, 500)
        return buf.value or path_str
    return path_str

@st.cache_resource
def load_lib_models():
    detector = dlib.get_frontal_face_detector()

    # sp = dlib.shape_predictor(
    #     #face_recognition_models.pose_predictor_model_location()
    #     r"C:\models\shape_predictor_68_face_landmarks.dat"
    # )

    # facerec = dlib.face_recognition_model_v1(
    #     #face_recognition_models.face_recognition_model_location() 
    #     r"C:\models\dlib_face_recognition_resnet_model_v1.dat"
    # )
    #     # Automatically locates models regardless of OS (Windows, Linux, Mac)
    # sp = dlib.shape_predictor(
    #     face_recognition_models.pose_predictor_model_location()
    # )
    # facerec = dlib.face_recognition_model_v1(
    #     face_recognition_models.face_recognition_model_location()
    # )

    sp = dlib.shape_predictor(
        get_safe_path(MODEL_DIR / "shape_predictor_68_face_landmarks.dat")
    )
    facerec = dlib.face_recognition_model_v1(
        get_safe_path(MODEL_DIR / "dlib_face_recognition_resnet_model_v1.dat")
    )

    return detector, sp, facerec

# taken image converted to number(embeddings)
def get_face_embeddings(image_np):
    detector, sp, facerec = load_lib_models()
    faces =  detector(image_np, 1)

    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) #128 embeddings

        encodings.append(np.array(face_descriptor))
    return encodings


@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embedding")
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get("student_usn"))

    if len(X) == 0:
        return None

    clf = SVC(kernel="linear", probability=True, class_weight="balanced")

    try:
        clf.fit(X, y)
    except ValueError:
        pass
    return {"clf":clf, "X":X, "y":y}

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendence(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_students = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_students, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_student = sorted(list(set(y_train)))

    for encoding in encodings:
        if  len(all_student) >= 2:
            predicted_usn = str(clf.predict([encoding])[0])
        else:
            predicted_usn = str(all_student[0])

        student_embedding = X_train[y_train.index(predicted_usn)]

        best_match_score = np.linalg.norm(student_embedding - encoding)
        resemblence_threshold = 0.6

        if best_match_score <= resemblence_threshold:
            detected_students[predicted_usn] = True
    return detected_students, all_student, len(encodings)