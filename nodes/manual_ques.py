from state.chat_state import ChatState

def add_manual_questions(state: ChatState) -> dict:
    """
    Adds doctor-provided compliance questions from ChatState.
    If no questions are provided, returns an empty list.
    """

    # 🧠 Get raw questions from ChatState
    raw_questions = (
        state.get("raw_manual_questions")
        if isinstance(state, dict)
        else getattr(state, "raw_manual_questions", [])
    )

    # ✅ Handle empty or invalid input
    if not raw_questions:
        print("\n⚠️ No manual compliance questions provided.\n")
        return {"manual_ques": []}

    # --- Debug print ---
    print("\n================ 📝 MANUAL COMPLIANCE QUESTIONS =================\n")
    for q in raw_questions:
        print("-", q)

    # ✅ Return properly formatted dict for LangGraph
    return {"manual_ques": raw_questions}

