
import os
import json
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configura o modelo de IA
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("A variável de ambiente GOOGLE_API_KEY não foi encontrada.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ Modelo Gemini configurado com sucesso!")
except Exception as e:
    print(f"❌ ERRO CRÍTICO ao configurar o modelo Gemini: {e}")
    model = None

# Define os formatos de dados para a API
class AnaliseRequest(BaseModel):
    codigo: str
    linguagem: str | None = "python"

class AnaliseResponse(BaseModel):
    pontuacao: float
    sugestoes: list[str]
    codigo_refatorado: str

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Code-Mentor AI API",
    version="1.1.0",
)

# Configura o CORS para permitir a comunicação com o front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define os endpoints (rotas) da API
@app.get("/")
def read_root():
    return {"status": "Code-Mentor AI API está no ar!"}

@app.post("/analise", response_model=AnaliseResponse)
def analisar_codigo(request: AnaliseRequest):
    if not model:
        return AnaliseResponse(
            pontuacao=0.0,
            sugestoes=["Erro: Modelo de IA não configurado."],
            codigo_refatorado=request.codigo
        )

    # O prompt é a instrução detalhada que damos para a IA
    prompt = f"""
    Você é um "Code-Mentor", um especialista sênior em programação. Sua tarefa é analisar o código na linguagem {request.linguagem}.

    Sua resposta DEVE SER EXATAMENTE um JSON com a seguinte estrutura:
    {{
      "pontuacao": <um número float de 0.0 a 10.0 para a qualidade do código original>,
      "sugestoes": ["uma lista de 3 a 5 sugestões de melhoria explicando o porquê"],
      "codigo_refatorado": "<o código completo e melhorado aqui>"
    }}

    --- CÓDIGO PARA ANÁLISE ---
    ```
    {request.codigo}
    ```
    """
    try:
        resposta_ia = model.generate_content(prompt)
        texto_limpo = resposta_ia.text.replace("```json", "").replace("```", "").strip()
        dados_resposta = json.loads(texto_limpo)
        
        return AnaliseResponse(**dados_resposta)

    except Exception as e:
        print(f"❌ ERRO AO PROCESSAR A RESPOSTA DA IA: {e}")
        return AnaliseResponse(
            pontuacao=0.0,
            sugestoes=[f"Ocorreu um erro ao comunicar com a IA: {e}."],
            codigo_refatorado=request.codigo
        )