

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from ClassDatabase import  DatabaseManger
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)
app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")


FOLDERPdf = "tempTestUpload"
database_server = ""

users = {

}
sid_of_users = []

#TODO: Kamers al voorladen

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    print("\033[34mClient connected", client_id,"\033[0m")



@socketio.on('register')
def handle_register(data):
        request_sid = request.sid

        user_id = data["user_id"]

        user_c = databasemrg.get_user(user_id)

        if user_c["dateMade"] == "No-Date-Created":
            databasemrg.add_user(user_id, "User")
            print("\033[33mUser registered", user_id, "\033[0m")

        users[request_sid] = {"user_name": user_id, "current_room": "ffffffff", "requestSid": request_sid}
        sid_of_users.append(request_sid)

        pp.pprint(users)

@socketio.on('created_room')
def handle_created_room(data):
    databasemrg.create_room(data["room_name"])
    chat_names = databasemrg.retrive_available_rooms()
    print(chat_names)

    for i in range(len(sid_of_users)):
         socketio.emit("getChatNames", {"Name": chat_names["rooms"], "RoomId": chat_names["id"], "datemade":chat_names["datemade"]}, to=sid_of_users[i])




@socketio.on('send_message')
def give_awnser(data):
    # {content: message, user: current_user, room: current_chat}
    room_sendfrom=  data["room"]
    print(data["user"], data["content"], data["room"])
    date = datetime.now().isoformat()
    extract = {"messageId": [1], "userName": [data["user"]], "room" : [data["room"]], "content": [data["content"]], "dateMade": [datetime.fromisoformat(date).strftime("%H:%M")]}


    databasemrg.add_message(data["room"], data["user"], data["content"],date)

    for i in range(len(sid_of_users)):
        if users[sid_of_users[i]]["current_room"] == room_sendfrom and sid_of_users[i] != request.sid:
            print("\033[34mSending message", sid_of_users[i], "\033[0m")
            socketio.emit("LoadinComming", {"messageData": extract}, to=sid_of_users[i])

@socketio.on("change_room_to")
def change_room_to(data):
    request_sid = request.sid
    room = data["room_name"]
    users[request_sid]["current_room"] = room
    pp.pprint(users)


@socketio.on('disconnect')
def disconnect():
    request_sid = request.sid
    print("\033[33m [ - ] Disconnected", users[request_sid]["user_name"], "\033[0m")
    del users[request_sid]
    sid_of_users.remove(request_sid)



@socketio.on("getmessagesofchat")
def getmessagesofchat(data):
    room_messages = data["room_name"]
    messages_of_rooms =databasemrg.retrive_available_messages_of_room(room_messages)

    socketio.emit("LoadinComming", {"messageData": messages_of_rooms}, to= request.sid)

@socketio.on("goGetChatNames")
def GetChatNames():
    chat_names = databasemrg.retrive_available_rooms()
    print(chat_names)
    socketio.emit("getChatNames", {"Name": chat_names["rooms"], "RoomId": chat_names["id"], "datemade": chat_names["datemade"]}, to= request.sid)


if __name__ == '__main__':
    databasemrg = DatabaseManger("sqlite:///MMe.db")

    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=5000,host="0.0.0.0")



#Host met: , als nodig