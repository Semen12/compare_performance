from pydantic import BaseModel, Field

# Базовая модель для термина. Используется для вывода данных.
class TermBase(BaseModel):
    term: str
    definition: str

# Модель для создания нового термина.
# Указываем, что поля должны быть непустыми.
class TermCreate(BaseModel):
    term: str = Field(..., min_length=1, description="Ключевое слово")
    definition: str = Field(..., min_length=1, description="Определение термина")

# Модель для обновления существующего термина.
# Позволяем менять только определение.
class TermUpdate(BaseModel):
    definition: str = Field(..., min_length=1, description="Новое определение")