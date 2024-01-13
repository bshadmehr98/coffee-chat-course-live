var box_html = `
<button id="chat-toggle-btn" style="width: 50px; height: 50px;">
    <i class="material-icons">chat</i>
</button>

<div id="chat-box" class="card">
    <div class="card-header">
        Chat
        <button type="button" class="close" id="close-chat-box" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    <div class="card-body" id="chat-messages">
        <!-- Example chat messages -->
        <div class="chat-message">
            <p class="user">User: Hello!</p>
        </div>
        <div class="chat-message">
            <p class="site">Site: Hi there!</p>
        </div>
    </div>
    <div class="card-footer">
        <div class="input-group">
            <input type="text" id="user-message" class="form-control" placeholder="Type your message">
            <div class="input-group-append">
                <button class="btn btn-primary" id="send-btn">
                    <i class="material-icons">send</i>
                </button>
            </div>
        </div>
    </div>
</div>
`

var box_css = `
<style>
    body {
        background-color: #f8f9fa;
    }

    #chat-box {
        display: none;
        position: fixed;
        bottom: 70px;
        left: 20px;
        max-width: 300px;
        border: 1px solid #ced4da;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }

    #chat-box .card-header {
        background-color: #007bff;
        color: #ffffff;
        border-radius: 10px 10px 0 0;
        padding: 10px;
        position: relative;
    }

    #close-chat-box {
        position: absolute;
        top: 50%;
        right: 10px;
        transform: translateY(-50%);
        color: #ffffff;
        cursor: pointer;
    }

    #chat-box .card-body {
        padding: 10px;
        max-height: 200px;
        overflow-y: auto;
    }

    .chat-message {
        margin-bottom: 10px;
    }

    .chat-message p {
        margin: 0;
        padding: 8px 12px;
        border-radius: 8px;
    }

    .chat-message .user {
        background-color: #007bff;
        color: #ffffff;
    }

    .chat-message .site {
        background-color: #ffffff;
        color: #333333;
    }

    #chat-box .card-footer {
        background-color: transparent;
        border: none;
        padding: 0;
    }

    #chat-box input.form-control {
        border-radius: 0;
        height: 40px;
    }

    #chat-box .input-group {
        width: 100%;
    }

    #send-btn {
        border-radius: 0;
        padding: 10px;
        height: 40px;
    }

    #chat-toggle-btn {
        position: fixed;
        bottom: 20px;
        left: 20px;
        border-radius: 50%;
        padding: 12px;
        background-color: #007bff;
        color: #ffffff;
        border: none;
        cursor: pointer;
        z-index: 999;
        /* Add z-index to ensure it's above the chat box */
    }

    #chat-toggle-btn i {
        font-size: 24px;
    }
</style>
`

var socket
var chat_id

document.addEventListener("DOMContentLoaded", function() {
    // This function will be executed when the DOM is fully loaded

    // Insert the HTML code just before the end of the body
    document.body.insertAdjacentHTML('beforeend', box_css);
    document.body.insertAdjacentHTML('beforeend', box_html);

    start_socket_connection()
});

function add_message_to_box(message){
    var userMessage = message.text;
    if (userMessage.trim() !== '') {
        var chatMessages = $('#chat-messages');
        if (message.from_user){
            var newMessage = '<div class="chat-message"><p class="user">User: ' + userMessage + '</p></div>';
        } else {
            var newMessage = '<div class="chat-message"><p class="site">Site: ' + userMessage + '</p></div>';
        }
        chatMessages.append(newMessage);
    }
}

function inject_chat_box(data) {
    for (let mId in data.messages) {
        add_message_to_box(data.messages[mId])
    }
    
    $(document).ready(function () {
        $('#chat-toggle-btn').click(function () {
            $('#chat-box').toggle();
        });

        $('#close-chat-box').click(function () {
            $('#chat-box').hide();
        });

        $('#send-btn').click(function () {
            sendMessage();
        });

        $('#user-message').keypress(function (e) {
            if (e.which === 13) {
                sendMessage();
            }
        });

        function sendMessage() {
            var userMessage = $('#user-message').val();
            if (userMessage.trim() !== '') {
              var chatMessages = $('#chat-messages');
              var newMessage = '<div class="chat-message"><p class="user">User: ' + userMessage + '</p></div>';
              chatMessages.append(newMessage);
              send_mesasge_to_server(userMessage);
              // Clear the input field after sending
              $('#user-message').val('');
              scrollToBottom();
            }
          }

          function send_mesasge_to_server(message){
            var data = {   
              "command": "new_user_message",
              "data":{
                  "chat_id": load_chat_id(),
                  "message": message
              }
            }
            console.log(data)
            send_new_message(socket, JSON.stringify(data))
          }
    
          function scrollToBottom() {
            var chatBody = $('#chat-box .card-body');
            chatBody.scrollTop(chatBody.prop("scrollHeight"));
          }
    });
}

function on_new_message(event){
    data = JSON.parse(event.data)
    if (data['command'] == "get_chat"){
        console.log(data)
        set_chat_id(data.data.session_token)
        inject_chat_box(data["data"])
    }
}

function send_new_message(socket, message){
    socket.send(message)
}

function load_chat_id(){
    chat_id = localStorage.getItem("chat-token")
    return chat_id
}

function set_chat_id(token){
    alert(1111)
    localStorage.setItem("chat-token", token)
}

function on_socket_open(){
    var data = {
        "command": "get_chat",
        "data":{
            "chat_id": chat_id
        }
    }
    send_new_message(socket, JSON.stringify(data))
}

function start_socket_connection(){
    load_chat_id()
    socket = new WebSocket("ws://localhost:8000/feed")
    socket.addEventListener('message', on_new_message)
    socket.addEventListener('open', on_socket_open)

    return socket
}
