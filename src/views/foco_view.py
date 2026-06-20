from controllers.tarefa_controller import listar_tarefas
from models.tarefa_model import buscar_tarefa_por_id
from controllers.foco_controller import calcular_duracao, iniciar_pomodoro
from datetime import datetime


def tela_modo_foco(

    id_usuario

):

    tarefas = listar_tarefas(

        id_usuario

    )


    print(

        "\n===== MODO FOCO =====\n"

    )


    for tarefa in tarefas:

        print(

            f"{tarefa[0]} - {tarefa[1]}"

        )


    id_tarefa = int(

        input(

            "\nEscolha ID tarefa: "

        )

    )


    tarefa = buscar_tarefa_por_id(

        id_tarefa,

        id_usuario

    )


    inicio = tarefa[2]

    fim = tarefa[3]


    minutos = calcular_duracao(

        inicio,

        fim

    )


    print(

        f"""

Tarefa:

{tarefa[1]}

Tempo total:

{minutos} min

 Pomodoro iniciado

"""

    )


    iniciar_pomodoro(

        minutos

    )


    print(

        "\n Sessão encerrada!"

    )