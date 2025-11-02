from pydantic import BaseModel, Field
from typing import List, Annotated, TypedDict, Dict
from langgraph.channels import LastValue
from langgraph.graph import add_messages
import operator

class ChatState(BaseModel):
    """LangGraph state model with additive merging behavior."""
    
    # Combine multiple text updates
    # pdf_hist_path: str = Field(default="")
    pdf_hist_path: List[str] = Field(default_factory=list)   # ✅ supports multiple PDFs
    history_text: str = Field(default="")
    # history_text: Annotated[list[str], add_messages]
    image_path: str = Field(default="")
    cv_model_text: str = Field(default="")

    raw_medicine_text: str = Field(default="")
    medicine_text: List[str] = Field(default_factory=list)

    raw_manual_questions: List[str] = Field(default_factory=list)
    manual_ques: List[str] = Field(default_factory=list)
    merge_text: str = Field(default="")
    generated_llm_Qprompt: str = Field(default="")

    compliance_questions_json: Dict[str, List[str]] = Field(default_factory=dict)

    retrieved_chunks: str = Field(default="")

    fda_info: str = Field(default="")

    compliance_prompt: str = Field(default="")

    medicine_query: str = Field(default="")   # single drug extracted from medicine_text

    # fda_info: str = Field(default="")        # FDA info fetched from MCP

    compliance_answer: str = Field(default="")  # final LLM compliance output

    
    
