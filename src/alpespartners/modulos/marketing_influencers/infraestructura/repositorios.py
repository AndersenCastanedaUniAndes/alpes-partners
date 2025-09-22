from datetime import datetime, timezone
from uuid import UUID
import uuid

from alpespartners.modulos.marketing_influencers.aplicacion.dto import CampañaDTO
from alpespartners.modulos.marketing_influencers.dominio.fabricas import FabricaMarketingDeInfluencers
from alpespartners.modulos.marketing_influencers.dominio.repositorios import RepositorioCampañas

from alpespartners.modulos.marketing_influencers.infraestructura.db.session import UnidadDeTrabajo
from alpespartners.modulos.marketing_influencers.infraestructura.db.models import Campaña, Outbox

from sqlalchemy import select
from sqlalchemy.orm import Session

from alpespartners.modulos.marketing_influencers.infraestructura.despachadores import Despachador
from alpespartners.modulos.marketing_influencers.infraestructura.schema.v1.eventos import CampañaCreadaPayload, EventoCampañaCreada

class RepositorioCampañasDB(RepositorioCampañas):

    def __init__(self):
        self._fabrica_campaña: FabricaMarketingDeInfluencers = FabricaMarketingDeInfluencers()

    @property
    def fabrica_campaña(self):
        return self._fabrica_campaña

    def obtener_por_id(self, id: UUID) -> Campaña:
        return Campaña()

    def obtener_todos(self) -> list[Campaña]:
        # TODO
        raise NotImplementedError

    def agregar(self, campaña_dto: CampañaDTO):
        with UnidadDeTrabajo() as uow:
            session: Session = uow.session

            existente = session.execute(
                select(Campaña).where(Campaña.creacion_comando_id == campaña_dto.id)
            ).scalar_one_or_none()
            if existente:
                print(f'La campaña con id {campaña_dto.id} ya existe. No se crea de nuevo.')

            camp_id = uuid.uuid4()
            record = Campaña(
                id=camp_id,
                nombre=campaña_dto.nombre,
                estado="CREATED",
                version=1,
                creacion_comando_id=campaña_dto.id,
            )
            session.add(record)

            # 3) Registrar evento en outbox (mismo commit)
            payload = {
                "event_id": str(uuid.uuid4()),
                "campaña_id": str(camp_id),
                "nombre": campaña_dto.nombre,
                "estado": "CREATED",
                "version": 1,
            }

            headers = {
                "aggregate": "Campaña",
                "eventType": "CampañaCreada",
                "occurredAt": datetime.now(timezone.utc).isoformat(),
                "traceId": str(campaña_dto.id),
            }

            evt = Outbox(
                aggregate_type="Campaña",
                aggregate_id=camp_id,
                type="CampañaCreada",
                payload=payload,
                headers=headers,
                status="PENDING",
                command_id=campaña_dto.id,
            )

            session.add(evt)

            Despachador().publicar_evento(campaña_dto, 'campana-creada')


    def actualizar(self, reserva: Campaña):
        # TODO
        raise NotImplementedError


    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError
