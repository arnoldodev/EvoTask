from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

modelo = genai.GenerativeModel("gemini-2.5-flash")

INSTRUCOES_TOM = {
    "motivacional": "Use um tom animado e encorajador, como um treinador pessoal.",
    "direto": "Use um tom direto, sem rodeios e sem floreios. Frases curtas e objetivas.",
    "gentil": "Use um tom acolhedor, calmo e gentil, com empatia.",
}


def conversar(mensagem, perfil, tarefas_hoje_pendentes, tarefas_hoje_concluidas,
              tarefas_ontem_pendentes, tarefas_ontem_concluidas,
              hora_atual, data_atual, periodo_atual, tom_comunicacao="gentil"):

    hoje_pendentes = "\n".join([f"- {t}" for t in tarefas_hoje_pendentes]) if tarefas_hoje_pendentes else "Nenhuma tarefa pendente para hoje."
    hoje_concluidas = "\n".join([f"- {t}" for t in tarefas_hoje_concluidas]) if tarefas_hoje_concluidas else "Nenhuma tarefa concluída hoje ainda."
    ontem_pendentes = "\n".join([f"- {t}" for t in tarefas_ontem_pendentes]) if tarefas_ontem_pendentes else "Nenhuma tarefa ficou pendente ontem!"
    ontem_concluidas = "\n".join([f"- {t}" for t in tarefas_ontem_concluidas]) if tarefas_ontem_concluidas else "Nenhuma tarefa foi concluída ontem."

    nome_usuario = perfil[1]
    nivel_ansiedade = perfil[2]
    horario_foco = perfil[5]

    instrucao_tom = INSTRUCOES_TOM.get(tom_comunicacao, INSTRUCOES_TOM["gentil"])

    prompt = f"""
Você é o EvoTask, um assistente de produtividade cirúrgico, breve e empático.
Sua missão é dar respostas extremamente curtas (máximo 2 parágrafos pequenos ou 1 parágrafo + tópicos).

--- PREFERÊNCIA DE COMUNICAÇÃO DO USUÁRIO ---
{instrucao_tom}

--- CONTEXTO DO USUÁRIO ---
- Nome: {nome_usuario} | Ansiedade: {nivel_ansiedade}/10 | Foco: {horario_foco}
- Horário Atual: {hora_atual} ({periodo_atual}) | Data: {data_atual}

--- DADOS REALISTAS ---
[ONTEM] Concluídas: {ontem_concluidas} | Pendentes: {ontem_pendentes}
[HOJE] Concluídas: {hoje_concluidas} | Pendentes: {hoje_pendentes}

--- REGRAS DE OURO DE CONVERSA (STRICT) ---
1. Responda em no máximo 3 ou 4 linhas corridas de texto, ou use bullet points diretos.
2. Analise o "Horário Atual" ({hora_atual}): se tiver tarefa pendente agora ou perto de começar, avise em uma única frase curta.
3. Se o usuário disser que vai dormir ou sumir e for tarde, diga apenas para ele descansar.
4. NUNCA faça introduções longas ou textos motivacionais clichês. Vá direto ao ponto.
5. Siga sempre a preferência de comunicação indicada acima.

Mensagem do usuário: "{mensagem}"
Resposta curta do EvoTask:
"""

    try:
        resposta = modelo.generate_content(prompt)
        return resposta.text

    except Exception as e:
        erro = str(e)
        if "RESOURCE_EXHAUSTED" in erro or "429" in erro:
            return (
                " Assistente temporariamente indisponível. "
                "Limite de requisições atingido. Tente novamente em alguns minutos."
            )
        return " Não consegui conectar com a Inteligência Artificial agora."
