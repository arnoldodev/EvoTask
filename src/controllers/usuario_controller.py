from models.usuario_model import (
    buscar_perfil_usuario,
    editar_cadastro_bd,
    alterar_senha_bd,
    buscar_preferencias,
    atualizar_tom_comunicacao_bd,
)


def obter_perfil(id_usuario):
    return buscar_perfil_usuario(id_usuario)


def editar_cadastro(id_usuario, nome, idade, genero, email,
                     nivel_ansiedade, faz_terapia, frequencia_crises,
                     procrastina, periodo_foco, atividade_fisica) -> bool:
    return editar_cadastro_bd(
        id_usuario, nome, idade, genero, email,
        nivel_ansiedade, faz_terapia, frequencia_crises,
        procrastina, periodo_foco, atividade_fisica
    )


def alterar_senha(id_usuario, nova_senha) -> bool:
    return alterar_senha_bd(id_usuario, nova_senha)


def obter_preferencias(id_usuario) -> tuple:
    return buscar_preferencias(id_usuario)


def definir_tom_comunicacao(id_usuario, tom_comunicacao) -> bool:
    return atualizar_tom_comunicacao_bd(id_usuario, tom_comunicacao)
