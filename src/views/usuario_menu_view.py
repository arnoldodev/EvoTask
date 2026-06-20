from views.tarefa_view import tela_ver_tarefas
from views.dashboard_view import tela_dashboard, exibir_lembretes
from views.perfil_view import tela_perfil


def menu_usuario(usuario):
    id_usuario = usuario[0]

    
    exibir_lembretes(id_usuario)

    while True:
        print(f"\nBem vindo {usuario[1]}!")

        print("\n1 - Dashboard")
        print("2 - Meu Perfil")
        print("3 - Ver Tarefas")
        print("0 - Logout")

        opcao = input("Escolha: ")

        if opcao == "1":
            tela_dashboard(id_usuario)

        elif opcao == "2":
            tela_perfil(id_usuario)

        elif opcao == "3":
            tela_ver_tarefas(id_usuario)

        elif opcao == "0":
            break