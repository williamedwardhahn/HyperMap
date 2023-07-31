from microdot import Microdot, Request, Response
import sys
import io

app = Microdot()
Response.default_content_type = 'text/html'

@app.route("/")
def index(request: Request):
    return get_editor_html()

@app.route("/repl", methods=["POST"])
def repl(request: Request):
    code = request.form.get("code")
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    final_result = None
    try:
        final_result = eval(code, {})
        printed_output = new_stdout.getvalue().strip()
        if printed_output:
            result = printed_output
        elif final_result is not None:
            result = str(final_result)
        else:
            result = "Executed successfully, no output."
    except Exception as e:
        result = "An error occurred: " + str(e)

    sys.stdout = old_stdout
    return result

def get_editor_html():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simple Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            #chat-wrapper {
                width: 100%;
                max-width: 350px;
                text-align: center;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
            }
            #chat-container {
                height: 400px;
                border: 1px solid #ccc;
                overflow: auto;
                padding: 10px;
                display: flex;
                flex-direction: column;
            }
            #input-container {
                margin-top: 10px;
                display: flex;
            }
            #user-input {
                flex-grow: 1;
                padding: 5px;
                border-radius: 3px;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }
            button {
                padding: 5px 15px;
                margin-left: 5px;
                background-color: #007BFF;
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 3px;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #0056b3;
            }
            .bot, .user {
                padding: 5px;
                margin: 5px;
                border-radius: 5px;
                max-width: 90%;
                box-sizing: border-box;
                word-break: break-word;
            }
            .bot {
                background-color: #f1f1f1;
                align-self: flex-start;
            }
            .user {
                background-color: #007BFF;
                color: white;
                align-self: flex-end;
            }
        </style>
    </head>
    <body>
        <div id="chat-wrapper">
            <div id="chat-container"></div>
            <div id="input-container">
                <textarea id="user-input" rows="3" placeholder="Type your message..." onkeydown="if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); sendMessage(); }"></textarea>
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
        <script>
            function appendMessage(who, message) {
                var chatContainer = document.getElementById('chat-container');
                var messageDiv = document.createElement('div');
                messageDiv.className = who === 'You' ? 'user' : 'bot';
                messageDiv.textContent = message;
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            function sendMessage() {
                var input = document.getElementById('user-input');
                var userMessage = input.value;
                appendMessage('You', userMessage);
                input.value = '';

                // Send user input to the server for execution
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "/repl", true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.onload = function () {
                    var botResponse = xhr.responseText;
                    appendMessage('Bot', botResponse);
                };
                xhr.send('code=' + encodeURIComponent(userMessage));
            }
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

