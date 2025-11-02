# --- Node 1: Build Prompt ---
from state.chat_state import ChatState

def merge_all_text(state: ChatState) -> dict:
    """Merge all extracted texts into a combined report."""
    try:
        medicines_combined = ", ".join(state.medicine_text)
        merged = (
            f"🩺 Patient History:\n{state.history_text}\n\n"
            f"🧬 CV Model Findings:\n{state.cv_model_text}\n\n"
            f"💊 Prescribed Medicines:\n{medicines_combined}"
        )
        return {"merge_text": merged}
    except Exception as e:
        return {"merge_text": f"❌ Error while merging text: {str(e)}"}


def generate_llm_Qprompt(state: ChatState) -> dict:
    """Generate compliance-checking questions using the merged text."""
    context_text = state.merge_text

    query_text = f"""
You are a medical compliance assistant.
Your task is to support doctors by checking prescribed medicines against WHO rules and guidelines.

Context Provided
{context_text}

Your Role
For each prescribed medicine, generate 3 precise and distinct questions that should be asked to verify compliance with WHO rules and medical best practices.

Guidelines
Questions must be clear, specific, and relevant to the medicine and patient case.
Focus on WHO guidelines for dosage, contraindications, interactions, and suitability for the patient’s condition.

Do not answer the questions yourself — only generate them.

    """

    return {"generated_llm_Qprompt": query_text}



# =================================================================================


def build_compliance_prompt(state) -> dict:
    """
    Builds a structured compliance query for the LLM using
    history, image, medicine text, and WHO/FDA context.
    Works safely whether 'state' is a ChatState or a dict.
    """

    # ✅ Extract fields safely
    # get = lambda key: state.get(key, "") if isinstance(state, dict) else getattr(state, key, "")

    # context = state.get("retrieved_chunks")
    context = getattr(state, "retrieved_chunks", "")
    get_fda_info = getattr(state, "fda_info", "")
    hist_text = getattr(state, "history_text", "")
    image_text = getattr(state, "cv_model_text", "")
    med_text = getattr(state, "medicine_text", "")
   

    # ✅ Build structured prompt
    prompt = f"""
    You are a WHO compliance checker.

    Context from WHO standards:
    {context}

    Context from openFDA API End Points:
    {get_fda_info}

    Patient history:
    {hist_text}

    Image findings:
    {image_text}

    Doctor’s prescribed medicine(s):
    {med_text}

    Task:
    Check whether the suggested medicine is compliant with WHO treatment guidelines.
    Give a concise doctor-facing response with:
    - Compliance status (Yes/No)
    - Justification (short, clear)
    """.strip()
    
    return {"compliance_prompt": prompt}




