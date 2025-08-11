import logging
from pathlib import Path
from config.config import config
from core.file_dispatcher import FileDispatcher
from data_processing.parsers import (
    PDFParser, ExcelParser, XMLParser, EDIParser
)
from data_processing.normalization import DataNormalizer
from data_processing.db_handler import save_document

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.parsers = {
            ".pdf": PDFParser,
            ".xlsx": ExcelParser,
            ".xls": ExcelParser,
            ".xml": XMLParser,
            ".edi": EDIParser
        }
    
    def process_file(self, file_path: Path):
        """Обрабатывает один файл"""
        try:
            logger.info(f"Processing file: {file_path.name}")
            
            # Определяем тип документа
            doc_type = FileDispatcher.get_document_type(file_path)
            if doc_type == "unknown":
                logger.warning(f"Unknown document type for file: {file_path.name}")
                return False
            
            # Выбираем парсер
            parser_class = self.parsers.get(file_path.suffix.lower())
            if not parser_class:
                logger.error(f"No parser for extension: {file_path.suffix}")
                return False
            
            # Парсим документ
            parser = parser_class(file_path)
            raw_data = parser.parse()
            
            # Валидируем данные
            if not parser.validate(raw_data):
                logger.error(f"Validation failed for: {file_path.name}")
                return False
            
            # Нормализуем данные
            normalized_data = DataNormalizer.normalize(raw_data, doc_type)
            normalized_data = DataNormalizer.calculate_totals(normalized_data)
            
            # Сохраняем в БД
            doc_id = save_document(file_path, doc_type, normalized_data)
            logger.info(f"Document processed successfully. ID: {doc_id}")
            
            return True
        except Exception as e:
            logger.exception(f"Error processing file {file_path.name}: {str(e)}")
            return False