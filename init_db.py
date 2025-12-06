from sqlalchemy import create_engine
from models import Base
from database import DATABASE_URL

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
