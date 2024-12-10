from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/proxy', methods=['POST'])
def proxy_post():
    # Extract the target URL and data from the request
    target_url = request.json.get('target_url')
    payload = request.json.get('payload')
    headers = request.json.get('headers', {})

    if not target_url or not payload:
        return jsonify({"error": "Missing target_url or payload in request"}), 400

    try:
        # Make the POST request to the target URL
        response = requests.post(target_url, json=payload, headers=headers)

        # Forward the response from the target URL back to the client
        return jsonify({
            "status_code": response.status_code,
            "response": response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
        }), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
