from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd


load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
    f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Requête SQL d'extraction des données
query = text("SELECT filename, pub FROM image WHERE pub IS NOT NULL;")

# Exécution de la requête et chargement dans un DataFrame
with engine.connect() as conn:
    df = pd.read_sql(query, conn)

# Affichage des 5 premières lignes (optionnel)
print(df.head())


# Requêtes
query_pub = text("SELECT COUNT(*) AS total_pub FROM image WHERE pub = 0;")
query_no_pub = text("SELECT COUNT(*) AS total_no_pub FROM image WHERE pub = 1;")

# Connexion et exécution
with engine.connect() as conn:
    total_pub = conn.execute(query_pub).scalar()
    total_no_pub = conn.execute(query_no_pub).scalar()


print(f"Total d'images avec pub : {total_pub}")
print(f"Total d'images sans pub : {total_no_pub}")