from controllers.tarefa_controller import (
    criar_tarefa,
    listar_tarefas,
    finalizar_tarefa,
    remover_tarefa,
    editar_tarefa,
)
from models.tarefa_model import buscar_tarefas_pendentes_hoje
from utils.validacoes import validar_datas_tarefa, ler_inteiro

CATEGORIAS = {"1": "diaria", "2": "educacional"}


def escolher_categoria() -> str:
    print("\nCategoria da tarefa")
    print("1 - Diária (rotina pessoal)")
    print("2 - Educacional (estudos/curso)")

    while True:
        opcao = input("Escolha: ")
        if opcao in CATEGORIAS:
            return CATEGORIAS[opcao]
        print("Opção inválida. Digite 1 ou 2.")


def rotulo_categoria(categoria: str) -> str:
    return "Diária" if categoria == "diaria" else "Educacional"


def tela_criar_tarefa(id_usuario):
    print("\nCRIAR TAREFA")

    titulo = input("Titulo: ")
    descricao = input("Descricao: ")
    categoria = escolher_categoria()
    prioridade = input("Prioridade (baixa/media/alta): ")

    while True:
        horario_inicio = input("Inicio (AAAA-MM-DD HH:MM): ")
        horario_fim = input("Fim (AAAA-MM-DD HH:MM): ")

        valido, erro = validar_datas_tarefa(horario_inicio, horario_fim)

        if valido:
            break

        print(f"\n{erro}")

    print("\nRecorrencia")
    print("1 Nenhuma")
    print("2 Diaria")
    print("3 Semanal")
    print("4 Mensal")
    opcao = input("Escolha: ")

    tipo_recorrencia = "nenhuma"
    dias_semana = None
    dia_mes = None

    if opcao == "2":
        tipo_recorrencia = "diaria"

    elif opcao == "3":
        tipo_recorrencia = "semanal"
        dias_semana = input("Dias (seg,qua,sex): ")

    elif opcao == "4":
        tipo_recorrencia = "mensal"
        dia_mes = ler_inteiro("Dia do mes: ", minimo=1, maximo=31)

    criar_tarefa(
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

    print("\nTarefa criada")


def tela_concluir_tarefa(id_usuario):
    from views.dashboard_view import tela_dashboard

    tarefas = buscar_tarefas_pendentes_hoje(id_usuario)

    print("\n===== SUAS TAREFAS =====\n")

    if not tarefas:
        print("Nenhuma tarefa encontrada")
        return

    for tarefa in tarefas:
        print(f"""
ID: {tarefa[0]}
Titulo: {tarefa[1]}
----------------
""")

    id_tarefa = ler_inteiro("\nDigite ID concluir: ")

    finalizar_tarefa(id_tarefa, id_usuario)

    print("\n Tarefa concluída")

    tela_dashboard(id_usuario)


def tela_excluir_tarefa(id_usuario):
    tarefas = listar_tarefas(id_usuario)

    print("\n===== SUAS TAREFAS =====\n")

    if not tarefas:
        print("Nenhuma tarefa encontrada")
        return

    for tarefa in tarefas:
        print(f"""
ID: {tarefa[0]}
Titulo: {tarefa[1]}
----------------
""")

    id_tarefa = ler_inteiro("\nDigite ID excluir: ")

    remover_tarefa(id_tarefa, id_usuario)

    print("\nTarefa removida")


def _imprimir_lista_tarefas(tarefas):
    for tarefa in tarefas:
        print(f"""
ID: {tarefa[0]}
Titulo: {tarefa[1]}
Categoria: {rotulo_categoria(tarefa[9])}
Prioridade: {tarefa[2]}
Inicio: {tarefa[3]}
Fim: {tarefa[4]}
""")

        recorrencia = tarefa[5]
        dias = tarefa[6]
        dia_mes = tarefa[7]

        if recorrencia == "diaria":
            print("Recorrência: diária")
        elif recorrencia == "semanal":
            print(f"Recorrência: semanal ({dias})")
        elif recorrencia == "mensal":
            print(f"Recorrência: mensal (dia {dia_mes})")
        else:
            print("Recorrência: nenhuma")

        print("\n------------------\n")


def tela_ver_tarefas(id_usuario):
    tarefas = listar_tarefas(id_usuario)

    print("\n===== SUAS TAREFAS =====\n")

    if not tarefas:
        print("Nenhuma tarefa cadastrada")
    else:
        _imprimir_lista_tarefas(tarefas)

    print("\n AÇÕES RÁPIDAS")
    print("\n1 - Filtrar por categoria")
    print("0 - Voltar")

    acao = input("\nEscolha: ")

    if acao == "1":
        print("\nFiltrar por categoria")
        print("1 - Apenas diárias")
        print("2 - Apenas educacionais")
        filtro = input("Escolha: ")

        categoria = None
        if filtro == "1":
            categoria = "diaria"
        elif filtro == "2":
            categoria = "educacional"

        tarefas_filtradas = listar_tarefas(id_usuario, categoria)

        print("\n===== TAREFAS FILTRADAS =====\n")

        if not tarefas_filtradas:
            print("Nenhuma tarefa encontrada para esse filtro")
        else:
            _imprimir_lista_tarefas(tarefas_filtradas)


def tela_editar_tarefa(id_usuario):
    print("\n=== EDITAR TAREFA ===")

    id_tarefa = ler_inteiro("Digite o ID da tarefa que deseja editar: ")
    titulo = input("Novo título: ")
    prioridade = input("Nova prioridade: ")

    while True:
        horario_inicio = input("Novo horário de início (AAAA-MM-DD HH:MM): ")
        horario_fim = input("Novo horário de fim (AAAA-MM-DD HH:MM): ")

        valido, erro = validar_datas_tarefa(horario_inicio, horario_fim)
        if valido:
            break
        print(f"\n{erro}")

    alterar_categoria = input("Deseja alterar a categoria? (sim/nao): ").strip().lower()
    categoria = escolher_categoria() if alterar_categoria == "sim" else None

    resultado = editar_tarefa(
        id_tarefa,
        id_usuario,
        titulo,
        prioridade,
        horario_inicio,
        horario_fim,
        categoria
    )

    if resultado:
        print("Tarefa editada com sucesso.")
    else:
        print("Não foi possível editar a tarefa.")
