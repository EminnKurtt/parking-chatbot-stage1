from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from core.config import settings

class VectorDatabase:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.vector_store = self._initialize_vector_db()

    def _initialize_vector_db(self):
        """Creates a FAISS vector store with static parking information."""
        static_data = [
            "The parking location is at 123 Main Street, Downtown.",
            "To book a spot, you need to provide your name, car number, and reservation period.",
            "We accept cash and credit cards.",
            "Our parking facility has EV charging stations.",
            "General information: The parking space is covered and has 24/7 security."
        ]
        return FAISS.from_texts(static_data, self.embeddings)

    def get_static_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": 2})