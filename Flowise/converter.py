import os
import json
from datetime import datetime
import re

# Configurações de chunk
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def detectar_subtitulos(texto):
    """
    Detecta subtítulos com base em estrutura do texto:
    - Linhas isoladas (seguida de quebra de linha e parágrafo)
    - Linhas inteiras em maiúsculas
    - Linhas curtas (≤ 10 palavras)
    """
    linhas = texto.splitlines()
    subtitulos = []
    pos = 0

    for i, linha in enumerate(linhas):
        linha_limpa = linha.strip()
        if not linha_limpa:
            pos += len(linha) + 1
            continue

        # Verifica se a próxima linha é texto (começa com letra)
        proxima_linha = linhas[i + 1].strip() if i + 1 < len(linhas) else ""
        eh_possivel_subtitulo = (
            proxima_linha
            and not proxima_linha.isupper()  # não é outro título
            and not linha_limpa.endswith(".")  # evita frases
            and (linha_limpa.isupper() or linha_limpa.istitle() or len(linha_limpa.split()) <= 10)
        )

        if eh_possivel_subtitulo:
            subtitulos.append((pos, linha_limpa))

        pos += len(linha) + 1

    return subtitulos

def encontrar_subtitulo_para_chunk(subtitulos, indice_chunk):
    """Retorna o último subtítulo anterior ao chunk."""
    ultimo_subtitulo = None
    for pos, subtitulo in subtitulos:
        if pos <= indice_chunk:
            ultimo_subtitulo = subtitulo
        else:
            break
    return ultimo_subtitulo


def dividir_em_chunks(texto, chunk_size=1000, overlap=200):
    """Divide o texto em pedaços com sobreposição."""
    chunks = []
    for i in range(0, len(texto), chunk_size - overlap):
        pedaço = texto[i:i + chunk_size]
        chunks.append((i, pedaço))  # armazenar índice inicial
    return chunks


def txt_para_json(caminho_txt, fonte="", titulo="Documento"):
    """Lê um TXT e gera um JSON com os chunks + metadados (incluindo subtítulos)."""
    with open(caminho_txt, "r", encoding="utf-8") as f:
        texto = f.read()

    # Detecta subtítulos
    subtitulos = detectar_subtitulos(texto)

    # Divide em chunks
    chunks = dividir_em_chunks(texto, CHUNK_SIZE, CHUNK_OVERLAP)

    # Metadados gerais
    documento_id = os.path.splitext(os.path.basename(caminho_txt))[0]
    data_extracao = datetime.now().strftime("%Y-%m-%d")

    # Gera estrutura JSON
    saida = []
    for idx, (inicio, chunk) in enumerate(chunks, start=1):
        subtitulo = encontrar_subtitulo_para_chunk(subtitulos, inicio)
        saida.append({
            "id": f"{documento_id}_chunk_{idx}",
            "conteudo": chunk.strip(),
            "metadata": {
                "fonte": fonte,
                "titulo": titulo,
                "subtitulo": subtitulo or "Sem subtítulo",
                "data_extracao": data_extracao,
                "chunk_index": idx
            }
        })

    # Cria pasta de saída
    pasta_saida = "./jsons"
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_json = os.path.join(pasta_saida, documento_id + ".json")

    # Salva em JSON
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON gerado: {caminho_json} ({len(chunks)} chunks)")

# Exemplo de uso
if __name__ == "__main__":
    txt_arquivo = "artigos/Secretaria_Desenvolvimento_Social.txt"

    fonte = "https://social.rs.gov.br/estudo-revela-que-79-das-pessoas-com-autismo-em-idade-escolar-frequentam-algum-nivel-de-escolarizacao-no-estado"
    titulo = "Estudo revela que 79% das pessoas com autismo em idade escolar frequentam algum nível de escolarização no Estado"

    txt_para_json(txt_arquivo, fonte, titulo)
