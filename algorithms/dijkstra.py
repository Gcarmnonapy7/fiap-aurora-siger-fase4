"""
Dijkstra's algorithm for shortest path.
"""

import heapq
from typing import List, Tuple, Dict
from modules.grafo import InfrastructureGraph

class Dijkstra:
    """
    Implements Dijkstra's algorithm to find the shortest path.
    Uses heap (priority queue) for optimization.
    """
    
    def __init__(self, graph: InfrastructureGraph):
        self.graph = graph
    
    def find_path(self, origin: str, destination: str) -> Tuple[List[str], float]:
        """
        Finds the shortest path between origin and destination.
        
        Args:
            origin: Source module ID
            destination: Destination module ID
            
        Returns:
            Tuple (path, total_distance)
        """
        if origin not in self.graph.modules or destination not in self.graph.modules:
            return [], float('inf')
        
        if origin == destination:
            return [origin], 0.0
        
        # Initializes distances
        distances = {module: float('inf') for module in self.graph.modules}
        distances[origin] = 0
        previous = {origin: None}
        
        # Priority queue: (distance, module_id)
        heap = [(0, origin)]
        visited = set()
        
        print(f"\n=== Dijkstra - Caminho Minimo ===")
        print(f"Origem: {self.graph.modules[origin].name}")
        print(f"Destino: {self.graph.modules[destination].name}")
        print("-" * 50)
        print("Processando vertices:")
        
        while heap:
            current_dist, current = heapq.heappop(heap)
            
            if current in visited:
                continue
            
            visited.add(current)
            print(f"  * {self.graph.modules[current].name} (distancia: {current_dist:.2f})")
            
            if current == destination:
                break
            
            for neighbor in self.graph.get_neighbors(current):
                if neighbor in visited:
                    continue
                
                weight = self.graph.get_weight(current, neighbor)
                if weight == float('inf'):
                    continue
                    
                new_dist = current_dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(heap, (new_dist, neighbor))
        
        # Reconstructs the path
        if distances[destination] == float('inf'):
            print("\nDestino inalcancavel!")
            return [], float('inf')
        
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        
        print(f"\nCaminho encontrado:")
        print(f"   {' -> '.join([self.graph.modules[m].name for m in path])}")
        print(f"   Distancia total: {distances[destination]:.2f}")
        
        return path, distances[destination]
    
    def find_all_paths(self, origin: str) -> Dict[str, Tuple[List[str], float]]:
        """
        Finds the shortest paths from origin to all other vertices.
        """
        results = {}
        
        for destination in self.graph.modules:
            if destination != origin:
                path, distance = self.find_path(origin, destination)
                if path:
                    results[destination] = (path, distance)
        
        return results
    
    def find_path_with_constraints(self, origin: str, destination: str, 
                                   min_priority: int = 0) -> Tuple[List[str], float]:
        """
        Finds the shortest path considering priority constraints.
        Modules with priority lower than min_priority are avoided.
        
        Args:
            origin: Source module ID
            destination: Destination module ID
            min_priority: Minimum required priority (0-10)
            
        Returns:
            Tuple (path, total_distance)
        """
        if origin not in self.graph.modules or destination not in self.graph.modules:
            return [], float('inf')
        
        # Checks if source and destination meet the criteria
        if self.graph.modules[origin].priority < min_priority:
            print(f"Modulo de origem nao atende a prioridade minima ({min_priority})")
            return [], float('inf')
        
        if self.graph.modules[destination].priority < min_priority:
            print(f"Modulo de destino nao atende a prioridade minima ({min_priority})")
            return [], float('inf')
        
        # Initializes distances
        distances = {module: float('inf') for module in self.graph.modules}
        distances[origin] = 0
        previous = {origin: None}
        
        heap = [(0, origin)]
        visited = set()
        
        print(f"\n=== Dijkstra com Restricao de Prioridade (min: {min_priority}) ===")
        print(f"Origem: {self.graph.modules[origin].name}")
        print(f"Destino: {self.graph.modules[destination].name}")
        print("-" * 50)
        print("Processando vertices:")
        
        while heap:
            current_dist, current = heapq.heappop(heap)
            
            if current in visited:
                continue
            
            visited.add(current)
            print(f"  * {self.graph.modules[current].name} (distancia: {current_dist:.2f})")
            
            if current == destination:
                break
            
            for neighbor in self.graph.get_neighbors(current):
                if neighbor in visited:
                    continue
                
                # Checks if neighbor meets minimum priority
                if self.graph.modules[neighbor].priority < min_priority:
                    print(f"    - {self.graph.modules[neighbor].name} ignorado (prioridade {self.graph.modules[neighbor].priority} < {min_priority})")
                    continue
                
                weight = self.graph.get_weight(current, neighbor)
                if weight == float('inf'):
                    continue
                    
                new_dist = current_dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(heap, (new_dist, neighbor))
        
        # Reconstructs the path
        if distances[destination] == float('inf'):
            print("\nDestino inalcancavel com as restricoes!")
            return [], float('inf')
        
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        
        print(f"\nCaminho encontrado:")
        print(f"   {' -> '.join([self.graph.modules[m].name for m in path])}")
        print(f"   Distancia total: {distances[destination]:.2f}")
        
        return path, distances[destination]