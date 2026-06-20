import string
from datetime import datetime


def validar_email(email: str) -> bool:
    if "@" not in email:
        return False
    if "." not in email:
        return False

    partes = email.split("@")
    if len(partes) != 2:
        return False

    if partes[0] == "":
        return False

    if partes[1] == "":
        return False

    if "." not in partes[1]:
        return False

    return True


def validar_senha(senha: str) -> bool:
    especiais = string.punctuation

    if len(senha) < 4:
        return False

    if len(senha) > 16:
        return False

    maiuscula = False
    minuscula = False
    numero = False
    especial = False

    for c in senha:
        if c.isupper():
            maiuscula = True
        if c.islower():
            minuscula = True
        if c.isdigit():
            numero = True
        if c in especiais:
            especial = True

    return maiuscula and minuscula and numero and especial


def validar_datas_tarefa(horario_inicio: str, horario_fim: str) -> tuple[bool, str]:
    try:
        inicio = datetime.strptime(horario_inicio, "%Y-%m-%d %H:%M")
        fim = datetime.strptime(horario_fim, "%Y-%m-%d %H:%M")
        agora = datetime.now()

        if inicio < agora:
            return (False, "Data início não pode ser passada")

        if fim <= inicio:
            return (False, "Data fim deve ser após início")

        return (True, "")

    except ValueError:
        return (False, "Formato inválido. Use: AAAA-MM-DD HH:MM")


def ler_inteiro(mensagem: str, minimo: int | None = None, maximo: int | None = None) -> int:
    """Lê um número inteiro do usuário, repetindo a pergunta até receber
    uma entrada válida (e dentro do intervalo, se informado)."""
    while True:
        valor_digitado = input(mensagem)
        try:
            valor = int(valor_digitado)
        except ValueError:
            print("Por favor, digite um número inteiro válido.")
            continue

        if minimo is not None and valor < minimo:
            print(f"O valor deve ser maior ou igual a {minimo}.")
            continue

        if maximo is not None and valor > maximo:
            print(f"O valor deve ser menor ou igual a {maximo}.")
            continue

        return valor
