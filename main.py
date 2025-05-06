import sys
import os
sys.path.insert(0, os.path.abspath("libs"))

from view.simulador import simular

if __name__ == "__main__":
    simular()