# src/main.py

import os
import json
from pathlib import Path
from gerar_contorno import gerar_png_contorno
from gerar_planta import gerar_planta_via_gpt_image

def main():
    # 1) Definir pastas de entrada (JSONs) e saída (PNGs)
    pasta_inputs  = Path("C:/Users/gusta/Images/inputs")
    pasta_outputs = Path("C:/Users/gusta/Images/outputs")
    pasta_outputs.mkdir(exist_ok=True)

    # 2) Para cada JSON em inputs/
    for arquivo in pasta_inputs.glob("*.json"):
        print(f"\nProcessando JSON: {arquivo.name}")

        # 2.1) Ler e parsear o JSON
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ✗ Erro ao ler/parsing JSON: {e}")
            continue

        nome_base = arquivo.stem  # ex: "projeto1"

        # 2.2) Gerar o PNG de contorno (lote + recuos) via gerar_contorno.py
        try:
            contorno_png = gerar_png_contorno(
                dados=dados,
                escala=10,  # 1 metro = 10 pixels (ajuste se quiser outra escala)
                saida_dir=pasta_outputs
            )
            print(f"  ✔ PNG de contorno gerado: {contorno_png}")
        except Exception as e:
            print(f"  ✗ Falha ao gerar PNG de contorno: {e}")
            continue

        # 2.3) Gerar as 3 variações da planta usando o prompt fixo + plano diretor + descrição do usuário
        try:
            caminhos_imagens = gerar_planta_via_gpt_image(
                png_contorno_path=str(contorno_png),
                saida_dir=str(pasta_outputs),
                escala=10,
                dados=dados
            )
            for idx, img_path in enumerate(caminhos_imagens, start=1):
                print(f"    ✔ Variação #{idx}: {img_path}")
        except Exception as e:
            print(f"  ✗ Falha ao gerar planta via GPT Image 1: {e}")
            continue

if __name__ == "__main__":
    main()
