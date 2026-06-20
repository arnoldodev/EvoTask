from models.db_config import conectar
from datetime import datetime, timedelta
from utils.logger import get_logger

logger = get_logger("tarefa_model")

CATEGORIAS_VALIDAS = ("diaria", "educacional")

DIAS_MAP = {
    "mon": "seg",
    "tue": "ter",
    "wed": "qua",
    "thu": "qui",
    "fri": "sex",
    "sat": "sab",
    "sun": "dom",
}


def salvar_tarefa(
    id_usuario,
    titulo,
    descricao,
    categoria,
    prioridade,
    horario_inicio,
    horario_fim,
    tipo_recorrencia,
    dias_semana,
    dia_mes
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tarefas(
            id_usuario, titulo, descricao, categoria, prioridade,
            horario_inicio, horario_fim, tipo_recorrencia, dias_semana, dia_mes
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            id_usuario,
            titulo,
            descricao,
            categoria,
            prioridade,
            horario_inicio,
            horario_fim,
            tipo_recorrencia,
            dias_semana,
            dia_mes
        )
    )

    conn.commit()
    cursor.close()
    conn.close()


def buscar_tarefas(id_usuario, categoria=None):
    """Lista as tarefas do usuário. Se `categoria` for informada, filtra
    apenas tarefas 'diaria' ou 'educacional'."""
    conn = conectar()
    cursor = conn.cursor()

    if categoria:
        cursor.execute(
            """
            SELECT id, titulo, prioridade, horario_inicio, horario_fim,
                   tipo_recorrencia, dias_semana, dia_mes, concluida, categoria
            FROM tarefas
            WHERE id_usuario=%s AND categoria=%s
            ORDER BY horario_inicio
            """,
            (id_usuario, categoria)
        )
    else:
        cursor.execute(
            """
            SELECT id, titulo, prioridade, horario_inicio, horario_fim,
                   tipo_recorrencia, dias_semana, dia_mes, concluida, categoria
            FROM tarefas
            WHERE id_usuario=%s
            ORDER BY horario_inicio
            """,
            (id_usuario,)
        )

    tarefas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tarefas


def concluir_tarefa(id_tarefa, id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tarefas
        SET concluida=1, ultima_conclusao=CURDATE()
        WHERE id=%s AND id_usuario=%s
        """,
        (id_tarefa, id_usuario)
    )

    conn.commit()
    cursor.close()
    conn.close()
    _registrar_snapshot_dia(id_usuario)


def _tarefa_ocorre_hoje(tipo, dias, dia_mes, inicio, hoje):
    """Decide se uma tarefa recorrente (ou pontual) deve aparecer hoje."""
    if isinstance(inicio, str):
        inicio = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")

    # Tarefas com início futuro não aparecem ainda.
    if inicio.date() > hoje.date():
        return False

    if tipo == "diaria":
        return True

    if tipo == "semanal":
        hoje_semana = DIAS_MAP[hoje.strftime("%a").lower()]
        return bool(dias and hoje_semana in dias.lower())

    if tipo == "mensal":
        return bool(dia_mes and hoje.day == dia_mes)

    # tipo == "nenhuma" (tarefa pontual, sem recorrência)
    return inicio.date() == hoje.date()


def buscar_dados_dashboard(id_usuario, categoria=None):
    conn = conectar()
    cursor = conn.cursor()

    # RESET AUTOMÁTICO DAS TAREFAS DIÁRIAS (uma vez por novo dia)
    cursor.execute(
        """
        UPDATE tarefas
        SET concluida=0
        WHERE tipo_recorrencia='diaria'
          AND (ultima_conclusao IS NULL OR ultima_conclusao < CURDATE())
        """
    )
    conn.commit()

    hoje = datetime.now()

    query = """
        SELECT id, titulo, tipo_recorrencia, dias_semana, dia_mes,
               horario_inicio, concluida, ultima_conclusao, categoria
        FROM tarefas
        WHERE id_usuario=%s
    """
    params = [id_usuario]
    if categoria:
        query += " AND categoria=%s"
        params.append(categoria)

    cursor.execute(query, tuple(params))
    tarefas = cursor.fetchall()
    cursor.close()
    conn.close()

    pendentes_lista = []
    concluidas_lista = []

    for tarefa in tarefas:
        (id_tarefa, titulo, tipo, dias, dia_mes, inicio,
         concluida, ultima_conclusao, cat) = tarefa

        if not _tarefa_ocorre_hoje(tipo, dias, dia_mes, inicio, hoje):
            continue

        # Reset lógico: se a última conclusão não foi hoje, a recorrência
        # ainda não foi cumprida no dia de hoje.
        if tipo in ("diaria", "semanal", "mensal") and ultima_conclusao:
            if ultima_conclusao < hoje.date():
                concluida = 0

        tarefa_dashboard = (id_tarefa, titulo, tipo, dias, dia_mes, cat)

        if concluida:
            concluidas_lista.append(tarefa_dashboard)
        else:
            pendentes_lista.append(tarefa_dashboard)

    return {
        "total": len(pendentes_lista) + len(concluidas_lista),
        "concluidas": len(concluidas_lista),
        "pendentes": len(pendentes_lista),
        "pendentes_lista": pendentes_lista,
        "concluidas_lista": concluidas_lista,
    }


def excluir_tarefa(id_tarefa, id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tarefas WHERE id=%s AND id_usuario=%s",
        (id_tarefa, id_usuario)
    )
    conn.commit()
    cursor.close()
    conn.close()


def buscar_tarefas_pendentes_hoje(id_usuario):
    dados = buscar_dados_dashboard(id_usuario)
    return dados["pendentes_lista"]


def buscar_tarefa_por_id(id_tarefa, id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, titulo, horario_inicio, horario_fim
        FROM tarefas
        WHERE id=%s AND id_usuario=%s
        """,
        (id_tarefa, id_usuario)
    )
    tarefa = cursor.fetchone()
    cursor.close()
    conn.close()
    return tarefa


