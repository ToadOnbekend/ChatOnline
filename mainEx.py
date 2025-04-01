from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected users
connected_clients = {}


@socketio.on('connect')
def handle_connect():
    client_id = request.sid  # Unique session ID
    connected_clients[client_id] = {"username": None, "room": None}
    print(f"Client {client_id} connected.")


@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in connected_clients:
        leave_room(connected_clients[client_id]["room"])
        del connected_clients[client_id]
    print(f"Client {client_id} disconnected.")


@socketio.on('set_username')
def handle_set_username(data):
    client_id = request.sid
    username = data['username']
    connected_clients[client_id]['username'] = username
    emit('user_list', list(connected_clients.values()), broadcast=True)


@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    client_id = request.sid

    leave_room(connected_clients[client_id]['room'])  # Leave previous room if any
    join_room(room)
    connected_clients[client_id]['room'] = room

    emit('room_joined', {'room': room}, room=client_id)
    send(f"{connected_clients[client_id]['username']} has joined the room.", room=room)


@socketio.on('message')
def handle_message(data):
    client_id = request.sid
    username = connected_clients[client_id]['username']
    room = connected_clients[client_id]['room']

    if room:
        emit('message', {'username': username, 'message': data['message']}, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

=========================

from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Opslaan van verbonden gebruikers {username: sid}
connected_users = {}

@socketio.on('connect')
def handle_connect():
    print(f"Client {request.sid} connected.")

@socketio.on('disconnect')
def handle_disconnect():
    username = None
    for user, sid in connected_users.items():
        if sid == request.sid:
            username = user
            break
    if username:
        del connected_users[username]
        print(f"User {username} disconnected.")

@socketio.on('set_username')
def handle_set_username(data):
    username = data['username']
    connected_users[username] = request.sid  # Bewaar gebruikersnaam met hun session ID
    print(f"User {username} set with session {request.sid}")

@socketio.on('private_message')
def handle_private_message(data):
    sender = request.sid
    receiver_username = data['to']
    message = data['message']

    if receiver_username in connected_users:
        receiver_sid = connected_users[receiver_username]
        emit('private_message', {'from': sender, 'message': message}, room=receiver_sid)
        print(f"Private message sent from {sender} to {receiver_username}")
    else:
        emit('error', {'message': 'User not found'}, room=sender)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
