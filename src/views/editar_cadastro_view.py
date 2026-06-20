from controllers.usuario_controller import obter_perfil, editar_cadastro, alterar_senha
from utils.validacoes import validar_email, validar_senha, ler_inteiro


def _ler_com_padrao(mensagem, valor_atual):
    """Lê uma entrada do usuário; se ele apertar Enter sem digitar nada,
    mantém o valor atual."""
    novo = input(f"{mensagem} [{valor_atual}]: ").strip()
    return novo if novo else valor_atual


def tela_editar_cadastro(id_usuario):
    perfil = obter_perfil(id_usuario)

    if not perfil:
        print("\nNão foi possível carregar seu cadastro.")
        return

    (nome_atual, nivel_ansiedade_atual, faz_terapia_atual, frequencia_crises_atual,
     procrastina_atual, periodo_foco_atual, atividade_fisica_atual,
     idade_atual, genero_atual, email_atual) = perfil

    print("\n=== EDITAR CADASTRO ===")
    print("Pressione Enter para manter o valor atual.\n")

    nome = _ler_com_padrao("Nome", nome_atual)

    while True:
        idade_str = input(f"Idade [{idade_atual}]: ").strip()
        if not idade_str:
            idade = idade_atual
            break
        try:
            idade = int(idade_str)
            break
        except ValueError:
            print("Digite um número inteiro válido.")

    genero = _ler_com_padrao("Genero", genero_atual)

    while True:
        email = _ler_com_padrao("Email", email_atual)
        if email == email_atual or validar_email(email):
            break
        print("Email inválido")

    print("\n--- Perfil emocional ---")

    alterar_ansiedade = input(
        f"Deseja alterar o nível de ansiedade? (sim/nao) [atual: {nivel_ansiedade_atual}]: "
    ).strip().lower()

    if alterar_ansiedade == "sim":
        nivel_ansiedade = ler_inteiro("Novo nível de ansiedade (1-10): ", minimo=1, maximo=10)
    else:
        nivel_ansiedade = nivel_ansiedade_atual

    faz_terapia = _ler_com_padrao("Faz terapia? (sim/nao)", faz_terapia_atual)
    frequencia_crises = _ler_com_padrao("Crises (baixa/media/alta)", frequencia_crises_atual)
    procrastina = _ler_com_padrao("Procrastina? (sim/nao)", procrastina_atual)
    periodo_foco = _ler_com_padrao("Melhor periodo foco (manha/tarde/noite)", periodo_foco_atual)
    atividade_fisica = _ler_com_padrao("Faz atividade fisica? (sim/nao)", atividade_fisica_atual)

    sucesso = editar_cadastro(
        id_usuario, nome, idade, genero, email,
        nivel_ansiedade, faz_terapia, frequencia_crises,
        procrastina, periodo_foco, atividade_fisica
    )

    if sucesso:
        print("\n Cadastro atualizado com sucesso!")
    else:
        print("\n Não foi possível atualizar o cadastro. Verifique se o email já está em uso.")
        return

    trocar_senha = input("\nDeseja alterar sua senha agora? (sim/nao): ").strip().lower()
    if trocar_senha == "sim":
        while True:
            nova_senha = input("Nova senha: ")
            if validar_senha(nova_senha):
                break
            print(
                "\nSenha inválida.\n"
                "Precisa: Maiúscula, Minúscula, Número, Especial, 4-8 caracteres"
            )

        if alterar_senha(id_usuario, nova_senha):
            print(" Senha alterada com sucesso!")
        else:
            print(" Não foi possível alterar a senha.")
