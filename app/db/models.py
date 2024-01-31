from sqlalchemy import Column, Integer, String, Float

from app.db.database import Base


class Outlet(Base):
    __tablename__ = "outlet"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    operation_hour = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
