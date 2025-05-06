import subprocess
import sys
import importlib.util
import os
import time

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
    print("Dependências não encontradas. Instalando a partir de requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Instalação concluída. Reiniciando o programa...\n")
    time.sleep(2)

def reiniciar():
    """Reinicia o script atual"""
    os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == "__main__":
    if not dependencias_instaladas():
        instalar_dependencias()
        reiniciar()

    # Importa somente após garantir que está tudo instalado
    from view.simulador import simular
    from testes.comparador_testes import comparar_algoritmos

    print("Abrindo o projeto. Por favor, aguarde...")
    time.sleep(1)

    simular()
    comparar_algoritmos()
    