from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ==============================
# Model
# ==============================
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}


# ==============================
# Web (HTML) routes – optional UI
# ==============================
@app.route("/")
def index():
    products = Product.query.all()
    # Simple HTML (can be your Bootstrap template if you prefer)
    html = "<h2>Product List</h2><ul>"
    for p in products:
        html += f"<li>{p.name} - ${p.price}</li>"
    html += "</ul><p>Use /api/products for API endpoints.</p>"
    return html


# ==============================
# API routes – used by your tests
# ==============================

# ONE function handling both GET and POST for /api/products
@app.route("/api/products", methods=["GET", "POST"])
def api_products():
    if request.method == "GET":
        # List all products
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products])

    # POST: create new product
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Invalid input"}), 400

    product = Product(name=data["name"], price=float(data["price"]))
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201


# (Optional for later) – full CRUD API
@app.route("/api/products/<int:product_id>", methods=["GET"])
def api_get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@app.route("/api/products/<int:product_id>", methods=["PUT"])
def api_update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json() or {}
    product.name = data.get("name", product.name)
    product.price = float(data.get("price", product.price))
    db.session.commit()
    return jsonify(product.to_dict())


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def api_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"})


# ==============================
# Main entry
# ==============================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
