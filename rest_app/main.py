from typing import List
from fastapi import FastAPI, HTTPException, status

# Импортируем наши модули
from . import db
from .models import TermBase, TermCreate, TermUpdate

# Создаем экземпляр FastAPI
app = FastAPI(
    title="API для Глоссария",
    description="Простой сервис для управления словарем терминов.",
    version="1.0.0",
)

# --- Операции CRUD ---

@app.get("/terms", response_model=List[TermBase], summary="Получить все термины")
def get_all_terms():
    """
    Возвращает список всех терминов и их определений.
    """
    database = db.get_db()
    return [{"term": term, "definition": definition} for term, definition in database.items()]

@app.get("/terms/{term}", response_model=TermBase, summary="Получить конкретный термин")
def get_term(term: str):
    """
    Возвращает определение для указанного термина.
    """
    database = db.get_db()
    if term not in database:
        raise HTTPException(status_code=404, detail=f"Термин '{term}' не найден")
    return TermBase(term=term, definition=database[term])

@app.post("/terms", response_model=TermBase, status_code=status.HTTP_201_CREATED, summary="Добавить новый термин")
def create_term(term_in: TermCreate):
    """
    Добавляет новый термин в глоссарий.
    """
    database = db.get_db()
    if term_in.term in database:
        raise HTTPException(status_code=409, detail=f"Термин '{term_in.term}' уже существует")
    
    database[term_in.term] = term_in.definition
    db.save_db(database)
    return TermBase(term=term_in.term, definition=term_in.definition)

@app.put("/terms/{term}", response_model=TermBase, summary="Обновить термин")
def update_term(term: str, term_update: TermUpdate):
    """
    Обновляет определение существующего термина.
    """
    database = db.get_db()
    if term not in database:
        raise HTTPException(status_code=404, detail=f"Термин '{term}' не найден")
        
    database[term] = term_update.definition
    db.save_db(database)
    return TermBase(term=term, definition=term_update.definition)

@app.delete("/terms/{term}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить термин")
def delete_term(term: str):
    """
    Удаляет термин из глоссария.
    """
    database = db.get_db()
    if term not in database:
        raise HTTPException(status_code=404, detail=f"Термин '{term}' не найден")
        
    del database[term]
    db.save_db(database)