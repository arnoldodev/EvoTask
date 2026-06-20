from controllers.usuario_controller import obter_perfil


def tela_perfil(id_usuario):
    perfil = obter_perfil(id_usuario)

    print("\n===== MEU PERFIL =====")
    print(f"\nNome: {perfil[0]}")
    print(f"Ansiedade: {perfil[1]}")
    print(f"Terapia: {perfil[2]}")
    print(f"Crises: {perfil[3]}")
    print(f"Procrastina: {perfil[4]}")
    print(f"Foco: {perfil[5]}")
    print(f"Atividade física: {perfil[6]}")
    print(f"Idade: {perfil[7]}")
    print(f"Gênero: {perfil[8]}")
    print(f"Email: {perfil[9]}")

    print("\n1 - Editar cadastro")
    print("2 - Preferência de comunicação")
    print("0 - Voltar")

    acao = input("\nEscolha: ")

    if acao == "1":
        from views.editar_cadastro_view import tela_editar_cadastro
        tela_editar_cadastro(id_usuario)

    elif acao == "2":
        from views.preferencias_view import tela_preferencias
        tela_preferencias(id_usuario)
