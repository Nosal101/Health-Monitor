from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///./health.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():   
    SQLModel.metadata.create_all(engine)
