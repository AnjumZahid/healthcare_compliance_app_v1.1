import re

from langchain_google_genai import ChatGoogleGenerativeAI
from state.chat_state import ChatState
# from constants import DEFAULT_CHAT_MODEL


from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from config.settings import DEFAULT_CHAT_MODEL
from state.chat_state import ChatState
import json


# =====================================================================================

from langchain_core.messages import HumanMessage

def generate_llm_compliance_json(state: ChatState) -> dict:
    """
    Uses Gemini to generate structured compliance questions in JSON format.
    Structure: { "medicine_name": ["question1", "question2", "question3"] }
    """

    print("🔹 Entered generate_llm_compliance_json node")

    # Initialize Gemini model
    llm = ChatGoogleGenerativeAI(model=DEFAULT_CHAT_MODEL)
    print("🔹 Initialized Gemini model")

    # Dynamically create JSON schema based on medicines
    properties = {med: {"type": "array", "items": {"type": "string"}} for med in state.medicine_text}

    json_schema = {
        "title": "ComplianceQuestions",
        "type": "object",
        "properties": properties,
        "required": state.medicine_text  # all medicines are required keys
    }

    # Structured model
    structured_model = llm.with_structured_output(json_schema)
    print("🔹 Wrapped model with structured output schema")

    prompt = state.generated_llm_Qprompt

    print("🔹 Prompt prepared for LLM:\n", prompt)

    # Generate structured output
    response = structured_model.invoke(prompt)
    print("🔹 Raw response from structured LLM:", response)

    if not response:
        print("⚠️ WARNING: LLM returned empty response!")

    # ✅ Return updated state
    return {"compliance_questions_json": response}




# =====================================================================================

def compliance_check_llm(state) -> dict:
    """
    Uses LLM to evaluate compliance with WHO guidelines
    based on the built compliance prompt.
    Safe for both dict and ChatState types.
    """

    # # ✅ Helper to safely extract values
    # def get_value(key, default=""):
    #     return state.get(key, default) if isinstance(state, dict) else getattr(state, key, default)

    # compliance_query = get_value("compliance_query")
    if not isinstance(state, dict):
        state = state.model_dump()

    compliance_query = state.get("compliance_prompt")

    if not compliance_query:
        raise ValueError("❌ Missing 'compliance_query' in state — cannot run compliance check.")

    # ✅ Use Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    prompt_template = ChatPromptTemplate.from_template("{query}")
    chain = prompt_template | llm

    # ✅ Run LLM
    result = chain.invoke({"query": compliance_query})
    compliance_answer = result.content.strip() if hasattr(result, "content") else str(result)
   
    return {"compliance_answer": compliance_answer}
