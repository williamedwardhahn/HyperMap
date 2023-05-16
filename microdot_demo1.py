from microdot_asyncio import Microdot, Response
import pandas as pd
import os

app = Microdot()
Response.default_content_type = 'text/html'

CSV_FILE = 'state.csv'

# Initialize the DataFrame
system_df = pd.DataFrame([{
    'water_pump': 'OFF',
    'air_pump': 'OFF',
    'light': 'OFF',
    'water_level': '0',
    'temperature': '0',
    'pH_level': '0',
}])

def load_state_from_csv():
    global system_df
    system_df = pd.read_csv(CSV_FILE)


def save_state_to_csv():
    system_df.to_csv(CSV_FILE, index=False)

def htmldoc(data):

    doc = f'''
        <html>
            <head>
                <title>Aquaponics System Control</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                    }}
                    h1 {{
                        background-color: #4CAF50;
                        color: white;
                        padding: 20px;
                    }}
                    .container {{
                        padding: 20px;
                    }}
                    button {{
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 10px 2px;
                        cursor: pointer;
                        border-radius: 4px;
                        width: 200px;
                    }}
                    .ON {{
                        background-color: #4CAF50;
                    }}
                    .ON:hover {{
                        background-color: #45a049;
                    }}
                    .OFF {{
                        background-color: #f44336;
                    }}
                    .OFF:hover {{
                        background-color: #da190b;
                    }}
                    .parameter {{
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <h1>Aquaponics System Control</h1>
                <div class="container">
                    <a href="/toggle/water_pump">
                        <button class="{data['water_pump']}">
                            Water Pump: {data['water_pump']}
                        </button>
                    </a>
                    <br>
                    <a href="/toggle/air_pump">
                        <button class="{data['air_pump']}">
                            Air Pump: {data['air_pump']}
                        </button>
                    </a>
                    <br>
                    <a href="/toggle/light">
                        <button class="{data['light']}">
                            Light: {data['light']}
                        </button>
                    </a>
                    <br><br>
                    <div class="parameter">System Parameters:</div>
                    <ul>
                        <li>Water Level: {data['water_level']}</li>
                        <li>Temperature: {data['temperature']}</li>
                        <li>pH Level: {data['pH_level']}</li>
                    </ul>
                </div>
            </body>
        </html>
    '''
    return doc



def generate_html_doc():
    load_state_from_csv()
    data = system_df.iloc[0]
    return htmldoc(data)

@app.route('/')
def control(request):
    return generate_html_doc()

@app.route('/toggle/<component>')
def toggle(request, component):
        system_df.at[0, component] = 'ON' if system_df.at[0, component] == 'OFF' else 'OFF'
        save_state_to_csv()
        return generate_html_doc()

@app.route('/set_parameter/<parameter>/<value>')
def set_parameter(request, parameter, value):
        system_df.at[0, parameter] = str(value)
        save_state_to_csv()
        return generate_html_doc()


if not os.path.isfile(CSV_FILE):
        # If the file does not exist, create it
        save_state_to_csv()

app.run(debug=True, port=8008)
