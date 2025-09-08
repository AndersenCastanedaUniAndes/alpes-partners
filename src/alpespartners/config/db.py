from sqlmodel import SQLModel, Session, create_engine, Field

# DATABASE_URL = "postgresql+psycopg2://postgres:postgres@postgres:5432/postgres"

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, echo=True)

# class Item(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
