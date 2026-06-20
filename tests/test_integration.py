"""
Script de teste de integração para validar a lógica do EvoTask
sem depender de input() interativo. Roda contra um banco MariaDB real.
"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models.db_config import criar_banco, conectar
from models.usuario_model import (
    registrar_usuario_bd, verificar_login, buscar_perfil_usuario,
    editar_cadastro_bd, buscar_preferencias, atualizar_tom_comunicacao_bd,
    alterar_senha_bd,
)
from models.tarefa_model import (
    salvar_tarefa, buscar_tarefas, concluir_tarefa, buscar_dados_dashboard,
    excluir_tarefa, editar_tarefa_bd, buscar_tarefas_por_status,
    buscar_tarefas_pendentes_proximas, buscar_historico_produtividade,
    buscar_tarefa_por_id,
)

erros = []


def checar(descricao, condicao):
    status = "OK " if condicao else "FALHOU"
    print(f"[{status}] {descricao}")
    if not condicao:
        erros.append(descricao)


print("=== 1. Criando banco (schema) ===")
criar_banco()
checar("Schema criado sem exceção", True)

print("\n=== 2. Registro de usuário ===")
id_usuario = registrar_usuario_bd(
    "Maria Teste", 22, "feminino", "maria@teste.com", "Senha1!",
    7, "sim", "media", "sim", "noite", "nao"
)
checar("Usuário criado com ID válido", isinstance(id_usuario, int) and id_usuario > 0)

id_dup = registrar_usuario_bd(
    "Outra Maria", 30, "feminino", "maria@teste.com", "Outra1!",
    5, "nao", "baixa", "nao", "manha", "sim"
)
checar("Email duplicado é rejeitado (retorna None)", id_dup is None)

print("\n=== 3. Login ===")
usuario = verificar_login("maria@teste.com", "Senha1!")
checar("Login correto retorna usuário", usuario is not None)
checar("Login incorreto retorna None", verificar_login("maria@teste.com", "errada") is None)
checar("Login email inexistente retorna None", verificar_login("naoexiste@x.com", "x") is None)

print("\n=== 4. Perfil ===")
perfil = buscar_perfil_usuario(id_usuario)
checar("Perfil tem 10 campos (nome..email)", len(perfil) == 10)
checar("Nome do perfil correto", perfil[0] == "Maria Teste")

print("\n=== 5. Editar cadastro ===")
sucesso_edicao = editar_cadastro_bd(
    id_usuario, "Maria Editada", 23, "feminino", "maria.editada@teste.com",
    8, "sim", "alta", "nao", "manha", "sim"
)
checar("Edição de cadastro retorna sucesso", sucesso_edicao)
perfil_editado = buscar_perfil_usuario(id_usuario)
checar("Nome foi atualizado", perfil_editado[0] == "Maria Editada")
checar("Email foi atualizado", perfil_editado[9] == "maria.editada@teste.com")
checar("Idade foi atualizada", perfil_editado[7] == 23)
login_apos_edicao = verificar_login("maria.editada@teste.com", "Senha1!")
checar("Login funciona com novo email", login_apos_edicao is not None)

print("\n=== 6. Alterar senha ===")
checar("Alterar senha retorna sucesso", alterar_senha_bd(id_usuario, "NovaSenha2!"))
checar("Login com senha antiga falha", verificar_login("maria.editada@teste.com", "Senha1!") is None)
checar("Login com senha nova funciona", verificar_login("maria.editada@teste.com", "NovaSenha2!") is not None)

print("\n=== 7. Preferência de comunicação ===")
notif, tom = buscar_preferencias(id_usuario)
checar("Tom padrão é 'gentil'", tom == "gentil")
checar("Atualizar para tom válido funciona", atualizar_tom_comunicacao_bd(id_usuario, "direto"))
_, tom_novo = buscar_preferencias(id_usuario)
checar("Tom foi persistido como 'direto'", tom_novo == "direto")
checar("Tom inválido é rejeitado", atualizar_tom_comunicacao_bd(id_usuario, "agressivo") is False)

print("\n=== 8. Criar tarefas (diária e educacional) ===")
agora = datetime.now()
inicio_str = agora.strftime("%Y-%m-%d %H:%M:%S")
fim_str = (agora + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

salvar_tarefa(id_usuario, "Lavar louça", "Tarefa de casa", "diaria", "baixa",
              inicio_str, fim_str, "diaria", None, None)
salvar_tarefa(id_usuario, "Estudar SQL", "Curso Senac", "educacional", "alta",
              inicio_str, fim_str, "nenhuma", None, None)
salvar_tarefa(id_usuario, "Revisar redação", "Tarefa de português", "educacional", "media",
              inicio_str, fim_str, "semanal", "seg,qua,sex", None)

todas = buscar_tarefas(id_usuario)
checar("3 tarefas criadas", len(todas) == 3)

diarias = buscar_tarefas(id_usuario, categoria="diaria")
checar("1 tarefa diária filtrada corretamente", len(diarias) == 1 and diarias[0][1] == "Lavar louça")

educacionais = buscar_tarefas(id_usuario, categoria="educacional")
checar("2 tarefas educacionais filtradas corretamente", len(educacionais) == 2)

print("\n=== 9. Dashboard (hoje) ===")
dados = buscar_dados_dashboard(id_usuario)
checar("Dashboard sem categoria retorna dict com chaves esperadas",
       all(k in dados for k in ("total", "concluidas", "pendentes", "pendentes_lista", "concluidas_lista")))
checar(f"Total esperado >= 2 (semanal pode não cair hoje) -- total={dados['total']}", dados['total'] >= 2)

id_tarefa_lavar = [t[0] for t in todas if t[1] == "Lavar louça"][0]
id_tarefa_sql = [t[0] for t in todas if t[1] == "Estudar SQL"][0]

print("\n=== 10. Concluir tarefa ===")
concluir_tarefa(id_tarefa_lavar, id_usuario)
dados_pos_conclusao = buscar_dados_dashboard(id_usuario)
titulos_concluidos = [t[1] for t in dados_pos_conclusao["concluidas_lista"]]
checar("'Lavar louça' aparece como concluída", "Lavar louça" in titulos_concluidos)

print("\n=== 11. Registro de produtividade (snapshot) ===")
conn = conectar()
cursor = conn.cursor()
cursor.execute("SELECT tarefas_concluidas, tarefas_totais, data FROM registro WHERE id_usuario=%s", (id_usuario,))
registro_hoje = cursor.fetchone()
cursor.close()
conn.close()
checar("Snapshot de hoje foi criado na tabela registro", registro_hoje is not None)
if registro_hoje:
    checar("Snapshot tem ao menos 1 tarefa concluída", registro_hoje[0] >= 1)

print("\n=== 12. Editar tarefa ===")
novo_inicio = (agora + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
novo_fim = (agora + timedelta(days=1, hours=2)).strftime("%Y-%m-%d %H:%M:%S")
resultado_edicao = editar_tarefa_bd(id_tarefa_sql, id_usuario, "Estudar SQL avançado",
                                     "alta", novo_inicio, novo_fim, categoria="educacional")
checar("Edição de tarefa retorna sucesso", resultado_edicao)
tarefa_editada = buscar_tarefa_por_id(id_tarefa_sql, id_usuario)
checar("Título da tarefa foi atualizado", tarefa_editada[1] == "Estudar SQL avançado")

print("\n=== 13. Lembretes (atrasada / próxima) ===")
inicio_passado = (agora - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
fim_passado = (agora - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
salvar_tarefa(id_usuario, "Tarefa Atrasada", "desc", "diaria", "alta",
              inicio_passado, fim_passado, "nenhuma", None, None)

inicio_proximo = (agora + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
fim_proximo = (agora + timedelta(minutes=90)).strftime("%Y-%m-%d %H:%M:%S")
salvar_tarefa(id_usuario, "Tarefa Próxima", "desc", "diaria", "media",
              inicio_proximo, fim_proximo, "nenhuma", None, None)

atrasadas, proximas = buscar_tarefas_pendentes_proximas(id_usuario)
titulos_atrasadas = [t[0] for t in atrasadas]
titulos_proximas = [t[0] for t in proximas]
checar("Tarefa atrasada detectada", "Tarefa Atrasada" in titulos_atrasadas)
checar("Tarefa próxima detectada", "Tarefa Próxima" in titulos_proximas)

print("\n=== 14. Histórico de produtividade ===")
historico = buscar_historico_produtividade(id_usuario, dias=7)
checar("Histórico retorna ao menos 1 registro (hoje)", len(historico) >= 1)

print("\n=== 15. Buscar tarefas por status (hoje/ontem) ===")
pendentes_hoje = buscar_tarefas_por_status(id_usuario, "hoje", "pendente")
concluidas_hoje = buscar_tarefas_por_status(id_usuario, "hoje", "concluida")
checar("buscar_tarefas_por_status não lança exceção (hoje/pendente)", isinstance(pendentes_hoje, list))
checar("buscar_tarefas_por_status não lança exceção (hoje/concluida)", isinstance(concluidas_hoje, list))
pendentes_ontem = buscar_tarefas_por_status(id_usuario, "ontem", "pendente")
concluidas_ontem = buscar_tarefas_por_status(id_usuario, "ontem", "concluida")
checar("buscar_tarefas_por_status não lança exceção (ontem/pendente)", isinstance(pendentes_ontem, list))
checar("buscar_tarefas_por_status não lança exceção (ontem/concluida)", isinstance(concluidas_ontem, list))

print("\n=== 16. Excluir tarefa ===")
excluir_tarefa(id_tarefa_lavar, id_usuario)
todas_apos_exclusao = buscar_tarefas(id_usuario)
checar("Tarefa excluída não aparece mais", id_tarefa_lavar not in [t[0] for t in todas_apos_exclusao])

print("\n=== 17. Validações (utils) ===")
from utils.validacoes import validar_email, validar_senha, validar_datas_tarefa, ler_inteiro

checar("Email válido aceito", validar_email("a@b.com"))
checar("Email sem @ rejeitado", not validar_email("ab.com"))
checar("Email sem domínio rejeitado", not validar_email("a@b"))
checar("Senha válida aceita (Abc1!)", validar_senha("Abc1!"))
checar("Senha curta rejeitada", not validar_senha("Ab1!"[:3]))
checar("Senha sem especial rejeitada", not validar_senha("Abcd123"))
valido, _ = validar_datas_tarefa(
    (agora + timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
    (agora + timedelta(days=2, hours=1)).strftime("%Y-%m-%d %H:%M")
)
checar("Datas futuras válidas aceitas", valido)
invalido, msg = validar_datas_tarefa("2020-01-01 10:00", "2020-01-01 11:00")
checar("Data passada rejeitada", not invalido)

print("\n\n========================")
if erros:
    print(f"RESULTADO: {len(erros)} FALHA(S) ENCONTRADA(S):")
    for e in erros:
        print(f" - {e}")
    sys.exit(1)
else:
    print("RESULTADO: TODOS OS TESTES PASSARAM ✅")
    sys.exit(0)
