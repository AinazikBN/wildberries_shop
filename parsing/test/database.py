from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, UniqueConstraint

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

    # __table_args__ = (UniqueConstraint('name', 'price', name='name_price_us'),)


DATABASE_URL = 'postgresql://ainazik:1@localhost/wb_shop'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

#Создаем таблицу 
metadata = MetaData()
# metadata.create_all(bind=engine)
Product.metadata.create_all(bind=engine)


