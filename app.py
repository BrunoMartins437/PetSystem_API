import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from werkzeug.utils import secure_filename

from model import db, Pet
from schemas import (
    ESPECIES_OPCOES,
    PET_SEXO_OPCOES,
    normalize_color_to_masculine,
    is_valid_uf,
    apresenta_pet,
    apresenta_pets,
    apresenta_erro
)
from logger import logger

app = Flask(__name__)
CORS(app)
Swagger(app)

# ---------------------------------------------------------
# CONFIGURAÇÃO DE DIRETÓRIOS E BANCO DE DADOS
# ---------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "petsystem.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

# ---------------------------------------------------------
# ROTAS PET
# ---------------------------------------------------------
@app.route('/pets', methods=['POST'])
def criar_pet():
    """
    Cria um novo pet
    ---
    tags:
      - Pets
    consumes:
      - multipart/form-data
    parameters:
      - name: nome
        in: formData
        type: string
        required: true
      - name: especie
        in: formData
        type: string
        enum: ["Cachorro", "Gato"]
        required: true
      - name: sexo
        in: formData
        type: string
        enum: ["Fêmea", "Macho"]
        required: true
      - name: cor_pelagem
        in: formData
        type: string
        description: "Informe no masculino. Ex: branco (não 'branca')"
      - name: raca
        in: formData
        type: string
      - name: idade
        in: formData
        type: integer
      - name: bairro
        in: formData
        type: string
      - name: municipio
        in: formData
        type: string
      - name: uf
        in: formData
        type: string
      - name: foto
        in: formData
        type: file
        required: false
    responses:
      201:
        description: Pet criado com sucesso
      400:
        description: Requisição inválida
    """
    form = request.form

    nome = form.get('nome')
    especie = form.get('especie')
    sexo = form.get('sexo')

    if not nome:
        logger.warning("Tentativa de criar pet sem o campo 'nome'")
        return jsonify(apresenta_erro("Campo 'nome' é obrigatório.")), 400
    if not especie or especie not in ESPECIES_OPCOES or especie == "--":
        return jsonify(apresenta_erro("Campo 'especie' inválido. Selecione uma opção válida.")), 400
    if not sexo or sexo not in PET_SEXO_OPCOES or sexo == "--":
        return jsonify(apresenta_erro("Campo 'sexo' inválido. Selecione uma opção válida.")), 400

    cor_pelagem_raw = form.get('cor_pelagem')
    cor_pelagem = normalize_color_to_masculine(cor_pelagem_raw) if cor_pelagem_raw else None

    raca = form.get('raca')
    idade_raw = form.get('idade')
    idade_int = None
    if idade_raw:
        try:
            idade_int = int(idade_raw)
            if idade_int < 0:
                return jsonify(apresenta_erro("Campo 'idade' deve ser inteiro não-negativo.")), 400
        except ValueError:
            return jsonify(apresenta_erro("Campo 'idade' deve ser um número inteiro.")), 400

    bairro = form.get('bairro')
    municipio = form.get('municipio')
    uf = form.get('uf')

    novo_pet = Pet(
        nome=nome,
        especie=especie,
        sexo=sexo,
        cor_pelagem=cor_pelagem,
        raca=raca,
        idade=idade_int,
        bairro=bairro,
        municipio=municipio,
        uf=uf
    )

    if 'foto' in request.files:
        foto = request.files['foto']
        if foto and foto.filename:
            filename = secure_filename(foto.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(path)
            novo_pet.foto = path

    logger.info(f"Adicionando pet '{novo_pet.nome}'")
    db.session.add(novo_pet)
    db.session.commit()

    return jsonify(apresenta_pet(novo_pet)), 201


@app.route('/pets', methods=['GET'])
def listar_pets():
    """
    Lista pets ou filtra por parâmetros
    ---
    tags:
      - Pets
    parameters:
      - name: id
        in: query
        type: integer
      - name: nome
        in: query
        type: string
      - name: especie
        in: query
        type: string
        enum: ["--", "Cachorro", "Gato"]
      - name: sexo
        in: query
        type: string
        enum: ["--", "Fêmea", "Macho"]
      - name: bairro
        in: query
        type: string
      - name: municipio
        in: query
        type: string
      - name: uf
        in: query
        type: string
    responses:
      200:
        description: Lista de pets
      400:
        description: Parâmetro inválido
    """
    logger.info("Buscando registros de pets...")
    q = Pet.query
    id_q = request.args.get('id')
    nome_q = request.args.get('nome')
    especie_q = request.args.get('especie')
    sexo_q = request.args.get('sexo')
    bairro_q = request.args.get('bairro')
    municipio_q = request.args.get('municipio')
    uf_q = request.args.get('uf')

    if id_q:
        try:
            id_int = int(id_q)
            q = q.filter_by(id=id_int)
        except ValueError:
            return jsonify(apresenta_erro("Parâmetro 'id' deve ser inteiro.")), 400

    if nome_q:
        q = q.filter(Pet.nome.ilike(f"%{nome_q}%"))

    if especie_q:
        if especie_q not in ESPECIES_OPCOES or especie_q == "--":
            return jsonify(apresenta_erro("Parâmetro 'especie' inválido.")), 400
        q = q.filter_by(especie=especie_q)

    if sexo_q and sexo_q.strip() not in ("", "--"):
        if sexo_q not in PET_SEXO_OPCOES:
            return jsonify(apresenta_erro("Parâmetro 'sexo' inválido.")), 400
        q = q.filter_by(sexo=sexo_q)

    if bairro_q:
        q = q.filter(Pet.bairro.ilike(f"%{bairro_q}%"))
    if municipio_q:
        q = q.filter(Pet.municipio.ilike(f"%{municipio_q}%"))
    if uf_q:
        q = q.filter(Pet.uf.ilike(f"%{uf_q}%"))

    pets = q.all()
    if not pets:
        return jsonify({"message": "A pesquisa com esses parâmetros não retornou nenhum resultado."}), 200

    return jsonify(apresenta_pets(pets)), 200


@app.route('/pets/<int:id>', methods=['PUT'])
def atualizar_pet(id):
    """
    Atualiza um pet existente
    ---
    tags:
      - Pets
    consumes:
      - multipart/form-data
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: nome
        in: formData
        type: string
        description: "Exemplo: Rex"
      - name: especie
        in: formData
        type: string
        enum: ["--", "Cachorro", "Gato"]
      - name: sexo
        in: formData
        type: string
        enum: ["--", "Fêmea", "Macho"]
      - name: cor_pelagem
        in: formData
        type: string
        description: "Informe no masculino. Ex: branco (não 'branca')"
      - name: raca
        in: formData
        type: string
      - name: idade
        in: formData
        type: integer
      - name: bairro
        in: formData
        type: string
      - name: municipio
        in: formData
        type: string
      - name: uf
        in: formData
        type: string
        description: "Sigla UF válida. Ex: RJ, SP"
      - name: foto
        in: formData
        type: file
    responses:
      200:
        description: Pet atualizado com sucesso
      400:
        description: Requisição inválida
      404:
        description: Pet não encontrado
    """
    pet = Pet.query.get_or_404(id)
    form = request.form

    nome = form.get('nome', pet.nome)
    especie = form.get('especie', pet.especie)
    sexo = form.get('sexo', pet.sexo)
    cor_pelagem_raw = form.get('cor_pelagem', pet.cor_pelagem)
    raca = form.get('raca', pet.raca)
    idade_raw = form.get('idade')
    bairro = form.get('bairro', pet.bairro)
    municipio = form.get('municipio', pet.municipio)
    uf = form.get('uf', pet.uf)

    if especie is None or especie not in ESPECIES_OPCOES or especie == "--":
        return jsonify(apresenta_erro("Campo 'especie' inválido. Selecione uma opção válida.")), 400
    if sexo is None or sexo not in PET_SEXO_OPCOES or sexo == "--":
        return jsonify(apresenta_erro("Campo 'sexo' inválido. Selecione uma opção válida.")), 400

    idade_int = pet.idade
    if idade_raw is not None and idade_raw != "":
        try:
            idade_int = int(idade_raw)
            if idade_int < 0:
                return jsonify(apresenta_erro("Campo 'idade' deve ser inteiro não-negativo.")), 400
        except ValueError:
            return jsonify(apresenta_erro("Campo 'idade' deve ser um número inteiro.")), 400

    if uf is not None and uf != "":
        if not is_valid_uf(uf):
            return jsonify(apresenta_erro("Campo 'uf' inválido. Use sigla UF válida (ex: RJ, SP).")), 400
        uf = uf.strip().upper()

    cor_pelagem = normalize_color_to_masculine(cor_pelagem_raw) if cor_pelagem_raw else None

    pet.nome = nome
    pet.especie = especie
    pet.sexo = sexo
    pet.cor_pelagem = cor_pelagem
    pet.raca = raca
    pet.idade = idade_int
    pet.bairro = bairro
    pet.municipio = municipio
    pet.uf = uf

    if 'foto' in request.files:
        foto = request.files['foto']
        if foto and foto.filename:
            filename = secure_filename(foto.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(path)
            pet.foto = path

    logger.info(f"Atualizando pet ID {id} ('{pet.nome}')")
    db.session.commit()

    return jsonify(apresenta_pet(pet)), 200


@app.route('/pets/<int:id>', methods=['DELETE'])
def deletar_pet(id):
    """
    Deleta um pet pelo ID
    ---
    tags:
      - Pets
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Pet deletado com sucesso
      404:
        description: Pet não encontrado
    """
    pet = Pet.query.get_or_404(id)
    logger.info(f"Deletando pet ID {id}")
    db.session.delete(pet)
    db.session.commit()
    return jsonify({"message": "Pet deletado com sucesso."}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)