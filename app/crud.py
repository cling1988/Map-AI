from sqlalchemy.orm import Session

from app.db import models
from app.db import schemas


def get_outlets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Outlet).offset(skip).limit(limit).all()


def create_outlets(db: Session, item: schemas.OutletBase):
    db_item = models.Outlet(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
