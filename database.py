from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.db"
engine = create_engine(
    f"sqlite:///{sqlite_file_name}",
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)