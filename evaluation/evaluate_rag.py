from sklearn.metrics import precision_score, recall_score
from core.rag_agent import ParkingRAGAgent

def evaluate_rag_system():
    """
    Mock evaluation of the RAG system.
    In a real scenario, you would have a dataset of questions and expected answers.
    """
    agent = ParkingRAGAgent()
    
    # Mock test dataset
    test_queries = [
        "What are your working hours?",
        "Where are you located?",
        "How much does it cost?"
    ]
    
    # Mock ground truth (1 if relevant info retrieved, 0 if not)
    y_true = [1, 1, 1] 
    y_pred = []
    
    for query in test_queries:
        context = agent._get_combined_context(query)
        # Simple heuristic: if context contains relevant keywords, predict 1
        if any(keyword in context.lower() for keyword in ["hours", "street", "price"]):
            y_pred.append(1)
        else:
            y_pred.append(0)
            
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    
    print(f"Evaluation Results:")
    print(f"Precision: {precision:.2f}")
    print(f"Recall@K: {recall:.2f}")
    print("Note: In production, use a larger dataset and LLM-as-a-judge for evaluation.")

if __name__ == "__main__":
    evaluate_rag_system()