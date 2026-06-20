from services.ia_service import conversar
from models.tarefa_model import buscar_tarefas_por_status
from models.usuario_model import buscar_preferencias
from datetime import datetime


def conversar_assistente(mensagem, usuario):
    perfil = usuario
    id_usuario = usuario[0] if isinstance(usuario, (tuple, list)) else usuario

    agora = datetime.now()
    hora_atual = agora.strftime("%H:%M")
    data_atual = agora.strftime("%d/%m/%Y")

    if 6 <= agora.hour < 12:
        periodo_atual = "manhã"
    elif 12 <= agora.hour < 18:
        periodo_atual = "tarde"
    else:
        periodo_atual = "noite"

    tarefas_hoje_pendentes = buscar_tarefas_por_status(id_usuario, data="hoje", status="pendente")
    tarefas_hoje_concluidas = buscar_tarefas_por_status(id_usuario, data="hoje", status="concluida")
    tarefas_ontem_pendentes = buscar_tarefas_por_status(id_usuario, data="ontem", status="pendente")
    tarefas_ontem_concluidas = buscar_tarefas_por_status(id_usuario, data="ontem", status="concluida")

    _notificacoes, tom_comunicacao = buscar_preferencias(id_usuario)

    return conversar(
        mensagem=mensagem,
        perfil=perfil,
        tarefas_hoje_pendentes=tarefas_hoje_pendentes,
        tarefas_hoje_concluidas=tarefas_hoje_concluidas,
        tarefas_ontem_pendentes=tarefas_ontem_pendentes,
        tarefas_ontem_concluidas=tarefas_ontem_concluidas,
        hora_atual=hora_atual,
        data_atual=data_atual,
        periodo_atual=periodo_atual,
        tom_comunicacao=tom_comunicacao,
    )
