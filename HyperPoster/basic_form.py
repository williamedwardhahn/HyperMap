from flask import *

app = Flask(__name__)


html_code = '''
<h1>
    This is home.html
</h1>

<form method="post">

    Name: <input name="name"/>

    <br/><br/>

    Email: <input name="email"/>

    <br/><br/>

    <button type="submit">Submit</button>
</form>
'''


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["email"])

    return render_template_string(html_code)

if __name__ == "__main__":
    app.run()
