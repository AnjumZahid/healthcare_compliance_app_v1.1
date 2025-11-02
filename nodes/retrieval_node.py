from state.chat_state import ChatState
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
# from config.settings import EMBEDDING_MODEL
from nodes.manual_ques import add_manual_questions
import os
from config.settings import DB_DIR

faiss_store_PATH = os.path.join(DB_DIR, "faiss_store")

# ===============================================================

async def retrieve_chunks(state) -> dict:
    """
    Retrieves relevant chunks from FAISS based on compliance questions stored in 
    `compliance_questions_json` and manually added questions in `manual_ques`.
    """
    add_manual_questions(state)

    # ✅ Step 2: Extract compliance questions
    questions_dict = (
        state.get("compliance_questions_json")
        if isinstance(state, dict)
        else getattr(state, "compliance_questions_json", {})
    )

    # ✅ Step 3: Extract manual questions (after insertion)
    manual_questions = (
        state.get("manual_ques")
        if isinstance(state, dict)
        else getattr(state, "manual_ques", [])
    )

    # ✅ Step 4: Combine all questions
    all_questions = []
    for q_list in questions_dict.values():
        all_questions.extend(q_list)
    all_questions.extend(manual_questions)

    if not all_questions:
        print("⚠️ No questions available for retrieval.")
        return state

    # ✅ Step 5: Load embeddings and FAISS vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    vector_store = FAISS.load_local(faiss_store_PATH, embeddings, allow_dangerous_deserialization=True)

    retr_chunks = []
    seen = set()

    # ✅ Step 6: Retrieve top chunks for each question
    for question in all_questions:
        results = await vector_store.asimilarity_search(question, k=2)
        for doc in results:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                retr_chunks.append(doc.page_content)

    # ✅ Step 7: Combine all retrieved text into a plain string
    combined_context = "\n\n".join(retr_chunks)

    # ✅ Step 9: Return updated state
    return {"retrieved_chunks": combined_context}


# =================================================================

# --- Safe version for both ChatState and dict ---
async def retrieve_chunks_node(state) -> dict:
    """
    Retrieves relevant chunks from FAISS based on generated questions.
    Works safely whether `state` is ChatState or dict.
    """

    # ✅ Safely extract answer list
    answers = state.get("answer") if isinstance(state, dict) else getattr(state, "answer", [])

    if not answers:
        # No questions generated yet
        return state

    # --- Load embeddings and FAISS vector store ---
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    vector_store = FAISS.load_local(faiss_store_PATH, embeddings, allow_dangerous_deserialization=True)

    retrieved_chunks = []
    seen = set()

    # --- Retrieve top chunks for each generated question ---
    for question in answers:
        results = await vector_store.asimilarity_search(question, k=2)
        for doc in results:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                retrieved_chunks.append(doc.page_content)

    # --- Combine all retrieved text ---
    context = "\n\n".join(retrieved_chunks)

    # --- Return updated state safely ---
    if isinstance(state, dict):
        updated_state = dict(state)
        updated_state["context"] = context
        return updated_state
    else:
        return state.model_copy(update={"context": context})
