from alpespartners.config.db import get_session as db

# Tabla para relacion las campañas con los influencers muchos a muchos
campaña_influencer = db.Table(
    'campaña_influencer',
    db.Column('campaña_id', db.String, db.ForeignKey('campañas.id'), primary_key=True),
    db.Column('influencer_id', db.String, db.ForeignKey('influencers.id'), primary_key=True)
)


class CampañaDTO(db.Model):
    __tablename__ = 'campañas'

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    producto = db.Column(db.String, nullable=False)
    presupuesto = db.Column(db.Float, nullable=False)
    moneda = db.Column(db.String, nullable=False)
    marca = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)

    influencers = db.relationship('InfluencerDTO', secondary=campaña_influencer, back_populates='campañas')


class InfluencerDTO(db.Model):
    __tablename__ = 'influencers'

    id = db.Column(db.String, primary_key=True)
    nombres = db.Column(db.String, nullable=False)
    apellidos = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, nullable=False)
    email_dominio = db.Column(db.String, nullable=False)
    email_es_empresarial = db.Column(db.Boolean, nullable=False)
    cedula_numero = db.Column(db.Integer, nullable=False)
    cedula_ciudad_nombre = db.Column(db.String, nullable=False)
    cedula_ciudad_pais = db.Column(db.String, nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    plataforma_nombre = db.Column(db.String, nullable=False)
    plataforma_url = db.Column(db.String, nullable=False)
    audiencia = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)

    campañas = db.relationship('CampañaDTO', secondary=campaña_influencer, back_populates='influencers')
