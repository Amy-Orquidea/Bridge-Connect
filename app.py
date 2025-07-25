from flask import Flask, jsonify, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
db = SQLAlchemy(app)

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    lingua = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(15), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)   

class Usuarios_Ongs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ong_id = db.Column(db.Integer, db.ForeignKey('ongs.id'))
    ong = db.relationship('Ongs', backref='usuarios_ongs') 
    usuarioId = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship('Usuarios', backref='usuarios_ongs')
    
class Usuarios_Advogados(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    advogadoId = db.Column(db.Integer, db.ForeignKey('advogados.id'))
    advogado = db.relationship('Advogados', backref='usuarios_advogados')   
    usuarioId = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship('Usuarios', backref='usuarios_advogados')
    
    
class Advogados(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    lingua = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(15), nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    
class Ongs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    
class Empresas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    salario = db.Column(db.Float(4.2), nullable=False)
    especificacoes = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    contato = db.Column(db.String(20), nullable=False)

class Advogados_Ongs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    advogado_email = db.Column(db.String(50), db.ForeignKey('advogados.email'))
    advogado = db.relationship('Advogados', backref='advogados')
    ong_id = db.Column(db.Integer, db.ForeignKey('ongs.id'))
    ong = db.relationship('Ongs', backref='ongs')
    
class Empresas_Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    empresa = db.relationship('Empresas', backref='empresas')
    usuarioId = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship('Usuarios', backref='usuarios')
        
with app.app_context():
    db.create_all()
    
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/cadastro/usuario', methods=['GET', 'POST'])
def cadastroUsuario():
    # advogado = Advogados.query.all()
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        lingua = request.form['lingua']
        senha = request.form['senha']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        if Usuarios.query.filter_by(email=email).first():
            return jsonify({'message': 'Email já cadastrado'}), 409
        
        db.session.add(Usuarios(email=email, nome=nome, lingua=lingua, senha=senha, telefone=telefone, endereco=endereco))
        db.session.commit()
        return redirect('/')
    return render_template('cadastroUsuario.html')

@app.route('/cadastro/advogado', methods=['GET', 'POST'])
def cadastroAdvogado():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        telefone = request.form['telefone']
        lingua = request.form['lingua']
        senha = request.form['senha']
        if Usuarios.query.filter_by(email=email).first():
           return jsonify({'mensagem': 'Email já cadastrado'}), 400
       
        db.session.add(Advogados(email=email, nome=nome, telefone=telefone, lingua=lingua, senha=senha))
        db.session.commit()
        return redirect('/')
    return render_template('criarAdvogado.html')

@app.route('/cadastro/ong', methods=['GET', 'POST'])
def cadastroOng():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        db.session.add(Ongs(nome=nome, endereco=endereco))
        db.session.commit()
        return redirect('/')
    return render_template('.html')

@app.route('/cadastro/empresa', methods=['GET', 'POST'])
def cadastroEmpresa():
    if request.method == 'POST':
        nome = request.form['nome']
        salario = float(request.form['salario'])
        especificacoes = request.form['especificacoes']
        endereco = request.form['endereco']
        contato = request.form['contato']
        db.session.add(Empresas(nome=nome, salario=salario, especificacoes=especificacoes, endereco=endereco, contato=contato))
        db.session.commit()
        return redirect('/')
    return render_template('.html')

@app.route('/lista/usuarios', methods=['GET'])
def listarUsuarios():
    usuarios = Usuarios.query.all()
    return render_template('listarUsuario.html', usuarios=usuarios)

@app.route('/lista/advogados', methods=['GET'])
def listaAdvogados():
    advogados = Advogados.query.all()
    return render_template('listarAdvogado.html', advogados=advogados)

@app.route('/lista/ongs', methods=['GET'])
def listarOngs():
    ongs = Ongs.query.all()
    return render_template('.html', ongs=ongs)

@app.route('/lista/empresas', methods=['GET'])
def listarEmpresas():
    empresas = Empresas.query.all()
    return render_template('.html', empresas=empresas)

@app.route('/edit/usuario/<int:id>', methods=['GET', 'POST'])
def editarUsuario(id):
    usuario = Usuarios.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.lingua = request.form['lingua']
        usuario.email = request.form['email']
        usuario.senha = request.form['senha']
        usuario.telefone = request.form['telefone']
        usuario.endereco = request.form['endereco']
        db.session.commit()
        return redirect('/lista/usuarios')
    return render_template('editarUsuario.html', usuario=usuario)

@app.route('/edit/advogado/<int:id>', methods=['GET', 'POST'])
def editarAdvogado(id):
    advogado = Advogados.query.get_or_404(id)
    if request.method == 'POST':
        advogado.nome = request.form['nome']
        advogado.email = request.form['email']
        advogado.telefone = request.form['telefone']
        db.session.commit()
        return redirect('/lista/advogados')
    return render_template('editarAdvogado.html', advogado=advogado)

@app.route('/edit/ong/<int:id>', methods=['GET', 'POST'])
def editarOng(id):
    ong = Ongs.query.get_or_404(id)
    if request.method == 'POST':
        ong.nome = request.form['nome']
        ong.endereco = request.form['endereco']
        db.session.commit()
        return redirect('/lista/ongs')
    return render_template('.html', ong=ong)

@app.route('/edit/empresa/<int:id>', methods=['GET', 'POST'])
def editarEmpresa(id):
    empresa = Empresas.query.get_or_404(id)
    if request.method == 'POST':
        empresa.nome = request.form['nome']
        empresa.salario = float(request.form['salario'])
        empresa.especificacoes = request.form['especificacoes']
        empresa.endereco = request.form['endereco']
        empresa.contato = request.form['contato']
        db.session.commit()
        return redirect('/lista/empresas')
    return render_template('.html', empresa=empresa)

@app.route('/delete/usuario/<email>', methods=['GET'])
def deletarUsuario(email):
    usuario = Usuarios.query.get_or_404(email)
    db.session.delete(usuario)
    db.session.commit()
    return redirect('/lista/usuarios')

@app.route('/delete/advogado/<email>', methods=['GET'])
def deletarAdvogado(email):
    advogado = Advogados.query.get_or_404(email)
    db.session.delete(advogado)
    db.session.commit()
    return redirect('/lista/advogados')

@app.route('/delete/ong/<int:id>', methods=['GET'])
def deletarOng(id):
    ong = Ongs.query.get_or_404(id)
    db.session.delete(ong)
    db.session.commit()
    return redirect('/lista/ongs')

@app.route('/delete/empresa/<int:id>', methods=['GET'])
def deletarEmpresa(id):
    empresa = Empresas.query.get_or_404(id)
    db.session.delete(empresa)
    db.session.commit()
    return redirect('/lista/empresas')

if __name__ == '__main__':
    app.run(debug=True)