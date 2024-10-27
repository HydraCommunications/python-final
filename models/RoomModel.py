from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from ModelBase import Base

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