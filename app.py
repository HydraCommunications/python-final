from flask import Flask, render_template, session, request, redirect, url_for
from models.Models import db_session, RoomModel, SupplyModel
import seaborn as sns
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "RunCurrentFile"

room_name_list = []
room_total_cost_list = []

@app.route('/')
def index():
    rooms = db_session.query(RoomModel).all()
    for room in rooms:
        room.total_cost_calculated = room.calculate_total_cost()

        room_name_list.append(room.name)
        room_total_cost_list.append(room.total_cost_calculated)

        plt.figure(figsize=(8, 8))
        sns.barplot(x=room_name_list, y=room_total_cost_list, palette="viridis")

        plt.xticks(rotation=25, ha="right")

        img_path = os.path.join(app.static_folder, 'plot.png')
        plt.savefig(img_path)
        plt.close()

    return render_template('home.html', rooms=rooms, plot_url=url_for("static", filename="plot.png"))


@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        name = request.form['name']
        surface_area = float(request.form['surface_area'])
        flooring_type = request.form['flooring_type']
        flooring_cost_per_sqft = float(request.form['flooring_cost_per_sqft'])
        is_tiling_needed = 'is_tiling_needed' in request.form
        tile_type = request.form.get('tile_type') if is_tiling_needed else None
        tile_cost_per_sqft = float(request.form.get('tile_cost_per_sqft', 0)) if is_tiling_needed else None
        tiling_area = float(request.form.get('tiling_area', 0)) if is_tiling_needed else None

        new_room = RoomModel(
            name=name,
            surface_area=surface_area,
            flooring_type=flooring_type,
            flooring_cost_per_sqft=flooring_cost_per_sqft,
            is_tiling_needed=is_tiling_needed,
            tile_type=tile_type,
            tile_cost_per_sqft=tile_cost_per_sqft,
            tiling_area=tiling_area
        )

        db_session.add(new_room)
        db_session.commit()

        return redirect(url_for('index'))

    return render_template('room.html')

def get_room_by_id(room_id):
    return db_session.query(RoomModel).filter(RoomModel.id == room_id).first()

@app.route('/edit_rooms/<int:room_id>', methods=['GET'])
def edit_room(room_id):
    room = get_room_by_id(room_id)
    if room is None:
        return "Room not found", 404
    return render_template('edit_room.html', room=room)

@app.route('/update_room/<int:room_id>', methods=['POST'])
def update_room(room_id):
    room = get_room_by_id(room_id)
    if room is None:
        return "Room not found", 404

    room.name = request.form['name']
    room.surface_area = float(request.form['surface_area'])
    room.flooring_type = request.form['flooring_type']
    room.flooring_cost_per_sqft = float(request.form['flooring_cost_per_sqft'])
    room.is_tiling_needed = 'is_tiling_needed' in request.form
    room.tiling_area = float(request.form.get('tiling_area', 0)) if room.is_tiling_needed else 0
    room.tile_cost_per_sqft = float(request.form.get('tile_cost_per_sqft', 0)) if room.is_tiling_needed else 0

    db_session.commit()  # Commit changes to the database

    return redirect(url_for('index'))


@app.route('/room_details/<int:room_id>')
def room_details(room_id):
    #these need to be broken into methods but I'm sleepy so no. Screw test code anyway.
    room = db_session.query(RoomModel).filter(RoomModel.id == room_id).first()

    if room is None:
        return "Room not found", 404

    # flooring crap
    total_flooring_cost = round(room.surface_area * room.flooring_cost_per_sqft, 2)

    # tiling crap
    total_tile_cost = 0
    if room.is_tiling_needed and room.tiling_area and room.tile_cost_per_sqft:
        total_tile_cost = round(room.tiling_area * room.tile_cost_per_sqft, 2)

    # costs total things
    total_supply_cost = 0
    if room.supplies:
        for supply in room.supplies:
            supply.total_supply_cost = round(supply.quantity * supply.cost_per_item, 2)
            total_supply_cost += supply.total_supply_cost

    # total remodel cost
    total_remodel_cost = round(total_flooring_cost + total_tile_cost + total_supply_cost, 2)

    return render_template(
        'room_details.html',
        room=room,
        total_flooring_cost=total_flooring_cost,
        total_tile_cost=total_tile_cost,
        total_supply_cost=total_supply_cost,
        total_remodel_cost=total_remodel_cost
    )


@app.route('/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    try:
        room_to_delete = db_session.query(RoomModel).filter_by(id=room_id).first()
        if room_to_delete:
            # delete all supplies related to room
            db_session.query(SupplyModel).filter_by(room_id=room_id).delete()

            # delete room
            db_session.delete(room_to_delete)
            db_session.commit()
            return redirect(url_for('index'))
    except Exception as e:
        db_session.rollback() # rollback db in case of oopsies
        return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/add_supplies/<int:room_id>', methods=['GET', 'POST'])
def add_supply(room_id):
    room = get_room_by_id(room_id)
    if room is None:
        return "Room not found", 404

    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        cost_per_item = float(request.form['cost_per_item'])

        new_supply = SupplyModel(
            name=name,
            quantity=quantity,
            cost_per_item=cost_per_item,
            room_id=room_id
        )

        db_session.add(new_supply)
        db_session.commit()

        return redirect(url_for('room_details', room_id=room_id))

    return render_template('add_supply.html', room=room)
@app.route('/supply_details')
def supply_details():
    return render_template('supply_details.html')

if __name__ == '__main__':
    app.run()
