from controllers.tarefa_controller import dashboard_usuario, lembretes_usuario


def _rotulo_categoria(categoria):
    return "Diária" if categoria == "diaria" else "Educacional"


def _imprimir_tarefa(tarefa):
    print(f"• {tarefa[1]} [{_rotulo_categoria(tarefa[5])}]")

    if tarefa[2] == "diaria":
        print("  ↳ diária")
    elif tarefa[2] == "semanal":
        print(f"  ↳ semanal ({tarefa[3]})")
    elif tarefa[2] == "mensal":
        print(f"  ↳ mensal (dia {tarefa[4]})")
    else:
        print("  ↳ sem recorrência")


def exibir_lembretes(id_usuario):
    """Mostra tarefas atrasadas e tarefas próximas (próximas 2h)."""
    atrasadas, proximas = lembretes_usuario(id_usuario)

    if not atrasadas and not proximas:
        return

    print("\n LEMBRETES")

    for titulo, horario in atrasadas:
        print(f"  Atrasada: {titulo} (era {horario.strftime('%H:%M')})")

    for titulo, horario in proximas:
        print(f" Em breve: {titulo} às {horario.strftime('%H:%M')}")

    print("\n━━━━━━━━━━━━━━━━━━")


def tela_dashboard(id_usuario):
    exibir_lembretes(id_usuario)

    dados = dashboard_usuario(id_usuario)

    total = dados["total"]
    concluidas = dados["concluidas"]
    pendentes_lista = dados["pendentes_lista"]
    concluidas_lista = dados["concluidas_lista"]

    produtividade = (concluidas / total) * 100 if total > 0 else 0

    print("\n====================")
    print("   DASHBOARD DE HOJE")
    print("====================")

    print(f"\n Total tarefas hoje: {total}")
    print(f"\n Produtividade: {produtividade:.1f}%")

    print("\n━━━━━━━━━━━━━━━━━━")
    print("\n PENDENTES:\n")

    if pendentes_lista:
        for tarefa in pendentes_lista:
            _imprimir_tarefa(tarefa)
    else:
        print("Nenhuma tarefa pendente")

    print("\n━━━━━━━━━━━━━━━━━━")
    print("\n CONCLUÍDAS:\n")

    if concluidas_lista:
        for tarefa in concluidas_lista:
            _imprimir_tarefa(tarefa)
    else:
        print("Nenhuma tarefa concluída")

    print("\n━━━━━━━━━━━━━━━━━━")
    print("\n AÇÕES RÁPIDAS")
    print("\n1 - Criar tarefa")
    print("2 - Concluir tarefa")
    print("3 - Editar Tarefa")
    print("4 - Excluir tarefa")
    print("5 - Dashboard semanal")
    print("6 - Modo Foco")
    print("7 - Conversar com Assistente")
    print("8 - Histórico de produtividade")
    print("0 - Voltar")

    acao = input("\nEscolha: ")

    if acao == "1":
        from views.tarefa_view import tela_criar_tarefa
        tela_criar_tarefa(id_usuario)

    elif acao == "2":
        from views.tarefa_view import tela_concluir_tarefa
        tela_concluir_tarefa(id_usuario)

    elif acao == "3":
        from views.tarefa_view import tela_editar_tarefa
        tela_editar_tarefa(id_usuario)

    elif acao == "4":
        from views.tarefa_view import tela_excluir_tarefa
        tela_excluir_tarefa(id_usuario)

    elif acao == "5":
        from views.dashboard_semanal_view import tela_dashboard_semanal
        tela_dashboard_semanal(id_usuario)

    elif acao == "6":
        from views.foco_view import tela_modo_foco
        tela_modo_foco(id_usuario)

    elif acao == "7":
        from views.ia_view import tela_assistente

        usuario_completo = _montar_usuario_para_assistente(id_usuario)
        tela_assistente(usuario_completo)

    elif acao == "8":
        from views.historico_view import tela_historico_produtividade
        tela_historico_produtividade(id_usuario)


def _montar_usuario_para_assistente(id_usuario):
    """Reconstrói a tupla 'usuario' (id, nome, nivel_ansiedade, email, senha,
    periodo_foco) a partir do id, para reaproveitar tela_assistente()
    quando chamada a partir do Dashboard (onde só temos o id_usuario)."""
    from models.usuario_model import buscar_perfil_usuario

    perfil = buscar_perfil_usuario(id_usuario)
    nome = perfil[0]
    nivel_ansiedade = perfil[1]
    periodo_foco = perfil[5]
    email = perfil[9]

    return (id_usuario, nome, nivel_ansiedade, email, None, periodo_foco)
