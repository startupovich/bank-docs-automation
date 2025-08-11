from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from config.config import config

Base = declarative_base()

class ProcessedDocument(Base):
    __tablename__ = 'processed_documents'
    
    id = Column(Integer, primary_key=True)
    file_name = Column(String(255), nullable=False)
    document_type = Column(String(50), nullable=False)
    supplier = Column(String(255))
    customer = Column(String(255))
    total_amount = Column(Float)
    currency = Column(String(3), default="RUB")
    processing_time = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    raw_data = Column(JSON)  # Для хранения оригинальных данных

engine = create_engine(config.DB_URL)
Session = sessionmaker(bind=engine)

def init_db():
    """Инициализирует базу данных"""
    Base.metadata.create_all(engine)

def save_document(file_path, document_type, normalized_data):
    """Сохраняет документ в базу данных"""
    session = Session()
    try:
        doc = ProcessedDocument(
            file_name=file_path.name,
            document_type=document_type,
            supplier=normalized_data.get("supplier"),
            customer=normalized_data.get("customer"),
            total_amount=normalized_data.get("total_amount", 0),
            currency=normalized_data.get("currency", "RUB"),
            processing_time=normalized_data.get("processing_time"),
            raw_data=normalized_data
        )
        session.add(doc)
        session.commit()
        return doc.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()