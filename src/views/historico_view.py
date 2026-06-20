from controllers.tarefa_controller import historico_produtividade

DIAS_SEMANA_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


def tela_historico_produtividade(id_usuario):
    registros = historico_produtividade(id_usuario, dias=7)

    print("\n=================================")
    print("   HISTÓRICO DE PRODUTIVIDADE")
    print("        (últimos 7 dias)")
    print("=================================\n")

    if not registros:
        print("Ainda não há histórico de produtividade.")
        print("Ele é construído automaticamente conforme você conclui tarefas.")
        return

    for data, concluidas, totais in registros:
        produtividade = (concluidas / totais) * 100 if totais > 0 else 0
        dia_semana = DIAS_SEMANA_PT[data.weekday()]

        print(f"📅 {data.strftime('%d/%m/%Y')} ({dia_semana})")
        print(f"   Tarefas concluídas: {concluidas}/{totais}")
        print(f"   Produtividade: {produtividade:.1f}%")
        print("   " + "-" * 30)

    melhor_dia = max(registros, key=lambda r: (r[1] / r[2]) if r[2] > 0 else 0)
    print(f"\n🏆 Melhor dia: {melhor_dia[0].strftime('%d/%m/%Y')} "
          f"({(melhor_dia[1] / melhor_dia[2]) * 100 if melhor_dia[2] > 0 else 0:.1f}%)")
