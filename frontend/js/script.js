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
    escreve("Olá, mundo!")
    retorna 0;
}`);

// URL do backend - altere para a URL do seu backend quando estiver implantado
const BACKEND_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000'
    : 'https://sentao-backend.onrender.com'; // Substitua com sua URL do Render

document.getElementById("run-btn").addEventListener("click", async function() {
    const button = this;
    const code = editor.getValue();
    const outputEwvm = document.getElementById("output-ewvm");
    const outputProgram = document.getElementById("output-program");
    
    try {
        // Disable button and show loading state
        button.disabled = true;
        outputProgram.textContent = "Executando o código...\n";
        document.querySelector('.editor-container').classList.add('loading');
        
        const response = await fetch(`${BACKEND_URL}/compile`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ code: code })
        });

        // Verifique se a resposta é JSON antes de tentar fazer o parse
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error(`Resposta não-JSON do servidor: ${await response.text()}`);
        }

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
        outputProgram.textContent = `Erro de conexão: ${error.message}\n\n` +
            'Se o servidor estiver inativo, a primeira requisição pode demorar até 30 segundos. ' +
            'Por favor, tente novamente.';
    } finally {
        // Re-enable button and remove loading state
        button.disabled = false;
        document.querySelector('.editor-container').classList.remove('loading');
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