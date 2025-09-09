from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    db_user = os.getenv("POSTGRES_USER", "user")
    db_pass = os.getenv("POSTGRES_PASSWORD", "pass")
    db_name = os.getenv("POSTGRES_DB", "mydb")
    db_host = os.getenv("DB_HOST", "db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo simples
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route("/")
def home():
    return "Aplicação Flask conectada ao Postgres!"

@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify(error="Campo 'name' é obrigatório"), 400

    user = User(name=data["name"])
    db.session.add(user)
    db.session.commit()
    return jsonify(id=user.id, name=user.name), 201

@app.route("/list_users")
def list_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name} for u in users])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # cria a tabela automaticamente
    app.run(host="0.0.0.0", port=5000) # nosec B104
