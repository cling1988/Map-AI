import os
from typing import Annotated

from fastapi import APIRouter, Body
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import pandas as pd
from fastapi.responses import JSONResponse

from app import crud
from app.db.schemas import OutletBase, OutletView
from app.db.database import get_db
from app.llm.agent import query

router = APIRouter(prefix="/api", )


@router.get("/outlets", response_model=list[OutletView])
def get_outlets(db: Session = Depends(get_db)):
    items = crud.get_outlets(db)
    return items


@router.get("/create/outlet", )
def create_outlets(db: Session = Depends(get_db)):
    csv_file = os.getenv('SOURCE_CSV_FILE')
    print(csv_file)
    df = pd.read_csv(csv_file, keep_default_na=False)
    for index, row in df.iterrows():
        item = OutletBase(name=row["Outlet Name"],
                          address=row["Address"],
                          operation_hour=row["Operation Hour"],
                          latitude=row["Latitude"],
                          longitude=row["Longitude"])
        crud.create_outlets(db, item)

    return {"status": "ok"}


@router.post("/query")
def query_llm(question: Annotated[str, Body(embed=True)]):
    llm_response = query(question)

    return JSONResponse(content=jsonable_encoder(llm_response))
