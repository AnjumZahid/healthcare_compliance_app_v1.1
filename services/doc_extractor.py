from pathlib import Path
import os, fitz, easyocr
from langchain_community.document_loaders import PyPDFLoader

# Initialize OCR once here
reader = easyocr.Reader(['en'], verbose=False)

def extract_text_from_file(file_path: str) -> str:
    """
    Detect file type (PDF or image) and extract text accordingly.
    """
    ext = Path(file_path).suffix.lower()
    text_content = ""

    if ext == ".pdf":
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            if docs and any(doc.page_content.strip() for doc in docs):
                return "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            print(f"⚠️ PyPDFLoader failed: {e}")

        # OCR fallback
        pdf_document = fitz.open(file_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            pix = page.get_pixmap()
            image_path = f"temp_page_{page_num}.png"
            pix.save(image_path)

            result = reader.readtext(image_path)
            page_text = " ".join([res[1] for res in result])
            text_content += f"\n{page_text}"
            os.remove(image_path)

    elif ext in [".jpg", ".jpeg", ".png"]:
        result = reader.readtext(file_path)
        text_content = " ".join([res[1] for res in result])
    else:
        text_content = f"Unsupported file type: {ext}"

    return text_content.strip()


# def extract_from_multiple(files: list) -> str:
def extract_from_multiple(files: list) -> str:
    """
    Process multiple files (PDFs or images) and combine all text into one variable.
    """
    all_text = ""
    # files = ["C:/Users/Admin/Downloads/Medi/pdf1.pdf"]
    for file_path in files:
        file_text = extract_text_from_file(file_path)
        all_text += f"\n\n---- File: {Path(file_path).name} ----\n\n{file_text}"
    return all_text.strip()

