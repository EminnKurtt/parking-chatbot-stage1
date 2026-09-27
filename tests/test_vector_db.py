from database.vector_db import VectorDatabase

def test_vector_db_initialization():
    vdb = VectorDatabase()
    assert vdb.vector_store is not None

def test_retriever():
    vdb = VectorDatabase()
    retriever = vdb.get_static_retriever()
    docs = retriever.invoke("Where is the parking?")
    assert len(docs) > 0
    assert "123 Main Street" in docs[0].page_content