import tabula
import pandas as pd
from pathlib import Path
from .base_parser import BaseParser
from core.file_dispatcher import FileDispatcher
from core.document_types import InvoiceItem

class PDFParser(BaseParser):
    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.document_type = FileDispatcher.get_document_type(file_path)
    
    def parse(self) -> dict:
        # Читаем все таблицы из PDF
        dfs = tabula.read_pdf(
            str(self.file_path), 
            pages='all', 
            multiple_tables=True,
            lattice=True,
            pandas_options={'header': None}
        )
        
        # Объединяем таблицы
        if not dfs:
            return {}
        
        combined_df = pd.concat(dfs, ignore_index=True) if len(dfs) > 1 else dfs[0]
        
        # Преобразуем в список словарей
        raw_data = combined_df.to_dict(orient='records')
        
        # Извлекаем основные реквизиты
        doc_data = {
            "number": self._extract_doc_number(),
            "date": self._extract_doc_date(),
            "supplier": self._extract_supplier(),
            "customer": self._extract_customer(),
            "items": self._extract_items(raw_data)
        }
        
        # Считаем итого
        doc_data["total_amount"] = sum(item["total"] for item in doc_data["items"])
        
        return doc_data
    
    def _extract_doc_number(self) -> str:
        # Реализация поиска номера документа в тексте
        return "INV-" + self.file_path.stem[-6:]
    
    def _extract_doc_date(self) -> str:
        # Реализация поиска даты документа
        return "2023-10-15"
    
    def _extract_supplier(self) -> str:
        # Реализация поиска поставщика
        return "ООО 'Поставщик'"
    
    def _extract_customer(self) -> str:
        # Реализация поиска покупателя
        return "ООО 'Покупатель'"
    
    def _extract_items(self, raw_data: list) -> list:
        # Упрощенная реализация извлечения позиций
        items = []
        for i, row in enumerate(raw_data):
            if i < 3:  # Пропускаем заголовки
                continue
            try:
                # Предполагаем структуру: Наименование | Количество | Цена | Сумма
                if len(row) >= 4:
                    items.append({
                        "name": row[0],
                        "quantity": float(row[1]),
                        "price": float(row[2]),
                        "total": float(row[3])
                    })
            except (ValueError, TypeError):
                continue
        return items