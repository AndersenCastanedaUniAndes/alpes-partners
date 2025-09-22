from alpespartners.modulos.marketing_influencers.infraestructura.db.session import engine
from alpespartners.modulos.marketing_influencers.infraestructura.db.models import Base

def init_db():
    Base.metadata.create_all(engine)
