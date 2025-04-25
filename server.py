from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)

# ✅ Configuración de CORS específica para el frontend
CORS(app, resources={r"/*": {"origins": "https://prototipojesus.zerotoplan.com"}})

# Opcional mientras pruebas: permitir todo
# CORS(app, resources={r"/*": {"origins": "*"}})

EMBEDDINGS_DIR = "embeddings"
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

@app.route("/")
def index():
    return "Servidor activo desde Render 🚀"

@app.route("/guardar_registro", methods=["POST", "OPTIONS"])
def guardar_registro():
    data = request.json

    nombre = data.get("nombre")
    cedula = data.get("identificacion")
    embedding = data.get("embedding")

    if not nombre or not cedula or not embedding:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    path = os.path.join(EMBEDDINGS_DIR, f"{cedula}.json")
    contenido = {
        "nombre": nombre,
        "identificacion": cedula,
        "embedding": embedding
    }

    with open(path, "w") as f:
        json.dump(contenido, f, indent=4)

    return jsonify({"mensaje": "Registro guardado exitosamente"}), 200

@app.route("/obtener_registros", methods=["GET"])
def obtener_registros():
    registros = []
    for filename in os.listdir(EMBEDDINGS_DIR):
        if filename.endswith(".json"):
            path = os.path.join(EMBEDDINGS_DIR, filename)
            with open(path, "r") as f:
                data = json.load(f)
                registros.append(data)
    return jsonify(registros), 200
