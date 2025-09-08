from datetime import datetime
from alpespartners.seedwork.aplicacion.dto import Mapeador as AppMap
from alpespartners.seedwork.dominio.objetos_valor import Monto
from alpespartners.modulos.marketing_influencers.dominio.entidades import Campaña
from alpespartners.seedwork.dominio.repositorios import Mapeador as RepMap
from .dto import CampañaDTO

class MapeadorCampañaDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> CampañaDTO:
        campaña_dto = CampañaDTO(
            id=externo.get("id"),
            nombre=externo.get("nombre"),
            producto=externo.get("producto"),
            presupuesto=externo.get("presupuesto"),
            moneda=externo.get("moneda"),
            marca=externo.get("marca"),
            influencers_ids=externo.get("influencers_ids", []),
            conversiones=externo.get("conversiones", [])
        )
        return campaña_dto

    def dto_a_externo(self, dto: CampañaDTO) -> dict:
        return dto.__dict__


class MapeadorCampaña(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'


    def obtener_tipo(self) -> type:
        return Campaña.__class__


    def entidad_a_dto(self, entidad: Campaña) -> CampañaDTO:
        return CampañaDTO(
            id=entidad.id,
            nombre=entidad.nombre,
            producto=entidad.producto,
            presupuesto=entidad.presupuesto.valor,
            moneda=entidad.presupuesto.moneda,
            marca=entidad.marca,
            influencers_ids=entidad.influencers_ids,
            conversiones=entidad.conversiones
        )


    def dto_a_entidad(self, dto: CampañaDTO) -> Campaña:
        return Campaña(
            id=dto.id,
            nombre=dto.nombre,
            producto=dto.producto,
            presupuesto=Monto(
                valor=dto.presupuesto,
                moneda=dto.moneda
            ),
            marca=dto.marca,
            influencers_ids=dto.influencers_ids,
            conversiones=dto.conversiones
        )
