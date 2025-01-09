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

        const result = await response.json();

        if (!response.ok) {
            if (result.error_type === 'compilation_error') {
                outputEwvm.textContent = '';
                outputProgram.textContent = result.error;
            } else {
                outputEwvm.textContent = '';
                outputProgram.textContent = "Erro do servidor: " + result.error;
            }
            return;
        }

        outputEwvm.textContent = result.ewvm || '';
        outputProgram.textContent = result.output || '';

    } catch (error) {
        outputEwvm.textContent = '';
        outputProgram.textContent = "Erro de conexão: " + error.message;
    }
});

// Função para copiar texto
function copyText(text) {
    // Criar elemento temporário
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    
    // Selecionar e copiar
    textarea.select();
    document.execCommand('copy');
    
    // Remover elemento temporário
    document.body.removeChild(textarea);
}

// Adicionar event listeners para os botões de cópia
document.querySelectorAll('.copy-btn').forEach(button => {
    button.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const text = document.getElementById(targetId).textContent;
        
        copyText(text);
        
        // Feedback visual
        this.classList.add('success');
        this.textContent = 'Copiado!';
        
        // Resetar botão após 2 segundos
        setTimeout(() => {
            this.classList.remove('success');
            this.textContent = 'Copiar';
        }, 2000);
    });
});