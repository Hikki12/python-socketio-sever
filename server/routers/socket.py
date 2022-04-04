from flask_socketio import emit


def socket_router(socketio):

    @socketio.on("connect")
    def connect(ssid):
        print("Welcome: ", ssid)


    @socketio.on("disconnect")
    def disconnect(ssid):
        print("Bye: ", ssid)


    @socketio.on("stream")
    def stream(frame):
        emit("stream", frame, broadcast=True)
