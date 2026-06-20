import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cadastro (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            idade INT,
            genero VARCHAR(50),
            email VARCHAR(255) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_emocional (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            nivel_ansiedade INT,
            faz_terapia VARCHAR(10),
            frequencia_crises VARCHAR(20),
            dificuldade_tarefas VARCHAR(20),
            procrastina VARCHAR(20),
            periodo_foco VARCHAR(10),
            atividade_fisica VARCHAR(10),
            FOREIGN KEY (id_usuario) REFERENCES cadastro(id)
        )
    """)

    # 'tom_comunicacao' é a preferência de comunicação do usuário, usada
    # tanto nas mensagens do sistema quanto no prompt enviado à IA.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferencias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            notificacoes VARCHAR(10) DEFAULT 'sim',
            tom_comunicacao VARCHAR(20) DEFAULT 'gentil',
            FOREIGN KEY (id_usuario) REFERENCES cadastro(id)
        )
    """)

    # Schema corrigido: estas são as colunas que o restante do sistema
    # (tarefa_model.py) efetivamente usa em seus INSERTs/SELECTs/UPDATEs.
    # 'categoria' separa as tarefas em "diaria" (rotina pessoal) e
    # "educacional" (estudos/curso), conforme solicitado.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            titulo VARCHAR(255) NOT NULL,
            descricao TEXT,
            categoria VARCHAR(20) NOT NULL DEFAULT 'diaria',
            prioridade VARCHAR(50) DEFAULT 'media',
            horario_inicio DATETIME,
            horario_fim DATETIME,
            tipo_recorrencia VARCHAR(50) DEFAULT 'nenhuma',
            dias_semana VARCHAR(50),
            dia_mes INT,
            concluida INT DEFAULT 0,
            ultima_conclusao DATE,
            FOREIGN KEY (id_usuario) REFERENCES cadastro(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_ia (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            mensagem TEXT NOT NULL,
            resposta TEXT NOT NULL,
            hora VARCHAR(50) NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES cadastro(id)
        )
    """)

    # 'registro' guarda um snapshot diário de produtividade (quantas
    # tarefas existiam e quantas foram concluídas naquele dia). É a base
    # do Dashboard Semanal e do Histórico de Produtividade.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registro (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            tarefas_concluidas INT DEFAULT 0,
            tarefas_totais INT DEFAULT 0,
            humor_dia VARCHAR(50),
            data DATE NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES cadastro(id),
            UNIQUE KEY uniq_usuario_data (id_usuario, data)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
