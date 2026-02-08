from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# SQLite DB (persistent, simple, interview-friendly)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ims.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ------------------------
# Database Model
# ------------------------
class IMSRegistration(db.Model):
    subscriber_id = db.Column(db.String, primary_key=True)
    status = db.Column(db.String)
    updated_at = db.Column(db.DateTime)

# Create table
with app.app_context():
    db.create_all()

# ------------------------
# APIs
# ------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200


@app.route("/ims/register", methods=["POST"])
def ims_register():
    data = request.get_json(force=True, silent=True)

    if not isinstance(data, dict) or "subscriberId" not in data:
        return jsonify({"error": "subscriberId missing"}), 400

    subscriber_id = str(data["subscriberId"])

    record = IMSRegistration.query.get(subscriber_id)

    if not record:
        # First request → async start
        record = IMSRegistration(
            subscriber_id=subscriber_id,
            status="IN_PROGRESS",
            updated_at=datetime.utcnow()
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({
            "subscriberId": subscriber_id,
            "status": "IN_PROGRESS"
        }), 202

    return jsonify({
        "subscriberId": subscriber_id,
        "status": record.status
    }), 202


@app.route("/ims/status/<subscriber_id>", methods=["GET"])
def ims_status(subscriber_id):
    record = IMSRegistration.query.get(subscriber_id)

    if not record:
        return jsonify({"error": "not found"}), 404

    # Simulate async completion
    if record.status == "IN_PROGRESS":
        record.status = "REGISTERED"
        record.updated_at = datetime.utcnow()
        db.session.commit()

    return jsonify({
        "subscriberId": subscriber_id,
        "status": record.status
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
