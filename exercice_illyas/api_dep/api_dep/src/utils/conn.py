from sqlmodel import Session, create_engine

def get_session():
    postgres_url = "postgresql://ROOT:ROOT@localhost:5432/BDD_TEST"
    engine = create_engine(postgres_url)
    with Session(engine) as session:
        yield session