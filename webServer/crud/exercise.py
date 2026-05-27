from crud.base import CRUDBase
from model.exercise import Exercise
from schema.exercise import ExerciseCreate, ExerciseUpdate


class CRUDExercise(CRUDBase[Exercise, ExerciseCreate, ExerciseUpdate]):
    def __init__(self):
        super().__init__(Exercise)
