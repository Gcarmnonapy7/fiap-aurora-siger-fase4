"""
Network analysis algorithms: BFS, DFS, efficiency, centrality, and critical points.
"""

from collections import deque
from typing import Dict, List, Set, Optional
from modules.grafo import InfrastructureGraph

class SearchAlgorithms:
    """
    Implements graph search algorithms (BFS and DFS).
    """
    
    def __init__(self, graph: InfrastructureGraph):
        self.graph = graph
    
    def bfs(self, start: str, target: str = None) -> Dict[str, List[str]]:
        """
        Breadth-First Search (BFS) - Explores the network by levels.
        Useful for finding connections and analyzing network structure.
        
        Returns dictionary with paths to all nodes.
        """
        if start not in self.graph.modules:
            return {}
        
        visited = {start}
        queue = deque([start])
        paths = {start: [start]}
        levels = {start: 0}
        
        print(f"\n=== BFS - Busca em Largura ===")
        print(f"Iniciando busca a partir de: {self.graph.modules[start].name}")
        print(f"Nivel 0: {self.graph.modules[start].name}")
        
        level = 1
        while queue:
            level_size = len(queue)
            current_level = []
            
            for _ in range(level_size):
                current = queue.popleft()
                
                for neighbor in self.graph.get_neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        paths[neighbor] = paths[current] + [neighbor]
                        levels[neighbor] = level
                        current_level.append(self.graph.modules[neighbor].name)
                        
                        if target and neighbor == target:
                            print(f"Alvo encontrado no nivel {level}!")
                            return paths
            
            if current_level:
                print(f"Nivel {level}: {' -> '.join(current_level)}")
            level += 1
        
        return paths
    
    def dfs(self, start: str, target: str = None, 
            visited: Set[str] = None, path: List[str] = None,
            depth: int = 0) -> List[str]:
        """
        Depth-First Search (DFS) - Explores complete paths.
        Useful for finding paths and detecting cycles.
        """
        if start not in self.graph.modules:
            return []
        
        if visited is None:
            visited = set()
            path = []
            print(f"\n=== DFS - Busca em Profundidade ===")
            print(f"Iniciando busca a partir de: {self.graph.modules[start].name}")
            print("-" * 40)
        
        visited.add(start)
        path.append(start)
        
        indent = "  " * depth
        print(f"{indent}Visitando: {self.graph.modules[start].name}")
        
        if target and start == target:
            print(f"{indent}Alvo encontrado!")
            return path
        
        for neighbor in self.graph.get_neighbors(start):
            if neighbor not in visited:
                result = self.dfs(neighbor, target, visited, path, depth + 1)
                if result:
                    return result
        
        path.pop()
        return []
    
    def bfs_components(self) -> List[List[str]]:
        """
        Finds all connected components using BFS.
        """
        components = []
        unvisited = set(self.graph.modules.keys())
        
        while unvisited:
            start = unvisited.pop()
            component = []
            queue = deque([start])
            
            while queue:
                current = queue.popleft()
                component.append(current)
                
                for neighbor in self.graph.get_neighbors(current):
                    if neighbor in unvisited:
                        unvisited.remove(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
        
        return components


class NetworkAnalysis:
    """
    Performs network analysis: efficiency, critical points, centrality.
    """
    
    def __init__(self, graph: InfrastructureGraph):
        self.graph = graph
    
    def detect_critical_points(self) -> List[str]:
        """
        Detects critical points in the network (articulations).
        Modules whose removal would disconnect the network.
        """
        critical_points = set()
        visited = set()
        time = 0
        discovery = {}
        low = {}
        parent = {}
        
        def dfs_articulation(current):
            nonlocal time
            visited.add(current)
            discovery[current] = low[current] = time
            time += 1
            
            children = 0
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    children += 1
                    parent[neighbor] = current
                    dfs_articulation(neighbor)
                    
                    low[current] = min(low[current], low[neighbor])
                    
                    if parent.get(current) is None and children > 1:
                        critical_points.add(current)
                    if parent.get(current) is not None and low[neighbor] >= discovery[current]:
                        critical_points.add(current)
                
                elif neighbor != parent.get(current):
                    low[current] = min(low[current], discovery[neighbor])
        
        for module in self.graph.modules:
            if module not in visited:
                dfs_articulation(module)
        
        return list(critical_points)
    
    def analyze_efficiency(self) -> Dict:
        """
        Analyzes the operational efficiency of the network.
        """
        total_modules = self.graph.get_module_count()
        total_connections = self.graph.get_connection_count()
        
        # Average degree of the network
        average_degree = (2 * total_connections) / total_modules if total_modules > 0 else 0
        
        # Communication efficiency (normalized)
        communication_efficiency = min(1.0, average_degree / 4.0)
        
        # Energy efficiency
        avg_consumption = sum(m.consumption for m in self.graph.module_list) / total_modules if total_modules > 0 else 0
        energy_efficiency = max(0, 1.0 - (avg_consumption / 100.0))
        
        # Critical modules (high priority, low connectivity)
        critical_modules = []
        for module_id, module in self.graph.modules.items():
            if module.priority >= 8 and len(self.graph.get_neighbors(module_id)) <= 2:
                critical_modules.append(module.name)
        
        # Articulation points
        articulations = self.detect_critical_points()
        critical_connections = [self.graph.modules[art].name for art in articulations if art in self.graph.modules]
        
        # Clustering coefficient
        clustering_coefficient = self._calculate_clustering_coefficient()
        
        # Edge weight metrics
        if self.graph.edge_weights:
            weights = list(self.graph.edge_weights.values())
            avg_weight = sum(weights) / len(weights) if weights else 0
            max_weight = max(weights) if weights else 0
            min_weight = min(weights) if weights else 0
        else:
            avg_weight = max_weight = min_weight = 0
        
        return {
            'total_modules': total_modules,
            'total_connections': total_connections,
            'average_degree': average_degree,
            'communication_efficiency': communication_efficiency,
            'energy_efficiency': energy_efficiency,
            'critical_modules': critical_modules,
            'critical_connections': critical_connections,
            'clustering_coefficient': clustering_coefficient,
            'avg_edge_weight': avg_weight,
            'max_edge_weight': max_weight,
            'min_edge_weight': min_weight,
            'overall_status': 'otimo' if communication_efficiency > 0.7 and energy_efficiency > 0.7 else 
                             'bom' if communication_efficiency > 0.5 and energy_efficiency > 0.5 else 'critico'
        }
    
    def _calculate_clustering_coefficient(self) -> float:
        """
        Calculates the average clustering coefficient of the network.
        Measures how clustered the modules are.
        """
        if not self.graph.module_list:
            return 0.0
        
        total_coefficient = 0.0
        total_vertices = 0
        
        for module in self.graph.module_list:
            neighbors = self.graph.get_neighbors(module.id)
            k = len(neighbors)
            
            if k < 2:
                continue
            
            # Counts edges between neighbors
            edges_between_neighbors = 0
            for i in range(k):
                for j in range(i + 1, k):
                    if neighbors[j] in self.graph.get_neighbors(neighbors[i]):
                        edges_between_neighbors += 1
            
            # Clustering coefficient for this vertex
            possible = k * (k - 1) / 2
            if possible > 0:
                total_coefficient += edges_between_neighbors / possible
                total_vertices += 1
        
        return total_coefficient / total_vertices if total_vertices > 0 else 0.0
    
    def analyze_centrality(self) -> Dict[str, Dict]:
        """
        Analyzes the centrality of modules in the network.
        """
        centrality = {}
        
        for module in self.graph.module_list:
            # Degree centrality (number of connections)
            degree = len(self.graph.get_neighbors(module.id))
            
            # Betweenness centrality (approximation via BFS)
            betweenness = self._calculate_betweenness(module.id)
            
            centrality[module.id] = {
                'name': module.name,
                'degree': degree,
                'betweenness': betweenness,
                'priority': module.priority
            }
        
        return centrality
    
    def _calculate_betweenness(self, module_id: str) -> float:
        """
        Calculates the betweenness centrality for a module.
        """
        total_paths = 0
        paths_passing = 0
        
        # For each pair of modules (except itself)
        module_ids = list(self.graph.modules.keys())
        for i, origin in enumerate(module_ids):
            if origin == module_id:
                continue
            for destination in module_ids[i+1:]:
                if destination == module_id:
                    continue
                
                # Finds paths using simplified BFS
                paths = self._find_simple_paths(origin, destination)
                total_paths += len(paths)
                
                for path in paths:
                    if module_id in path:
                        paths_passing += 1
        
        return paths_passing / total_paths if total_paths > 0 else 0.0
    
    def _find_simple_paths(self, origin: str, destination: str) -> List[List[str]]:
        """
        Finds simple paths between two nodes (for betweenness calculation).
        """
        if origin == destination:
            return [[origin]]
        
        paths = []
        queue = deque([(origin, [origin])])
        
        while queue:
            current, path = queue.popleft()
            
            if current == destination:
                paths.append(path)
                continue
            
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in path:
                    queue.append((neighbor, path + [neighbor]))
        
        return paths