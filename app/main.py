
from flask import Flask, request, send_file
from flask_cors import CORS
from io import BytesIO
import requests
import os
from rembg import remove  # Make sure rembg is installed

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def server_running():
    return {'status': 'Server is running ✅'}, 200


@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    file = request.files['image']
    input_bytes = file.read()
    output_bytes = remove(input_bytes)
    return send_file(BytesIO(output_bytes), mimetype='image/png')

@app.route('/remove-bg-url', methods=['POST'])
def remove_bg_url():
    data = request.json
    image_url = data.get('url')
    print("Image URL:", image_url)

    if not image_url:
        return "No URL provided", 400

    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            return "Failed to download image", 400

        input_bytes = response.content
        output_bytes = remove(input_bytes)
        return send_file(BytesIO(output_bytes), mimetype='image/png')

    except Exception as e:
        return f"Error: {str(e)}", 500

# Use dynamic port from Railway
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Uses Railway's PORT
    app.run(host='0.0.0.0', port=port)        # Listens on 0.0.0.0
