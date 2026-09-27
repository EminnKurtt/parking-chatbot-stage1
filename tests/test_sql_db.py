from database.sql_db import SQLDatabase

def test_sql_db_initialization():
    db = SQLDatabase()
    assert db.db_path is not None

def test_get_dynamic_info():
    db = SQLDatabase()
    info = db.get_dynamic_info("price")
    assert "Price:" in info