from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DATA_FILE = "/data/orders.txt"

@app.route("/orders", methods=["POST"])
def create_order():
    order = request.json
    with open(DATA_FILE, "a") as f:
        f.write(str(order) + "\n")
    return {"status": "order created"}, 201

@app.route("/orders", methods=["GET"])
def get_orders():
    if not os.path.exists(DATA_FILE):
        return {"orders": []}
    with open(DATA_FILE, "r") as f:
        orders = f.readlines()
    return jsonify(orders)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

