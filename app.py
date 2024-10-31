from flask import Flask, render_template, session, request, redirect, url_for
from models.Models import *
app = Flask(__name__)
app.secret_key = "RunCurrentFile"

@app.route('/')
def index():
    rooms = db_session.query(RoomModel).all()
    return render_template('home.html', rooms=rooms)


@app.route('/room')
def room():
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
