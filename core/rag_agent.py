from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from database.sql_db import SQLDatabase
from database.vector_db import VectorDatabase
from guardrails.pii_filter import PIIGuardrail
from core.config import settings

class ParkingRAGAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=settings.OPENAI_API_KEY)
        self.sql_db = SQLDatabase()
        self.vector_db = VectorDatabase()
        self.guardrail = PIIGuardrail()
        self.retriever = self.vector_db.get_static_retriever()

    def _get_combined_context(self, query: str) -> str:
        """Retrieves static data from Vector DB and dynamic data from SQL DB."""
        # 1. Static Data (Vector DB)
        static_docs = self.retriever.invoke(query)
        static_context = "\n".join([doc.page_content for doc in static_docs])
        
        # 2. Dynamic Data (SQL DB)
        dynamic_context = self.sql_db.get_dynamic_info(query)
        
        return f"Static Information:\n{static_context}\n\nDynamic Information:\n{dynamic_context}"

    def generate_response(self, user_input: str) -> str:
        # 1. Input Guardrails
        if self.guardrail.contains_sensitive_data(user_input):
            return "Security Alert: Sensitive data (e.g., credit card, SSN) detected. Please do not share personal information."

        # 2. RAG Pipeline
        prompt = ChatPromptTemplate.from_template(
            "You are a helpful parking assistant. Answer the user's question based on the context below.\n"
            "If the user wants to make a reservation, ask for their Name, Car Number, and Reservation Period.\n\n"
            "Context:\n{context}\n\nQuestion: {question}"
        )

        chain = (
            {"context": self._get_combined_context, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        response = chain.invoke(user_input)
        
        # 3. Output Guardrails (ensure LLM didn't hallucinate PII)
        return self.guardrail.analyze_and_mask(response)