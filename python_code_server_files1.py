from microdot import Microdot, Request, Response
import sys
import io
import os

app = Microdot()
Response.default_content_type = 'text/html'
USER_FILES_PATH = 'user_files'

if not os.path.exists(USER_FILES_PATH):
    os.makedirs(USER_FILES_PATH)

def get_next_filename():
    i = 1
    while os.path.exists(os.path.join(USER_FILES_PATH, f'code{i}.py')):
        i += 1
    return f'code{i}.py'

@app.route("/")
def index(request: Request):
    files = [f for f in os.listdir(USER_FILES_PATH) if f.endswith('.py')]
    return get_editor_html(files)

@app.route("/create", methods=["POST"])
def create_file(request: Request):
    filename = request.form.get("filename") or get_next_filename()
    content = request.form.get("content")

    with open(os.path.join(USER_FILES_PATH, filename), 'w') as file:
        file.write(content)

    return index(request)

@app.route("/execute/<filename>", methods=["GET"])
def execute_file(request: Request, filename):
    result = None
    with open(os.path.join(USER_FILES_PATH, filename), 'r') as file:
        code = file.read()
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            exec(code, {})
            printed_output = new_stdout.getvalue().strip()
            if printed_output:
                result = printed_output
            else:
                result = "Executed successfully, no output."
        except Exception as e:
            result = "An error occurred: " + str(e)

        sys.stdout = old_stdout

    return str(result)


def get_editor_html(files):
    files_html = ''.join(f'<li><a href="/execute/{file}">{file}</a></li>' for file in files)
    default_filename = get_next_filename()
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Python File Executor</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            #wrapper {{
                width: 100%;
                max-width: 450px;
                text-align: center;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
            }}
            button {{
                padding: 5px 15px;
                margin-left: 5px;
                background-color: #007BFF;
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 3px;
                transition: background-color 0.3s;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
            textarea {{
                width: 100%;
                padding: 5px;
                border-radius: 3px;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }}
        </style>
    </head>
    <body>
        <div id="wrapper">
            <h1>Create a new file:</h1>
            <form action="/create" method="post">
                <label for="filename">File name:</label>
                <input type="text" name="filename" id="filename" value="{default_filename}" required>
                <label for="content">Content:</label>
                <textarea name="content" id="content" rows="10"></textarea>
                <button type="submit">Create File</button>
            </form>
            <h2>Files:</h2>
            <ul style="text-align: left;">
                {files_html}
            </ul>
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

