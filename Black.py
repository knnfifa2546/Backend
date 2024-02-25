from flask import request, Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

MONGO_URI = "mongodb+srv://Shop1:kunanon2121@cluster0.qq9ckiq.mongodb.net/"
DB_NAME = "Shop"

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client[DB_NAME]
collection = db['Labtop']

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    return response

@app.route('/product', methods=['OPTIONS'])
def handle_options():
    return jsonify(), 200

@app.route("/")
def greet():
    return "<p>Welcome to Product Management Systems</p>"

@app.route("/product", methods=["GET"])
def get_all_product():
    products = list(collection.find())
    return jsonify({"product": products})

@app.route("/product", methods=["POST"])
def create_product():
    data = request.get_json()
    new_product = {
        "_id": data["id"],
        "name": data["name"],
        "price": data["price"],
        "img": data["img"]
    }

    existing_product = collection.find_one({"_id": new_product["_id"]})

    if existing_product:
        return jsonify({"error": "Cannot create a new product with an existing ID"}), 500

    try:
        collection.insert_one(new_product)
        return jsonify({"product": new_product}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to create a new product: {str(e)}"}), 500

@app.route("/product/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    print(f"Deleting product with ID: {product_id}")  
    result = collection.delete_one({"_id": product_id})
    if result.deleted_count > 0:
        print("Product deleted successfully")  
        products = list(collection.find())
        return jsonify({"message": "Product deleted successfully", "product": products}), 200
    else:
        print("Product not found")  
        return jsonify({"error": "Product not found"}), 404

@app.route("/product/<product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()
    updated_product = {
        "_id": data["id"],
        "name": data["name"],
        "price": data["price"],
        "img": data["img"]
    }

    result = collection.update_one({"_id": product_id}, {"$set": updated_product})
    if result.modified_count > 0:
        print(f"Product with ID {product_id} updated successfully")
        updated_product["_id"] = product_id
        return jsonify(updated_product), 200
    else:
        print(f"Product with ID {product_id} not found")
        return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)