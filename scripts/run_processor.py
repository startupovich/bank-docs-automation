import time
import logging
from pathlib import Path
from config.config import config
from core.file_dispatcher import FileDispatcher
from core.document_processor import DocumentProcessor

# Настройка логирования
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting document processing service")
    
    # Создаем директории, если их нет
    config.INPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    config.FAILED_DIR.mkdir(parents=True, exist_ok=True)
    
    processor = DocumentProcessor()
    
    logger.info(f"Monitoring directory: {config.INPUT_DIR}")
    
    while True:
        try:
            # Получаем список файлов для обработки
            files_to_process = list(config.INPUT_DIR.glob('*'))
            
            if not files_to_process:
                time.sleep(config.POLL_INTERVAL)
                continue
            
            for file_path in files_to_process:
                if file_path.is_file():
                    success = processor.process_file(file_path)
                    FileDispatcher.move_file(file_path, success)
        
        except KeyboardInterrupt:
            logger.info("Shutting down by user request")
            break
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            time.sleep(config.POLL_INTERVAL * 2)

if __name__ == "__main__":
    main()