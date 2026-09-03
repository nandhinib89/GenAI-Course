import streamlit as st
from dotenv import load_dotenv
import hashlib

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

st.title("RAG App with PDF Uploader")


# --------------------------------------------------
# PDF uploader
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF file",
    type=["pdf"]
)


# --------------------------------------------------
# Process uploaded PDF
# --------------------------------------------------

if uploaded_file is not None:

    # Create a unique ID for the uploaded PDF
    file_bytes = uploaded_file.getvalue()
    file_id = hashlib.md5(file_bytes).hexdigest()

    # Check whether this is a new PDF
    if st.session_state.get("file_id") != file_id:

        # Remember the new file
        st.session_state.file_id = file_id

        # Remove old vector database
        st.session_state.pop("vector_db", None)

        with st.spinner("Building vector database..."):

            # Save uploaded PDF temporarily
            with open("uploaded.pdf", "wb") as f:
                f.write(file_bytes)

            # Load PDF
            loader = PyPDFLoader("uploaded.pdf")
            documents = loader.load()

            # Check for readable text
            text = "\n".join(
                doc.page_content for doc in documents
            ).strip()

            if not text:
                st.error(
                    "This PDF does not contain readable text. "
                    "Please upload a PDF containing text."
                )
                st.stop()

            # Split into chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_documents(documents)

            # Create embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # Create FAISS vector database
            vector_db = FAISS.from_documents(
                chunks,
                embeddings
            )

            # Store vector DB in session state
            st.session_state.vector_db = vector_db

        st.success("Vector database is ready!")


# --------------------------------------------------
# Question section
# --------------------------------------------------

if "vector_db" in st.session_state:

    st.subheader("Ask a question about your PDF")

    # Different widget key for each uploaded PDF
    question = st.text_input(
        "Enter your question:",
        key=f"question_{st.session_state.file_id}"
    )

    if question:

        # Retrieve relevant chunks
        docs = st.session_state.vector_db.similarity_search(
            question,
            k=3
        )

        # Combine retrieved chunks
        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        # Prompt
        prompt = ChatPromptTemplate.from_template("""
You are a helpful RAG assistant.

Answer the user's question only using the given context.

If the answer is not available in the context, say:
"I don't know from the provided document."

Context:
{context}

Question:
{question}

Answer:
""")

        # OpenAI model
        llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0
        )

        # LangChain chain
        chain = prompt | llm

        # Generate answer
        response = chain.invoke({
            "context": context,
            "question": question
        })

        st.subheader("Answer")
        st.write(response.content)