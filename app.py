from flask import Flask, render_template
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

if __name__ == "__main__":
    app.run(debug=True)
