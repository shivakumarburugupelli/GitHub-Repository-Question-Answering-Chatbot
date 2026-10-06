# 🤖 GitHub Repository Q&A Chatbot

An AI-powered **GitHub Repository Question Answering Chatbot** that allows users to enter a GitHub repository URL and ask questions about its content.

The project uses a **Hybrid RAG (Retrieval-Augmented Generation)** approach combining **BM25 keyword retrieval** and **ChromaDB semantic retrieval** to find relevant repository information before generating an answer using a **Groq LLM**.

---

## 📌 Project Overview

Searching through a large GitHub repository manually can be time-consuming.

This project provides a simple chatbot interface where users can:

1. Enter a GitHub repository URL.
2. Load the repository content.
3. Ask questions about the repository.
4. Retrieve relevant information using hybrid search.
5. Generate an answer using an LLM.

The system uses the retrieved repository content as context, helping the LLM provide answers related to the selected repository.

---

## 🏗️ Architecture

```text
                    User
                      │
                      ▼
              ┌──────────────┐
              │   Streamlit  │
              │   Frontend   │
              └──────┬───────┘
                     │
                     │ HTTP Requests
                     ▼
              ┌──────────────┐
              │   FastAPI    │
              │   Backend    │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │  RAG Pipeline│
              └──────┬───────┘
                     │
              ┌──────┴───────┐
              ▼              ▼
        ┌──────────┐   ┌───────────┐
        │   BM25   │   │ ChromaDB  │
        │ Retrieval│   │ Semantic  │
        └────┬─────┘   │ Retrieval │
             │         └─────┬─────┘
             └──────┬────────┘
                    ▼
             Relevant Documents
                    │
                    ▼
             ┌──────────────┐
             │   Groq LLM   │
             └──────┬───────┘
                    │
                    ▼
                 Answer
                    │
                    ▼
              Streamlit UI
```

---

## 🔄 How It Works

### 1. Enter GitHub Repository

The user enters a GitHub repository URL in the Streamlit interface.

Example:

```text
https://github.com/shivakumarburugupelli/customer-churn-prediction
```

### 2. FastAPI Receives the Request

The Streamlit frontend sends the repository URL to the FastAPI backend through:

```text
POST /load
```

FastAPI then calls the RAG pipeline.

### 3. Load Repository Content

The repository content is loaded using `WebBaseLoader`.

### 4. Split Documents

The loaded content is divided into smaller chunks using:

```text
RecursiveCharacterTextSplitter
```

Current configuration:

```text
chunk_size = 500
chunk_overlap = 50
```

Chunking makes the documents easier to retrieve and process.

### 5. Hybrid Retrieval

The project uses two retrieval methods.

#### BM25

BM25 performs **keyword-based retrieval**.

For example, if the user asks:

```text
What is CustomerID?
```

BM25 looks for relevant matching terms.

#### ChromaDB

ChromaDB performs **semantic similarity search** using Hugging Face embeddings.

This allows the system to find content based on meaning, even when the exact words are different.

### 6. Combine Retrieved Documents

The results from BM25 and ChromaDB are combined.

Duplicate documents are removed before creating the final context.

### 7. Generate Answer

The retrieved repository context and the user's question are sent to the Groq LLM.

The LLM generates the final answer using the repository context.

### 8. Return Answer

FastAPI returns the answer to Streamlit, and Streamlit displays it to the user.

---

## 🧠 RAG Pipeline

```text
GitHub Repository
       │
       ▼
Document Loading
       │
       ▼
Text Splitting
       │
       ▼
   ┌───┴────┐
   ▼        ▼
 BM25    ChromaDB
   │        │
   └───┬────┘
       ▼
Combine Results
       │
       ▼
Remove Duplicates
       │
       ▼
Repository Context
       │
       ▼
    Groq LLM
       │
       ▼
     Answer
```

---

## 🛠️ Technologies Used

