import sys, os, asyncio, json 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langgraph.graph import StateGraph, START, END
from state.chat_state import ChatState
from nodes.history_node import extract_history
from nodes.image_node import extract_image
from nodes.prescription_node import extract_med
from nodes.prompts_node import merge_all_text, generate_llm_Qprompt, build_compliance_prompt
from nodes.retrieval_node import retrieve_chunks
from nodes.compliance_node import generate_llm_compliance_json, compliance_check_llm
from nodes.fda_node import fda_node

from pydantic import BaseModel, Field, ValidationError
from typing import List, Annotated, TypedDict, Dict
from langgraph.channels import LastValue
import operator

# --- Graph definition ---
graph = StateGraph(ChatState)

# --- Add nodes ---
graph.add_node("extr_history", extract_history)
graph.add_node("extr_image", extract_image)
graph.add_node("extr_med", extract_med)
graph.add_node("merge_text", merge_all_text)
graph.add_node("gen_llm_Qprompt", generate_llm_Qprompt)
graph.add_node("gen_llm_Qjson", generate_llm_compliance_json)
graph.add_node("retrieved_chunksk", retrieve_chunks)

# New nodes
graph.add_node("fda_lookup", fda_node)
graph.add_node("build_compliance_prompt", build_compliance_prompt)
graph.add_node("compliance_check_llm", compliance_check_llm)


# --- Define flow ---
graph.add_edge(START, "extr_history")
graph.add_edge(START, "extr_image")
graph.add_edge(START, "extr_med")
graph.add_edge("extr_med", "fda_lookup")
graph.add_edge("extr_history", "merge_text")
graph.add_edge("extr_image", "merge_text")
graph.add_edge("extr_med", "merge_text")
graph.add_edge("merge_text", "gen_llm_Qprompt")
graph.add_edge("gen_llm_Qprompt", "gen_llm_Qjson")
graph.add_edge("gen_llm_Qjson", "retrieved_chunksk")
graph.add_edge("retrieved_chunksk", "build_compliance_prompt")
graph.add_edge("build_compliance_prompt", "compliance_check_llm")
graph.add_edge("compliance_check_llm", END)

# Compile app
graph_app = graph.compile()

