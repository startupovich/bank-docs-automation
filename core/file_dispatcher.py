import os
import re
from pathlib import Path
from config.config import config

class FileDispatcher:
    @staticmethod
    def get_document_type(file_path: Path) -> str:
        """
        Определяет тип документа по имени файла
        """
        filename = file_path.name.lower()
        
        if re.search(r'счет|invoice', filename):
            return "invoice"
        elif re.search(r'акт|act', filename):
            return "act"
        elif re.search(r'накладн|waybill', filename):
            return "waybill"
        else:
            # Попробуем определить по расширению
            ext = file_path.suffix.lower()
            if ext == '.pdf':
                return "invoice"  # По умолчанию для PDF
            elif ext in ['.xls', '.xlsx']:
                return "act"
            elif ext == '.xml':
                return "waybill"
            elif ext == '.edi':
                return "invoice"
            else:
                return "unknown"

    @staticmethod
    def move_file(file_path: Path, success: bool = True):
        """
        Перемещает обработанный файл в соответствующую директорию
        """
        target_dir = config.PROCESSED_DIR if success else config.FAILED_DIR
        target_dir.mkdir(exist_ok=True, parents=True)
        
        new_path = target_dir / file_path.name
        file_path.rename(new_path)
        return new_path