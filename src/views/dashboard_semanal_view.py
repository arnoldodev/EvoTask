from controllers.tarefa_controller import historico_produtividade

DIAS_SEMANA_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


def tela_dashboard_semanal(id_usuario):
    registros = historico_produtividade(id_usuario, dias=7)

    print("\n========================")
    print("   DASHBOARD SEMANAL")
    print("========================")

    if not registros:
        print("\nAinda não há dados de produtividade registrados nos últimos 7 dias.")
        print("Conclua tarefas para começar a ver seu progresso aqui!")
        return

    total_concluidas = 0
    total_tarefas = 0

    print("\nResumo dos últimos 7 dias:\n")

    for data, concluidas, totais in registros:
        produtividade = (concluidas / totais) * 100 if totais > 0 else 0
        dia_semana = DIAS_SEMANA_PT[data.weekday()]

        barra = "█" * round(produtividade / 10)
        print(f"{data.strftime('%d/%m')} ({dia_semana[:3]}): {barra:<10} {produtividade:5.1f}%  ({concluidas}/{totais})")

        total_concluidas += concluidas
        total_tarefas += totais

    media_semanal = (total_concluidas / total_tarefas) * 100 if total_tarefas > 0 else 0

    print("\n━━━━━━━━━━━━━━━━━━")
    print(f"\n Produtividade média da semana: {media_semanal:.1f}%")
    print(f" Total concluídas: {total_concluidas} de {total_tarefas}")

    if media_semanal >= 80:
        print("\n Excelente semana! Continue assim.")
    elif media_semanal >= 50:
        print("\n Boa semana, mas ainda há espaço para melhorar.")
    else:
        print("\n Semana difícil. Considere reduzir o número de tarefas diárias ou ajustar prioridades.")
