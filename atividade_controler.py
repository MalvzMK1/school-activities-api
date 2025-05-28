from flask import Blueprint, jsonify, request
import atividade_model
from clients import PessoaServiceClient

atividade_bp = Blueprint('atividade_bp', __name__)

def enrich_atividade_data(atividade_dict):
    """
    Enriquece um dicionário de atividade com dados do professor e respostas com dados do aluno.
    """
    if 'professor_id' in atividade_dict:
        professor_data = PessoaServiceClient.get_professor_data(atividade_dict['professor_id'])
        if professor_data:
            atividade_dict['professor'] = {
                'id': professor_data.get('id'),
                'nome': professor_data.get('nome')
            }
        else:
            atividade_dict['professor'] = None

    if 'respostas' in atividade_dict and atividade_dict['respostas'] is not None:
        for resposta in atividade_dict['respostas']:
            if 'id_aluno' in resposta:
                aluno_data = PessoaServiceClient.get_aluno_data(resposta['id_aluno'])
                if aluno_data:
                    resposta['aluno'] = {
                        'id': aluno_data.get('id'),
                        'nome': aluno_data.get('nome')
                    }
                else:
                    resposta['aluno'] = None
    return atividade_dict


@atividade_bp.route('/', methods=['GET'])
def listar_atividades():
    atividades = atividade_model.listar_atividades()
    enriched_atividades = [enrich_atividade_data(ativ) for ativ in atividades]
    return jsonify(enriched_atividades)

@atividade_bp.route('/', methods=['POST'])
def criar_atividade():
    data = request.json
    id_disciplina = data.get('id_disciplina')
    professor_id = data.get('professor_id')
    enunciado = data.get('enunciado')

    if not all([id_disciplina, professor_id, enunciado]):
        return jsonify({'erro': 'id_disciplina, professor_id e enunciado são obrigatórios'}), 400

    nova_atividade = atividade_model.criar_atividade(id_disciplina, professor_id, enunciado)
    enriched_nova_atividade = enrich_atividade_data(nova_atividade)
    return jsonify({'mensagem': 'Atividade criada com sucesso', 'atividade': enriched_nova_atividade}), 201

@atividade_bp.route('/<int:id_atividade>/respostas', methods=['POST'])
def adicionar_resposta(id_atividade):
    data = request.json
    id_aluno = data.get('id_aluno')
    resposta_texto = data.get('resposta')

    if not all([id_aluno, resposta_texto]):
        return jsonify({'erro': 'id_aluno e resposta são obrigatórios'}), 400
    
    try:
        nova_resposta = atividade_model.adicionar_resposta(id_atividade, id_aluno, resposta_texto)
        return jsonify({'mensagem': 'Resposta adicionada com sucesso', 'resposta': nova_resposta}), 201
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/<int:id_atividade>/respostas/<int:id_aluno>/nota', methods=['PUT'])
def atualizar_nota_resposta(id_atividade, id_aluno):
    data = request.json
    nova_nota = data.get('nota')

    if nova_nota is None:
        return jsonify({'erro': 'O campo "nota" é obrigatório'}), 400
    
    try:
        resposta_atualizada = atividade_model.atualizar_nota_resposta(id_atividade, id_aluno, nova_nota)
        return jsonify({'mensagem': 'Nota atualizada com sucesso', 'resposta': resposta_atualizada})
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 404

@atividade_bp.route('/<int:id_atividade>', methods=['DELETE'])
def deletar_atividade(id_atividade):
    try:
        atividade_model.deletar_atividade(id_atividade)
        return jsonify({'mensagem': 'Atividade deletada com sucesso'}), 204
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
