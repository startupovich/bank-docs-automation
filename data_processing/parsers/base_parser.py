from abc import ABC, abstractmethod
from pathlib import Path
from core.document_types import DOCUMENT_TYPES

class BaseParser(ABC):
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.document_type = None
        
    @abstractmethod
    def parse(self) -> dict:
        """Основной метод парсинга, должен возвращать словарь с данными"""
        pass
    
    def validate(self, data: dict) -> bool:
        """Валидация данных через Pydantic"""
        if not self.document_type or self.document_type not in DOCUMENT_TYPES:
            return False
        
        try:
            DOCUMENT_TYPES[self.document_type](**data)
            return True
        except Exception:
            return False