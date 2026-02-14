import sqlalchemy as sa
from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from datetime import datetime
from uuid import UUID as UUIDType, uuid4
import os

# Fix: Add +psycopg to use the psycopg driver
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/appdb",
)

### Models
class Base(DeclarativeBase):
    pass


class Vehicle(Base):
    __tablename__ = "vehicle"
    
    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    make: Mapped[str] = mapped_column(String(40), nullable=False)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    year: Mapped[str] = mapped_column(String(4), nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Uncomment if you want the relationship back
    # sightings: Mapped[list["PlateSighting"]] = relationship(back_populates="vehicle")


class PlateSighting(Base):
    __tablename__ = "plate_sighting"
    
    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    vehicle_id: Mapped[UUIDType | None] = mapped_column(UUID(as_uuid=True), ForeignKey("vehicle.id"), nullable=True)
    plate_id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), ForeignKey("plate.id"), nullable=False)
    
    # Relationships
    # vehicle: Mapped["Vehicle"] = relationship(back_populates="sightings")
    plate: Mapped["Plate"] = relationship(back_populates="sightings")


class Plate(Base):
    __tablename__ = "plate"
    
    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(8), nullable=False)
    
    sightings: Mapped[list["PlateSighting"]] = relationship(back_populates="plate")