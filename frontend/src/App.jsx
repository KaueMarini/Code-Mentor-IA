import { useState } from 'react';
import EditorDeCodigo from './components/EditorDeCodigo';
import PainelDeAnalise from './components/PainelDeAnalise';

function App() {
  const [codigo, setCodigo] = useState('');
  const [analise, setAnalise] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [linguagem, setLinguagem] = useState('python');
  const [showResultado, setShowResultado] = useState(false);

  const handleAnalisar = async () => {
    setCarregando(true);
    setShowResultado(true);
    setAnalise(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/analise', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ codigo, linguagem }),
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      setAnalise(data);
    } catch (error) {
      console.error("Erro ao chamar a API:", error);
      setAnalise({ pontuacao: 0, sugestoes: ["Erro de comunicação. Verifique se o servidor back-end está rodando."], codigo_refatorado: "N/A" });
    }
    setCarregando(false);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Code-Mentor AI</h1>
        <p>Cole seu código, selecione a linguagem e receba uma análise instantânea da nossa IA.</p>
      </header>
      
      <main className="main-content">
        <EditorDeCodigo
          codigo={codigo}
          setCodigo={setCodigo}
          onAnalisar={handleAnalisar}
          carregando={carregando}
          linguagem={linguagem}
          setLinguagem={setLinguagem}
        />
        {/* A área de análise só aparece depois de clicar no botão */}
        {showResultado && (
          <PainelDeAnalise analise={analise} carregando={carregando} />
        )}
      </main>
    </div>
  )
}

export default App;