import os
import sys
import subprocess
import importlib.util
import time
import traceback

PROJETO_RAIZ = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(PROJETO_RAIZ, "venv", "Scripts", "python.exe")

def carregar_dependencias():
    """Lê os nomes dos pacotes a partir do requirements.txt (ignora versões)."""
    try:
        caminho = os.path.join(PROJETO_RAIZ, "requirements.txt")
        with open(caminho, "r", encoding="utf-8") as req:
            linhas = req.readlines()
            pacotes = []
            for linha in linhas:
                linha = linha.strip()
                if linha and not linha.startswith("#"):
                    nome = linha.split("==")[0].strip()
                    pacotes.append(nome)
            return pacotes
    except Exception as e:
        print(f"❌ Erro ao carregar requirements.txt: {e}")
        with open("erro.log", "a", encoding="utf-8") as log:
            log.write(f"Erro ao carregar dependências: {traceback.format_exc()}\n")
        raise e


def esta_na_venv():
    """Verifica se o programa está sendo executado dentro de uma venv."""
    try:
        return sys.prefix != sys.base_prefix
    except Exception as e:
        print(f"❌ Erro ao verificar se está na venv: {e}")
        with open("erro.log", "a", encoding="utf-8") as log:
            log.write(f"Erro ao verificar venv: {traceback.format_exc()}\n")
        raise e

def dependencias_instaladas():
    """Verifica se as dependências listadas em requirements.txt estão instaladas."""
    try:
        pacotes = carregar_dependencias()
        return all(importlib.util.find_spec(pkg) for pkg in pacotes)
    except Exception as e:
        print(f"❌ Erro ao verificar dependências: {e}")
        with open("erro.log", "a", encoding="utf-8") as log:
            log.write(f"Erro ao verificar dependências: {traceback.format_exc()}\n")
        raise e


def instalar_dependencias():
    """Instala as dependências a partir de requirements.txt."""
    try:
        print("📦 Instalando dependências...")
        requirements = os.path.join(PROJETO_RAIZ, "requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements])
        print("✅ Instalação concluída.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        with open("erro.log", "a", encoding="utf-8") as log:
            log.write(f"Erro ao instalar dependências: {traceback.format_exc()}\n")
        raise e

def criar_venv():
    """Cria um ambiente virtual se não existir."""
    try:
        if not os.path.exists(VENV_PYTHON):
            print("🛠 Criando ambiente virtual...")
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            print("✅ Ambiente virtual criado.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar venv: {e}")
        with open("erro.log", "a", encoding="utf-8") as log:
            log.write(f"Erro ao criar venv: {traceback.format_exc()}\n")
        raise e

def reiniciar_com_venv():
    """Reinicia o programa utilizando o Python da venv"""
    print("♻ Reiniciando com o Python da venv...")

    # Caminho absoluto para o script atual
    caminho_script = os.path.abspath(__file__)
    print(f"Comando a ser executado: {VENV_PYTHON} {caminho_script}")

    # Verifica se o Python da venv existe
    if not os.path.exists(VENV_PYTHON):
        raise FileNotFoundError(f"Python da venv não encontrado: {VENV_PYTHON}")
    
    # Executa o comando para reiniciar o programa
    try:
        subprocess.run([VENV_PYTHON, caminho_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao reiniciar o programa com a venv: {e}")
        with open("erro.log", "a", encoding="utf-8") as log:
            log.write(f"Erro ao reiniciar com a venv: {traceback.format_exc()}\n")
        raise e
    
    sys.exit()

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    os.chdir(PROJETO_RAIZ)

    try:
        if not esta_na_venv():
            criar_venv()
            reiniciar_com_venv()

        if not dependencias_instaladas():
            try:
                instalar_dependencias()
                subprocess.run([sys.executable, __file__], check=True)

                sys.exit()
            
            except Exception as e:
                print("❌ Erro ao instalar dependências:")
                with open("erro.log", "a", encoding="utf-8") as log:
                    log.write(f"Erro ao instalar dependências: {traceback.format_exc()}\n")
                print(str(e))
                input("\nPressione Enter para sair...")

        # Limpa a tela depois que tudo está OK
        limpar_tela()

        try:
            # Importa os módulos após garantir que as dependências estão instaladas
            from view.simulador import simular
            from testes.comparador_testes import comparar_algoritmos_estruturas

            print("🚀 Executando o programa. Por favor, aguarde...\n")
            time.sleep(1)
            simular()
            # comparar_algoritmos_estruturas()
            input("\n✅ Execução concluída. Pressione Enter para sair...")

        except Exception as e:
            print("❌ Erro durante execução:")
            with open("erro.log", "a", encoding="utf-8") as log:
                log.write(f"Erro durante execução: {traceback.format_exc()}\n")
            print(str(e))
            input("\nPressione Enter para sair...")

    except Exception as e:
        print("❌ Erro ao iniciar o programa:")
        with open("erro.log", "a", encoding="utf-8") as log:
            log.write(f"Erro ao iniciar o programa: {traceback.format_exc()}\n")
        print(str(e))
        input("\nPressione Enter para sair...")
