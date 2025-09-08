from dataclasses import dataclass, field
import uuid
from datetime import datetime

@dataclass
class Entidad:
    # id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(default_factory=uuid.uuid4, init=False, repr=False, hash=True)
    fecha_creacion: datetime = field(default_factory=datetime.now, init=False)
    fecha_actualizacion: datetime = field(default_factory=datetime.now, init=False)

    @classmethod
    def siguiente_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        print("El id ya fue asignado, no se puede modificar.")
