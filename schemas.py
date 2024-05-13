from pydantic import BaseModel


class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    email: str
