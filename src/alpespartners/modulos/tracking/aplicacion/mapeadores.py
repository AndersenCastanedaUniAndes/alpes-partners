from alpespartners.seedwork.aplicacion.mapeadores import Mapeador
from alpespartners.modulos.tracking.aplicacion.dto import ImpresionDTO, ConversionDTO
from alpespartners.modulos.tracking.dominio.entidades import Impresion, Conversion
from alpespartners.modulos.tracking.dominio.objetos_valor import Metadatos, UserAgent, IPAddress, Referrer, TipoConversion, ValorConversion
from datetime import datetime


class MapeadorImpresion(Mapeador):
    def entidad_a_dto(self, entidad: Impresion) -> ImpresionDTO:
        return ImpresionDTO(
            id=entidad.id,
            campaña_id=entidad.campaña_id,
            influencer_id=entidad.influencer_id,
            usuario_id=entidad.usuario_id,
            tipo_evento=entidad.tipo_evento,
            user_agent=entidad.metadatos.user_agent.valor,
            ip_address=entidad.metadatos.ip_address.direccion,
            referrer=entidad.metadatos.referrer.url,
            timestamp=entidad.timestamp.isoformat()
        )

    def dto_a_entidad(self, dto: ImpresionDTO) -> Impresion:
        metadatos = Metadatos(
            user_agent=UserAgent(dto.user_agent),
            ip_address=IPAddress(dto.ip_address),
            referrer=Referrer(dto.referrer),
            timestamp=dto.timestamp
        )
        
        return Impresion(
            id=dto.id,
            campaña_id=dto.campaña_id,
            influencer_id=dto.influencer_id,
            usuario_id=dto.usuario_id,
            tipo_evento=dto.tipo_evento,
            metadatos=metadatos,
            timestamp=datetime.fromisoformat(dto.timestamp)
        )


class MapeadorConversion(Mapeador):
    def entidad_a_dto(self, entidad: Conversion) -> ConversionDTO:
        return ConversionDTO(
            id=entidad.id,
            campaña_id=entidad.campaña_id,
            influencer_id=entidad.influencer_id,
            usuario_id=entidad.usuario_id,
            tipo_conversion=entidad.tipo_conversion.value,
            valor=entidad.valor.valor,
            moneda=entidad.valor.moneda,
            user_agent=entidad.metadatos.user_agent.valor,
            ip_address=entidad.metadatos.ip_address.direccion,
            referrer=entidad.metadatos.referrer.url,
            timestamp=entidad.timestamp.isoformat()
        )

    def dto_a_entidad(self, dto: ConversionDTO) -> Conversion:
        metadatos = Metadatos(
            user_agent=UserAgent(dto.user_agent),
            ip_address=IPAddress(dto.ip_address),
            referrer=Referrer(dto.referrer),
            timestamp=dto.timestamp
        )
        
        valor = ValorConversion(dto.valor, dto.moneda)
        
        return Conversion(
            id=dto.id,
            campaña_id=dto.campaña_id,
            influencer_id=dto.influencer_id,
            usuario_id=dto.usuario_id,
            tipo_conversion=TipoConversion(dto.tipo_conversion),
            valor=valor,
            metadatos=metadatos,
            timestamp=datetime.fromisoformat(dto.timestamp)
        )


class MapeadorImpresionDTOJson(Mapeador):
    def externo_a_dto(self, externo: dict) -> ImpresionDTO:
        return ImpresionDTO(
            id=externo.get('id', ''),
            campaña_id=externo.get('campaña_id', ''),
            influencer_id=externo.get('influencer_id'),
            usuario_id=externo.get('usuario_id'),
            tipo_evento=externo.get('tipo_evento', 'IMPRESION'),
            user_agent=externo.get('user_agent', ''),
            ip_address=externo.get('ip_address', ''),
            referrer=externo.get('referrer', ''),
            timestamp=externo.get('timestamp', datetime.now().isoformat())
        )


class MapeadorConversionDTOJson(Mapeador):
    def externo_a_dto(self, externo: dict) -> ConversionDTO:
        return ConversionDTO(
            id=externo.get('id', ''),
            campaña_id=externo.get('campaña_id', ''),
            influencer_id=externo.get('influencer_id'),
            usuario_id=externo.get('usuario_id'),
            tipo_conversion=externo.get('tipo_conversion', 'VENTA'),
            valor=externo.get('valor', 0.0),
            moneda=externo.get('moneda', 'COP'),
            user_agent=externo.get('user_agent', ''),
            ip_address=externo.get('ip_address', ''),
            referrer=externo.get('referrer', ''),
            timestamp=externo.get('timestamp', datetime.now().isoformat())
        )
