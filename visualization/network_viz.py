"""
Network visualization utilities.
"""

from typing import Dict, List, Tuple
from modules.grafo import InfrastructureGraph

class NetworkVisualization:
    """
    Simple network visualization (text-based and structural).
    """
    
    def __init__(self, graph: InfrastructureGraph):
        self.graph = graph
    
    def generate_network_description(self) -> str:
        """
        Generates a text description of the network.
        """
        description = []
        description.append("=" * 60)
        description.append("DESCRICAO DA REDE AURORA SIGER")
        description.append("=" * 60)
        
        # Modules
        description.append(f"\nMODULOS ({self.graph.get_module_count()}):")
        for module in self.graph.module_list:
            description.append(f"  - {module.name} (ID: {module.id})")
            description.append(f"    Consumo: {module.consumption} kWh")
            description.append(f"    Prioridade: {module.priority}/10")
            description.append(f"    Status: {module.status}")
        
        # Connections
        description.append(f"\nCONEXOES ({self.graph.get_connection_count()}):")
        seen_connections = set()
        for id1, neighbors in self.graph.adjacency_list.items():
            for id2 in neighbors:
                key = tuple(sorted([id1, id2]))
                if key not in seen_connections:
                    seen_connections.add(key)
                    weight = self.graph.get_weight(id1, id2)
                    description.append(f"  - {self.graph.modules[id1].name} <-> {self.graph.modules[id2].name}")
                    description.append(f"    Distancia: {weight}")
        
        return "\n".join(description)
    
    def generate_graph_structure(self) -> str:
        """
        Generates a graph structure representation.
        """
        structure = []
        structure.append("ESTRUTURA DO GRAFO:")
        structure.append("-" * 40)
        
        for module in self.graph.module_list:
            neighbors = self.graph.get_neighbors(module.id)
            if neighbors:
                names = [self.graph.modules[v].name for v in neighbors]
                structure.append(f"{module.name} -> {', '.join(names)}")
            else:
                structure.append(f"{module.name} -> (isolado)")
        
        return "\n".join(structure)
    
    def generate_statistics(self) -> str:
        """
        Generates network statistics.
        """
        total_modules = self.graph.get_module_count()
        total_connections = self.graph.get_connection_count()
        
        degrees = [len(self.graph.get_neighbors(mod.id)) for mod in self.graph.module_list]
        avg_degree = sum(degrees) / len(degrees) if degrees else 0
        
        statistics = []
        statistics.append("ESTATISTICAS DA REDE:")
        statistics.append("-" * 40)
        statistics.append(f"Total de modulos: {total_modules}")
        statistics.append(f"Total de conexoes: {total_connections}")
        statistics.append(f"Grau medio: {avg_degree:.2f}")
        statistics.append(f"Modulos com maior grau:")
        
        # Finds modules with highest degree
        sorted_modules = sorted(
            [(mod, len(self.graph.get_neighbors(mod.id))) for mod in self.graph.module_list],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        for mod, degree in sorted_modules:
            statistics.append(f"  - {mod.name}: {degree} conexoes")
        
        return "\n".join(statistics)