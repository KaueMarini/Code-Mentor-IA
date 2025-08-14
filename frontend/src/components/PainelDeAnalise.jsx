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
      <div className="card card-score">
        <h3>Pontuação de Qualidade</h3>
        <div className="score-circle">
          <span>{analise.pontuacao.toFixed(1)}</span>
        </div>
        <p>Nota de 0 a 10 para o código original.</p>
      </div>

      <div className="card card-suggestions">
        <h3>Sugestões do Mentor</h3>
        <ul>
          {analise.sugestoes.map((sugestao, index) => (
            <li key={index} dangerouslySetInnerHTML={{ __html: sugestao }}></li>
          ))}
        </ul>
      </div>

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