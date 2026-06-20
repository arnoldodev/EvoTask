import mysql.connector
from models.db_config import conectar
import bcrypt
from utils.logger import get_logger

logger = get_logger("usuario_model")

TONS_VALIDOS = ("motivacional", "direto", "gentil")


def buscar_nome_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nome FROM cadastro WHERE id=%s",
        (id_usuario,)
    )
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado[0] if resultado else None


def registrar_usuario_bd(
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
):
    conn = conectar()
    cursor = conn.cursor()

    try:
        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO cadastro (nome, idade, genero, email, senha)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (nome, idade, genero, email, senha_hash)
        )

        id_usuario = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO historico_emocional
            (id_usuario, nivel_ansiedade, faz_terapia, frequencia_crises,
             procrastina, periodo_foco, atividade_fisica)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                id_usuario,
                nivel_ansiedade,
                faz_terapia,
                frequencia_crises,
                procrastina,
                periodo_foco,
                atividade_fisica
            )
        )

        cursor.execute(
            "INSERT INTO preferencias (id_usuario) VALUES (%s)",
            (id_usuario,)
        )

        conn.commit()
        return id_usuario

    except mysql.connector.Error as err:
        logger.error(f"Erro MySQL ao registrar usuário: {err}")
        conn.rollback()
        return None

    finally:
        cursor.close()
        conn.close()


def verificar_login(email, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.id, c.nome, h.nivel_ansiedade, c.email, c.senha, h.periodo_foco
        FROM cadastro c
        INNER JOIN historico_emocional h ON c.id = h.id_usuario
        WHERE c.email = %s
        """,
        (email,)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if usuario is None:
        return None

    senha_hash_banco = usuario[4]  # coluna senha

    if bcrypt.checkpw(senha.encode("utf-8"), senha_hash_banco.encode("utf-8")):
        return usuario
    else:
        return None


def buscar_perfil_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            c.nome,
            h.nivel_ansiedade,
            h.faz_terapia,
            h.frequencia_crises,
            h.procrastina,
            h.periodo_foco,
            h.atividade_fisica,
            c.idade,
            c.genero,
            c.email
        FROM cadastro c
        JOIN historico_emocional h ON c.id = h.id_usuario
        WHERE c.id = %s
        """,
        (id_usuario,)
    )

    perfil = cursor.fetchone()
    cursor.close()
    conn.close()
    return perfil


def editar_cadastro_bd(id_usuario, nome, idade, genero, email,
                        nivel_ansiedade, faz_terapia, frequencia_crises,
                        procrastina, periodo_foco, atividade_fisica):
    """Atualiza os dados de cadastro e o perfil emocional do usuário."""
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE cadastro
            SET nome=%s, idade=%s, genero=%s, email=%s
            WHERE id=%s
            """,
            (nome, idade, genero, email, id_usuario)
        )

        cursor.execute(
            """
            UPDATE historico_emocional
            SET nivel_ansiedade=%s, faz_terapia=%s, frequencia_crises=%s,
                procrastina=%s, periodo_foco=%s, atividade_fisica=%s
            WHERE id_usuario=%s
            """,
            (
                nivel_ansiedade,
                faz_terapia,
                frequencia_crises,
                procrastina,
                periodo_foco,
                atividade_fisica,
                id_usuario
            )
        )

        conn.commit()
        return True

    except mysql.connector.Error as err:
        logger.error(f"Erro MySQL ao editar cadastro do usuário {id_usuario}: {err}")
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()


def alterar_senha_bd(id_usuario, nova_senha):
    conn = conectar()
    cursor = conn.cursor()

    try:
        senha_hash = bcrypt.hashpw(nova_senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cursor.execute(
            "UPDATE cadastro SET senha=%s WHERE id=%s",
            (senha_hash, id_usuario)
        )
        conn.commit()
        return True

    except mysql.connector.Error as err:
        logger.error(f"Erro MySQL ao alterar senha do usuário {id_usuario}: {err}")
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()


def buscar_preferencias(id_usuario):
    """Retorna (notificacoes, tom_comunicacao) do usuário."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT notificacoes, tom_comunicacao FROM preferencias WHERE id_usuario=%s",
        (id_usuario,)
    )
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    if resultado is None:
        return ("sim", "gentil")
    return resultado


def atualizar_tom_comunicacao_bd(id_usuario, tom_comunicacao):
    if tom_comunicacao not in TONS_VALIDOS:
        return False

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE preferencias SET tom_comunicacao=%s WHERE id_usuario=%s",
            (tom_comunicacao, id_usuario)
        )
        conn.commit()
        return cursor.rowcount > 0

    except mysql.connector.Error as err:
        logger.error(f"Erro MySQL ao atualizar tom de comunicação do usuário {id_usuario}: {err}")
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()
