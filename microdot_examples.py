from microdot_asyncio import Microdot, Response
import random

app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc(guesses, message, color):
    return f'''
        <html>
            <head>
                <title>High Low Guessing Game</title>
            </head>
            <body>
                <div>
                    <h1>High Low Guessing Game</h1>
                    <p>{message}</p>
                    <form method="post" action="/">
                        <label for="guess">Guess a number between 1 and 100:</label>
                        <input type="number" name="guess" id="guess" min="1" max="100" required>
                        <button type="submit">Submit</button>
                    </form>
                    <p>Guesses: {guesses}</p>
                    <svg width="100" height="100" viewBox="0 0 512 512">
                        <circle style="fill:#{color}" cx="255.995" cy="255.995" r="200"/>
                    </svg>
                    <form method="post" action="/new_game">
                        <button type="submit">New Game</button>
                    </form>
                </div>
            </body>
        </html>
        '''

random_number = random.randint(1, 100)
guesses = 0

@app.route('/', methods=['GET', 'POST'])
async def home(request):
    global random_number, guesses

    if request.method == 'POST':
        guess = int(request.form.get('guess'))

        if guess < random_number:
            message = 'Too low!'
            color = '853737' # Red
        elif guess > random_number:
            message = 'Too high!'
            color = '907A4A' # Yellow
        else:
            message = 'Correct!'
            color = '4E7039' # Green

        guesses += 1

    else:
        message = 'Guess a number between 1 and 100.'
        color = '515262' # Grey

    return htmldoc(guesses, message, color)

@app.route('/new_game', methods=['POST'])
async def new_game(request):
    global random_number, guesses
    random_number = random.randint(1, 100)
    guesses = 0
    return htmldoc(guesses, 'Guess a number between 1 and 100.', '515262') # Grey

app.run(debug=True, port=8008)



from microdot_asyncio import Microdot, Response
import random
app = Microdot()
Response.default_content_type = 'text/html'

def random_color():
    return ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

def htmldoc(dice_faces, background_colors):
    dice_faces_svg = {
        1: '''
            <circle cx="100" cy="100" r="10" fill="black" />
        ''',
        2: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        3: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="100" cy="100" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        4: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        5: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="100" cy="100" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        6: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="50" cy="100" r="10" fill="black" />
            <circle cx="150" cy="100" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        '''
    }

    dice_svgs = ''
    for i in range(len(dice_faces)):
        x_offset = 220 * i
        dice_svgs += f'''
            <svg x="{x_offset}" width="200" height="200" viewBox="0 0 200 200">
                <rect x="10" y="10" width="180" height="180" rx="20" ry="20" fill="#{background_colors[i]}" />
                {dice_faces_svg[dice_faces[i]]}
            </svg>
        '''

    return f'''
        <html>
            <head>
                <title>SVG Dice Roll</title>
            </head>
            <body>
                <div>
                    <h1>Click the Buttons to Roll Dice</h1>
                    <div>
                        {dice_svgs}
                    </div>
                    <div>
                        <a href="/roll/1"><button>Roll 1 Dice</button></a>
                        <a href="/roll/2"><button>Roll 2 Dice</button></a>
                        <a href="/roll/3"><button>Roll 3 Dice</button></a>
                        <a href="/roll/4"><button>Roll 4 Dice</button></a>
                        <a href="/roll/5"><button>Roll 5 Dice</button></a>
                        <a href="/roll/6"><button>Roll 6 Dice</button></a>
                    </div>
                </div>
            </body>
        </html>
    '''

@app.route('/')
async def home(request):
    return htmldoc([1], ['F0E68C'])

@app.route('/roll/<num_dice>')
async def roll_dice(request, num_dice):
    num_dice = int(num_dice)
    dice_faces = [random.randint(1, 6) for _ in range(num_dice)]
    background_colors = [random_color() for _ in range(num_dice)]
    return htmldoc(dice_faces, background_colors)


app.run(debug=True, port=8008)



from microdot_asyncio import Microdot, Response
app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc():

    reds     = ["853737","ff6465"]
    yellows  = ["907A4A","ffd782"]
    greens   = ["4E7039","a5eb78"]

    red     =     reds[lights[0]]
    yellow  =  yellows[lights[1]]
    green   =   greens[lights[2]]

    return f'''
        <html>
            <head>
                <title>Hahn Traffic Light</title>
            </head>
            <body>
                <div>
                    <h1>Hahn's Traffic Light</h1>
                    <svg width="100" height="100" viewBox="0 0 512 512">
                      <path style="fill:#515262" d="M324.683 41.53H187.317c-28.304 0-51.249 22.946-51.249 51.249V460.75c0 28.305 22.946 51.249 51.249 51.249h137.366c28.304 0 51.249-22.946 51.249-51.249V92.779c0-28.303-22.945-51.249-51.249-51.249z"/>
                      <a href="/toggle/0">
                          <circle style="fill:#{red}" cx="255.995" cy="133.818" r="48.281"/>
                      </a>
                      <a href="/toggle/1">
                          <circle style="fill:#{yellow}" cx="255.995" cy="276.765" r="48.281"/>
                      </a>
                      <a href="/toggle/2">
                          <circle style="fill:#{green}" cx="255.995" cy="419.712" r="48.281"/>
                      </a>
                    </svg>
                </div>
            </body>
        </html>
        '''

lights = [0,0,1]

@app.route('/')
def hello(request):
    return htmldoc()


@app.route('/toggle/<light_index>')
def toggle_light(request, light_index):
    light_index = int(light_index)
    lights[light_index] = 1 - lights[light_index]
    return htmldoc()

app.run(debug=True, port=8008)



from microdot_asyncio import Microdot, Response
app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc(counter):
    return f'''
        <html>
            <head>
                <title>Counter Demo</title>
            </head>
            <body>
                <div>
                    <h1>Counter: {counter}</h1>
                    <a href="/change/{counter}/1"><button>Increment</button></a>
                    <a href="/change/{counter}/-1"><button>Decrement</button></a>
                </div>
            </body>
        </html>
        '''

@app.route('/')
def home(request):
    return htmldoc(0)

@app.route('/change/<current_counter>/<step>')
def change(request, current_counter, step):
    counter = int(current_counter) + int(step)
    return htmldoc(counter)

app.run(debug=True, port=8008)
