import xml.etree.ElementTree as ET
from pathlib import Path
from .base_parser import BaseParser
from core.file_dispatcher import FileDispatcher
from core.document_types import InvoiceItem

class XMLParser(BaseParser):
    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.document_type = FileDispatcher.get_document_type(file_path)
    
    def parse(self) -> dict:
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            
            # Извлекаем основные реквизиты
            doc_data = {
                "number": root.find('number').text if root.find('number') is not None else "UNKNOWN",
                "date": root.find('date').text if root.find('date') is not None else "1970-01-01",
                "supplier": root.find('supplier').text if root.find('supplier') is not None else "",
                "customer": root.find('customer').text if root.find('customer') is not None else "",
                "items": []
            }
            
            # Извлекаем позиции
            total_amount = 0.0
            for item in root.findall('item'):
                name = item.find('name').text if item.find('name') is not None else ""
                quantity = float(item.find('quantity').text) if item.find('quantity') is not None else 0.0
                price = float(item.find('price').text) if item.find('price') is not None else 0.0
                total = quantity * price
                total_amount += total
                
                doc_data["items"].append({
                    "name": name,
                    "quantity": quantity,
                    "price": price,
                    "total": total
                })
            
            doc_data["total_amount"] = total_amount
            
            return doc_data
        except Exception as e:
            print(f"XML parsing error: {str(e)}")
            return {}