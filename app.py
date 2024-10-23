import os
from flask import Flask, render_template, jsonify, request
import requests
import random

app = Flask(__name__)

def get_meme():
    # Fetch meme templates from the Memegen API
    url = "https://api.memegen.link/templates"
    response = requests.get(url).json()
    
    # Choose a random meme template
    meme_template = random.choice(response)
    
    # Create a meme URL using the template's example text
    example_text = meme_template["example"]["text"]
    meme_url = meme_template["example"]["url"]  # Use the example URL provided by the API

    return meme_url, meme_template["name"]

@app.route("/")
def index():
    meme_pic, meme_name = get_meme()  # Get a random meme
    return render_template("index.html", meme_pic=meme_pic, meme_name=meme_name)

@app.route("/get_meme")
def get_new_meme():
    meme_pic, meme_name = get_meme()  # Get a new random meme
    return jsonify(meme_pic=meme_pic, meme_name=meme_name)  # Return as JSON

@app.route('/get_shareable_link', methods=['POST'])
def get_shareable_link():
    data = request.json
    meme_url = data.get('meme_url')
    
    # Generate a unique filename
    filename = "meme.jpg"
    
    # Save the image to a public directory
    public_dir = os.path.join(app.static_folder, 'shared_memes')
    os.makedirs(public_dir, exist_ok=True)
    
    # Download and save the image
    import requests
    response = requests.get(meme_url)
    if response.status_code == 200:
        with open(os.path.join(public_dir, filename), 'wb') as f:
            f.write(response.content)
    
    # Generate the shareable link
    shareable_link = f"{request.host_url}static/shared_memes/{filename}"
    
    return jsonify({'shareable_link': shareable_link})

if __name__ == "__main__":
    app.run(debug=True)
