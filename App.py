from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para armazenar as inscrições
inscricoes = []

# Contador de inscrições
contador_inscricoes = 0

# Número máximo de inscrições permitidas
max_inscricoes = 50

@app.route('/')
def index():
    return render_template('index.html', inscricoes=inscricoes, contador_inscricoes=contador_inscricoes, max_inscricoes=max_inscricoes)

@app.route('/inscrever', methods=['POST'])
def inscrever():
    global contador_inscricoes

    nome = request.form.get('nome')
    idade = request.form.get('idade')
    endereco = request.form.get('endereco')
    residencia_sp = request.form.get('residencia_sp')
    evento_noite = request.form.get('evento_noite')

    mensagem_idade = ''
    mensagem_residencia_sp = ''
    mensagem_evento_noite = ''
    mensagem_endereco = ''
    mensagem_nome = ''
    mensagem_sucesso = ''  # Adicionada mensagem de sucesso

    # Verificar se a idade é maior ou igual a 18
    try:
        idade = int(idade)
        if idade < 18:
            mensagem_idade = 'A participação é restrita a maiores de 18 anos.'
    except (ValueError, TypeError):
        mensagem_idade = 'Idade inválida. Informe um número.'

    # Verificar se o endereço foi preenchido
    if not endereco:
        mensagem_endereco = 'O endereço é obrigatório.'

    # Verificar se a checkbox de residência em SP está marcada
    if residencia_sp is None:
        mensagem_residencia_sp = 'Confirme que você reside em São Paulo (SP).'

    # Verificar se a checkbox do evento à noite está marcada
    if evento_noite is None:
        mensagem_evento_noite = 'Confirme que você pode participar do evento à noite.'

    # Verificar se o nome contém números
    if any(char.isdigit() for char in nome):
        mensagem_nome = 'O nome não pode conter números.'

    if mensagem_idade or mensagem_residencia_sp or mensagem_evento_noite or mensagem_endereco or mensagem_nome:
        return render_template('index.html', inscricoes=inscricoes,
                               mensagem_idade=mensagem_idade,
                               mensagem_residencia_sp=mensagem_residencia_sp,
                               mensagem_evento_noite=mensagem_evento_noite,
                               mensagem_endereco=mensagem_endereco,
                               mensagem_nome=mensagem_nome,
                               nome=nome, idade=idade, endereco=endereco, residencia_sp=residencia_sp, evento_noite=evento_noite,
                               contador_inscricoes=contador_inscricoes, max_inscricoes=max_inscricoes)

    # Incrementar o contador de inscrições
    contador_inscricoes += 1

    # Adicionar a inscrição à lista
    nome_formatado = ' '.join([parte[0] + '*' * (len(parte)-2) + parte[-1] if len(parte) > 1 else parte for parte in nome.split()])
    inscricao = {
        'numero': f'{contador_inscricoes:04d}',
        'nome': nome_formatado,
    }
    inscricoes.append(inscricao)

    mensagem_sucesso = 'Inscrição efetuada com sucesso!'  # Adicionada mensagem de sucesso

    return render_template('index.html', inscricoes=inscricoes,
                           mensagem_sucesso=mensagem_sucesso,
                           contador_inscricoes=contador_inscricoes, max_inscricoes=max_inscricoes)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    global contador_inscricoes, inscricoes

    if request.method == 'POST':
        # Reinicializar a lista de inscrições e o contador
        contador_inscricoes = 0
        inscricoes = []

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
