from fastapi import FastAPI, HTTPException, Body
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
import sqlite3 as sql
import database
import uvicorn

app = FastAPI()

class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=3)
    model_config = ConfigDict(extra='forbid')
    
    @field_validator("nome")
    @classmethod
    def validateName(cls, value):
        if not value.strip():
            raise HTTPException(
                status_code=400,
                detail="Nome inválido"
                )
        return value.strip()
# -----------------------------------------------
@app.get("/")
def root():
    return { "message": "API funcionando" }

@app.get("/saudacao")
def saudar(nome: Optional[str] = None):
    if nome:
        return {  "message": f"Olá, {nome}!" }
    return  { "message": "Olá, anônimo!" }

@app.post("/usuario", status_code=201)
def register(user: UsuarioCreate = Body()):
    conexao = None
    try:
        conexao = database.get_connection()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (nome) VALUES (?)",
                       (user.nome,))
        last_id = cursor.lastrowid
        conexao.commit()
        return {
            "id": last_id,
            "nome": user.nome
            }
    except sql.OperationalError as e:
        raise HTTPException(
            status_code=500,
            detail="Erro no servidor. Tente novamente mais tarde..."
            )
    finally:
        if conexao is not None:
            conexao.close()

@app.get("/usuarios")
def get_user(id: Optional[int] = None):
    conexao = None
    try:
        conexao = database.get_connection()
        cursor = conexao.cursor()
        if id is not None:
            cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
            user = cursor.fetchone()
            if user is not None:
                return {
                    "id": user['id'],
                    "nome": user['nome']
                    }
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado"
                )
        else:
            cursor.execute("SELECT * FROM usuarios")
            users = cursor.fetchall()
            if users:
                return users
            raise HTTPException(
                status_code=404,
                detail="Sem usuários no database"
                )
    except sql.OperationalError as e:
        raise HTTPException(
            status_code=500,
            detail="Erro interno. Tente novamente mais tarde..."
    )
    finally:
        if conexao is not None:
            conexao.close()
    
@app.put("/usuarios/{id}")
def update_user(id: int,
                user: UsuarioCreate = Body()):
    conexao = None
    try:
        conexao = database.get_connection()
        cursor = conexao.cursor()
        user_exists = cursor.execute("""SELECT * FROM usuarios
        WHERE id = ?""", (id,)).fetchone()
        if user_exists:
            cursor.execute("""UPDATE usuarios
                SET nome = ?
                WHERE id = ?""", (user.nome, id))
            conexao.commit()
            return {
                "id": id,
                "nome": user.nome
                }
        raise HTTPException(status_code=404,
            detail="Este user não existe no banco"
            )
    except sql.OperationalError as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error."
            )
    finally:
        if conexao is not None:
            conexao.close()
        

@app.delete("/usuarios/{id}")
def remove(id: int):
    conexao = None
    try:
        conexao = database.get_connection()
        cursor = conexao.cursor()
        cursor.execute("""DELETE FROM usuarios
            WHERE id = ?""", (id,))
        affected = cursor.rowcount
        if affected > 0:
            conexao.commit()
            return { "message": f"User {id} deletado" }
        raise HTTPException(
            status_code=404,
            detail=f"Usuário com id {id} não encontrado"
            )
    finally:
        if conexao is not None:
            conexao.close()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)