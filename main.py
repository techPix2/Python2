from flask import Flask, jsonify
from extract import coletar_todas_metricas

app = Flask(__name__)

@app.route("/api/dados", methods=["GET"])
def get_dados():
    dados = coletar_todas_metricas()
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)