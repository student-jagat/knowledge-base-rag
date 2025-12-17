from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from backend.vector_store import get_vector_store
from langchain_community.vectorstores import FAISS
import os

def get_rag_chain():
    """Creates the RAG chain."""
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
    
    template = """Answer the question based only on the following context:
    {context}
    
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # Simple retriever that doesn't fail if empty
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists("./data/faiss_index"):
        vector_store = FAISS.load_local("./data/faiss_index", embeddings, allow_dangerous_deserialization=True)
        retriever = vector_store.as_retriever()
    else:
         # Return empty retriever-like if no index
        class EmptyRetriever:
            def invoke(self, q): return []
        retriever = EmptyRetriever()

    
    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain, retriever

def query_rag(question: str):
    """Queries the RAG pipeline."""
    chain, retriever = get_rag_chain()
    
    # Retrieve docs separately to return sources
    docs = retriever.invoke(question)
    sources = list(set([doc.metadata.get("source", "Unknown") for doc in docs]))
    
    answer = chain.invoke(question)
    
    return answer, sources
