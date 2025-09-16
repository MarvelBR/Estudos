import os
import json
from datetime import datetime

# Configurações de chunk
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def dividir_em_chunks(texto, chunk_size=1000, overlap=200):
    """Divide o texto em pedaços com sobreposição."""
    chunks = []
    for i in range(0, len(texto), chunk_size - overlap):
        pedaço = texto[i:i + chunk_size]
        chunks.append(pedaço)
    return chunks

def txt_para_json(caminho_txt, fonte="", titulo="Documento"):
    """Lê um TXT e gera um JSON com os chunks + metadados."""
    # Lê o texto
    with open(caminho_txt, "r", encoding="utf-8") as f:
        texto = f.read()

    # Divide em chunks
    chunks = dividir_em_chunks(texto, CHUNK_SIZE, CHUNK_OVERLAP)

    # Gera estrutura JSON
    documento_id = os.path.splitext(os.path.basename(caminho_txt))[0]
    data_extracao = datetime.now().strftime("%Y-%m-%d")

    saida = []
    for idx, chunk in enumerate(chunks, start=1):
        saida.append({
            "id": f"{documento_id}_chunk_{idx}",
            "conteudo": chunk,
            "metadata": {
                "fonte": fonte,
                "titulo": titulo,
                "data_extracao": data_extracao,
                "chunk_index": idx
            }
        })

    # Salva em JSON
    caminho_json = documento_id + ".json"
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON gerado: {caminho_json} ({len(chunks)} chunks)")

# -------------------------
# Exemplo de uso
# -------------------------
if __name__ == "__main__":
    # Arquivo de entrada
    txt_arquivo = "./documentos/secretaria-SaudePR.txt"

    # Metadados (personalize aqui)
    fonte = "https://www.saude.pr.gov.br/Pagina/Transtorno-do-Espectro-Autista-TEA#:~:text=Dificuldade%20na%20comunica%C3%A7%C3%A3o%2C%20caracterizado%20por,espec%C3%ADficas%20e%20dificuldade%20de%20imagina%C3%A7%C3%A3o"
    titulo = "Transtorno do Espectro Autista (TEA)"

    txt_para_json(txt_arquivo, fonte, titulo)
