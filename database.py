from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Neon PostgreSQL connection string
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_tQONfVv40UxD@ep-damp-darkness-a1qessyn-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
