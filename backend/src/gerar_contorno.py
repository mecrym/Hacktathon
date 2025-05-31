# src/gerar_contorno.py

import json
from pathlib import Path
from PIL import Image, ImageDraw

def gerar_png_contorno(dados: dict, escala: int, saida_dir: Path) -> Path:
    """
    Gera um PNG que mostra apenas:
      • Contorno externo do lote.
      • Retângulo interno de recuos (Plano Diretor) em tracejado.
    Parâmetros:
      - dados: dict com "lote" (largura, comprimento, restricoes.recuos).
      - escala: quantos pixels correspondem a 1 metro (ex: 10 → 1m = 10px).
      - saida_dir: Path para a pasta onde salvar o PNG gerado.
    Retorna:
      Path completo do PNG (por ex.: outputs/projeto1.png).
    """

    lote = dados["lote"]
    largura_m = lote["largura"]
    comprimento_m = lote["comprimento"]
    recuos = lote["restricoes"]["recuos"]
    rec_frontal_m = recuos["frontal"]
    rec_lateral_m = recuos["laterais"]
    rec_fundos_m = recuos["fundos"]

    # Converter metros para pixels
    largura_px = int(largura_m * escala)
    comprimento_px = int(comprimento_m * escala)
    rec_frontal_px = int(rec_frontal_m * escala)
    rec_lateral_px = int(rec_lateral_m * escala)
    rec_fundos_px = int(rec_fundos_m * escala)

    # Criar imagem branca (RGB) do tamanho do lote em pixels
    img = Image.new("RGB", (largura_px, comprimento_px), "white")
    draw = ImageDraw.Draw(img)

    # 1) Desenhar contorno externo (retângulo preto, 2px de espessura)
    draw.rectangle(
        [(0, 0), (largura_px - 1, comprimento_px - 1)],
        outline="black",
        width=3
    )

    # 2) Desenhar recuos internos (retângulo tracejado em vermelho, 1px)
    x0 = rec_lateral_px
    y0 = rec_frontal_px
    x1 = largura_px - rec_lateral_px - 1
    y1 = comprimento_px - rec_fundos_px - 1

    dash = 5  # pixels ligados/desligados
    # tracejado horizontal superior
    for x in range(x0, x1, dash * 2):
        draw.line([(x, y0), (min(x + dash, x1), y0)], fill="red", width=1)
    # tracejado horizontal inferior
    for x in range(x0, x1, dash * 2):
        draw.line([(x, y1), (min(x + dash, x1), y1)], fill="red", width=1)
    # tracejado vertical esquerda
    for y in range(y0, y1, dash * 2):
        draw.line([(x0, y), (x0, min(y + dash, y1))], fill="red", width=1)
    # tracejado vertical direita
    for y in range(y0, y1, dash * 2):
        draw.line([(x1, y), (x1, min(y + dash, y1))], fill="red", width=1)

    # Definir o nome de saída baseando-se em “metadata.nome” ou “contorno”
    nome_base = dados.get("metadata", {}).get("nome", "contorno")
    png_path = saida_dir / f"{nome_base}.png"
    img.save(png_path, format="PNG")

    return png_path
