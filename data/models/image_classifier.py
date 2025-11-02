import numpy as np
from keras._tf_keras.keras.models import load_model
from keras._tf_keras.keras.utils import load_img, img_to_array
import os

# Go up one level (from services → Medi)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Build the full path to the model
MODEL_PATH = os.path.join(BASE_DIR, "models", "final_pneumonia_model.h5")

# Load model
model = load_model(MODEL_PATH, compile=False)

def classify_xray(img_path: str) -> str:

    """
    Classify chest X-ray into normal, moderate pneumonia, or severe pneumonia.
    Returns a descriptive string with confidence score.
    """

    # img_path = "C:/Users/Admin/Downloads/Medi/data/images/normal_img.jpeg"

    if not os.path.exists(img_path):
        return f"❌ Image not found: {img_path}"

    img = load_img(img_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    prob = float(prediction[0][0])  # probability of pneumonia

    if prob < 0.4:
        return f"Chest X-ray appears normal (pneumonia probability: {prob:.2f})"
    elif prob < 0.7:
        return f"Chest X-ray shows moderate signs of pneumonia (pneumonia probability: {prob:.2f})"
    else:
        return f"Chest X-ray shows severe pneumonia (pneumonia probability: {prob:.2f})"
