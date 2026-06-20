from controllers.auth_controller import fazer_cadastro
from utils.validacoes import validar_email, validar_senha, ler_inteiro


def tela_cadastro():
    print("\nCADASTRO")

    nome = input("Nome: ")
    idade = ler_inteiro("Idade: ")
    genero = input("Genero: ")

    while True:
        email = input("Email: ")
        if validar_email(email):
            break
        print("Email inválido")

    while True:
        senha = input("Senha: ")
        if validar_senha(senha):
            break
        print(
            "\nSenha inválida.\n"
            "Precisa: Maiúscula, Minúscula, Número, Especial, 4-8 caracteres"
        )

    print("\nPERFIL EMOCIONAL")

    nivel_ansiedade = ler_inteiro("Ansiedade (1-10): ", minimo=1, maximo=10)
    faz_terapia = input("Faz terapia? (sim/nao): ")
    frequencia_crises = input("Crises (baixa/media/alta): ")
    procrastina = input("Procrastina? (sim/nao): ")
    periodo_foco = input("Melhor periodo foco (manha/tarde/noite): ")
    atividade_fisica = input("Faz atividade fisica? (sim/nao): ")

    usuario = fazer_cadastro(
        nome,
        idade,
        genero,
        email,
        senha,
        nivel_ansiedade,
        faz_terapia,
        frequencia_crises,
        procrastina,
        periodo_foco,
        atividade_fisica
    )

    if usuario:
        print("\nUsuario criado com sucesso! ID:", usuario)
    else:
        print("\nNão foi possível criar o usuário. O email já pode estar em uso.")
