import time


def calcular_duracao(inicio, fim):
    minutos = int((fim - inicio).total_seconds() / 60)
    return minutos


def iniciar_pomodoro(minutos_total):
    restante = minutos_total
    ciclo = 1

    while restante > 0:
        foco = min(25, restante)

        print(f"\n Ciclo {ciclo}")
        print(f"Foco: {foco} min")

        timer(foco)

        restante -= foco

        if restante <= 0:
            break

        print("\n Pausa: 5 min")
        timer(5)

        ciclo += 1

    print("\n Tarefa finalizada!")


def timer(minutos):
    segundos = minutos * 60

    while segundos > 0:
        mins = segundos // 60
        segs = segundos % 60

        print(f"\r⏳ {mins:02}:{segs:02}", end="", flush=True)

        time.sleep(1)
        segundos -= 1
