

current_chat = "D99F1A1A-1D1A-4D1A-9D1A-1D1A1D1A1D1A-aAAx"
current_user = prompt("What is your name?");

document.getElementById("currentUser_info").textContent=current_user;
users_online = []
users_inroom = []
f= "fdd"


// const socket = io("http://localhost:5000/", {
//     transports: ["websocket"], //
//     secure: false,             //  WiFi: 192.168.2.69:5000
// });
const socket = io();

socket.emit("register", {user_id: current_user});


// const socket = io("http://localhost:5000");




function SendMsg() {
    const input_user = document.getElementById('chatt-input');
    const message = input_user.textContent.trim();

    if (message !== "" && current_chat !== "D99F1A1A-1D1A-4D1A-9D1A-1D1A1D1A1D1A-aAAx") {
        const messagess = document.getElementById('messages');

        const element_message_user = document.createElement('li');
        element_message_user.classList.add('humanQuestion');
        element_message_user.innerHTML = message
        messagess.appendChild(element_message_user);

        socket.emit('send_message', {content: message, user: current_user, room: current_chat});
        input_user.textContent = "";
        scrollOnNewMSG()
    }
}

function userMSG(data){
     const messagess = document.getElementById('messages');
    const element_message_user = document.createElement('li');

    element_message_user.classList.add('humanQuestion');
    element_message_user.innerHTML = data
    messagess.appendChild(element_message_user);

}

function show_config_screen(){
    document.getElementById('configScreen').style.display = 'flex';
    const messages = document.getElementById('messages');
    messages.innerHTML = ''; }

function llmawnserMSG(data, user_name, dateSendMsg){
     const messages = document.getElementById('messages');
     const newMessage = document.createElement('li');
     const message_info = document.createElement('div');
     const user_name_sec = document.createElement('div');
     const dateSend = document.createElement('div');
     const message_content = document.createElement('div');
     dateSend.innerHTML = dateSendMsg;
     user_name_sec.innerHTML = user_name;
     message_content.innerHTML = marked.parse(data)

     dateSend.classList.add('date_of_message');
     user_name_sec.classList.add('name_of_user');

     message_content.classList.add('message_content');

     message_info.classList.add('info-of-message');

     message_info.appendChild(user_name_sec);
     message_info.appendChild(dateSend);


     newMessage.classList.add('LLMresponds');

     newMessage.append(message_info);
     newMessage.append(message_content);

     messages.appendChild(newMessage);





}
socket.on('ReceivedRequest', (data) => {
    alert("FROM SERVER: " + data.message);
})

 socket.on('AwnserLLM', (data) => {
  llmawnserMSG(data.message);
 });

function getCnames(data,idE){
      const messages = document.getElementById('chatsL');
         const newMessage = document.createElement('li');
         const button = document.createElement('button')
              button.textContent = data
              button.addEventListener('click', () => {
                  change_room_to(data,idE);

              });

              newMessage.appendChild(button);
              messages.appendChild(newMessage);
}


function change_room_to(data) {
    if (data != current_chat) {

        users_inroom = []
        update_information_room()
        old_room = current_chat;
        const messages = document.getElementById('messages');
        messages.innerHTML = '';
        document.getElementById('configScreen').style.display = 'none';
        socket.emit("getmessagesofchat", {"room_name":data})
        socket.emit("change_room_to", {"room_name":data, "old_room": old_room});
        current_chat = data;

        document.getElementById("currentRoom_info").textContent=current_chat;
    }

}

socket.on('AwnserSystem', (data) => {
     const messages = document.getElementById('messages');
     const newMessage = document.createElement('li');
     newMessage.innerHTML = marked.parse(data.message)


     newMessage.classList.add('system');
     messages.appendChild(newMessage);
 });



socket.on("getChatNames", (data) => {
    document.getElementById("chatsL").innerHTML = ""
    for (let i = 0; i < data.Name.length; i++) {
         getCnames(data.Name[i])
    }

 })

socket.on("LoadinComming", (data) => {
    // alert("IN comming")
    data = data.messageData
    for (let i = 0; i < data.messageId.length; i++) {
        let v = data.userName[i]
        let date_send = data.dateMade[i]
        console.log(date_send)

        if (v != current_user){
            //user_name = v
            //date_of_msg = data.dateMade[i]
            llmawnserMSG(data.content[i], v, date_send);
        } else {
            userMSG(data.content[i]);
        }

    }
    scrollOnNewMSG();

 })




function create_room(){
    const input_user = document.getElementById('collectionNaming');
    const message = input_user.value;

    if (message !== "") {
        old_room = current_chat;
        socket.emit('created_room', {"room_name": message});


        socket.emit("getmessagesofchat", {"room_name": message})
        socket.emit("change_room_to", {"room_name": message, "old_room": old_room});
        current_chat = message;
        input_user.value = "";
        document.getElementById('configScreen').style.display = 'none';
        users_inroom = []
        document.getElementById("currentRoom_info").textContent=current_chat
        update_information_room()
        getCnames(message)

    }
}


function scrollOnNewMSG(){
    const messagesContainer = document.getElementById('messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}



function create_notify(data,status, info_text){
     const messages = document.getElementById('messages');
     const notify = document.createElement('li');
     const user_left = document.createElement('span');

     user_left.innerHTML = data["Name"] + info_text;

     user_left.classList.add('person_name');
     notify.classList.add(status);

     notify.appendChild(user_left);

     messages.appendChild(notify);
     scrollOnNewMSG()
}

socket.on("PersonLeft", (data) => {
     users_inroom = users_inroom.filter(item => item !== data["Name"])
     update_information_room()
     create_notify(data,"PersonLeft", " | Left room");
     })

socket.on("PersonJoined", (data) => {
    users_inroom.push(data["Name"])
    update_information_room()
    create_notify(data,"PersonJoined", " | Joined room");


})

socket.on("PersonDisconnected", (data) => {

    users_online = users_online.filter(item => item !== data["Name"])
    update_information_online()
    create_notify(data,"PersonDisconnected", " | Disconnected");

})

socket.on("PersonConnected", (data) => {

    users_online.push(data["Name"])
    update_information_online()
    create_notify(data,"PersonConnected", " | Connected");

})

function update_information_online(){
     let info_who_is_online = users_online.join(', ')

     console.log(info_who_is_online)
     document.getElementById("user_who_are_online").textContent=info_who_is_online;
}

function update_information_room(){
     let roomUsers = users_inroom.join(', ')

     console.log(roomUsers)
     document.getElementById("user_who_are_inroom").textContent=roomUsers;
}

socket.on("GetUsersOnline", (data) => {

    users_online = users_online.concat(data["Users"])
    update_information_online()


})

socket.on("GetUsersOfRoom", (data) => {
    users_inroom = users_inroom.concat(data["Users"])
    update_information_room()


})

