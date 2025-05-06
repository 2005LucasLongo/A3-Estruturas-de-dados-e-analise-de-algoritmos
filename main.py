import subprocess
import sys
import importlib.util
import os
import time
import traceback

# Lista de dependências que você usa no projeto
DEPENDENCIAS = ["tabulate"]

def dependencias_instaladas():
    """Verifica se todas as dependências estão disponíveis"""
    for pacote in DEPENDENCIAS:
        if importlib.util.find_spec(pacote) is None:
            return False
    return True

def instalar_dependencias():
    """Instala as dependências usando o pip"""
    caminho_requirements = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(caminho_requirements):
        raise FileNotFoundError(f"Arquivo requirements.txt não encontrado em {caminho_requirements}")

    print("Dependências não encontradas. Instalando a partir de requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", caminho_requirements])
    print("Instalação concluída. Reiniciando o programa...\n")
    time.sleep(2)

def reiniciar():
    """Reinicia o script atual"""
    os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == "__main__":
    # Garante que o diretório atual é a raiz do projeto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if not dependencias_instaladas():
        try:
            instalar_dependencias()
            reiniciar()
        except Exception as e:
            print("❌ Ocorreu um erro durante a instalação:")
            with open("erro.log", "w", encoding="utf-8") as log:
                log.write(traceback.format_exc())
            print(str(e))
            print("Veja mais detalhes no arquivo 'erro.log'.")
            input("\nPressione Enter para sair...")

    try:
        # Importa somente após garantir que está tudo instalado
        from view.simulador import simular
        from testes.comparador_testes import comparar_algoritmos

        print("Abrindo o projeto. Por favor, aguarde...")
        time.sleep(1)

        simular()
        comparar_algoritmos()
        input("\nPressione Enter para sair...")

    except Exception as e:
        print("❌ Ocorreu um erro durante a execução do programa:")
        with open("erro.log", "w", encoding="utf-8") as log:
            log.write(traceback.format_exc())
        print(str(e))
        print("Veja mais detalhes no arquivo 'erro.log'.")
        input("\nPressione Enter para sair...")