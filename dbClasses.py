from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


base = declarative_base()

#category
class cat(base):
    __tablename__ = 'cats'
    id = Column(Integer, primary_key = True, autoincrement = True)
    cat = Column(String(20), nullable=False)


#subcategory
class subcat(base):
    __tablename__ = 'subcats'
    id = Column(Integer, primary_key = True, autoincrement = True)
    subcat = Column(String(30), nullable = False)
    cat = Column(Integer, ForeignKey('cats.id'), nullable = False)

    rel = relationship("cat")


#shipping mode
class shippingmode(base):
    __tablename__ = 'shippingmode'
    id = Column(Integer, primary_key = True, autoincrement = True)
    mode = Column(String(25))


#segment (customer type)
class segments(base):
    __tablename__ = 'segments'
    id = Column(Integer, primary_key = True, autoincrement = True)
    seg = Column(String(20))


#sales info
class sales(base):
    __tablename__ = 'sales'
    rowID = Column(Integer, primary_key = True, autoincrement = True)
    city = Column(String(25))
    state = Column(String(20))
    zipcode = Column(String(8))
    subcat = Column(Integer, ForeignKey('subcats.id'))
    salesTotal = Column(Float)
    profit = Column(Float)
    retailprice = Column(Float)
    highPrice = Column(Boolean)
    qty = Column(Integer)
    discount = Column(Float)
    shipMode = Column(Integer, ForeignKey('shippingmode.id'))
    cat = Column(Integer, ForeignKey('cats.id'))
    segment = Column(Integer, ForeignKey('segments.id'))

    cat_rel = relationship("cat")
    ship_rel = relationship("shippingmode")
    seg_rel = relationship("segments")
    subcat_rel = relationship("subcat")