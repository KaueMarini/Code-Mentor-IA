import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-csharp';
import 'prismjs/components/prism-java';
import 'prismjs/themes/prism-okaidia.css';

function EditorDeCodigo({ codigo, setCodigo, onAnalisar, carregando, linguagem, setLinguagem }) {
  return (
    <div className="editor-container">
      <div className="editor-header">
        <h2>Seu Código</h2>
        <select
          value={linguagem}
          onChange={(e) => setLinguagem(e.target.value)}
          disabled={carregando}
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="typescript">TypeScript</option>
          <option value="java">Java</option>
          <option value="csharp">C#</option>
          <option value="html">HTML</option>
          <option value="css">CSS</option>
        </select>
      </div>
      
      <div className="editor-wrapper">
        <Editor
          value={codigo}
          onValueChange={code => setCodigo(code)}
          highlight={code => highlight(code, languages[linguagem] || languages.clike, linguagem)}
          padding={15}
          style={{
            fontFamily: '"Fira Code", "Fira Mono", monospace',
            fontSize: 14,
            outline: 0,
          }}
        />
      </div>

      <button onClick={onAnalisar} disabled={!codigo || carregando}>
        {carregando ? 'Analisando...' : 'Analisar Código'}
      </button>
    </div>
  );
}

export default EditorDeCodigo;