# src/gerar_planta.py

import os
import base64
import openai
from dotenv import load_dotenv
from urllib.request import urlopen
from PIL import Image
from pathlib import Path

# Importamos apenas a função que gera a parte variável do prompt
from gerar_prompt import gerar_prompt_variavel

def gerar_planta_via_gpt_image(png_contorno_path: str, saida_dir: str, escala: int, dados: dict) -> list[str]:
    """
    1) Gera máscara RGBA branca do mesmo tamanho do PNG de contorno.
    2) Define um bloco fixo de regras (base_regras).
    3) Chama gerar_prompt_variavel(dados) → retorna apenas a parte do prompt que muda conforme o JSON/usuário.
    4) Concatena: prompt_final = base_regras + "\n" + prompt_variavel.
    5) Chama openai.images.edit(model="gpt-image-1", image=open(contorno), mask=open(mascara),
       prompt=prompt_final, n=3, size="auto").
    6) Salva cada uma das 3 imagens em disco:
       outputs/planta_completa_<nome_base>_1.png
       outputs/planta_completa_<nome_base>_2.png
       outputs/planta_completa_<nome_base>_3.png
    Retorna a lista com os 3 caminhos gerados.
    """

    # Carregar chave de API
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("Defina OPENAI_API_KEY no .env ou variáveis de ambiente.")

    # 1) Ler dimensões do PNG de contorno (para criar a máscara e saber o size="auto")
    img_contorno = Image.open(png_contorno_path)
    largura_px, altura_px = img_contorno.size

    # 2) Criar e salvar a máscara RGBA branca (canal alfa=255)
    mask_png_path = Path(saida_dir) / f"mask_branca_{Path(png_contorno_path).stem}.png"
    mask = Image.new("RGBA", (largura_px, altura_px), (255, 255, 255, 255))
    mask.save(mask_png_path, format="PNG")

    # 3) Abrir os arquivos de contorno e máscara
    image_file = open(png_contorno_path, "rb")
    mask_file  = open(mask_png_path, "rb")

    # 4) Bloco fixo de regras (base_regras)
    base_regras = (
        "Always generate black and white 2D architectural floor plans. "
        "Use clear, technical lines. "
        "Include walls, doors, windows and car gates in a clean, schematic style. "
        "Draw all elements to scale (e.g., 1m = {}px). "
        "Do not exceed the boundary lines of the lot or any setback lines.\n"
        "Name all rooms clearly and make sure they are at the correct place for a typical house layout.\n"
    ).format(escala)

    # 5) Chamar GPT para obter apenas a parte variável do prompt com base no JSON
    prompt_variavel = gerar_prompt_variavel(dados)

    # 6) Concatena base_regras + prompt_variavel
    prompt_final = base_regras + "\n" + prompt_variavel

    # 7) Chamar a API de edição pedindo 3 variações (n=3) e size="auto"
    try:
        response = openai.images.edit(
            model="gpt-image-1",
            image=image_file,
            mask=mask_file,
            prompt=prompt_final,
            n=3,
            size="auto"
        )
    except Exception as e:
        image_file.close()
        mask_file.close()
        raise RuntimeError(f"Falha ao chamar openai.images.edit(): {e}")

    # 8) Fechar arquivos abertos
    image_file.close()
    mask_file.close()

    # 9) Extrair cada uma das 3 imagens retornadas e salvar em disco
    resultados = []
    nome_base = Path(png_contorno_path).stem  # ex: "projeto1"
    for idx, item in enumerate(response.data, start=1):
        url = getattr(item, "url", None)
        b64_json = getattr(item, "b64_json", None)

        caminho_saida = os.path.join(saida_dir, f"planta_completa_{nome_base}_{idx}.png")

        if url:
            try:
                img_data = urlopen(url).read()
                with open(caminho_saida, "wb") as out_f:
                    out_f.write(img_data)
            except Exception as e:
                raise RuntimeError(f"Falha ao baixar PNG da URL (variação {idx}): {e}")
        elif b64_json:
            try:
                img_data = base64.b64decode(b64_json)
                with open(caminho_saida, "wb") as out_f:
                    out_f.write(img_data)
            except Exception as e:
                raise RuntimeError(f"Falha ao decodificar base64 (variação {idx}): {e}")
        else:
            raise RuntimeError(f"A resposta da API não retornou nem URL nem b64_json na variação {idx}.")

        resultados.append(caminho_saida)

    return resultados
