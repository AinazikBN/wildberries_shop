from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    brand = Column(String)
    rating = Column(Float)
    volume = Column(String)
    supplier_id = Column(Integer)
    image_links = Column(String)

    __table_args__ = (UniqueConstraint('name', 'price', name='name_price_us'),)