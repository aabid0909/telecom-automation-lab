from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory job store (safe for demo)
jobs = {}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200


# IMS Register

@app.route("/ims/register", methods=["POST"])
def ims_register():
    data = request.get_json(force=True, silent=True)

    if not isinstance(data, dict) or "subscriberId" not in data:
        return jsonify({"error": "subscriberId missing"}), 400

    subscriber_id = str(data["subscriberId"])

    jobs[subscriber_id] = "IN_PROGRESS"

    return jsonify({
        "subscriberId": subscriber_id,
        "status": "IN_PROGRESS"
    }), 202


@app.route("/ims/status/<subscriber_id>", methods=["GET"])
def ims_status(subscriber_id):
    # First poll -> complete
    if jobs.get(subscriber_id) == "IN_PROGRESS":
        jobs[subscriber_id] = "REGISTERED"

    return jsonify({
        "subscriberId": subscriber_id,
        "status": jobs.get(subscriber_id, "UNKNOWN")
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
