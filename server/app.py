from flask import Flask, render_template
from flask_socketio import SocketIO
from routers import socket_router


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
socket_router(socketio)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)