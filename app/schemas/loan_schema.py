from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.user_schema import UserResponse
from app.schemas.device_schema import DeviceResponse

class LoanCreate(BaseModel):
    user_id: int
    device_id: int

class LoanUpdate(BaseModel):
    status: Optional[str] = None
    return_date: Optional[datetime] = None

class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    model_config = ConfigDict(from_attributes=True)

class LoanDetailResponse(BaseModel):
    loan_id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime]
    user: UserResponse
    device: DeviceResponse

    model_config = ConfigDict(from_attributes=True)