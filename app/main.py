from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, Vehicle, PlateSighting, Plate, DATABASE_URL

# Create FastAPI app
app = FastAPI(title="Vehicle Tracking API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas
class VehicleBase(BaseModel):
    make: str = Field(..., max_length=40)
    model: str = Field(..., max_length=40)
    year: str = Field(..., max_length=4)
    color: str = Field(..., max_length=20)

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    make: Optional[str] = Field(None, max_length=40)
    model: Optional[str] = Field(None, max_length=40)
    year: Optional[str] = Field(None, max_length=4)
    color: Optional[str] = Field(None, max_length=20)

class VehicleResponse(VehicleBase):
    id: UUID

    class Config:
        from_attributes = True

class PlateBase(BaseModel):
    code: str = Field(..., max_length=8)

class PlateCreate(PlateBase):
    pass

class PlateUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=8)

class PlateResponse(PlateBase):
    id: UUID

    class Config:
        from_attributes = True

class PlateSightingBase(BaseModel):
    longitude: float
    latitude: float
    timestamp: datetime
    vehicle_id: Optional[UUID] = None
    plate_id: UUID

class PlateSightingCreate(PlateSightingBase):
    pass

class PlateSightingUpdate(BaseModel):
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    timestamp: Optional[datetime] = None
    vehicle_id: Optional[UUID] = None
    plate_id: Optional[UUID] = None

class PlateSightingResponse(PlateSightingBase):
    id: UUID

    class Config:
        from_attributes = True

# ============== VEHICLE ENDPOINTS ==============

@app.post("/vehicles/", response_model=VehicleResponse, status_code=201)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """Create a new vehicle"""
    db_vehicle = Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.get("/vehicles/", response_model=List[VehicleResponse])
def list_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all vehicles with pagination"""
    vehicles = db.query(Vehicle).offset(skip).limit(limit).all()
    return vehicles

@app.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: UUID, db: Session = Depends(get_db)):
    """Get a specific vehicle by ID"""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@app.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: UUID, vehicle: VehicleUpdate, db: Session = Depends(get_db)):
    """Update a vehicle"""
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    update_data = vehicle.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_vehicle, field, value)
    
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.delete("/vehicles/{vehicle_id}", status_code=204)
def delete_vehicle(vehicle_id: UUID, db: Session = Depends(get_db)):
    """Delete a vehicle"""
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(db_vehicle)
    db.commit()
    return None

# ============== PLATE ENDPOINTS ==============

@app.post("/plates/", response_model=PlateResponse, status_code=201)
def create_plate(plate: PlateCreate, db: Session = Depends(get_db)):
    """Create a new plate"""
    db_plate = Plate(**plate.model_dump())
    db.add(db_plate)
    db.commit()
    db.refresh(db_plate)
    return db_plate

@app.get("/plates/", response_model=List[PlateResponse])
def list_plates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all plates with pagination"""
    plates = db.query(Plate).offset(skip).limit(limit).all()
    return plates

@app.get("/plates/{plate_id}", response_model=PlateResponse)
def get_plate(plate_id: UUID, db: Session = Depends(get_db)):
    """Get a specific plate by ID"""
    plate = db.query(Plate).filter(Plate.id == plate_id).first()
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")
    return plate

@app.get("/plates/code/{plate_code}", response_model=PlateResponse)
def get_plate_by_code(plate_code: str, db: Session = Depends(get_db)):
    """Get a plate by its code"""
    plate = db.query(Plate).filter(Plate.code == plate_code).first()
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")
    return plate

@app.put("/plates/{plate_id}", response_model=PlateResponse)
def update_plate(plate_id: UUID, plate: PlateUpdate, db: Session = Depends(get_db)):
    """Update a plate"""
    db_plate = db.query(Plate).filter(Plate.id == plate_id).first()
    if not db_plate:
        raise HTTPException(status_code=404, detail="Plate not found")
    
    update_data = plate.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_plate, field, value)
    
    db.commit()
    db.refresh(db_plate)
    return db_plate

