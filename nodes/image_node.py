from state.chat_state import ChatState
from data.models.image_classifier import classify_xray

def extract_image(state: ChatState) -> dict:
    """
    Uses the CV model to classify the given medical image
    and updates the state with extracted findings.
    """

    try:
        # 🧠 Safely get image path (works for dict or ChatState)
        image_path = (
            state.get("image_path")
            if isinstance(state, dict)
            else getattr(state, "image_path", "")
        )

        # ✅ Handle missing image path
        if not image_path:
            return {"cv_model_text": "❌ No image path provided."}

        # 🩻 Run classification model
        prediction = classify_xray(image_path)

        # 📝 Build descriptive text
        extracted_text = f"{prediction}"

    except Exception as e:
        # ❌ If any error occurs, record it instead
        extracted_text = f"❌ Image processing error: {str(e)}"

    # ✅ Return updated field for state merge
    return {"cv_model_text": extracted_text}

