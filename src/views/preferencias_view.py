from controllers.usuario_controller import obter_preferencias, definir_tom_comunicacao

TONS = {
    "1": ("motivacional", "Motivacional — animado e encorajador"),
    "2": ("direto", "Direto — sem rodeios, foco no essencial"),
    "3": ("gentil", "Gentil — acolhedor e calmo"),
}


def tela_preferencias(id_usuario):
    _notificacoes, tom_atual = obter_preferencias(id_usuario)

    print("\n===== PREFERÊNCIA DE COMUNICAÇÃO =====")
    print(f"\nTom atual: {tom_atual}\n")

    for chave, (valor, descricao) in TONS.items():
        marcador = " (atual)" if valor == tom_atual else ""
        print(f"{chave} - {descricao}{marcador}")

    print("0 - Voltar sem alterar")

    opcao = input("\nEscolha: ")

    if opcao not in TONS:
        return

    novo_tom, _descricao = TONS[opcao]

    if definir_tom_comunicacao(id_usuario, novo_tom):
        print(f"\n Preferência de comunicação atualizada para: {novo_tom}")
    else:
        print("\n Não foi possível atualizar a preferência de comunicação.")
