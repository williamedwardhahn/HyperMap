from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def image(): 
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
