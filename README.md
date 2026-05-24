# PDF RAG Chatbot

An AI-powered PDF RAG (Retrieval-Augmented Generation) Chatbot built using LangChain, Mistral AI, FAISS, Streamlit, HuggingFace Embeddings, and SQLite.

This project allows users to upload PDF documents and ask questions directly from the uploaded content. The chatbot understands document context, supports follow-up questions, maintains chat history, and provides a smooth conversational experience similar to ChatGPT.

---

# Project Overview

Traditional chatbots answer questions using general knowledge.
This project uses the RAG (Retrieval-Augmented Generation) architecture, which means the chatbot first retrieves relevant information from uploaded PDF documents and then generates accurate answers using an LLM (Large Language Model).

This allows the chatbot to:

* answer document-specific questions
* understand context
* support follow-up questions
* maintain conversation memory
* provide more accurate and contextual responses

The application is built with a clean Streamlit UI and stores chat history permanently using SQLite database.

---

# Features

## PDF Upload

Users can upload their own PDF documents and chat with them.

## Conversational RAG

The chatbot remembers previous questions and supports follow-up conversations.

## Multiple Chat Sessions

Users can create and manage multiple chat conversations.

## Persistent Chat History

All chats are stored using SQLite database and remain available even after refreshing the browser.

## Streaming Responses

Answers are generated with typing effect similar to ChatGPT.

## Human-Friendly Error Handling

Instead of technical Python errors, users see understandable messages.

## Delete Individual Chats

Users can permanently delete specific chat conversations.

## Clear All Chats

Complete chat history can be cleared from settings.

## Beautiful UI

Clean and simple Streamlit-based interface.

## Dynamic Greetings

Displays Good Morning, Good Afternoon, or Good Evening according to system time.

---

# Screenshots

## Home Page

![Home Page](screenshots/home.png)

---

## PDF Upload

![PDF Upload](screenshots/upload.png)

---

## Chat Interface

![Chat Interface](screenshots/chat.png)

---

## Chat History Sidebar

![Sidebar](screenshots/sidebar.png)


# Tech Stack

| Technology                           | Purpose                               |
| ------------------------------------ | ------------------------------------- |
| Python                               | Backend Programming                   |
| Streamlit                            | Web Application UI                    |
| RAG (Retrieval-Augmented Generation) | AI Retrieval + Response Architecture  |
| LangChain                            | RAG Pipeline and Conversational Chain |
| Mistral AI                           | Large Language Model (LLM)            |
| FAISS                                | Vector Database for Similarity Search |
| HuggingFace Embeddings               | Text Embedding Generation             |
| SQLite                               | Persistent Chat Storage               |
| PyPDF                                | PDF Text Extraction                   |
| Sentence Transformers                | Semantic Embedding Model              |

---

# How RAG Works In This Project

This project follows the Retrieval-Augmented Generation pipeline.

## Step 1: Upload PDF

The user uploads a PDF document using the Streamlit interface.

---

## Step 2: Extract Text

LangChain's `PyPDFLoader` extracts text content from the uploaded PDF.

---

## Step 3: Split Text Into Chunks

Large documents are divided into smaller chunks using:

```python id="v2m8qp"
RecursiveCharacterTextSplitter
```

This improves retrieval quality and embedding generation.

Example:

* Chunk Size = 500
* Chunk Overlap = 50

---

## Step 4: Create Embeddings

Each text chunk is converted into vector embeddings using:

```python id="x7k4rt"
sentence-transformers/all-MiniLM-L6-v2
```

These embeddings capture semantic meaning of text.

---

## Step 5: Store Embeddings In FAISS

FAISS vector database stores all embeddings for fast similarity search.

When user asks a question:

* FAISS searches most relevant chunks
* retrieves related information from document

---

## Step 6: Send Context To LLM

Retrieved chunks + user question are sent to Mistral AI.

Mistral AI generates a contextual answer using:

* uploaded document data
* previous conversation history

---

## Step 7: Display Streaming Response

The answer appears word-by-word with typing effect for better user experience.

---

## Step 8: Store Chat In SQLite

Each chat conversation is permanently stored inside SQLite database.

This allows:

* reopening old chats
* chat persistence after refresh
* multi-chat support

---

# Project Structure

```bash id="a4m9zp"
PDF-RAG-Chatbot/
│
├── app.py
├── main.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── domestic_travel.pdf
├── foreign_travel.pdf
│
├── venv/
```

---

# Installation Guide

## Step 1: Clone Repository

```bash id="w8q2rm"
git clone https://github.com/Suryanandankumar2003/PDF-RAG-Chatbot.git
```

---

## Step 2: Move To Project Directory

```bash id="k5m1xt"
cd PDF-RAG-Chatbot
```

---

## Step 3: Create Virtual Environment

### Windows

```bash id="f3q7vp"
python -m venv venv
```

### Linux / Mac

```bash id="u9x4rt"
python3 -m venv venv
```

---

## Step 4: Activate Virtual Environment

### Windows

```bash id="d2m8qp"
venv\Scripts\activate
```

### Linux / Mac

```bash id="p6k1vr"
source venv/bin/activate
```

After activation you will see:

```bash id="x4m7zt"
(venv)
```

in terminal.

---

## Step 5: Install Dependencies

```bash id="n7q2xp"
pip install -r requirements.txt
```

This installs:

* LangChain
* Streamlit
* FAISS
* HuggingFace
* Mistral AI SDK
* PyPDF
* SQLite dependencies

---

## Step 6: Create Environment File

Create a file named:

```bash id="m9k4qt"
.env
```

Add your Mistral API key:

```env id="z5x1rm"
mistral_api_key=YOUR_API_KEY
```

You can get API key from:

https://console.mistral.ai/

---

## Step 7: Run Application

```bash id="t8q3vp"
streamlit run app.py
```

---

## Step 8: Open In Browser

Streamlit automatically opens browser.

Usually:

```text id="r1m7zk"
http://localhost:8501
```

---

# How To Use

## Upload PDF

Upload any PDF document using upload button.

---

## Ask Questions

Example:

* What is travel reimbursement policy?
* What are leave rules?
* Explain foreign travel process.

---

## Follow-Up Questions

The chatbot remembers previous context.

Example:

User:

```text id="g4k9qp"
What is leave policy?
```

Follow-Up:

```text id="b7m2rt"
What about sick leave?
```

---

# Database Functionality

SQLite database stores:

* chat names
* user messages
* assistant responses

This enables:

* persistent history
* multiple chats
* reopening old chats
* deleting chats

Database file:

```bash id="h3q8vx"
chat_history.db
```

---

# Error Handling

The application handles:

* invalid PDFs
* empty answers
* API failures
* unexpected errors

Instead of technical errors, users see understandable messages.

---

# Future Improvements

* Source citations
* Authentication system
* Docker support
* Cloud deployment
* Voice assistant
* Chat export
* Persistent vector database
* Dark/Light themes

---

# Author

Suryanandan Kumar

GitHub:
https://github.com/Suryanandankumar2003

---

# License

This project is licensed under the MIT License.
