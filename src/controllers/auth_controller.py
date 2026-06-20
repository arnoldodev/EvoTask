from models.usuario_model import verificar_login, registrar_usuario_bd

def fazer_login(email: str, senha: str) -> tuple | None:
    return verificar_login(email, senha)

def fazer_cadastro(*args) -> int | None:
    return registrar_usuario_bd(*args)