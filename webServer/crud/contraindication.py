from crud.base import CRUDBase
from model.contraindication import Contraindication
from schema.contraindication import ContraindicationCreate, ContraindicationUpdate


class CRUDContraindication(CRUDBase[Contraindication, ContraindicationCreate, ContraindicationUpdate]):
    def __init__(self):
        super().__init__(Contraindication)
