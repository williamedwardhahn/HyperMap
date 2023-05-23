# Import necessary libraries
from microdot import Microdot, Response
import pandas as pd
import os

# Initialize the app
app = Microdot()
Response.default_content_type = 'text/html'

# Define a function to create a card csv
def create_card_csv(card_name, title, text, image):
    new_card = pd.DataFrame([{
        'card_name': card_name,
        'title': title,
        'text': text,
        'image': image
    }])
    
    # Check if the csv file already exists
    if os.path.isfile(csv_file):
        # If yes, read the existing file and append the new card
        card_df = pd.read_csv(csv_file)
        card_df = pd.concat([card_df, new_card])
    else:
        # If no, create a new DataFrame with the new card
        card_df = new_card

    # Save the DataFrame to a csv file
    card_df.to_csv(csv_file, index=False)


# Define a function to load a card from the csv file
def load_card_from_csv(card_name):
    card_df = pd.read_csv(csv_file)
    return card_df.loc[card_df['card_name'] == card_name].iloc[0]


# Define a function to get all the cards
def get_cards():
    if os.path.isfile(csv_file):
        card_df = pd.read_csv(csv_file)
        return card_df['card_name'].tolist()
    return []


# Define a function to create the HTML for a card document
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
                    #delete-button {{
                        top: 10px;
                        right: 10px;
                    }}
                    .nav-button:before {{
                        position: absolute;
                        content: attr(data-content);
                        opacity: 0;
                        transition: opacity 0.5s;
                    }}
                    .nav-button:hover:before {{
                        opacity: 1;
                    }}
                    #delete-button:before {{
                        content: 'Delete';
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
                    <button id="prev-button" class="nav-button" data-content="Prev" onclick="location.href='/card/{prev_card}'"></button>
                    <button id="next-button" class="nav-button" data-content="Next" onclick="location.href='/card/{next_card}'"></button>
                    <form action="/delete_card/{card_name}" method="post">
                        <button id="delete-button" class="nav-button" data-content="Delete" type="submit"></button>
                    </form>
                </div>
            </body>
        </html>
    """
    return doc


# Define a function to create the HTML for creating a new card document
def create_card_doc():
    doc = '''
        <!-- HTML content for creating a new card document -->
        <!-- This will be the content of the web page when creating a new card -->
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


# Define a list of default cards
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




# Define routes and their corresponding functions
@app.route('/')
def home(request):
    cards_df = pd.read_csv(csv_file) if os.path.isfile(csv_file) else pd.DataFrame() 
    grid_cells = []
    for _ in range(25):  # Creating a 5x5 grid
        if not cards_df.empty:
            card = cards_df.iloc[0]
            cards_df = cards_df.iloc[1:]
            cell = f'''
                <a href="/card/{card["card_name"]}" class="grid-item">
                    <div class="image-container">
                        <img src="{card["image"]}" alt="{card["card_name"]}">
                        <div class="overlay">
                            <div class="text">{card["title"]}</div>
                        </div>
                    </div>
                </a>
            '''
        else:
            cell = '<div class="grid-item"></div>'  # Empty cell
        grid_cells.append(cell)

    doc = f'''
        <html>
            <head>
                <title>HyperCard Demo</title>
                <style>
                    .grid-container {{
                        display: grid;
                        grid-template-columns: repeat(5, 1fr);
                        grid-template-rows: repeat(5, 1fr);
                        gap: 10px;
                        padding: 10px;
                    }}
                    .grid-item {{
                        background-color: #ddd;
                        border: 1px solid #333;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        text-decoration: none;
                        color: black;
                    }}
                    .grid-item img {{
                        max-width: 100%;
                        max-height: 100%;
                    }}
                    .image-container {{
                        position: relative;
                        width: 100%;
                    }}
                    .overlay {{
                        position: absolute;
                        bottom: 0;
                        left: 0;
                        right: 0;
                        background-color: rgba(255,255,255,0.8);
                        overflow: hidden;
                        width: 100%;
                        height: 0;
                        transition: .5s ease;
                    }}
                    .image-container:hover .overlay {{
                        height: 100%;
                    }}
                    .text {{
                        color: black;
                        font-size: 20px;
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        text-align: center;
                    }}
                </style>
            </head>
            <body>
                <h1>HyperCard Demo</h1>
                <div class="grid-container">
                    {''.join(grid_cells)}
                </div>
                <a href="/new_card">Create a new Card</a>
            </body>
        </html>
    '''
    return doc

    
def delete_card_csv(card_name):
    if os.path.isfile(csv_file):
        card_df = pd.read_csv(csv_file)
        card_df = card_df[card_df['card_name'] != card_name]
        card_df.to_csv(csv_file, index=False)

@app.route('/delete_card/<card_name>', methods=['POST'])
def delete_card(request, card_name):
    delete_card_csv(card_name)
    return f'Card {card_name} has been deleted. <a href="/">Return Home</a>'


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


# Set the csv file name
csv_file = 'cards.csv'
if not os.path.isfile(csv_file):
	# Create default cards
	for card in default_cards:
	    create_card_csv(card['card_name'], card['title'], card['text'], card['image'])

# Run the app
app.run(debug=True, port=8008)
