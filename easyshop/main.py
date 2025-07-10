from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "easyshop_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///easyshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))

# Create tables
with app.app_context():
    db.create_all()

# Homepage
@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

# Register
@app.route("/register", methods=["POST"])
def register():
    username = request.form["first_name"] + " " + request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]
    
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect("/")

# Login
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/")
    return "Login failed", 401

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Add Product
@app.route("/add-product", methods=["POST"])
def add_product():
    if "user_id" not in session:
        return redirect("/login")

    name = request.form["title"]
    category = request.form["category"]
    description = request.form["description"]
    image = request.files["image"]
    
    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(image_path)

    product = Product(
        name=name,
        category=category,
        description=description,
        image_url=image_path
    )
    db.session.add(product)
    db.session.commit()
    return redirect("/")

# Admin panel
@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect("/")
    users = User.query.all()
    products = Product.query.all()
    return render_template("admin.html", users=users, products=products)

if __name__ == "__main__":
    app.run(debug=True)