from microdot_asyncio import Microdot, Response
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

app = Microdot()
Response.default_content_type = 'text/html'

CSV_FILE = 'microscope_state.csv'
IMG_FILE = 'image.png'

# Assuming you have a 4D numpy array with dimensions (batch_size, height, width, channels)
# For simplicity, let's create a random 4D numpy array
image_data = np.random.rand(10, 64, 64, 3)

# Initialize the DataFrame
system_df = pd.DataFrame([{
    'light_source': 'OFF',
    'heater': 'OFF',
    'objective_lens': 'OFF',
    'magnification_level': '0',
    'sample_temperature': '0',
    'focus_depth': '0',
    'current_image': 0  # index of the current image in the image_data
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
                <title>Microscopy System Control</title>
                <title>Microscopy System Control</title>
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
                <h1>Microscopy System Control</h1>
                <div class="container">
                     <a href="/toggle/light_source">
                        <button class="{data['light_source']}">
                            Light Source: {data['light_source']}
                        </button>
                    </a>
                    <br>
                    <a href="/toggle/heater">
                        <button class="{data['heater']}">
                            Heater: {data['heater']}
                        </button>
                    </a>
                    <br>
                    <a href="/toggle/objective_lens">
                        <button class="{data['objective_lens']}">
                            Objective Lens: {data['objective_lens']}
                        </button>
                    </a>
                    <br><br>
                    <div class="parameter">System Parameters:</div>
                    <ul>
                        <li>Magnification Level: {data['magnification_level']}</li>
                        <li>Sample Temperature: {data['sample_temperature']}</li>
                        <li>Focus Depth: {data['focus_depth']}</li>
                    </ul>
                    <br><br>
                    <div class="parameter">Current Image:</div>
                    <img src="/image" alt="Current Image" style="width: 300px; height: 300px;">
                    <a href="/next_image">
                        <button>
                            Next Image
                        </button>
                    </a>
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

@app.route('/image')
def get_image(request):
    load_state_from_csv()
    current_image_index = system_df.at[0, 'current_image']
    img = image_data[current_image_index]

    # Save the image to a temporary buffer
    buf = BytesIO()
    plt.imshow(img)
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Return the image file
    return Response(body=buf, headers={'Content-Type': 'image/png'})

@app.route('/next_image')
def next_image(request):
    load_state_from_csv()
    current_image_index = system_df.at[0, 'current_image']
    # Increment the current_image index, wrap around to 0 if it exceeds the batch size
    system_df.at[0, 'current_image'] = (current_image_index + 1) % image_data.shape[0]
    save_state_to_csv()
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

