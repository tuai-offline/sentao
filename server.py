from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tempfile
import subprocess
import os

app = Flask(__name__)

# Configure CORS para aceitar requisições do seu domínio Netlify
CORS(app, origins=[
    'http://localhost:3000',
    'http://localhost:5000',
    'https://loquacious-crumble-b743a9.netlify.app',
    'https://seu-app.herokuapp.com'  # Adicione seu domínio Heroku aqui
])

@app.route('/compile', methods=['POST'])
def compile():
    try:
        print("Received request:", request.get_json())
        code = request.json['code']
        
        def clean_ansi(text):
            import re
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            return ansi_escape.sub('', text)
        
        # Criar arquivo temporário com o código
        with tempfile.NamedTemporaryFile(suffix='.ent', mode='w', delete=False) as f:
            f.write(code)
            temp_file = f.name

        # Compilar o código
        output_file = temp_file + '.ewvm'
        result = subprocess.run(['python', 'parser.py', temp_file, '-o', output_file], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            error_output = result.stderr if result.stderr else result.stdout
            return jsonify({
                'error': clean_ansi(error_output),
                'error_type': 'compilation_error'
            }), 400

        # Ler o conteúdo do arquivo EWVM
        ewvm_content = ''
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                ewvm_content = f.read()

        # Executar o código compilado (você precisará implementar o interpretador)
        # result = subprocess.run(['python', 'interpreter.py', output_file], 
        #                        capture_output=True, text=True)
        
        # Limpar arquivos temporários
        os.unlink(temp_file)
        if os.path.exists(output_file):
            os.unlink(output_file)
        
        return jsonify({
            'ewvm': ewvm_content,
            'output': clean_ansi(result.stdout)
        })

    except Exception as e:
        print("Server error:", str(e))
        return jsonify({
            'error': str(e),
            'error_type': 'server_error'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)