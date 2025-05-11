from flask import Flask, request, jsonify, abort
from env import secret_token
import trilium
import time
import hmac

app = Flask(__name__)


def validate_token(token: str) -> bool:
    if not hmac.compare_digest(token, secret_token):
        # Bad token → delay before rejecting
        time.sleep(2)
        return False

    return True


@app.before_request
def require_token():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401, description="Missing Bearer token")
    token = auth.split(None, 1)[1]
    if not validate_token(token):
        abort(401, description="Invalid or expired token")


@app.route("/search")
def search():
    keyword = request.args.get("keyword", "").strip()
    if not keyword:
        return jsonify({"error": "Missing 'keyword' parameter"}), 400

    results = trilium.search(keyword)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
