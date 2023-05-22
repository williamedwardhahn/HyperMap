from microdot_asyncio import Microdot, Response
import pandas as pd
import os

app = Microdot()
Response.default_content_type = 'text/html'

def create_card_csv(card_file, title, text, image):
    card_df = pd.DataFrame([{
        'title': title,
        'text': text,
        'image': image
    }])
    card_df.to_csv(card_file, index=False)

def load_card_from_csv(card_file):
    card_df = pd.read_csv(card_file)
    return card_df.iloc[0]

def card_doc(data, card_name):
    card_index = cards.index(card_name)
    prev_card = cards[card_index - 1] if card_index - 1 >= 0 else cards[-1]
    next_card = cards[card_index + 1] if card_index + 1 < len(cards) else cards[0]
    
    doc = f'''
        <html>
            <head>
                <title>{data['title']}</title>
                <style>
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
                    img {{
                        max-width: 100%;
                        height: auto;
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
    '''
    return doc


def create_card_doc():
    doc = '''
        <html>
            <head>
                <title>Create a new Card</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        padding: 10px;
                    }}
                    h1 {{
                        color: #333;
                    }}
                    input, textarea {{
                        width: 100%;
                        margin-bottom: 10px;
                        padding: 5px;
                    }}
                    textarea {{
                        height: 100px;
                    }}
                    input[type="submit"] {{
                        background-color: #4CAF50; /* Green */
                        border: none;
                        color: white;
                        padding: 15px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                    }}
                </style>
            </head>
            <body>
                <h1>Create a new Card</h1>
                <form action="/create_card" method="post">
                    Card Name: <input type="text" name="card_name" required><br>
                    Title: <input type="text" name="title" required><br>
                    Text: <textarea name="text" required></textarea><br>
                    Image URL: <input type="text" name="image" required><br>
                    <input type="submit" value="Create Card">
                </form>
            </body>
        </html>
    '''
    return doc

@app.route('/')
def home(request):
    return create_card_doc()

@app.route('/card/<card_name>')
def card(request, card_name):
    card_file = f'{card_name}_state.csv'
    if not os.path.isfile(card_file):
        return create_card_doc()
    card_data = load_card_from_csv(card_file)
    return card_doc(card_data, card_name)

cards = []

@app.route('/create_card', methods=['POST'])
def create_card(request):
    global cards
    card_name = request.form.get('card_name')
    card_file = f'{card_name}_state.csv'
    if os.path.isfile(card_file):
        return f'Card {card_name} already exists.'
    title = request.form.get('title')
    text = request.form.get('text')
    image = request.form.get('image')
    create_card_csv(card_file, title, text, image)
    cards.append(card_name)
    return f'Card {card_name} has been created. <a href="/card/{card_name}">View Card</a>'


app.run(debug=True, port=8008)
