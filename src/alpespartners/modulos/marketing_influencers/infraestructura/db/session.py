from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from alpespartners.modulos.marketing_influencers.infraestructura.db.config import DATABASE_URL

engine: Engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

class UnidadDeTrabajo:
    def __enter__(self):
        self.session: Session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc:
            self.session.rollback()
        else:
            self.session.commit()

        self.session.close()
