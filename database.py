import sqlite3 as sql
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = sql.connect("banco.db")
    conn.row_factory = sql.Row
    try:
        yield conn
    finally:
        conn.close()

def criar_tabela():
    with get_connection() as conexao:
        cursor = conexao.cursor()
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        nome TEXT NOT NULL
                                        )
                                        """
                                )
        conexao.commit()
    
