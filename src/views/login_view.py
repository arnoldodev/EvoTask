from controllers.auth_controller import fazer_login
from views.usuario_menu_view import menu_usuario

def tela_login():

    print("\nLOGIN")

    email=input("Email: ")

    senha=input("Senha: ")

    usuario = fazer_login(
        email,
        senha
    )

    if usuario:

        menu_usuario(
            usuario
        )

    else:

        print(

            "\nEmail ou senha incorretos"

        )