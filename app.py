from flask import Flask, render_template, session, request, redirect, url_for
from models.Models import *
app = Flask(__name__)
app.secret_key = "RunCurrentFile"

@app.route('/')
def index():
    rooms = db_session.query(RoomModel).all()
    return render_template('home.html', rooms=rooms)


@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        # Get data from form
        name = request.form['name']
        surface_area = float(request.form['surface_area'])
        flooring_type = request.form['flooring_type']
        flooring_cost_per_sqft = float(request.form['flooring_cost_per_sqft'])
        is_tiling_needed = 'is_tiling_needed' in request.form
        tile_type = request.form.get('tile_type') if is_tiling_needed else None
        tile_cost_per_sqft = float(request.form.get('tile_cost_per_sqft', 0)) if is_tiling_needed else None
        tiling_area = float(request.form.get('tiling_area', 0)) if is_tiling_needed else None

        # create room model instance
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


@app.route('/edit_room')
def edit_room():
    return render_template('edit_room.html')


@app.route('/room_details')
def room_details():
    return render_template('room_details.html')


@app.route('/supply')
def supply():
    return render_template('supply.html')


@app.route('/supply_details')
def supply_details():
    return render_template('supply_details.html')


if __name__ == '__main__':
    app.run()
