
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import  Chroma
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
bm25_retriever = None

vector_retriever = None
def load_repository(github_url):

    global bm25_retriever
    global vector_retriever

    loader = WebBaseLoader(github_url)

    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    splits = splitter.split_documents(documents)

    bm25_retriever=BM25Retriever.from_documents(splits)

    bm25_retriever.k=5
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        collection_name="github_repo"
    )
    vector_retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
    return "Repository loaded successfully!"


def ask_question(question):

    global bm25_retriever
    global vector_retriever

    if bm25_retriever is None or vector_retriever is None:
          return "Please load a GitHub repository first."

    bm25_docs = bm25_retriever.invoke(question)
    vector_docs = vector_retriever.invoke(question)

    
    all_docs = (bm25_docs + vector_docs)
    unique_docs = {}

    for doc in all_docs:

        unique_docs[doc.page_content] = doc
    final_docs = list(unique_docs.values())
    context = "\n\n".join(doc.page_content for doc in final_docs)
    prompt = ChatPromptTemplate.from_template(
        """You are a helpful GitHub Repository Question Answering Assistant.Answer the user's question using only the repository context below.
        If the answer is not available in thecontext, say:"I could not find the answer
        in the repository."Repository Context:{context}User Question:{question} Answer:""")


    llm = ChatGroq(
        model="openai/gpt-oss-20b",temperature=0)
    final_prompt = prompt.invoke(
        {
            "context": context,
            "question": question
        }
    )
    response=llm.invoke(final_prompt)
    return response.content



