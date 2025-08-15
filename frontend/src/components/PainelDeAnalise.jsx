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
    return null; 
  }

  return (
    <div className="analise-container">
      {/*pontuaçao + sugestoes)*/}
      <div className="card card-diagnostico">
        <div className="diagnostico-header">
          <h3>Diagnóstico do Mentor</h3>
          <div className="score-badge">
            Nota: <span>{analise.pontuacao.toFixed(1)}</span>
          </div>
        </div>
       <ul>
  {analise.sugestoes.map((sugestao, index) => {
   
    const parts = sugestao.split(':**');
    const title = parts[0] ? parts[0].replace(/\*\*/g, '') : '';
    const description = parts.length > 1 ? parts.slice(1).join(':**') : '';

    return (
      <li key={index}>
        <strong>{title}:</strong>
        <span>{description}</span>
      </li>
    );
  })}
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