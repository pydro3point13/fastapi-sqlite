import sqlite3 as sql

def get_connection():
    conn = sql.connect("banco.db")
    conn.row_factory = sql.Row
    return conn

def criar_tabela():
    conexao = get_connection()
    cursor = conexao.cursor()
    
    query = cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                                               nome TEXT NOT NULL
                                               """
                                        )
    affected = cursor.rowcount
    conexao.commit()
    conexao.close()
    