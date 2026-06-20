# Evo.Task

Projeto de conclusão de curso desenvolvido no Senac com foco em produtividade, organização pessoal e apoio a pessoas com ansiedade, procrastinação e sintomas relacionados ao TDAH.

O Evo.Task foi criado como um assistente inteligente de apoio pessoal e educacional, buscando reduzir a paralisia por sobrecarga através da organização de tarefas, acompanhamento emocional e técnicas de produtividade.

## Funcionalidades

* Cadastro e Login de usuários
* Edição de cadastro e troca de senha
* Tarefas separadas por categoria: **diárias** e **educacionais**
* Tarefas recorrentes (diária, semanal ou mensal)
* Lembrete de tarefas (atrasadas e próximas) ao abrir o app
* Dashboard diário de produtividade
* Dashboard semanal de produtividade
* Histórico de produtividade (últimos 7 dias)
* Preferência de comunicação (tom motivacional, direto ou gentil)
* Assistente inteligente contextual, que adapta o tom de resposta à preferência do usuário
* Modo Foco (Pomodoro adaptativo)
* Histórico emocional

## Tecnologias Utilizadas

* Python
* MySQL
* MVC Architecture (Models / Views / Controllers)
* Google Gemini API (assistente inteligente)
* bcrypt (hash de senhas)
* Git / GitHub

## Configuração

1. Copie `.env.example` para `.env` e preencha com suas credenciais:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   DB_HOST=localhost
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_NAME=evotask
   ```
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute o sistema:
   ```
   python src/main.py
   ```

O banco de dados e suas tabelas são criados automaticamente na primeira execução.

## Objetivo do Projeto

O objetivo do Evo.Task é auxiliar usuários que enfrentam dificuldades relacionadas à organização, procrastinação, ansiedade e gestão de tarefas, oferecendo ferramentas práticas de apoio e acompanhamento.

## Instituição

Projeto desenvolvido como Trabalho de Conclusão de Curso (TCC) do Senac.
