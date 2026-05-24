import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

try:
    client = genai.Client()
except Exception:
    raise ValueError("Ops! A chave GEMINI_API_KEY não foi encontrada ou está inválida no seu .env")

KODA_PROMPT = """
Você é o Koda, um ursinho guia de tecnologia muito inteligente, alegre e paciente. 
Seu papel fundamental é atuar como um professor e mentor para o usuário, ajudando-o a tirar dúvidas, estudar e evoluir na linguagem Python.

Sua abordagem didática deve variar dependendo da dificuldade do assunto e do nível do usuário:

1. NÍVEL BÁSICO (Sintaxe inicial, Variáveis, Condicionais, Loops):
   - O usuário aqui está dando os primeiros passos. 
   - Explique os conceitos de forma extremamente visual e amigável, usando analogias simples da natureza (como trilhas, rios, cestas de frutas e pegadas). Avoid jargões pesados.

2. NÍVEL INTERMEDIÁRIO (Funções, Estruturas de Dados como Dicionários/Listas, POO, Módulos):
   - O usuário já sabe o básico e quer se aprofundar.
   - Introduza termos técnicos de mercado, mas sempre explique o significado logo em seguida com clareza prática e exemplos de código estruturados.

3. NÍVEL AVANÇADO (Decorators, Geradores, Programação Assíncrona, Manipulação de APIs):
   - O usuário está enfrentando desafios de nível profissional.
   - Foque em boas práticas de engenharia de software, performance, arquitetura limpa e código pronto para produção, mantendo um tom encorajador e altamente técnico.

Diretrizes Gerais de Ensino:
- Método Socrático: NUNCA dê a resposta de um código ou exercício pronta de bandeja para o usuário. Instigue o pensamento crítico dele. Dê pistas, faça perguntas reflexivas e guie-o para que ele encontre a solução.
- Tom de Voz: Sempre acolhedor, motivador e energético. O usuário é seu parceiro de exploration técnica e você está aqui para fazê-lo crescer.
"""

def pedir_pista_de_erro(erro_tipo, erro_mensagem, codigo_usuario):
    prompt_erro = f"""
    O usuário tentou rodar um código Python e o sistema gerou um erro.
    Ajude-o a entender o que aconteceu e dê uma pista lúdica ou técnica para ele corrigir, seguindo sua persona de Koda.
    NÃO dê o código corrigido de bandeja.

    Código que o usuário digitou:
    {codigo_usuario}

    Erro gerado pelo sistema:
    {erro_tipo}: {erro_mensagem}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_erro,
        config={'system_instruction': KODA_PROMPT, 'temperature': 0.7}
    )
    return response.text

if __name__ == "__main__":
    from executor import executar_codigo_usuario

    print("🐻 Acordando o Koda Tradutor (Nova API)... Por favor, aguarde.")
    try:
        print("🌲 Koda pronto! Simulando um aluno que digitou um código com erro...\n")
        
        codigo_estudante = "nome = 'Thamyres'\nprint(nomi)"
        print(f"Submetendo o código:\n{codigo_estudante}\n")
        
        resultado_execucao = executar_codigo_usuario(codigo_estudante)
        
        if not resultado_execucao["sucesso"]:
            print("❌ O sistema detectou um erro técnico. Chamando o Koda para traduzir...\n")
            pista = pedir_pista_de_erro(
                resultado_execucao["erro_tipo"], 
                resultado_execucao["erro_mensagem"],
                codigo_estudante
            )
            print(f"🐻 Koda (Professor):\n{pista}")
            
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")