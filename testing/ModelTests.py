import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.Models import Base, RoomModel, SupplyModel

# setup for mocking sql. had to do lots of googling... pain
@pytest.fixture(scope="module")
def engine():
    return create_engine("sqlite:///:memory:", echo=True)

@pytest.fixture(scope="module")
def tables(engine):
    # create tables
    Base.metadata.create_all(bind=engine)
    yield
    # drop tables after test session
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def session(engine, tables):
    # new session
    local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = local_session()
    yield session
    session.close()


# actual tests
def test_room_model_creation(session):
    #arrange
    room = RoomModel(
        name="Living Room",
        surface_area=150.0,
        flooring_type="Wood",
        flooring_cost_per_sqft=10.0,
        is_tiling_needed=True,
        tile_type="Ceramic",
        tile_cost_per_sqft=12.0,
        tiling_area=50.0
    )
    session.add(room) # act
    session.commit()

    # assert
    stored_room = session.query(RoomModel).first()
    assert stored_room.name == "Living Room"
    assert stored_room.surface_area == 150.0
    assert stored_room.flooring_type == "Wood"
    assert stored_room.flooring_cost_per_sqft == 10.0
    assert stored_room.is_tiling_needed is True
    assert stored_room.tile_type == "Ceramic"
    assert stored_room.tile_cost_per_sqft == 12.0
    assert stored_room.tiling_area == 50.0

def test_supply_model_creation(session):
    room = RoomModel( # arrange
        name="Kitchen",
        surface_area=120.0,
        flooring_type="Tile",
        flooring_cost_per_sqft=8.0,
        is_tiling_needed=False
    )
    session.add(room) # act
    session.commit()

    supply = SupplyModel(
        room_id=room.id,
        name="Paint",
        quantity=2,
        cost_per_item=15.0
    )
    session.add(supply) #act but again
    session.commit()

    # assert
    stored_supply = session.query(SupplyModel).first()
    assert stored_supply.name == "Paint"
    assert stored_supply.quantity == 2
    assert stored_supply.cost_per_item == 15.0
    assert stored_supply.room_id == room.id

def test_calculate_total_cost(session):
    room = RoomModel( # you get the idea
        name="Bathroom",
        surface_area=100.0,
        flooring_type="Vinyl",
        flooring_cost_per_sqft=5.0,
        is_tiling_needed=True,
        tile_type="Porcelain",
        tile_cost_per_sqft=10.0,
        tiling_area=20.0
    )
    session.add(room) #act
    session.commit()

    # act but more
    expected_flooring_cost = 100.0 * 5.0
    expected_tiling_cost = 20.0 * 10.0
    expected_total_cost = round(expected_flooring_cost + expected_tiling_cost, 2)

    #assert
    assert room.calculate_total_cost() == expected_total_cost
