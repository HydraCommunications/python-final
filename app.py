from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/room.html')
def room():

@app.route('/edit_room.html')
def edit_room():
    return

@app.route('/room_details.html')
def room_details():
    return

@app.route('/supply.html')
def supply():
    return

@app.route('/supply_details.html')
def supply_details():
    return


if __name__ == '__main__':
    app.run()
