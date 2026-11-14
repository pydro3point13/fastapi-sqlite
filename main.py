from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return { "message": "API funcionando" }

@app.get("/saudacao")
def saudar(nome: str):
    if nome:
        return {  "message": f"Olá, {nome}!" }
    return  { "message": "Olá, anônimo!" }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)