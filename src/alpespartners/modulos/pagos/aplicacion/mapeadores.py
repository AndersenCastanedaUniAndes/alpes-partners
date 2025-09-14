from alpespartners.seedwork.aplicacion.dto import Mapeador as AppMap
from alpespartners.seedwork.dominio.repositorios import Mapeador as RepMap
from alpespartners.modulos.pagos.aplicacion.dto import PagoDTO, ComisionDTO
from alpespartners.modulos.pagos.dominio.entidades import Pago, Comision
from alpespartners.modulos.pagos.dominio.objetos_valor import ValorPago, MetadatosPago
from datetime import datetime
from typing import Optional

class MapeadorPago(RepMap):
    def entidad_a_dto(self, entidad: Pago) -> PagoDTO:
        return PagoDTO(
            pago_id=entidad.pago_id,
            usuario_id=entidad.usuario_id,
            nombre=entidad.nombre,
            email=entidad.email,
            monto=entidad.monto,
            moneda=entidad.moneda,
            numero_tarjeta=None,  # Nunca se mapea desde entidad
            expiracion=None,
            cvv=None,
            fecha_programada=entidad.fecha_programada
        )

    def dto_a_entidad(self, dto: PagoDTO) -> Pago:
        return Pago(
            pago_id=dto.pago_id,
            usuario_id=dto.usuario_id,
            nombre=dto.nombre,
            email=dto.email,
            monto=dto.monto,
            moneda=dto.moneda,
            fecha_programada=dto.fecha_programada
        )

class MapeadorComision(RepMap):
    def entidad_a_dto(self, entidad: Comision) -> ComisionDTO:
        return ComisionDTO(
            pago_id=entidad.pago_id,
            monto_comision=entidad.monto_comision,
            moneda=entidad.moneda
        )

    def dto_a_entidad(self, dto: ComisionDTO) -> Comision:
        return Comision(
            pago_id=dto.pago_id,
            monto_comision=dto.monto_comision,
            moneda=dto.moneda
        )

class MapeadorPagoDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> PagoDTO:
        return PagoDTO(
            pago_id=externo.get('pago_id', ''),
            usuario_id=externo.get('usuario_id'),
            nombre=externo.get('nombre'),
            email=externo.get('email'),
            monto=externo.get('monto', 0.0),
            moneda=externo.get('moneda', 'COP'),
            numero_tarjeta=externo.get('numero_tarjeta'),
            expiracion=externo.get('expiracion'),
            cvv=externo.get('cvv'),
            fecha_programada=externo.get('fecha_programada')
        )

    def dto_a_externo(self, dto: PagoDTO) -> dict:
        return dto.__dict__

class MapeadorComisionDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> ComisionDTO:
        return ComisionDTO(
            pago_id=externo.get('pago_id', ''),
            monto_comision=externo.get('monto_comision', 0.0),
            moneda=externo.get('moneda', 'COP')
        )

    def dto_a_externo(self, dto: ComisionDTO) -> dict:
        return dto.__dict__
