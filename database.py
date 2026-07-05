from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

password="postgres123"

db_url=f"postgresql://postgres:{password}@localhost:5432/notes"
engine=create_engine(db_url)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine,expire_on_commit=True)
# After commit(), SQLAlchemy "forgets" the values inside db_note
# (this is called expire_on_commit)(it is TRUE by default)
# refresh() asks the database for the latest values and fills db_note again,
# so we can return it with all its data instead of {}.
#or use db.refresh(db_note) 