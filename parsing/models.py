from pydantic import BaseModel, validator
from typing import List, Optional


class Price(BaseModel):
    basic: int
    product: int
    total: Optional[float]
    logistics: int

    @validator('total', pre=True, always=True)
    def convert_total_price(cls, total):
        if total is not None:
            return total / 100
        return None


class Size(BaseModel):
    price: Optional[Price] = None 


class Item(BaseModel):
    id: int 
    name: str 
    brand: str
    supplierId: int
    sizes: Optional[List[Size]] = None
    sale: Optional[int] = None
    rating: Optional[int] = None
    volume: Optional[int] = None
    pics: Optional[int] = None
    root: Optional[int] = None
    image_links: Optional[str] = None



class Items(BaseModel):
    products: List[Item]
    



