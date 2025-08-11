from core.document_types import DOCUMENT_TYPES
from datetime import datetime

class DataNormalizer:
    @staticmethod
    def normalize(data: dict, doc_type: str) -> dict:
        """
        Приводит данные к стандартному формату
        """
        if doc_type not in DOCUMENT_TYPES:
            return data
        
        # Создаем экземпляр модели для автоматической нормализации
        try:
            model = DOCUMENT_TYPES[doc_type](**data)
            normalized = model.dict()
            
            # Добавляем системные поля
            normalized["processing_time"] = datetime.utcnow().isoformat()
            normalized["original_doc_type"] = doc_type
            
            return normalized
        except Exception as e:
            print(f"Normalization error: {str(e)}")
            return data
    
    @staticmethod
    def calculate_totals(data: dict) -> dict:
        """
        Пересчитывает итоговые суммы, если нужно
        """
        if "items" in data and "total_amount" in data:
            calculated_total = sum(
                item.get("total", 0) or item.get("quantity", 0) * item.get("price", 0)
                for item in data["items"]
            )
            
            # Корректируем разницу
            if abs(calculated_total - data["total_amount"]) > 0.01:
                data["total_amount"] = round(calculated_total, 2)
                data["amount_corrected"] = True
        
        return data