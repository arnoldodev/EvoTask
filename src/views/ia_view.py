from controllers.ia_controller import conversar_assistente


def tela_assistente(

    usuario

):

    print(

        "\n===== ASSISTENTE ====="

    )

    print(

        "Digite 'sair' para voltar"

    )


    while True:

        mensagem = input(

            "\nVocê: "

        )


        if mensagem.lower()=="sair":

            break


        resposta = conversar_assistente(

            mensagem,

            usuario

        )


        print(

            "\nAssistente:",

            resposta

        )