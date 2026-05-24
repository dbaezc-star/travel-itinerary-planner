import os
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from contextlib import contextmanager

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./itineraries.db')

engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItineraryORM(Base):
    __tablename__ = 'itineraries'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=False)
    departure_airport_id = Column(Integer, nullable=False)
    arrival_airport_id = Column(Integer, nullable=False)
    travel_date = Column(Date, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

def create_tables():
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_session():
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
