from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import os

rag_directory = os.path.join(os.getcwd(), "rag")

DATA_SOURCE_FILE_PATH = os.path.join(rag_directory, "data", "emoji.csv")
VECTOR_DB_FAISS_PATH = os.path.join(rag_directory, "stores", "faiss")

class VectorDB:
  """
    FAISS Vector Database

    @docs: https://python.langchain.com/v0.2/docs/integrations/vectorstores/faiss/
  """
  db: FAISS = None

  def __init__(self):
    if self.db == None:
      self._load_local()

  def _ingestion(self):
    """Setups the vector database by ingesting documents into the vectorstore"""
    # Indexing: Load
    loader = CSVLoader(file_path=DATA_SOURCE_FILE_PATH, encoding='utf-8')

    documents = loader.load()

    # Indexing: Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(documents)

    # Indexing: Store
    embeddings = HuggingFaceEmbeddings(
      model_name="sentence-transformers/all-MiniLM-L6-v2",
      model_kwargs={'device': 'cpu'}
    )

    db = FAISS.from_documents(splits, embeddings)
    self.db = db

    # Save
    db.save_local(VECTOR_DB_FAISS_PATH)

  def _load_local(self):
    embeddings = HuggingFaceEmbeddings(
      model_name="sentence-transformers/all-MiniLM-L6-v2",
      model_kwargs={'device': 'cpu'}
    )

    self.db = FAISS.load_local(VECTOR_DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

  def query(self, query: str) -> list[Document]:
    """Queries"""
    retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    docs = retriever.invoke(query)
    return docs
  
  def get_retriever(self):
    retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    return retriever