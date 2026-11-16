from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Livro(BaseModel):
    titulo: str
    autor: str

livros = [
    {"id": 1, "titulo": "Dom Casmurro", "autor": "Machado de Assis"},
    {"id": 2, "titulo": "O Cortiço", "autor": "Aluísio Azevedo"},
    {"id": 3, "titulo": "Iracema", "autor": "José de Alencar"}
]

@app.get("/")
def inicio():
    return {"mensagem": "API de Livros funcionando!"}

@app.get("/livros")
def listar_livros():
    return livros

@app.get("/livros/{id}")
def buscar_livro(id: int):
    for livro in livros:
        if livro["id"] == id:
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado")

@app.post("/livros", status_code=201)
def adicionar_livro(livro: Livro):
    novo_id = max((l["id"] for l in livros), default=0) + 1
    novo_livro = {
        "id": novo_id,
        "titulo": livro.titulo,
        "autor": livro.autor
    }
    livros.append(novo_livro)
    return novo_livro

@app.put("/livros/{id}")
def atualizar_livro(id: int, dados: Livro):
    for livro in livros:
        if livro["id"] == id:
            livro["titulo"] = dados.titulo
            livro["autor"] = dados.autor
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado")

@app.delete("/livros/{id}")
def excluir_livro(id: int):
    for livro in livros:
        if livro["id"] == id:
            livros.remove(livro)
            return {"mensagem": "Livro excluido com sucesso"}
    raise HTTPException(status_code=404, detail="Livro não encontrado")
