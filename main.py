from fastapi import FastAPI
from typing import Optional
import database
import uvicorn

app = FastAPI()

# database.criar_tabela() deixei em comentario pra nao tentar criar toda vez q rodar a api

@app.get("/")
def root():
    return { "message": "API funcionando" }

@app.get("/saudacao")
def saudar(nome: Optional[str] = None):
    if nome:
        return {  "message": f"Olá, {nome}!" }
    return  { "message": "Olá, anônimo!" }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)