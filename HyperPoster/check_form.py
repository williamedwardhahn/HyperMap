from flask import *

app = Flask(__name__)


html_code = '''
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>Checkbox</title>
<style>
input[type=checkbox] {
  height: 0;
  width: 0;
  visibility: hidden;
}

label {
  cursor: pointer;
  text-indent: -9999px;
  width: 200px;
  height: 100px;
  background: grey;
  display: block;
  border-radius: 100px;
  position: relative;
}

label:after {
  content: "";
  position: absolute;
  top: 5px;
  left: 5px;
  width: 90px;
  height: 90px;
  background: #fff;
  border-radius: 90px;
  transition: 0.3s;
}

input:checked + label {
  background: #bada55;
}

input:checked + label:after {
  left: calc(100% - 5px);
  transform: translateX(-100%);
}

label:active:after {
  width: 130px;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>

</head>
<body>





<form method="post">

	<input type="checkbox" id="switch" name="switch" /><label for="switch">Toggle</label>

    Name: <input name="name"/>

    <br/><br/>

    Email: <input name="email"/>

    <br/><br/>

    <button type="submit">Submit</button>
</form>

</body>
</html>
'''


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["email"])
        print(request.form["switch"])

    return render_template_string(html_code)

if __name__ == "__main__":
    app.run()
