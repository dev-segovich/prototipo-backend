from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app,  origins="*")

# Carpeta donde se guardarán los archivos
EMBEDDINGS_DIR = "embeddings"
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)


@app.route("/")
def index():
    return "¡Backend Flask corriendo en Render!"

@app.route("/guardar_registro", methods=["POST"])
def guardar_registro():
    data = request.json

    nombre = data.get("nombre")
    cedula = data.get("identificacion")
    embedding = data.get("embedding")

    if not nombre or not cedula or not embedding:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # Ruta del archivo por cédula
    path = os.path.join(EMBEDDINGS_DIR, f"{cedula}.json")

    # Estructura que se guarda
    contenido = {
        "nombre": nombre,
        "identificacion": cedula,
        "embedding": embedding
    }

    # Guardar como JSON
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


if __name__ == "__main__":
    app.run(
        debug=True
    )


