from pydantic import BaseModel,ConfigDict


class OutletBase(BaseModel):
    name: str
    address: str
    operation_hour: str
    latitude: float
    longitude: float


class OutletView(OutletBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