def editar_tarefa_bd(id_tarefa, id_usuario, titulo, prioridade,
                      horario_inicio, horario_fim, categoria=None):
    conn = conectar()
    cursor = conn.cursor()

    try:
        if categoria:
            cursor.execute(
                """
                UPDATE tarefas
                SET titulo=%s, prioridade=%s, horario_inicio=%s,
                    horario_fim=%s, categoria=%s
                WHERE id=%s AND id_usuario=%s
                """,
                (titulo, prioridade, horario_inicio, horario_fim,
                 categoria, id_tarefa, id_usuario)
            )
        else:
            cursor.execute(
                """
                UPDATE tarefas
                SET titulo=%s, prioridade=%s, horario_inicio=%s, horario_fim=%s
                WHERE id=%s AND id_usuario=%s
                """,
                (titulo, prioridade, horario_inicio, horario_fim,
                 id_tarefa, id_usuario)
            )

        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        logger.error(f"Erro ao editar tarefa {id_tarefa} do usuário {id_usuario}: {e}")
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()


def buscar_tarefas_por_status(id_usuario, data, status):
    if data == "hoje":
        dados_dashboard = buscar_dados_dashboard(id_usuario)

        if status == "pendente":
            return [t[1] for t in dados_dashboard["pendentes_lista"]]
        elif status == "concluida":
            return [t[1] for t in dados_dashboard["concluidas_lista"]]

    elif data == "ontem":
        conn = conectar()
        cursor = conn.cursor()

        ontem = (datetime.now() - timedelta(days=1)).date()

        if status == "concluida":
            cursor.execute(
                """
                SELECT titulo, horario_inicio FROM tarefas
                WHERE id_usuario = %s AND ultima_conclusao = %s
                """,
                (id_usuario, ontem)
            )
            tarefas_ontem = cursor.fetchall()
            cursor.close()
            conn.close()

            return [
                f"{t[0]} às {t[1].strftime('%H:%M')}" if t[1] and hasattr(t[1], 'strftime') else t[0]
                for t in tarefas_ontem
            ]

        elif status == "pendente":
            cursor.execute(
                """
                SELECT titulo, horario_inicio FROM tarefas
                WHERE id_usuario = %s
                  AND DATE(horario_inicio) <= %s
                  AND (ultima_conclusao IS NULL OR ultima_conclusao < %s)
                """,
                (id_usuario, ontem, ontem)
            )
            tarefas_ontem = cursor.fetchall()
            cursor.close()
            conn.close()

            return [
                f"{t[0]} (Agendada para as {t[1].strftime('%H:%M')})" if t[1] and hasattr(t[1], 'strftime') else t[0]
                for t in tarefas_ontem
            ]

    return []


def buscar_tarefas_pendentes_proximas(id_usuario, janela_minutos=120):
    """Usado pelo lembrete de tarefa ao abrir o app: retorna duas listas,
    (atrasadas, proximas) com tarefas pendentes de hoje."""
    dados = buscar_dados_dashboard(id_usuario)
    agora = datetime.now()

    atrasadas = []
    proximas = []

    for tarefa in dados["pendentes_lista"]:
        id_tarefa, titulo = tarefa[0], tarefa[1]

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT horario_inicio FROM tarefas WHERE id=%s",
            (id_tarefa,)
        )
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()

        if not resultado or not resultado[0]:
            continue

        horario_inicio = resultado[0]
        if isinstance(horario_inicio, str):
            horario_inicio = datetime.strptime(horario_inicio, "%Y-%m-%d %H:%M:%S")

        if horario_inicio < agora:
            atrasadas.append((titulo, horario_inicio))
        elif horario_inicio <= agora + timedelta(minutes=janela_minutos):
            proximas.append((titulo, horario_inicio))

    return atrasadas, proximas


def _registrar_snapshot_dia(id_usuario):
    """Atualiza (ou cria) o registro de produtividade do dia de hoje.
    Chamado sempre que uma tarefa é concluída, para alimentar o
    Dashboard Semanal e o Histórico de Produtividade."""
    dados = buscar_dados_dashboard(id_usuario)
    hoje = datetime.now().date()

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO registro (id_usuario, tarefas_concluidas, tarefas_totais, data)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                tarefas_concluidas = %s,
                tarefas_totais = %s
            """,
            (
                id_usuario, dados["concluidas"], dados["total"], hoje,
                dados["concluidas"], dados["total"]
            )
        )
        conn.commit()

    except Exception as e:
        logger.error(f"Erro ao registrar snapshot diário do usuário {id_usuario}: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def buscar_historico_produtividade(id_usuario, dias=7):
    """Retorna os registros diários de produtividade dos últimos `dias`
    dias (incluindo hoje), ordenados do mais antigo para o mais recente."""
    inicio = (datetime.now().date() - timedelta(days=dias - 1))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT data, tarefas_concluidas, tarefas_totais
        FROM registro
        WHERE id_usuario=%s AND data >= %s
        ORDER BY data ASC
        """,
        (id_usuario, inicio)
    )
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    return registros
