import json
from pathlib import Path
from typing import Dict

# 1. Настройка путей (оставляем как было, это правильно)
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent 
DB_FILE = PROJECT_ROOT / "glossary.json"

def get_db() -> Dict[str, str]:
    """
    Загружает данные и преобразует список словарей в один словарь.
    JSON: [{"term": "A", "definition": "B"}, ...] 
    Python: {"A": "B", ...}
    """
    print(f"Попытка открыть файл: {DB_FILE}")
    
    if not DB_FILE.exists():
        return {}

    with open(DB_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        if not content:
            return {}
        
        # 1. Загружаем "сырой" список из JSON
        raw_list = json.loads(content)
        
        # 2. Превращаем список в словарь для удобного поиска O(1) и редактирования
        # Было: list[dict], Стало: dict[str, str]
        return {item["term"]: item["definition"] for item in raw_list}

def save_db(database: Dict[str, str]) -> None:
    """
    Преобразует словарь обратно в список и сохраняет в JSON.
    """
    # 1. Превращаем словарь обратно в формат, ожидаемый JSON-файлом
    # Было: {"A": "B"}, Стало: [{"term": "A", "definition": "B"}]
    list_to_save = [
        {"term": term, "definition": definition} 
        for term, definition in database.items()
    ]

    # 2. Сохраняем
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(list_to_save, f, ensure_ascii=False, indent=4)