from pydantic import BaseModel
from datetime import datetime
from typing import List


class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class AppointmentBase(BaseModel):
    patient_first_name: str
    patient_last_name: str
    date_time: datetime
    kind: str


class Doctor(DoctorBase):
    id: int
    appointments: List[AppointmentBase] = []
