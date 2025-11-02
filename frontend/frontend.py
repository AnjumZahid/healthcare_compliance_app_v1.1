# frontend.py
import streamlit as st
import requests
from streamlit_tags import st_tags  # pip install streamlit-tags
import json

st.set_page_config(page_title="Healthcare Compliance App", layout="wide")

# --- Sidebar inputs ---
st.sidebar.header("📂 Patient Data Upload")
uploaded_pdf = st.sidebar.file_uploader("Medical History Documents", type=["pdf"])
uploaded_img = st.sidebar.file_uploader("Diagnostic Images (X-ray / Scan / MRI / CT)", type=["png", "jpg", "jpeg"])

# --- App Title ---
st.markdown("#### AI-Powered")
st.title("🩺 Healthcare Compliance System")

# st.title("AI-Powered Healthcare Compliance System 🩺")
st.caption("AI in Healthcare: Smarter Decisions, Safer Outcomes")

# --- Medicines input ---
medicines = st_tags(
    label="💊 Add Prescribed Medicines",
    text="Type a medicine name and press Enter",
    value=["Amoxicillin", "Paracetamol"],
    suggestions=["Metformin", "Ibuprofen", "Azithromycin", "Ciprofloxacin"],
    maxtags=50,
)

# --- Custom Questions ---
# st.subheader("Custom Compliance Questions (Optional)")
doctor_questions = st_tags(
    label="Custom Compliance Questions (Optional)",
    text="Type a question and press Enter",
    value=[],
    suggestions=[],
    maxtags=50,
)

# Preview custom questions
if doctor_questions:
    st.write("📋 Your entered questions:")
    for q in doctor_questions:
        st.write(f"- {q}")

# --- Run button ---
if st.button("Run Compliance Check"):
    if medicines and uploaded_pdf and uploaded_img:
        try:
            raw_medicine_text = ", ".join(medicines)

            files = {
                "file": (uploaded_pdf.name, uploaded_pdf, "application/pdf"),
                "image": (uploaded_img.name, uploaded_img, uploaded_img.type),
            }
            # ✅ Send manual doctor questions along with medicines
            data = {
                "raw_medicine_text": raw_medicine_text,
                "raw_manual_questions": json.dumps(doctor_questions),  # send as JSON string
            }

            with st.spinner("⚙️ Running compliance pipeline..."):
                resp = requests.post(
                    "http://127.0.0.1:8000/process/",
                    data=data,
                    files=files,
                    timeout=150,
                )

            if resp.status_code == 200:
                result = resp.json()

                questions = result.get("questions", [])
                context = result.get("context", "")
                image_text = result.get("image_text", "")
                compliance_query = result.get("compliance_query", "")
                compliance_answer = result.get("compliance_answer", "")

                # ✅ Results display
                with st.expander("📋 Generated Questions"):
                    for i, q in enumerate(questions, start=1):
                        st.write(f"{i}. {q}")

                with st.expander("📑 Retrieved Context"):
                    st.write(context)

                with st.expander("🩻 Image Findings"):
                    st.write(image_text)

                with st.expander("📝 Final Compliance Prompt"):
                    st.code(compliance_query, language="text")

                # ✅ Final Answer (always visible, styled)
                st.success("✅ Compliance flow completed successfully!")
                st.markdown("### 🏥 Final Compliance Answer")
                st.info(compliance_answer)

            else:
                st.error("❌ Error from backend: " + resp.text)

        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")

    else:
        st.warning("⚠️ Please upload both a PDF and an image, and enter at least one medicine.")
