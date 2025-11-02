from state.chat_state import ChatState

def extract_med(state: ChatState) -> dict:
    """
    Extract and normalize (lowercase) doctor-prescribed medicines.
    Takes raw_medicine_text from ChatState instead of using hardcoded values.
    """

    # 🩺 Take raw medicine text from state
    raw_meds = (
        state.get("raw_medicine_text")
        if isinstance(state, dict)
        else getattr(state, "raw_medicine_text", "")
    )

    if not raw_meds:
        return {"medicine_text": []}

    # 🧹 Split and normalize (lowercase)
    medicines = [m.strip().lower() for m in raw_meds.split(",") if m.strip()]

    # ✅ Return normalized list
    return {"medicine_text": medicines}


