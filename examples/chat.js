// chat-box-injector.js

// Function to create and inject the chat box
function injectChatBox() {
    // Create a container for the chat box
    var chatContainer = document.createElement('div');
    chatContainer.id = 'chat-container';

    // Inject the chat box HTML into the container
    chatContainer.innerHTML = `
    <style>
        body {
            background-color: #f8f9fa;
        }

        #chat-box {
            display: none;
            position: fixed;
            bottom: 70px;
            right: 20px;
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
            right: 20px;
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

        <!-- Chat box HTML goes here -->
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

        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        <script>
            // Add your custom JavaScript here
            $(document).ready(function () {
                alert(1)
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
                        // Clear the input field after sending
                        $('#user-message').val('');
                        scrollToBottom();
                    }
                }

                function scrollToBottom() {
                    var chatBody = $('#chat-box .card-body');
                    chatBody.scrollTop(chatBody.prop("scrollHeight"));
                }
            });
        </script>
    `;

    // Append the chat container to the body
    document.body.appendChild(chatContainer);
}

// Call the injectChatBox function to create and inject the chat box
injectChatBox()