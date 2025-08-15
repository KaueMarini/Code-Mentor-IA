import os
import json
import re  # Importe o módulo de expressões regulares
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel, Field # Importe o Field
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

# --- ALTERAÇÃO AQUI ---
# Torna os campos opcionais e com valores padrão para evitar erros de validação
class AnaliseResponse(BaseModel):
    pontuacao: float = 0.0
    sugestoes: list[str] = Field(default_factory=list)
    codigo_refatorado: str | None = ""

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
        
        # --- ALTERAÇÃO AQUI ---
        # Usa regex para encontrar o bloco JSON de forma mais confiável
        match = re.search(r"```json\s*(\{.*?\})\s*```", resposta_ia.text, re.DOTALL)
        if match:
            texto_limpo = match.group(1)
        else:
            # Plano B caso o modelo não use o markdown ```json
            texto_limpo = resposta_ia.text.strip()
            
        dados_resposta = json.loads(texto_limpo)
        
        return AnaliseResponse(**dados_resposta)

    # --- ALTERAÇÃO AQUI ---
    # Captura erros específicos de decodificação de JSON
    except json.JSONDecodeError as e:
        print(f"❌ ERRO AO DECODIFICAR O JSON DA IA: {e}")
        return AnaliseResponse(
            sugestoes=[f"Ocorreu um erro ao processar a resposta da IA. O JSON retornado é inválido."],
            codigo_refatorado=request.codigo
        )
    except Exception as e:
        print(f"❌ ERRO AO PROCESSAR A RESPOSTA DA IA: {e}")
        return AnaliseResponse(
            sugestoes=[f"Ocorreu um erro ao comunicar com a IA: {e}."],
            codigo_refatorado=request.codigo
        )