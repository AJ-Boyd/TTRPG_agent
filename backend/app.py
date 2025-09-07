from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import run_agent  # Assuming you have a function to handle prompts

app = Flask(__name__)
CORS(app)

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/api/adventure", methods=["POST"])
def adventure():
    data = request.get_json()
    user_input = data.get("message", "")
    response = run_agent(user_input)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
