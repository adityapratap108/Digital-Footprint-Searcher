import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import urllib.request
import urllib.error
import threading

# Flask ko batana ki static aur templates folder kahan hain
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Platforms ki list
PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Instagram": "https://www.instagram.com/{}/",
    "Facebook": "https://www.facebook.com/{}",
    "Snapchat": "https://www.snapchat.com/add/{}"
}

# Route 1: Frontend load karne ke liye
@app.route('/')
def index():
    return render_template('index.html')

# Helper function site check karne ke liye
def check_site(name, url_template, username, results):
    url = url_template.format(username)
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.getcode() == 200:
                results.append({"platform": name, "url": url, "status": "Found"})
    except:
        results.append({"platform": name, "url": url, "status": "Not Found"})

# Route 2: Search API
@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "No username"}), 400
    
    results = []
    threads = []
    for name, url in PLATFORMS.items():
        t = threading.Thread(target=check_site, args=(name, url, username, results))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
        
    return jsonify(results)

if __name__ == '__main__':
    # Render dynamic port use karta hai, isliye os.environ zaroori hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
