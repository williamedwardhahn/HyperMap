from microdot import Microdot, Response
import pandas as pd
import os

app = Microdot()
Response.default_content_type = 'text/html'

csv_file = 'cards.csv'

def create_card_csv(card_name, title, text, image):
    new_card = pd.DataFrame([{
        'card_name': card_name,
        'title': title,
        'text': text,
        'image': image
    }])
    
    if os.path.isfile(csv_file):
        card_df = pd.read_csv(csv_file)
        card_df = pd.concat([card_df, new_card])
    else:
        card_df = new_card

    card_df.to_csv(csv_file, index=False)

def load_card_from_csv(card_name):
    card_df = pd.read_csv(csv_file)
    return card_df.loc[card_df['card_name'] == card_name].iloc[0]

def get_cards():
    if os.path.isfile(csv_file):
        card_df = pd.read_csv(csv_file)
        return card_df['card_name'].tolist()
    return []

def card_doc(data, card_name):
    cards = get_cards()
    card_index = cards.index(card_name)
    prev_card = cards[card_index - 1] if card_index - 1 >= 0 else cards[-1]
    next_card = cards[card_index + 1] if card_index + 1 < len(cards) else cards[0]
    
    doc = f"""
        <html>
            <head>
                <title>{data['title']}</title>
                <style>
                    img {{
                        max-width: 100%;
                        height: auto;
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                    }}
                    body {{
                        font-family: Arial, sans-serif;
                        display: grid;
                        place-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #f4f4f4;
                    }}
                    .card {{
                        background-color: white;
                        padding: 20px;
                        max-width: 800px;
                        width: 100%;
                        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
                        position: relative;
                    }}
                    .nav-button {{
                        width: 50px;
                        height: 50px;
                        position: absolute;
                        bottom: 10px;
                        opacity: 0;
                        background-color: transparent;
                        border: none;
                    }}
                    .nav-button:hover {{
                        opacity: 0.5;
                        background-color: #ddd;
                        cursor: pointer;
                    }}
                    #prev-button {{
                        left: 10px;
                    }}
                    #next-button {{
                        right: 10px;
                    }}
                    h1 {{
                        color: #333;
                        margin-top: 0;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>{data['title']}</h1>
                    <p>{data['text']}</p>
                    <img src="{data['image']}" alt="Card image">
                    <button id="prev-button" class="nav-button" onclick="location.href='/card/{prev_card}'"></button>
                    <button id="next-button" class="nav-button" onclick="location.href='/card/{next_card}'"></button>
                </div>
            </body>
        </html>
    """
    
    return doc


def create_card_doc():
    doc = '''
<html>
    <head>
        <title>Create a new Card</title>
        <style>
            :root {
                --primary-color: #4CAF50;
            }

            body {
                font-family: 'Roboto', sans-serif;
                padding: 20px;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }

            h1 {
                color: var(--primary-color);
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            form {
                background: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);
            }

            label {
                display: block;
                font-weight: bold;
                margin-bottom: 5px;
            }

            input, textarea {
                width: 100%;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
                margin: 10px 0;
                padding: 12px 20px;
                display: inline-block;
                transition: 0.3s all ease-in-out;
                box-shadow: 0px 0px 5px 0px rgba(0,0,0,0.1);
            }

            input:focus, textarea:focus {
                outline: none;
                border: 1px solid var(--primary-color);
            }

            textarea {
                height: 100px;
            }

            input[type="submit"] {
                background-color: var(--primary-color);
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 10px 0;
                cursor: pointer;
                transition: 0.3s all ease-in-out;
            }

            input[type="submit"]:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>Create a new Card</h1>
        <form action="/create_card" method="post">
            <label for="card_name">Card Name:</label>
            <input type="text" id="card_name" name="card_name" required>
            <label for="title">Title:</label>
            <input type="text" id="title" name="title" required>
            <label for="text">Text:</label>
            <textarea id="text" name="text" required></textarea>
            <label for="image">Image URL:</label>
            <input type="text" id="image" name="image" required>
            <input type="submit" value="Create Card">
        </form>
    </body>
</html>

    '''
    return doc




default_cards = [
    {
        'card_name': 'Introduction',
        'title': 'Introduction to HyperCard',
        'text': 'HyperCard is an application program and programming tool for Apple Macintosh and Apple IIGS computers...',
        'image': 'https://i.ytimg.com/vi/tx_WCIAM4bA/maxresdefault.jpg'
    },
    {
        'card_name': 'Features',
        'title': 'HyperCard Features',
        'text': 'HyperCard also includes a built-in programming language called HyperTalk for manipulating data...',
        'image': 'https://cdn.osxdaily.com/wp-content/uploads/2017/05/hypercard-on-mac-browser-emu-1-610x414.jpg'
    },
    {
        'card_name': 'Legacy',
        'title': 'HyperCard Legacy',
        'text': 'Though HyperCard was initially released in 1987 and later discontinued in 2004, it left a substantial impact...',
        'image': 'https://cdn.arstechnica.net//wp-content/uploads/2012/05/cosmic-osmo.png'
    }
]


for card in default_cards:
    card_name = card['card_name']
    create_card_csv(card_name, card['title'], card['text'], card['image'])
    
    
@app.route('/')
def home(request):
    doc = f'''
        <html>
            <head>
                <title>HyperCard Demo</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        padding: 10px;
                    }}
                    h1 {{
                        color: #333;
                    }}
                    ul {{
                        list-style-type: none;
                        padding: 0;
                    }}
                    ul li {{
                        margin-bottom: 10px;
                    }}
                    ul li a {{
                        text-decoration: none;
                        color: #333;
                    }}
                    ul li a:hover {{
                        color: #666;
                    }}
                </style>
            </head>
            <body>
                <h1>HyperCard Demo</h1>
                <ul>
                    {''.join([f'<li><a href="/card/{card}">{card}</a></li>' for card in get_cards()])}
                </ul>
                <a href="/new_card">Create a new Card</a>
            </body>
        </html>
    '''
    return doc



@app.route('/new_card')
def new_card(request):
    return create_card_doc()

@app.route('/card/<card_name>')
def card(request, card_name):
    card_data = load_card_from_csv(card_name)
    return card_doc(card_data, card_name)

@app.route('/create_card', methods=['POST'])
def create_card(request):
    card_name = request.form.get('card_name')
    title = request.form.get('title')
    text = request.form.get('text')
    image = request.form.get('image')
    create_card_csv(card_name, title, text, image)
    return f'Card {card_name} has been created. <a href="/card/{card_name}">View Card</a>'

app.run(debug=True, port=8008)
