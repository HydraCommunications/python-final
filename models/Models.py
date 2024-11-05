import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Define the base directory and database path
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'database', 'supply_tracker.db')
os.makedirs(os.path.dirname(database_path), exist_ok=True)

# Initialize the database engine
engine = create_engine(f'sqlite:///{database_path}', echo=True)

# Define the declarative base class
Base = declarative_base()

# Set up the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class RoomModel(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surface_area = Column(Float, nullable=False)
    flooring_type = Column(String, nullable=False)
    flooring_cost_per_sqft = Column(Float, nullable=False)
    is_tiling_needed = Column(Boolean, default=False, nullable=False)
    tile_type = Column(String, nullable=True)
    tile_cost_per_sqft = Column(Float, nullable=True)
    tiling_area = Column(Float, nullable=True)

    # relationship definition
    supplies = relationship("SupplyModel", back_populates="room")

    def calculate_total_cost(self):
        flooring_cost = self.surface_area * self.flooring_cost_per_sqft
        tiling_cost = (self.tiling_area * self.tile_cost_per_sqft) \
            if self.is_tiling_needed else 0
            # worst ternary format ever btw
        return round(flooring_cost + tiling_cost, 2)

class SupplyModel(Base):
    __tablename__ = 'supplies'

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost_per_item = Column(Float, nullable=False)

    # relationship definition
    room = relationship("RoomModel", back_populates="supplies")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

