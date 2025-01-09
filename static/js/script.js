// Inicializar o CodeMirror
let editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    mode: "python", // Usando modo Python por enquanto, podemos criar um modo específico depois
    theme: "monokai",
    lineNumbers: true,
    autoCloseBrackets: true,
    matchBrackets: true,
    indentUnit: 4,
    tabSize: 4,
    lineWrapping: true,
});

// Exemplo de código inicial
editor.setValue(`def int inicio() {
    int x;
    x = 10;
    enquanto (x > 0) faca {
        escrevei(x);
        x = x - 1;
    }
    retorna 0;
}`);

document.getElementById("run-btn").addEventListener("click", async function() {
    const code = editor.getValue();
    const outputEwvm = document.getElementById("output-ewvm");
    const outputProgram = document.getElementById("output-program");
    
    try {
        outputProgram.textContent = "Executando o código...\n";
        
        const response = await fetch('/compile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        });

        if (!response.ok) {
            throw new Error('Erro na compilação');
        }

        const result = await response.json();
        outputEwvm.textContent = result.ewvm || '';
        outputProgram.textContent = result.output || '';

    } catch (error) {
        outputEwvm.textContent = '';
        outputProgram.textContent = "Erro: " + error.message;
    }
});