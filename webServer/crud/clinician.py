from crud.base import CRUDBase
from model.clinician import Clinician
from schema.clinician import ClinicianCreate, ClinicianUpdate


class CRUDClinician(CRUDBase[Clinician, ClinicianCreate, ClinicianUpdate]):
    def __init__(self):
        super().__init__(Clinician)