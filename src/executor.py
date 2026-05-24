import sys
import io

def executar_codigo_usuario(codigo_texto):
    """
    Recebe uma string contendo código Python, executa de forma isolada
    e captura a saída do terminal (stdout) ou os erros (exceptions).
    """
    # Criamos um "buffer" para interceptar o que o código imprimiria na tela
    stdout_capturado = io.StringIO()
    sys.stdout = stdout_capturado
    
    # Dicionários para isolar as variáveis que o aluno criar no código dele
    escopo_global = {}
    escopo_local = {}
    
    resultado = {
        "sucesso": True,
        "saida": "",
        "erro_tipo": None,
        "erro_mensagem": None
    }
    
    try:
        # A mágica acontece aqui: exec() roda a string como código Python real
        exec(codigo_texto, escopo_global, escopo_local)
        # Se deu certo, guardamos o que foi impresso (ex: os prints)
        resultado["saida"] = stdout_capturado.getvalue()
    except Exception as e:
        # Se o código do aluno quebrar, capturamos o erro sem derrubar o nosso app
        resultado["sucesso"] = False
        resultado["erro_tipo"] = type(e).__name__      # Ex: 'NameError', 'SyntaxError'
        resultado["erro_mensagem"] = str(e)            # Ex: "name 'x' is not defined"
    finally:
        # Muito importante: devolvemos o controle do terminal padrão para o sistema
        sys.stdout = sys.__stdout__
        
    return resultado

# --- Bloco de Teste Local ---
if __name__ == "__main__":
    print("🧪 Testando o módulo Executor localmente...\n")
    
    # Teste 1: Um código que dá certo
    codigo_bom = "print('Oi, eu sou o aluno!')\nx = 10\ny = 20\nprint(f'A soma é: {x + y}')"
    print("--- Testando Código Correto ---")
    res_bom = executar_codigo_usuario(codigo_bom)
    print(f"Sucesso? {res_bom['sucesso']}")
    print(f"Saída do terminal:\n{res_bom['saida']}")
    
    print("\n" + "="*30 + "\n")
    
    # Teste 2: Um código que tem um erro de digitação (NameError)
    codigo_com_erro = "nome = 'Thamyres'\nprint(nomi)" # Erro: 'nomi' não existe
    print("--- Testando Código com Erro ---")
    res_erro = executar_codigo_usuario(codigo_com_erro)
    print(f"Sucesso? {res_erro['sucesso']}")
    print(f"Tipo do Erro: {res_erro['erro_tipo']}")
    print(f"Mensagem do Erro: {res_erro['erro_mensagem']}")