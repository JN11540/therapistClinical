from crud.base import CRUDBase
from model.treatment import Treatment
from schema.treatment import TreatmentCreate, TreatmentUpdate


class CRUDTreatment(CRUDBase[Treatment, TreatmentCreate, TreatmentUpdate]):
    def __init__(self):
        super().__init__(Treatment)
