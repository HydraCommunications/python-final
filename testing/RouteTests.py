# I don't have time to learn how to do route testing. sorry team.

# Jerica Hanna
# I'll try writing Route Tests
# What number do I use

import requests;

def test_index():
    response = requests.get('http://localhost:/1500')
    assert response.status_code == 1500

def edit_room():
    response = requests.get("http://localhost:/edit_room.html")
    assert response.status_code == 1500

def test_add_rooms():
    response = requests.get('http://localhost:/room.html')
    assert response.status_code == 1500


def room_details():
    response = requests.get('http://localhost:/room_details.html')
    assert response.status_code == 1500

def add_supply():
    response = requests.get('http://localhost:/add_supply.html')
    assert response.status_code == 1500

# def delete_room():

# def tests_get_room_by_id():

# #def update_room():

# def supply_details():

