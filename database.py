from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

password="postgres123"

db_url=f"postgresql://postgres:{password}@localhost:5432/notes"
engine=create_engine(db_url)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)