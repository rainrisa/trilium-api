from flask import Flask, request, jsonify
import trilium

app = Flask(__name__)


@app.route("/search")
def search():
    keyword = request.args.get("keyword", "").strip()
    if not keyword:
        return jsonify({"error": "Missing 'keyword' parameter"}), 400

    results = trilium.search(keyword)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
