from state.chat_state import ChatState
from services.doc_extractor import extract_from_multiple

def extract_history(state: ChatState) -> dict:
    """
    Extract patient history text from one or multiple uploaded PDFs.
    Automatically handles both single file path (str)
    and multiple file paths (list of str).
    """

    # 🔍 Get the PDF path(s) from state
    files = (
        state.get("pdf_hist_path")
        if isinstance(state, dict)
        else getattr(state, "pdf_hist_path", "")
    )

    if not files:
        return {"history_text": "❌ No PDF file found in state."}

    # 🧠 Normalize to a list
    if isinstance(files, str):
        files = [files]
    elif not isinstance(files, list):
        return {"history_text": f"⚠️ Unexpected pdf_hist_path type: {type(files)}"}

    # 🩺 Extract text from all PDFs
    combined_text = extract_from_multiple(files)

    return {"history_text": combined_text}

