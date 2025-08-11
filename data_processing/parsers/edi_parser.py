import xml.etree.ElementTree as ET
from pathlib import Path
from .base_parser import BaseParser

class EDIParser(BaseParser):
    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.document_type = "invoice"
    
    def parse(self) -> dict:
        try:
            # Для упрощения будем использовать XML-парсер
            # В реальном проекте здесь будет использоваться bots-edi
            return self._parse_as_xml()
        except Exception as e:
            print(f"EDI parsing error: {str(e)}")
            return {}
    
    def _parse_as_xml(self) -> dict:
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            
            # Простая конвертация XML в словарь
            return self._xml_to_dict(root)
        except Exception as e:
            print(f"XML parsing error: {str(e)}")
            return {}
    
    def _xml_to_dict(self, element):
        result = {}
        for child in element:
            if len(child) > 0:
                result[child.tag] = self._xml_to_dict(child)
            else:
                result[child.tag] = child.text
        return result