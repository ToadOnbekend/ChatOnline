

current_chat = "D99F1A1A-1D1A-4D1A-9D1A-1D1A1D1A1D1A"
current_user = prompt("What is your name?");

f= "fdd"


const socket = io("http://192.168.2.69:5000/", {
    transports: ["websocket"], //
    secure: false,             //  WiFi: 192.168.2.69:5000
});

socket.emit("register", {user_id: current_user});


// const socket = io("http://localhost:5000");


function SendMsg() {
    const input_user = document.getElementById('chatt-input');
    const message = input_user.textContent.trim();

    if (message !== "") {

        const messagess = document.getElementById('messages');

        const element_message_user = document.createElement('li');
        element_message_user.classList.add('humanQuestion');
        element_message_user.innerHTML = message
        messagess.appendChild(element_message_user);

        socket.emit('send_message', {content: message, user: current_user, room: current_chat});
        input_user.textContent = "";
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

     dateSend.innerHTML = dateSendMsg;
     user_name_sec.innerHTML = user_name;

     dateSend.classList.add('date_of_message');
     user_name_sec.classList.add('name_of_user');

     message_info.classList.add('info-of-message');

     message_info.appendChild(user_name_sec);
     message_info.appendChild(dateSend);

     newMessage.innerHTML = marked.parse(data)
     // Hier toepassen

     newMessage.classList.add('LLMresponds');

     newMessage.append(message_info);


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
                  change_room_to(data,idE); // Roep de functie aan bij klikken

              });

              newMessage.appendChild(button);
              messages.appendChild(newMessage);
}


function change_room_to(data) {
    if (data != current_chat) {
        const messages = document.getElementById('messages');
        messages.innerHTML = '';
        document.getElementById('configScreen').style.display = 'none';
        socket.emit("getmessagesofchat", {"room_name":data})
        socket.emit("change_room_to", {"room_name":data})
        current_chat = data;
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

    socket.emit('created_room', {"room_name":message});



    socket.emit("getmessagesofchat", {"room_name":message})
    socket.emit("change_room_to", {"room_name":message})
    current_chat = message;
    input_user.value = "";
    document.getElementById('configScreen').style.display = 'none';
}


function scrollOnNewMSG(){
    const messagesContainer = document.getElementById('messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

