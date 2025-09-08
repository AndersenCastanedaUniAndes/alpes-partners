from pulsar.schema import *
from dataclasses import dataclass, field
from alpespartners.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearCampañaPayload(ComandoIntegracion):
    id = String()
    nombre = String()
    producto = String()
    presupuesto = Long()
    moneda = String()
    marca = String()
    influencers_ids = Array(array_type=String())
    conversiones = Array(array_type=String())
    fecha_creacion = Long()

class ComandoCrearCampaña(ComandoIntegracion):
    data = ComandoCrearCampañaPayload()
