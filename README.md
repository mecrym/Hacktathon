# 🏗️ Backend - Geração de Plantas Baixas com GPT Image

Este backend tem como objetivo gerar **plantas arquitetônicas 2D** com base em um JSON de entrada, utilizando a API de imagens da OpenAI (`gpt-image-1`). A geração é guiada por regras fixas e pelo conteúdo do JSON enviado pelo usuário.

## 📁 Estrutura do Projeto

backend/
│
├── imagens teste/ # Pasta onde as imagens geradas são salvas
├── inputs/ # JSONs de entrada com especificações do projeto
├── outputs/ # SVGs e logs gerados
├── src/
│ ├── init.py
│ ├── gerar_contorno.py # Gera SVG com base no lote e recuos
│ ├── gerar_planta.py # Chama o GPT Image para gerar imagem da planta
│ ├── gerar_prompt.py # Constrói o prompt com base no JSON
│ └── main.py # Ponto principal de execução
├── .gitignore
├── requirements.txt
└── README.md

bash
Copy
Edit

## ▶️ Como Executar

### 1. Clone o repositório (se ainda não tiver feito)
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio/backend
2. Crie um ambiente virtual (recomendado)
bash
Copy
Edit
python -m venv .venv
source .venv/Scripts/activate  # Windows
# ou
source .venv/bin/activate      # Linux/Mac
3. Instale as dependências
bash
Copy
Edit
pip install -r requirements.txt
4. Configure a chave da OpenAI em um arquivo .env
Crie um arquivo .env na raiz da pasta backend/ com o seguinte conteúdo:

ini
Copy
Edit
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
🔐 Nunca exponha sua chave da API no código.

5. Execute o backend
Certifique-se de ter um JSON válido em inputs/projeto.json, então execute:

bash
Copy
Edit
python src/main.py
A imagem gerada será salva na pasta imagens teste/.

💡 Exemplo de JSON de entrada (inputs/projeto.json)
json
Copy
Edit
{
  "lote": {
    "dimensoes": { "largura": 10, "comprimento": 20, "area": 200 },
    "restricoes": {
      "recuos": { "frontal": 3, "laterais": 2, "fundos": 3 }
    }
  },
  "projeto": {
    "tipo_residencia": "unifamiliar",
    "numero_pavimentos": 1,
    "comodos": [
      { "tipo": "quarto", "quantidade": 2 },
      { "tipo": "banheiro", "quantidade": 1 },
      { "tipo": "sala", "quantidade": 1 },
      { "tipo": "cozinha", "quantidade": 1 },
      { "tipo": "garagem", "quantidade": 1 }
    ],
    "observacoes": "Planta pequena, compacta, ideal para casal com 1 filho"
  }
}
🧠 Tecnologias
Python 3.10+

OpenAI Python SDK

CairoSVG (para converter SVG em PNG)

dotenv para variáveis sensíveis

🚫 Avisos
O uso da API gpt-image-1 exige conta verificada na OpenAI e plano ativo com créditos.

Este projeto não armazena dados sensíveis nem deve expor sua API key.

