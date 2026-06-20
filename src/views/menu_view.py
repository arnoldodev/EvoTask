from views.login_view import tela_login
from views.cadastro_view import tela_cadastro


def menu_principal():

    while True:

        print("\n1 - Login")

        print("2 - Cadastro")

        print("0 - Sair")

        opcao=input("Escolha: ")

        if opcao=="1":

            tela_login()

        elif opcao=="2":

            tela_cadastro()

        elif opcao=="0":

            break