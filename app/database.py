from psycopg_pool import ConnectionPool
import sqlalchemy as sa
from sqlalchemy import create_engine, Integer, String, Float, DateTime, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Mapped
import os
from uuid import uuid4
from datetime import datetime

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/appdb",
)

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=10,
    open=False,
)

### Models
Base = declarative_base()

class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[UUID] = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    make: Mapped[str] = sa.Column(sa.String(40), nullable=False)
    model: Mapped[str] = sa.Column(sa.String(40), nullable=False)
    year: Mapped[str] = sa.Column(sa.String(4), nullable=False)
    color: Mapped[str] = sa.Column(sa.String(20), nullable=False)

class PlateSighting(Base): 
    __tablename__ = "platesighting"
    
    id: Mapped[UUID] = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    longitude: Mapped[float] = sa.Column(sa.Float, nullable=False)
    latitude: Mapped[float] = sa.Column(sa.Float, nullable=False)
    timestamp: Mapped[DateTime] = sa.Column(sa.DateTime, nullable=False)
    vehicle_id: Mapped[UUID] = sa.Column(UUID(as_uuid=True), sa.ForeignKey("vehicles.id"), nullable=True)
    plate_id: Mapped[UUID] = sa.Column(UUID(as_uuid=True), sa.ForeignKey("plates.id"), nullable=False)
    
    # Relationships
    #vehicle: Mapped["Vehicle"] = relationship("Vehicle", back_populates="platessightings")
    plate: Mapped["Plate"] = relationship("Plate", back_populates="sightings")

class Plate(Base):
    __tablename__ = "plates"
    
    id: Mapped[UUID] = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code: Mapped[str] = sa.Column(sa.String(8), nullable=False)
    
    sightings: Mapped[list["PlateSighting"]] = relationship("PlateSighting", back_populates="plate")


