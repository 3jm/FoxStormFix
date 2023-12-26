from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

API_URL = "https://fortnite-api.com/v2/stats/br/v2"
API_KEY = "api key here"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/fortnite/stats/<username>')
def get_fortnite_stats(username):
    print(f"Reached get_fortnite_stats for {username}")
    url = f'{API_URL}?name={username}'
    try:
        response = requests.get(url, headers={"Authorization": API_KEY})
        response.raise_for_status()
        stats = response.json()
        return render_template('stats.html', stats=stats)
    except requests.RequestException as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    username = data.get("username")

    if username:
        try:
            response = requests.get(f"{API_URL}?name={username}", headers={"Authorization": API_KEY})
            response.raise_for_status()

            if response.status_code == 200:
                stats = response.json()
                return redirect(url_for('get_fortnite_stats', username=username))
            else:
                return jsonify({'error': 'Failed to retrieve stats.'}), response.status_code
        except requests.RequestException as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Username is required.'}), 400


if __name__ == "__main__":
    app.run(debug=True)