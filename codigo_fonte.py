"""
SIGIC - Intelligent Management System for Colony Infrastructure
Main File - Aurora Siger

Integrated Disciplines: Algorithms, Data Structures, Mathematical Modeling
Author: SIGIC Team
Version: 1.0
"""

import sys
import os

# Adds current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.grafo import InfrastructureGraph
from modules.module import Module
from ui.menu import MenuSIGIC
from data.data_modules import DEFAULT_MODULES, DEFAULT_CONNECTIONS, MODULE_POSITIONS

class SIGICSystem:
    """
    Main SIGIC system.
    Initializes colony infrastructure and manages program execution.
    """
    
    def __init__(self):
        """Initializes the system with the colony infrastructure."""
        self.graph = self._initialize_infrastructure()
        self.menu = MenuSIGIC(self.graph)
    
    def _initialize_infrastructure(self) -> InfrastructureGraph:
        """
        Initializes the colony infrastructure.
        Uses standardized data from the data module.
        """
        graph = InfrastructureGraph()
        
        # Adds modules using data from the data file
        for data in DEFAULT_MODULES:
            module = Module(*data)
            position = MODULE_POSITIONS.get(data[0])
            graph.add_module(module, position)
        
        # Adds connections using data from the data file
        for id1, id2, weight in DEFAULT_CONNECTIONS:
            graph.add_connection(id1, id2, weight)
        
        return graph
    
    def run(self):
        """Executes the system."""
        print("\n" + "="*60)
        print("SIGIC - SISTEMA INTELIGENTE DE GERENCIAMENTO")
        print("INFRAESTRUTURA DA COLONIA AURORA SIGER")
        print("="*60)
        print("\nBem-vindo ao Sistema de Gerenciamento da Colonia!")
        print(f"Total de modulos ativos: {self.graph.get_module_count()}")
        
        # Executes the main menu
        self.menu.run()

def main():
    """Main system function."""
    try:
        system = SIGICSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuario.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("Por favor, reinicie o sistema.")
    finally:
        print("\n" + "="*60)
        print("SIGIC - Encerrando sistema...")
        print("Obrigado por utilizar o sistema!")

if __name__ == "__main__":
    main()