| Technology                         | Purpose                                |
| ---------------------------------- | -------------------------------------- |
| **Python**                         | Core programming language              |
| **Streamlit**                      | Frontend / user interface              |
| **FastAPI**                        | Backend REST API                       |
| **LangChain**                      | RAG pipeline and component integration |
| **WebBaseLoader**                  | Repository content loading             |
| **RecursiveCharacterTextSplitter** | Document chunking                      |
| **BM25**                           | Keyword-based retrieval                |
| **ChromaDB**                       | Vector/semantic retrieval              |
| **Hugging Face Embeddings**        | Convert text into embeddings           |
| **Groq**                           | Large Language Model inference         |
| **python-dotenv**                  | Environment variable management        |
| **Git & GitHub**                   | Version control and project hosting    |

---

## 📁 Project Structure

```text
github_rag/
│
├── app.py              # Streamlit frontend
│
├── main.py             # FastAPI backend
│
├── rag.py              # Hybrid RAG pipeline
│
├── .env                # API keys
│
├── requirements.txt    # Python dependencies
│
└── README.md           # Project documentation
```

---

## 🔌 API Endpoints

### GET `/`

Used to check whether the FastAPI server is running.

```text
GET /
```

Response:

```json
{
  "message": "GitHub RAG API is running"
}
```

### POST `/load`

Loads a GitHub repository.

```text
POST /load
```

Request:

```json
{
  "github_url": "https://github.com/username/repository"
}
```

### POST `/ask`

Sends a question about the loaded repository.

```text
POST /ask
```

Request:

```json
{
  "question": "What is customer churn?"
}
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/github-repository-qa-chatbot.git
```

### 2. Navigate to the project

```bash
cd github-repository-qa-chatbot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your actual API key.

**Do not upload your `.env` file to GitHub.**

Add this to `.gitignore`:

```text
.env
__pycache__/
.venv/
venv/
```

---

## ▶️ Running the Project

### Step 1 — Start FastAPI

Open the first terminal:

```bash
uvicorn main:app --reload
```

FastAPI will run at:

```text
http://127.0.0.1:8000
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Step 2 — Start Streamlit

Open a second terminal:

```bash
streamlit run app.py
```

Streamlit will run at:

```text
http://localhost:8501
```

### Step 3 — Use the chatbot

1. Open the Streamlit application.
2. Enter a GitHub repository URL.
3. Click **Load Repository**.
4. Enter a question.
5. Click **Ask**.
6. View the generated answer.

---

## 💡 Example

### Repository

```text
https://github.com/shivakumarburugupelli/customer-churn-prediction
```

### Question

```text
What is customer churn?
```

### System

```text
Question
   ↓
BM25 + ChromaDB
   ↓
Relevant repository content
   ↓
Groq LLM
   ↓
Generated answer
```

---

## 🎯 Key Features

* 🔗 GitHub repository-based question answering
* 🤖 Hybrid RAG architecture
* 🔍 BM25 keyword retrieval
* 🧠 ChromaDB semantic retrieval
* 📚 Hugging Face embeddings
* ⚡ Groq LLM inference
* 🚀 FastAPI backend
* 🖥️ Streamlit frontend
* 🔄 REST API communication
* ♻️ Duplicate document removal
* 🔐 Environment-based API key management

---

## 🚀 Future Improvements

* Support private GitHub repositories using GitHub authentication
* Use the GitHub Contents API to retrieve repository files more reliably
* Add conversation/chat history
* Add source citations for retrieved files
* Add RRF (Reciprocal Rank Fusion) for better hybrid ranking
* Support multiple programming languages and file types
* Improve repository indexing and caching
* Deploy the application to the cloud

---

## 👨‍💻 Author

**Shiva kumar Burugupelli**

GitHub: `https://github.com/shivakumarburugupelli`

---

## ⭐ Conclusion

This project demonstrates how **Generative AI, Retrieval-Augmented Generation, hybrid information retrieval, vector databases, REST APIs, and LLMs** can be combined to build a practical AI application for understanding GitHub repositories.
