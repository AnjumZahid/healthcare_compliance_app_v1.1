from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os
import time
from config.settings import PDF_DIR

PDF_PATH2 = os.path.join(PDF_DIR, "WHO_Good__rational_Prescribing.pdf")

load_dotenv()

# def process_pdf(pdf_path: str):
def process_pdf():
    loader = PyPDFLoader(PDF_PATH2)
    docs = loader.load()
    return docs

    # Split into chunks
def chunk_doc(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)

    # Print chunks in backend terminal
    print(f"Total Chunks: {len(all_splits)}\n")
    for i, chunk in enumerate(all_splits[:5]):  # show only first 5 chunks
        print(f"---- Chunk {i+1} ----")
        print(chunk.page_content[:300])  # first 300 chars
        print("----------------------\n")

    return all_splits

def vector_store(chunks, batch_size=10, max_retries=3):
    print("vector_store() CALLED")

    # Initialize embeddings
    print("Initializing embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    print("Embeddings initialized!")

    save_dir = "faiss_store"
    os.makedirs(save_dir, exist_ok=True)

    # 🔹 Try to load existing FAISS index
    if os.path.exists(os.path.join(save_dir, "index.faiss")):
        vector_store = FAISS.load_local(
            save_dir,
            embeddings,
            allow_dangerous_deserialization=True
        )
        print("📂 Existing FAISS index loaded!")

        # Count how many vectors already exist
        existing_count = vector_store.index.ntotal
        print(f"✅ Existing vectors in FAISS: {existing_count}")

        # Calculate how many batches already processed
        start_batch = existing_count // batch_size
    else:
        vector_store = None
        start_batch = 0
        print("🆕 No existing FAISS found, starting fresh.")

    # Process remaining chunks in batches
    for i in range(start_batch * batch_size, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        texts = [doc.page_content for doc in batch]
        metadatas = [doc.metadata for doc in batch]

        retries = 0
        while retries < max_retries:
            try:
                # Embed this batch
                batch_embeddings = embeddings.embed_documents(texts)

                # Create FAISS index for this batch
                batch_store = FAISS.from_texts(
                    texts,
                    embeddings,
                    metadatas=metadatas
                )

                # Merge into main FAISS store
                if vector_store is None:
                    vector_store = batch_store
                else:
                    vector_store.merge_from(batch_store)

                print(f"✅ Processed batch {i//batch_size+1} with {len(batch)} chunks")
                break  # success → exit retry loop

            except Exception as e:
                retries += 1
                print(f"⚠️ Error on batch {i//batch_size+1}: {e} (Retry {retries}/{max_retries})")
                time.sleep(5 * retries)  # exponential backoff

        else:
            print(f"❌ Failed batch {i//batch_size+1} after {max_retries} retries, skipping...")

        # ⏳ Add delay after every 5 batches to avoid rate-limit (429)
        if (i // batch_size + 1) % 5 == 0:
            print("⏳ Waiting 90 seconds to avoid rate limit...")
            time.sleep(90)

        # 🔹 Save progress after each batch
        vector_store.save_local(save_dir)

    print(f"\n💾 FAISS index saved to: {save_dir}/")

    # Reload FAISS index (to test persistence)
    reloaded_store = FAISS.load_local(save_dir, embeddings, allow_dangerous_deserialization=True)
    print("FAISS index reloaded successfully!")

    return vector_store


user_input = input("lets_start: ")

if user_input == "go":

    docs1 = process_pdf()
    chunks = chunk_doc(docs1)
    vector_store(chunks)


# ============================================================================

# def vector_store(chunks, batch_size=10, max_retries=3):
#     print("vector_store() CALLED")

#     # Initialize embeddings
#     print("Initializing embeddings...")
#     embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
#     print("Embeddings initialized!")

#     # Initialize empty FAISS index
#     vector_store = None  

#     # Process chunks in batches
#     for i in range(0, len(chunks), batch_size):
#         batch = chunks[i:i+batch_size]
#         texts = [doc.page_content for doc in batch]
#         metadatas = [doc.metadata for doc in batch]

#         retries = 0
#         while retries < max_retries:
#             try:
#                 # Embed this batch
#                 batch_embeddings = embeddings.embed_documents(texts)

#                 # Create FAISS index for this batch
#                 batch_store = FAISS.from_texts(
#                     texts,
#                     embeddings,
#                     metadatas=metadatas
#                 )

#                 # Merge into main FAISS store
#                 if vector_store is None:
#                     vector_store = batch_store
#                 else:
#                     vector_store.merge_from(batch_store)

#                 print(f"✅ Processed batch {i//batch_size+1} with {len(batch)} chunks")
#                 break  # success → exit retry loop

#             except Exception as e:
#                 retries += 1
#                 print(f"⚠️ Error on batch {i//batch_size+1}: {e} (Retry {retries}/{max_retries})")
#                 time.sleep(5 * retries)  # exponential backoff: 5s, 10s, 15s

#         else:
#             print(f"❌ Failed batch {i//batch_size+1} after {max_retries} retries, skipping...")

#         # ⏳ Add delay after every 5 batches to avoid rate-limit (429)
#         if (i // batch_size + 1) % 5 == 0:
#             print("⏳ Waiting 90 seconds to avoid rate limit...")
#             time.sleep(90)

#     # Save FAISS index to directory
#     save_dir = "faiss_store"
#     os.makedirs(save_dir, exist_ok=True)
#     vector_store.save_local(save_dir)
#     print(f"\n💾 FAISS index saved to: {save_dir}/")

#     # Reload FAISS index (to test persistence)
#     reloaded_store = FAISS.load_local(save_dir, embeddings, allow_dangerous_deserialization=True)
#     print("FAISS index reloaded successfully!")

#     return vector_store