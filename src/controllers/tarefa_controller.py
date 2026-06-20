from models.tarefa_model import (
    salvar_tarefa,
    buscar_tarefas,
    concluir_tarefa,
    buscar_dados_dashboard,
    excluir_tarefa,
    editar_tarefa_bd,
    buscar_tarefas_pendentes_proximas,
    buscar_historico_produtividade,
)


def criar_tarefa(
    id_usuario: int,
    titulo: str,
    descricao: str,
    categoria: str,
    prioridade: str,
    horario_inicio: str,
    horario_fim: str,
    tipo_recorrencia: str,
    dias_semana: str | None,
    dia_mes: int | None
) -> None:
    salvar_tarefa(id_usuario, titulo, descricao, categoria, prioridade,
                  horario_inicio, horario_fim, tipo_recorrencia,
                  dias_semana, dia_mes)


def listar_tarefas(id_usuario: int, categoria: str | None = None) -> list:
    return buscar_tarefas(id_usuario, categoria)


def finalizar_tarefa(id_tarefa: int, id_usuario: int) -> None:
    concluir_tarefa(id_tarefa, id_usuario)


def dashboard_usuario(id_usuario: int, categoria: str | None = None) -> dict:
    return buscar_dados_dashboard(id_usuario, categoria)


def editar_tarefa(id_tarefa: int, id_usuario: int, titulo: str, prioridade: str,
                   horario_inicio: str, horario_fim: str,
                   categoria: str | None = None) -> bool:
    return editar_tarefa_bd(id_tarefa, id_usuario, titulo, prioridade,
                             horario_inicio, horario_fim, categoria)


def remover_tarefa(id_tarefa: int, id_usuario: int) -> None:
    excluir_tarefa(id_tarefa, id_usuario)


def lembretes_usuario(id_usuario: int, janela_minutos: int = 120) -> tuple:
    """Retorna (atrasadas, proximas): tarefas pendentes de hoje que já
    passaram do horário ou que vão começar em breve."""
    return buscar_tarefas_pendentes_proximas(id_usuario, janela_minutos)


def historico_produtividade(id_usuario: int, dias: int = 7) -> list:
    return buscar_historico_produtividade(id_usuario, dias)
