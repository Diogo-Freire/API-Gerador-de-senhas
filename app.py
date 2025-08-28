from flask import Flask, render_template, request, jsonify
import random
import string
from flasgger import Swagger
import os

app = Flask(__name__)
swagger = Swagger(app)  # Inicializa o Swagger

# Função geradora de senha
def gerar_senha(tamanho=12, maiusculas=True, numeros=True, especiais=True):
    caracteres = string.ascii_lowercase
    if maiusculas:
        caracteres += string.ascii_uppercase
    if numeros:
        caracteres += string.digits
    if especiais:
        caracteres += "!@#$%&*?"

    return ''.join(random.choice(caracteres) for _ in range(tamanho))

# ---------------- INTERFACE WEB ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    senha = None
    if request.method == "POST":
        tamanho = int(request.form.get("tamanho", 12))
        maiusculas = "maiusculas" in request.form
        numeros = "numeros" in request.form
        especiais = "especiais" in request.form

        senha = gerar_senha(tamanho, maiusculas, numeros, especiais)

    return render_template("index.html", senha=senha)

# ---------------- API REST COM SWAGGER ----------------
@app.route("/api/gerar_senha", methods=["GET"])
def api_gerar_senha():
    """
    Gera uma senha personalizada.
    ---
    tags:
      - Senhas
    parameters:
      - name: tamanho
        in: query
        type: integer
        required: false
        default: 12
        description: Tamanho da senha (mínimo 4, máximo 64).
      - name: maiusculas
        in: query
        type: boolean
        required: false
        default: true
        description: Incluir letras maiúsculas.
      - name: numeros
        in: query
        type: boolean
        required: false
        default: true
        description: Incluir números.
      - name: especiais
        in: query
        type: boolean
        required: false
        default: true
        description: Incluir caracteres especiais.
    responses:
      200:
        description: Senha gerada com sucesso
        schema:
          type: object
          properties:
            senha:
              type: string
              example: "Ab9#pLx1"
      400:
        description: Erro ao gerar a senha
    """
    try:
        tamanho = int(request.args.get("tamanho", 12))
        maiusculas = request.args.get("maiusculas", "true").lower() == "true"
        numeros = request.args.get("numeros", "true").lower() == "true"
        especiais = request.args.get("especiais", "true").lower() == "true"

        senha = gerar_senha(tamanho, maiusculas, numeros, especiais)
        return jsonify({"senha": senha})

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


#if __name__ == '__main__':
    # Só roda em desenvolvimento local
#    port = int(os.environ.get('PORT', 5000))  # Porta padrão 5000 localmente
    #app.run(host='0.0.0.0', port=port, debug=True)
