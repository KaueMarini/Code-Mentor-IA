import os
import json
import re
import unicodedata
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# --- Setup ---
load_dotenv()
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Variável GOOGLE_API_KEY não encontrada.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("Modelo Gemini configurado com sucesso.")
except Exception as e:
    print(f"Erro ao configurar o modelo Gemini: {e}")
    model = None

# --- Schemas ---
class AnaliseRequest(BaseModel):
    codigo: str
    linguagem: str = "python"

class AnaliseResponse(BaseModel):
    pontuacao: float = 0.0
    sugestoes: list[str] = Field(default_factory=list)
    codigo_refatorado: str = ""

# --- App ---
app = FastAPI(title="Code-Mentor API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "API online"}

# --- Helpers ---
def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def _normalize_keys(d: dict) -> dict:
    """Mapeia chaves variantes para o contrato esperado."""
    out = {}
    for k, v in d.items():
        kn = _strip_accents(k.lower()).replace(" ", "").replace("-", "").replace("_", "")
        if kn in {"pontuacao", "nota", "score", "avaliacao", "grade"}:
            out["pontuacao"] = v
        elif kn.startswith("sugest"):
            out["sugestoes"] = v
        elif ("codigo" in kn and ("refatorado" in kn or "melhorado" in kn)) or kn in {"codigorefatorado", "refatorado"}:
            out["codigo_refatorado"] = v
    return out

def _coerce_response(payload: dict, original_code: str) -> AnaliseResponse:
    payload = _normalize_keys(payload) | payload  

    
    pont = payload.get("pontuacao", 0.0)
    try:
        pont = float(pont)
    except Exception:
        pont = 0.0

   
    sugs = payload.get("sugestoes", [])
    if isinstance(sugs, str):
        
        parts = [p.strip(" -•\t") for p in re.split(r"[\n;]+", sugs) if p.strip()]
        sugs = parts[:5] if parts else []
    if not isinstance(sugs, list):
        sugs = [str(sugs)]
    sugs = [str(x) for x in sugs][:5]

  
    cod = payload.get("codigo_refatorado", "")
    if not isinstance(cod, str):
        cod = str(cod)

    return AnaliseResponse(pontuacao=pont, sugestoes=sugs, codigo_refatorado=cod or original_code)

def _extract_json(text: str) -> str | None:
    """Tenta extrair um objeto JSON do texto."""
    if not text:
        return None

    
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    
    m = re.search(r"```\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()

   
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1].strip()
        return candidate

    return None

def _call_gemini(prompt: str) -> str:
    """
    Tenta forçar JSON puro. Se a SDK ou o modelo ignorarem, ainda assim retornamos text.
    """
    try:
        resp = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"},
        )
        return getattr(resp, "text", "") or ""
    except Exception:
        
        resp = model.generate_content(prompt)
        return getattr(resp, "text", "") or ""

# --- Endpoint ---
@app.post("/analise", response_model=AnaliseResponse)
def analisar_codigo(request: AnaliseRequest):
    if not model:
        return AnaliseResponse(
            sugestoes=["Modelo de IA não configurado."],
            codigo_refatorado=request.codigo,
        )

    prompt = (
        "Você é um serviço que retorna EXATAMENTE um JSON, sem comentários, markdown ou texto adicional.\n"
        "Contrato de saída:\n"
        "{\n"
        '  "pontuacao": <float de 0.0 a 10.0>,\n'
        '  "sugestoes": ["3 a 5 recomendações objetivas"],\n'
        '  "codigo_refatorado": "<código completo refatorado>"\n'
        "}\n\n"
        f"Linguagem selecionada: {request.linguagem}\n"
        "Se o código NÃO estiver na linguagem selecionada, retorne:\n"
        "{\n"
        '  "pontuacao": 0.0,\n'
        '  "sugestoes": ["Erro: O código fornecido não parece ser da linguagem selecionada."],\n'
        '  "codigo_refatorado": "<código original>"\n'
        "}\n\n"
        "Agora, gere SOMENTE o JSON de acordo com o contrato.\n\n"
        f"CÓDIGO:\n{request.codigo}\n"
    )

    try:
        raw = _call_gemini(prompt).strip()

        
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            j = _extract_json(raw)
            if not j:
                raise json.JSONDecodeError("JSON não encontrado no retorno do modelo.", raw, 0)
            data = json.loads(j)

        resp = _coerce_response(data, original_code=request.codigo)

        if not resp.sugestoes:
            resp.sugestoes = ["Sem sugestões disponíveis no retorno do modelo."]
        if resp.pontuacao < 0.0 or resp.pontuacao > 10.0:
            resp.pontuacao = max(0.0, min(10.0, resp.pontuacao))

        return resp

    except json.JSONDecodeError:
        return AnaliseResponse(
            sugestoes=["Erro ao interpretar a resposta do modelo (JSON inválido)."],
            codigo_refatorado=request.codigo,
        )
    except Exception as e:
        return AnaliseResponse(
            sugestoes=[f"Erro ao processar a análise: {e}"],
            codigo_refatorado=request.codigo,
        )
