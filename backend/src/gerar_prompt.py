# src/gerar_prompt.py
import os
import json
import openai
from dotenv import load_dotenv

def gerar_prompt_variavel(dados: dict) -> str:
    """
    Converte o JSON de projeto (que contém lote, recuos, lista de cômodos (tipo+quantidade)
    e um campo opcional 'descricao_usuario') em um texto descritivo dos aspectos variáveis do projeto.
    Este texto NÃO deve conter regras de estilo (monocromático, escala, linhas finas etc.),
    pois essas ficam em 'base_regras' no gerar_planta.py.
    
    Retorna: string que será concatenada ao base_regras para formar o prompt final.
    """

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("Defina OPENAI_API_KEY no .env ou em variáveis de ambiente.")

    # 1) Converter o dict inteiro em string JSON indentada
    projeto_json_str = json.dumps(dados, indent=2, ensure_ascii=False)

    # 2) system_msg: instrui o modelo a extrair apenas a parte variável
    system_msg = {
        "role": "system",
        "content": (
            "Você receberá um JSON que descreve um projeto arquitetônico. "
            "Descreva APENAS os detalhes variáveis do projeto, sem incluir NENHUMA instrução de estilo. "
            "Especificamente, inclua:\n"
            "- Dimensões do lote (largura × comprimento).\n"
            "- Medidas de recuos (frontal, laterais, fundos).\n"
            "- Lista de cômodos (tipo e quantidade).\n"
            "- Qualquer texto contido em 'descricao_usuario'.\n"
            "Retorne apenas o texto descritivo desses elementos, num parágrafo coeso."
        )
    }

    # 3) user_msg: passa o JSON completo
    user_msg = {
        "role": "user",
        "content": (
            "Aqui está o JSON completo do projeto. Gere apenas o texto descritivo dos aspectos variáveis:\n\n"
            f"{projeto_json_str}"
        )
    }

    # 4) Chamada ao GPT-4o-mini (ou outro GPT de sua preferência)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_msg, user_msg],
        temperature=0.0,
        max_tokens=600
    )

    prompt_variavel = response.choices[0].message.content.strip()
    return prompt_variavel
