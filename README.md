🏥 Healthcare Compliance App v1.1

MVP Prototype for Healthcare Compliance Checking
Now upgraded with parallel LangGraph workflows — enabling faster, more efficient compliance processing by running independent extraction and analysis nodes simultaneously.

🚀 What’s New in v1.1

✅ Parallel Workflow Execution
Instead of sequential execution, independent modules such as patient history, image extraction, and medicine analysis now run in parallel. This significantly reduces response time and improves throughput.

✅ Optimized LangGraph Orchestration
The new graph structure supports concurrent node execution, enabling faster results while maintaining state consistency.

✅ Refined Compliance Pipeline
FDA/WHO data querying, local RAG retrieval, and compliance report generation are now streamlined into an optimized workflow.


⚙️ Tech Stack
Component	Description
LangGraph	Workflow orchestration (parallel processing in v1.1)
LangChain (optional)	Utilities for chaining operations
MCP (Model Context Protocol)	Remote querying (FDA / WHO APIs)
RAG (Retrieval-Augmented Generation)	Local compliance document QA
FastAPI	Backend API services
Streamlit	Frontend doctor interface
FAISS	Local vector database for compliance storage
Python 3.10+	Core programming language
Pytest	Unit testing framework

📌 Features (v1.1)

📤 Upload & process patient history, prescriptions, and diagnostic scans

🧠 Extract medicines, text, and image insights in parallel

🌐 Query FDA/WHO APIs using MCP

📚 Retrieve compliance knowledge via RAG + FAISS

🤖 Generate AI-powered compliance reports

📊 Interactive Streamlit dashboard for doctors

⚡ Faster performance through parallel LangGraph execution

![parallel work flow](https://github.com/user-attachments/assets/ab668fbe-de45-4117-9cca-0e42ca7617bd)


🧭 How It Works:

Parallel start: History, image, and medicine extraction run simultaneously.

Merge stage: Their outputs are combined for unified processing.

Sequential flow: LLM generates questions → retrieves context → performs compliance check.

Result: Doctor receives an optimized, AI-verified compliance report.

📂 Project Structure
healthcare_compliance_app_v1.1/
│── backend/          # FastAPI backend (handles processing & LangGraph pipeline)
│── frontend/         # Streamlit UI for doctors
│── graphs/           # LangGraph pipeline definition (parallel flow in v1.1)
│── nodes/            # Modular nodes (history, image, FDA, compliance, etc.)
│── services/         # MCP server, RAG vectorstore, extractors
│── state/            # Shared state across parallel branches
│── config/           # Paths & environment configurations
│── data/             # Models, PDFs, and sample data
│── database/         # FAISS index for compliance retrieval
│── tests/            # Unit tests for each module
│── test_data/        # Sample test files (images, PDFs)
│── requirements.txt  # Dependencies
│── .gitignore        # Ignored files and virtual environments


🩺 Workflow Overview
Doctor uploads:

📑 Patient history (PDF)

🩻 Diagnostic scan (image)

💊 Prescribed medicines

❓ Optional custom compliance questions

System performs:

Parallel extraction of text, image, and medicine data

Merged analysis for context generation

FDA/WHO queries via MCP

RAG-based document retrieval

Compliance report generation

Doctor reviews:

🧾 Generated questions

📚 Retrieved context

🩺 Image findings

✅ Final compliance recommendation


▶️ Running the App
# 1. Clone Repository
git clone https://github.com/AnjumZahid/healthcare_compliance_app_v1.1.git
cd healthcare_compliance_app_v1.1

# 2. Create Environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Start Backend
uvicorn backend.main:app --reload

# 5. Launch Frontend
streamlit run frontend/app.py


📘 Summary

Healthcare Compliance App v1.1 introduces parallel LangGraph execution — allowing faster, more efficient, and modular healthcare compliance checking. It combines the power of LangGraph, MCP, RAG, and AI-driven medical analysis for real-time compliance intelligence.