@app.delete("/plates/{plate_id}", status_code=204)
def delete_plate(plate_id: UUID, db: Session = Depends(get_db)):
    """Delete a plate"""
    db_plate = db.query(Plate).filter(Plate.id == plate_id).first()
    if not db_plate:
        raise HTTPException(status_code=404, detail="Plate not found")
    
    db.delete(db_plate)
    db.commit()
    return None

# ============== PLATE SIGHTING ENDPOINTS ==============

@app.post("/sightings/", response_model=PlateSightingResponse, status_code=201)
def create_sighting(sighting: PlateSightingCreate, db: Session = Depends(get_db)):
    """Create a new plate sighting"""
    # Verify plate exists
    plate = db.query(Plate).filter(Plate.id == sighting.plate_id).first()
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")
    
    # Verify vehicle exists if provided
    if sighting.vehicle_id:
        vehicle = db.query(Vehicle).filter(Vehicle.id == sighting.vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db_sighting = PlateSighting(**sighting.model_dump())
    db.add(db_sighting)
    db.commit()
    db.refresh(db_sighting)
    return db_sighting

@app.get("/sightings/", response_model=List[PlateSightingResponse])
def list_sightings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all plate sightings with pagination"""
    sightings = db.query(PlateSighting).offset(skip).limit(limit).all()
    return sightings

@app.get("/sightings/{sighting_id}", response_model=PlateSightingResponse)
def get_sighting(sighting_id: UUID, db: Session = Depends(get_db)):
    """Get a specific sighting by ID"""
    sighting = db.query(PlateSighting).filter(PlateSighting.id == sighting_id).first()
    if not sighting:
        raise HTTPException(status_code=404, detail="Sighting not found")
    return sighting

@app.get("/sightings/plate/{plate_id}", response_model=List[PlateSightingResponse])
def get_sightings_by_plate(plate_id: UUID, db: Session = Depends(get_db)):
    """Get all sightings for a specific plate"""
    sightings = db.query(PlateSighting).filter(PlateSighting.plate_id == plate_id).all()
    return sightings

@app.get("/sightings/vehicle/{vehicle_id}", response_model=List[PlateSightingResponse])
def get_sightings_by_vehicle(vehicle_id: UUID, db: Session = Depends(get_db)):
    """Get all sightings for a specific vehicle"""
    sightings = db.query(PlateSighting).filter(PlateSighting.vehicle_id == vehicle_id).all()
    return sightings

@app.put("/sightings/{sighting_id}", response_model=PlateSightingResponse)
def update_sighting(sighting_id: UUID, sighting: PlateSightingUpdate, db: Session = Depends(get_db)):
    """Update a plate sighting"""
    db_sighting = db.query(PlateSighting).filter(PlateSighting.id == sighting_id).first()
    if not db_sighting:
        raise HTTPException(status_code=404, detail="Sighting not found")
    
    update_data = sighting.model_dump(exclude_unset=True)
    
    # Verify plate exists if being updated
    if "plate_id" in update_data:
        plate = db.query(Plate).filter(Plate.id == update_data["plate_id"]).first()
        if not plate:
            raise HTTPException(status_code=404, detail="Plate not found")
    
    # Verify vehicle exists if being updated
    if "vehicle_id" in update_data and update_data["vehicle_id"]:
        vehicle = db.query(Vehicle).filter(Vehicle.id == update_data["vehicle_id"]).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
    
    for field, value in update_data.items():
        setattr(db_sighting, field, value)
    
    db.commit()
    db.refresh(db_sighting)
    return db_sighting

@app.delete("/sightings/{sighting_id}", status_code=204)
def delete_sighting(sighting_id: UUID, db: Session = Depends(get_db)):
    """Delete a plate sighting"""
    db_sighting = db.query(PlateSighting).filter(PlateSighting.id == sighting_id).first()
    if not db_sighting:
        raise HTTPException(status_code=404, detail="Sighting not found")
    
    db.delete(db_sighting)
    db.commit()
    return None

# ============== HEALTH CHECK ==============

@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Platitude API"}

@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow()
    }
