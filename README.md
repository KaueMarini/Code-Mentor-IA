#  Code-Mentor AI

Code-Mentor AI é uma aplicação web Full Stack que utiliza a API generativa do Google (Gemini) para fornecer análises e sugestões de refatoração de código em tempo real. Este projeto foi construído para servir como uma ferramenta de aprendizado e um assistente de programação, ajudando desenvolvedores a escreverem código mais limpo e eficiente.

##  Funcionalidades

* **Análise Inteligente:** Submeta trechos de código em diversas linguagens (Python, JavaScript, etc.).
* **Pontuação de Qualidade:** Receba uma nota de 0 a 10 pela qualidade do código original.
* **Sugestões Detalhadas:** Obtenha uma lista de melhorias com explicações claras sobre o "porquê" de cada sugestão.
* **Código Refatorado:** Veja uma versão do seu código reescrita pela IA, aplicando as melhores práticas.
* **Interface Interativa:** Um editor de código com destaque de sintaxe para uma experiência de usuário agradável.

##  Tech Stack

* **Front-end:** React (com Vite)
* **Back-end:** Python com FastAPI
* **Inteligência Artificial:** Google Gemini API
* **Comunicação:** API REST
* **Bibliotecas Principais:** `google-generativeai`, `react-simple-code-editor`, `uvicorn`.

##  Como Executar Localmente

### Pré-requisitos
* Node.js e npm
* Python 3.9+
* Uma chave de API do Google AI Studio

### Back-end
1.  Navegue até a pasta do back-end:
    ```bash
    cd backend
    ```
2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  Crie um arquivo `.env` e adicione sua chave de API:
    ```
    GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
    ```
4.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
5.  Inicie o servidor:
    ```bash
    python -m uvicorn main:app --reload
    ```
O servidor estará rodando em `http://127.0.0.1:8000`.

### Front-end
1.  Abra um **novo terminal** e navegue até a pasta do front-end:
    ```bash
    cd frontend
    ```
2.  Instale as dependências:
    ```bash
    npm install
    ```
3.  Inicie o servidor de desenvolvimento:
    ```bash
    npm run dev
    ```
A aplicação estará acessível em `http://localhost:5173`.
