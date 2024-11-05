# I don't have time to learn how to do route testing. sorry team.

# Jerica Hanna
# I'll try writing Route Tests

import requests;

def test_index():
    response = requests.get('http://localhost:/1500')
    assert response.status_code == 400
    assert response.text == 'Index Route Tests'

def edit_room():
    response = requests.get("edit_room.html")
    assert response

def test_add_rooms():
    response = requests.get('room.html')
    assert response


def room_details():
    response = requests.get('room_details.html')
    assert response

def add_supply():
    response = requests.get('add_supply.html')
    assert response

# def delete_room():


# def tests_get_room_by_id():

# #def update_room():

# def supply_details():

