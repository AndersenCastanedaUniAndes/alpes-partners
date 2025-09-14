from alpespartners.seedwork.aplicacion.comandos import ComandoHandler
from alpespartners.modulos.tracking.aplicacion.comandos.registrar_impresion import RegistrarImpresion
from alpespartners.modulos.tracking.aplicacion.comandos.registrar_conversion import RegistrarConversion
from alpespartners.modulos.tracking.dominio.entidades import Impresion, Conversion
from alpespartners.modulos.tracking.dominio.objetos_valor import Metadatos, UserAgent, IPAddress, Referrer, TipoConversion, ValorConversion
from alpespartners.modulos.tracking.dominio.eventos import ImpresionRegistrada, ConversionRegistrada
from alpespartners.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
from typing import List


class RegistrarImpresionHandler(ComandoHandler):
    def __init__(self):
        self.eventos: List[EventoDominio] = []

    def handle(self, comando: RegistrarImpresion):
        # Crear metadatos
        metadatos = Metadatos(
            user_agent=UserAgent(comando.user_agent),
            ip_address=IPAddress(comando.ip_address),
            referrer=Referrer(comando.referrer),
            timestamp=comando.timestamp
        )

        # Crear entidad
        impresion = Impresion(
            id=comando.id,
            campaña_id=comando.campaña_id,
            influencer_id=comando.influencer_id,
            usuario_id=comando.usuario_id,
            tipo_evento=comando.tipo_evento,
            metadatos=metadatos,
            timestamp=datetime.fromisoformat(comando.timestamp) if comando.timestamp else datetime.now()
        )

        # Crear evento de dominio
        evento = ImpresionRegistrada(
            id=impresion.id,
            campaña_id=impresion.campaña_id,
            influencer_id=impresion.influencer_id,
            usuario_id=impresion.usuario_id,
            tipo_evento=impresion.tipo_evento,
            metadatos=impresion.metadatos,
            timestamp=impresion.timestamp
        )

        self.eventos.append(evento)
        return impresion


class RegistrarConversionHandler(ComandoHandler):
    def __init__(self):
        self.eventos: List[EventoDominio] = []

    def handle(self, comando: RegistrarConversion):
        # Crear metadatos
        metadatos = Metadatos(
            user_agent=UserAgent(comando.user_agent),
            ip_address=IPAddress(comando.ip_address),
            referrer=Referrer(comando.referrer),
            timestamp=comando.timestamp
        )

        # Crear valor de conversión
        valor = ValorConversion(comando.valor, comando.moneda)

        # Crear entidad
        conversion = Conversion(
            id=comando.id,
            campaña_id=comando.campaña_id,
            influencer_id=comando.influencer_id,
            usuario_id=comando.usuario_id,
            tipo_conversion=TipoConversion(comando.tipo_conversion),
            valor=valor,
            metadatos=metadatos,
            timestamp=datetime.fromisoformat(comando.timestamp) if comando.timestamp else datetime.now()
        )

        # Crear evento de dominio
        evento = ConversionRegistrada(
            id=conversion.id,
            campaña_id=conversion.campaña_id,
            influencer_id=conversion.influencer_id,
            usuario_id=conversion.usuario_id,
            tipo_conversion=conversion.tipo_conversion,
            valor=conversion.valor,
            metadatos=conversion.metadatos,
            timestamp=conversion.timestamp
        )

        self.eventos.append(evento)
        return conversion
