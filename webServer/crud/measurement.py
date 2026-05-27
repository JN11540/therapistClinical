from crud.base import CRUDBase
from model.measurement import Measurement
from schema.measurement import MeasurementCreate, MeasurementUpdate


class CRUDMeasurement(CRUDBase[Measurement, MeasurementCreate, MeasurementUpdate]):
    def __init__(self):
        super().__init__(Measurement)
