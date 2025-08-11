from pydantic import BaseModel, Field, validator
from datetime import date
from typing import List, Optional

class InvoiceItem(BaseModel):
    name: str
    quantity: float
    price: float
    unit: Optional[str] = "шт"
    total: float
    
    @validator('total', pre=True, always=True)
    def calculate_total(cls, v, values):
        if 'quantity' in values and 'price' in values:
            return round(values['quantity'] * values['price'], 2)
        return v

class Invoice(BaseModel):
    document_type: str = "invoice"
    number: str
    date: date
    supplier: str
    customer: str
    items: List[InvoiceItem]
    total_amount: float
    currency: str = "RUB"
    
    class Config:
        schema_extra = {
            "example": {
                "number": "INV-2023-001",
                "date": "2023-10-15",
                "supplier": "ООО 'Поставщик'",
                "customer": "ООО 'Покупатель'",
                "items": [
                    {"name": "Товар 1", "quantity": 10, "price": 100.0},
                    {"name": "Товар 2", "quantity": 5, "price": 250.0}
                ],
                "total_amount": 2250.0
            }
        }

class Act(Invoice):
    document_type: str = "act"

class Waybill(Invoice):
    document_type: str = "waybill"
    shipper: str
    consignee: str
    vehicle_number: Optional[str]

DOCUMENT_TYPES = {
    "invoice": Invoice,
    "act": Act,
    "waybill": Waybill
}