import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from config import (
    UPLOAD_FOLDER,
    CHROMA_DB_DIR,
    EMBEDDING_MODEL,
)


def process_documents(uploaded_files):
    """
    Process uploaded PDF documents and create a Chroma vector database.
    """

    try:

        print("\n" + "=" * 60)
        print("🚀 STEP 1: process_documents() called")

        # Create folders
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(CHROMA_DB_DIR, exist_ok=True)

        print("✅ STEP 2: Folders created")

        all_documents = []

        # ------------------------------------
        # Save PDFs and Load Documents
        # ------------------------------------
        print("📄 STEP 3: Saving and loading PDFs")

        for uploaded_file in uploaded_files:

            print(f"➡️ Processing: {uploaded_file.name}")

            file_path = os.path.join(
                UPLOAD_FOLDER,
                uploaded_file.name
            )

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            print("✅ PDF Saved")

            loader = PyPDFLoader(file_path)

            documents = loader.load()

            print(f"✅ Pages Loaded: {len(documents)}")

            all_documents.extend(documents)

        print(f"📚 Total Pages Loaded: {len(all_documents)}")

        # ------------------------------------
        # Split Documents
        # ------------------------------------
        print("✂️ STEP 4: Splitting Documents")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(all_documents)

        print(f"✅ Total Chunks Created: {len(chunks)}")

        if len(chunks) == 0:
            print("❌ ERROR: No chunks created.")
            return False

        print("\nFirst Chunk Preview:\n")
        print(chunks[0].page_content[:300])

        # ------------------------------------
        # Load Embedding Model
        # ------------------------------------
        print("🤖 STEP 5: Loading Embedding Model")

        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        print("✅ Embedding Model Loaded")

        # Test embedding
        test_embedding = embeddings.embed_query("Hello World")

        print(f"✅ Embedding Dimension: {len(test_embedding)}")

        # ------------------------------------
        # Create Chroma DB
        # ------------------------------------
        print("🗂️ STEP 6: Creating Chroma Database")

        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DB_DIR,
        )

        print("✅ Vector Database Created Successfully")
        print("=" * 60)

        return True

    except Exception as e:

        print("\n❌ ERROR OCCURRED")
        print(type(e).__name__)
        print(e)

        return False