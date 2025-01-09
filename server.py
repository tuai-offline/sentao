from flask import Flask, request, jsonify, send_from_directory
import tempfile
import subprocess
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/compile', methods=['POST'])
def compile():
    try:
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
            return jsonify({'error': clean_ansi(result.stderr)}), 400

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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)