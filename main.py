from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_mistralai import ChatMistralAI

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = ChatMistralAI(
    api_key=os.getenv("mistral_api_key"),
    model="mistral-large-latest"
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)


@st.cache_resource
def create_qa_chain(pdf_path):

    loader = PyPDFLoader(pdf_path)

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    split_docs = text_splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(
        split_docs,
        embedding_model
    )

    retriever = vectorstore.as_retriever()

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )

    return qa_chain


def get_answer(qa_chain, query):

    try:

        response = qa_chain.invoke(
            {
                "question": query
            }
        )

        answer = response["answer"]

        answer = answer.replace("**", "")

        if not answer.strip():

            return (
                "I could not find relevant information "
                "in the uploaded document."
            )

        return answer

    except Exception:

        return (
            "Sorry, I could not understand your question. "
            "It may be outside the uploaded document."
        )