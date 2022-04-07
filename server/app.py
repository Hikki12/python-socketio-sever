from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from routes import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")
users = {}


@socketio.on("connect")
def connect():
    """Connection callback."""
    print("Welcome: ")


@socketio.on("disconnect")
def disconnect():
    """Disconnection callback."""
    print("Bye:  ")


@socketio.on(JOIN_ROOM_WEB)
def on_join_web(data):
    """Web client joins to a room."""
    room = data["room"]
    join_room(room)


@socketio.on(JOIN_ROOM_CLIENT)
def on_join_client(data):
    """Client joins to a room."""
    room = data["room"]
    join_room(room)


@socketio.on(LEAVE_ROOM_WEB)
def on_leave_client(data):
    """Web client leaves a room."""
    room = data["room"]
    leave_room(room)


@socketio.on(LEAVE_ROOM_CLIENT)
def on_leave_client(data):
    """Client leaves a room."""
    room = data["room"]
    leave_room(room)


@socketio.on(SERIAL_EVENT_WEB_SERVER)
def serial_web_server(event):
    """Emits a serial event from web to the client.
    client <-- server <-- web
    """
    emit(SERIAL_EVENT_SERVER_CLIENT, event, broadcast=True)


@socketio.on(SERIAL_EVENT_CLIENT_SERVER)
def serial_client_server(event):
    """Emits a serial event from client to the web.
    client --> server --> web
    """
    emit(SERIAL_EVENT_SERVER_WEB, event, broadcast=True, include_self=False)


@socketio.on(REQUEST_UPDATE_WEB_SERVER)
def update_web_server(event):
    """Emits a request for update data from client to the web.
    client <-- server <-- web
    """
    emit(REQUEST_UPDATE_SERVER_CLIENT, event, broadcast=True, include_self=False)


@socketio.on(REQUEST_UPDATE_CLIENT_SERVER)
def update_client_server(event):
    """Emits a request for update data from client to the web.
    client --> server --> web
    """
    emit(REQUEST_UPDATE_SERVER_WEB, event, broadcast=True, include_self=False)


@socketio.on(STREAM_CLIENT_SERVER)
def stream(frame):
    """Recieves a frame (image) an emit it to the web.
    client --> server --> web 
    """
    emit(STREAM_SERVER_WEB, frame, broadcast=True, include_self=False)


@socketio.on(DATA_CLIENT_SERVER)
def receive_from_client(data):
    """Receives data from the client and emit it to the web.
    client --> server --> web
    """
    emit(DATA_SERVER_WEB, data, broadcast=True, include_self=False)


@socketio.on(DATA_WEB_SERVER)
def receive_from_web(data):
    """Receives data from web and emit it to the client.
    client <-- server <-- web
    """
    emit(DATA_SERVER_CLIENT, data, broadcast=True, include_self=False)


@socketio.on(EVENT_WEB_SERVER)
def event_from_web(event):
    """Receives an event from web and emit it to the client.
    client <-- server <-- web
    """
    emit(EVENT_SERVER_CLIENT, event, broadcast=True, include_self=False)


@socketio.on(EVENT_CLIENT_SERVER)
def event_from_client(event):
    """Receives an event from the client and emit it to the web.
    client --> server --> web
    """
    print("emit: ", event)
    emit(EVENT_SERVER_WEB, event, broadcast=True, include_self=False)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app)
