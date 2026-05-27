from crud.base import CRUDBase
from model.patient import Patient
from schema.patient import PatientCreate, PatientUpdate


class CRUDPatient(CRUDBase[Patient, PatientCreate, PatientUpdate]):
    def __init__(self):
        super().__init__(Patient)
