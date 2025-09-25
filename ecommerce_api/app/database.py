from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file (will be created automatically)
DATABASE_URL = "sqlite:///./ecommerce.db"

# Create the engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session for DB operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
