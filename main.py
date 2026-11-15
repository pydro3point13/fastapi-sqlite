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
    if id:
        conexao = database.get_connection()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        user = cursor.fetchone()
        if user:
            return {
                "id": user['id'],
                "nome": user['nome']
                }
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
            )
    raise HTTPException(
        status_code=400,
        detail="Id não informado"
        )
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)