"""
Testa o fluxo de telas (views) simulando entradas do usuário via stdin,
para garantir que os imports e a formatação funcionam de ponta a ponta
(não só a lógica de negócio testada em test_integration.py).
"""
import sys
import os
import io
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models.db_config import criar_banco
criar_banco()

from controllers.auth_controller import fazer_cadastro, fazer_login

agora = datetime.now()
inicio = (agora + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M")
fim = (agora + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")

# --- Cadastro via view, simulando stdin ---
entradas_cadastro = iter([
    "João da Silva",   # nome
    "28",              # idade
    "masculino",       # genero
    "joao@teste.com",  # email
    "Abc123!",         # senha
    "5",                # ansiedade
    "nao",             # terapia
    "baixa",           # crises
    "nao",             # procrastina
    "manha",           # foco
    "sim",             # atividade fisica
])

def fake_input(prompt=""):
    valor = next(entradas_cadastro)
    print(f"{prompt}{valor}")
    return valor

import builtins
builtins.input = fake_input

from views.cadastro_view import tela_cadastro

print("\n=== TELA CADASTRO ===")
tela_cadastro()

# --- Login ---
entradas_login = iter(["joao@teste.com", "Abc123!"])
builtins.input = lambda prompt="": next(entradas_login)

usuario = fazer_login("joao@teste.com", "Abc123!")
print("\nLogin direto via controller:", "OK" if usuario else "FALHOU")
assert usuario is not None

id_usuario = usuario[0]

# --- Criar tarefa diária via tela ---
entradas_tarefa = iter([
    "Estudar Python",      # titulo
    "Pratica diaria",      # descricao
    "2",                   # categoria -> educacional
    "alta",                # prioridade
    inicio,                # horario inicio
    fim,                   # horario fim
    "1",                   # recorrencia -> nenhuma
])
builtins.input = lambda prompt="": next(entradas_tarefa)

from views.tarefa_view import tela_criar_tarefa
print("\n=== TELA CRIAR TAREFA ===")
tela_criar_tarefa(id_usuario)

# --- Ver tarefas (todas) e depois voltar ---
entradas_ver = iter(["1", "0"])
builtins.input = lambda prompt="": next(entradas_ver)

from views.tarefa_view import tela_ver_tarefas
print("\n=== TELA VER TAREFAS ===")
tela_ver_tarefas(id_usuario)

# --- Dashboard ---
builtins.input = lambda prompt="": "0"
from views.dashboard_view import tela_dashboard
print("\n=== TELA DASHBOARD ===")
tela_dashboard(id_usuario)

# --- Dashboard semanal ---
from views.dashboard_semanal_view import tela_dashboard_semanal
print("\n=== TELA DASHBOARD SEMANAL ===")
tela_dashboard_semanal(id_usuario)

# --- Histórico de produtividade ---
from views.historico_view import tela_historico_produtividade
print("\n=== TELA HISTORICO PRODUTIVIDADE ===")
tela_historico_produtividade(id_usuario)

# --- Perfil + editar cadastro (Enter mantém tudo, depois nao troca senha) ---
entradas_perfil = iter(["1"])  # escolhe "Editar cadastro" no menu de perfil
builtins.input = lambda prompt="": next(entradas_perfil, "")

entradas_editar = iter([
    "", "", "", "",   # nome, idade, genero, email (mantém tudo)
    "nao",            # não altera ansiedade
    "", "", "", "", "",  # demais campos emocionais (mantém)
    "nao",            # não troca senha
])
def input_combinado(prompt=""):
    try:
        return next(entradas_perfil)
    except StopIteration:
        return next(entradas_editar)

builtins.input = input_combinado

from views.perfil_view import tela_perfil
print("\n=== TELA PERFIL -> EDITAR CADASTRO ===")
tela_perfil(id_usuario)

# --- Preferências de comunicação ---
entradas_pref = iter(["1"])  # motivacional
builtins.input = lambda prompt="": next(entradas_pref)

from views.preferencias_view import tela_preferencias
print("\n=== TELA PREFERENCIAS ===")
tela_preferencias(id_usuario)

print("\n\n✅ TODAS AS TELAS EXECUTARAM SEM EXCEÇÃO")
