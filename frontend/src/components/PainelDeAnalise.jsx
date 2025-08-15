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
  {analise.sugestoes.map((sugestao, index) => {
    // 1. Divide a string no primeiro ":**" para separar o título da descrição.
    const parts = sugestao.split(':**');
    
    // 2. Limpa o título, removendo os asteriscos.
    const title = parts[0] ? parts[0].replace(/\*\*/g, '') : '';
    
    // 3. O resto é a descrição. Juntamos caso haja outros ":" no texto.
    const description = parts.length > 1 ? parts.slice(1).join(':**') : '';

    return (
      <li key={index}>
        {/* Renderiza o título em negrito e a descrição como texto normal */}
        <strong>{title}:</strong>
        <span>{description}</span>
      </li>
    );
  })}
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