from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/buscar": {"origins": "http://localhost:8080"}})

# Carregar os dados do CSV
CSV_PATH = "Relatorio.csv"
df = pd.read_csv(CSV_PATH, encoding="utf-8", delimiter=";", dtype=str)

# Remover espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

# Certificar-se de que "Razao_Social", "CNPJ", "Representante" e "Telefone" estão no formato correto
df["Razao_Social"] = df["Razao_Social"].astype(str).str.lower().str.strip()
df["CNPJ"] = df["CNPJ"].astype(str).str.strip()
df["Representante"] = df["Representante"].astype(str).str.strip()
df["Telefone"] = df["Telefone"].astype(str).str.strip()

@app.route("/buscar", methods=["GET"])
def buscar_operadoras():
    termo = request.args.get("termo", "").lower().strip()

    if not termo:
        return jsonify({"erro": "Informe um termo para busca."}), 400

    if "Razao_Social" not in df.columns or "CNPJ" not in df.columns:
        return jsonify({"erro": "Coluna necessária não encontrada no CSV."}), 500

    # Filtrar os resultados pela Razão Social
    resultados = df[df["Razao_Social"].str.contains(termo, na=False, regex=False)]

    # Incluir as novas colunas na resposta
    return jsonify(resultados[["Razao_Social", "CNPJ", "Representante", "Telefone"]].to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
