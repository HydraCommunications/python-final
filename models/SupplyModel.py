from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ModelBase import Base

class SupplyModel(Base):
    __tablename__ = 'supplies'

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost_per_item = Column(Float, nullable=False)

    # relationship definition
    room = relationship("RoomModel", back_populates="supplies")
