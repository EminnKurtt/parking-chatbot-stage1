from core.rag_agent import ParkingRAGAgent

def test_rag_agent_initialization():
    agent = ParkingRAGAgent()
    assert agent.llm is not None

def test_rag_agent_sensitive_data_block():
    agent = ParkingRAGAgent()
    response = agent.generate_response("Here is my SSN 000-12-3456")
    assert "Security Alert" in response