from fastapi import FastAPI, HTTPException, Body
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
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
    conexao = database.get_connection()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO usuarios (nome) VALUES (?)",
                   (user.nome,))
    last_id = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return {
                    "id": last_id,
                    "nome": user.nome
                }

@app.get("/usuarios")
def get_user(id: Optional[int] = None):
    conexao = database.get_connection()
    cursor = conexao.cursor()
    if id:
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
    elif id is not None:
        cursor.execute("SELECT * FROM usuarios")
        users = cursor.fetchall()
        if users is not None:
            return users
        raise HTTPException(
            status_code=404,
            detail="Sem usuários no database"
            )
    raise HTTPException(
        status_code=400,
        detail="Id não informado"
        )
    conexao.close()
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)