from fastapi import FastAPI
from schemas import DoctorBase, AppointmentBase
from fastapi.exceptions import HTTPException

app = FastAPI()

doctors = [
    {"id": 1, "first_name": "John", "last_name": "Rambo", "email": 'firstblood@clinic.com'},
    {"id": 2, "first_name": "Jane", "last_name": "Gi", "email": "GiJane@clinic.com"},
    {"id": 3, "first_name": "Alicia", "last_name": "keys", "email":"newyork@clinic.com"},
    {"id": 4, "first_name": "Michael", "last_name": "Jackson", "email": "shamon@clinic.com"},
    {"id": 5, "first_name": "Elvis", "last_name": "Presley", "email": "hounddog@gmail.com"},
]

appointments = [
    {"id": 1, "doctor_id": 1, "patient_first_name": "Jimmy", "patient_last_name": "Carr", "date_time": "2021-01-01T12:00:00", "kind": "New Patient"},
    {"id": 2, "doctor_id": 2, "patient_first_name": "Timmy", "patient_last_name": "Thompson", "date_time": "2021-01-01T12:00:00", "kind": "Follow-up"},
    {"id": 3, "doctor_id": 3, "patient_first_name": "Kendrick", "patient_last_name": "Lamar", "date_time": "2021-01-01T12:00:00", "kind": "New Patient"},
]


@app.get("/doctors")
def get_doctors():
    return doctors


@app.get("/doctors/{doctor_id}/appointments")
def get_doctor_appointments(doctor_id: int):
    return [appointment for appointment in appointments if appointment["doctor_id"] == doctor_id]



@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    global appointments
    appointments = [appointment for appointment in appointments if appointment["id"] != appointment_id]
    return {"message": "apointment deleted"}


@app.post("/doctors/{doctor_id}/appointments")
def add_appointment(doctor_id: int, appointment: AppointmentBase):
    global appointments
    if not any(doctor["id"] == doctor_id for doctor in doctors):
        raise HTTPException(status_code=400, detail="Doctor does not exist")
    if appointment.date_time.minute not in [0, 15, 30, 45]:
        raise HTTPException(status_code=400, detail="Appointments can only start at 15 minute intervals")
    if len([a for a in appointments if a['doctor_id'] == doctor_id and a['date_time'] == appointment.date_time]) >= 3:
        raise HTTPException(status_code=400, detail="No more than 3 appointments can be added with the same time for a given doctor")
    appointment_id = max([a["id"] for a in appointments]) + 1
    new_appointment = appointment.dict()
    new_appointment["id"] = appointment_id
    new_appointment["doctor_id"] = doctor_id
    appointments.append(new_appointment)
    return new_appointment



@app.get("/")
def read_root():
    return {"Hello": "World"}
