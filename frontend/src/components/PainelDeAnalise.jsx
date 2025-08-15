function LoadingSpinner() {
  return (
    <div className="spinner-container">
      <div className="spinner"></div>
      <p>Analisando seu código...</p>
    </div>
  );
}

function PainelDeAnalise({ analise, carregando }) {
  if (carregando) {
    return <LoadingSpinner />;
  }

  if (!analise) {
    return null; // Não mostra nada se a análise ainda não começou
  }

  return (
    <div className="analise-container">
      {/* Card Principal: Diagnóstico (Pontuação + Sugestões) */}
      <div className="card card-diagnostico">
        <div className="diagnostico-header">
          <h3>Diagnóstico do Mentor</h3>
          <div className="score-badge">
            Nota: <span>{analise.pontuacao.toFixed(1)}</span>
          </div>
        </div>
        <ul>
          {analise.sugestoes.map((sugestao, index) => (
            <li key={index} dangerouslySetInnerHTML={{ __html: sugestao }}></li>
          ))}
        </ul>
      </div>

      {/* Card Secundário: Código Refatorado */}
      <div className="card card-refactored">
        <h3>Código Refatorado</h3>
        <pre>
          <code>{analise.codigo_refatorado}</code>
        </pre>
      </div>
    </div>
  );
}

export default PainelDeAnalise;