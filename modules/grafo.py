"""
Graph Infrastructure Class - Represents the colony network as a graph.
Uses adjacency list and adjacency matrix.
"""

from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Set
from .module import Module

class InfrastructureGraph:
    """
    Class that represents the colony infrastructure as a graph.
    """
    
    def __init__(self):
        """Initializes the graph with empty data structures."""
        # Adjacency list: dictionary for search efficiency
        self.adjacency_list: Dict[str, List[str]] = defaultdict(list)
        
        # Adjacency matrix: for complete representation
        self.adjacency_matrix: List[List[float]] = []
        
        # Module dictionary: quick access by ID
        self.modules: Dict[str, Module] = {}
        
        # Module list for iteration
        self.module_list: List[Module] = []
        
        # Edge weights: key "mod1-mod2" -> weight (int)
        self.edge_weights: Dict[str, int] = {}
        
        # Module positions for visualization
        self.positions: Dict[str, Tuple[float, float]] = {}
        
        # Connection types dictionary
        self.connection_types: Dict[str, str] = {}
        
        # Distance matrix (for quick reference)
        self.distance_matrix: Optional[List[List[float]]] = None
        
    def _get_edge_key(self, id1: str, id2: str) -> str:
        """
        Generates a unique key for an edge.
        Sorts IDs to ensure consistency.
        """
        return f"{min(id1, id2)}-{max(id1, id2)}"
        
    def add_module(self, module: Module, position: Tuple[float, float] = None):
        """
        Adds a module to the graph.
        
        Structure: Uses dictionary for quick access and list for iteration.
        """
        if module.id in self.modules:
            raise ValueError(f"Module {module.id} already exists!")
        
        self.modules[module.id] = module
        self.module_list.append(module)
        self.adjacency_list[module.id] = []
        
        if position:
            self.positions[module.id] = position
            module.position = position
        
        # Updates adjacency matrix
        self._update_matrix()
        
    def add_connection(self, id1: str, id2: str, weight: int, 
                       connection_type: str = 'energy'):
        """
        Adds a connection between two modules with a weight.
        
        Args:
            id1: First module ID
            id2: Second module ID
            weight: Connection weight (distance, consumption, time)
            connection_type: Connection type ('energy', 'communication', 'data')
        """
        if id1 not in self.modules or id2 not in self.modules:
            raise ValueError(f"Module not found: {id1} or {id2}")
        
        if id1 == id2:
            raise ValueError("Cannot connect a module to itself")
        
        # Adds to adjacency list (undirected graph)
        if id2 not in self.adjacency_list[id1]:
            self.adjacency_list[id1].append(id2)
        if id1 not in self.adjacency_list[id2]:
            self.adjacency_list[id2].append(id1)
        
        # Stores the weight using the key format "id1-id2"
        edge_key = self._get_edge_key(id1, id2)
        self.edge_weights[edge_key] = weight
        self.connection_types[edge_key] = connection_type
        
        # Updates the matrix
        self._update_matrix()
        
    def _update_matrix(self):
        """Updates the adjacency matrix based on the adjacency list."""
        n = len(self.module_list)
        self.adjacency_matrix = [[0] * n for _ in range(n)]
        
        # Maps ID to index
        id_to_idx = {mod.id: i for i, mod in enumerate(self.module_list)}
        
        for id1, neighbors in self.adjacency_list.items():
            if id1 in id_to_idx:
                i = id_to_idx[id1]
                for id2 in neighbors:
                    if id2 in id_to_idx:
                        j = id_to_idx[id2]
                        edge_key = self._get_edge_key(id1, id2)
                        weight = self.edge_weights.get(edge_key, 1)
                        self.adjacency_matrix[i][j] = float(weight)
        
        # Updates distance matrix
        self._update_distance_matrix()
    
    def _update_distance_matrix(self):
        """Updates the distance matrix for quick reference."""
        n = len(self.module_list)
        self.distance_matrix = [[float('inf')] * n for _ in range(n)]
        
        for i in range(n):
            self.distance_matrix[i][i] = 0
        
        for id1, neighbors in self.adjacency_list.items():
            i = self.get_index(id1)
            if i is not None:
                for id2 in neighbors:
                    j = self.get_index(id2)
                    if j is not None:
                        edge_key = self._get_edge_key(id1, id2)
                        weight = self.edge_weights.get(edge_key, 1)
                        self.distance_matrix[i][j] = float(weight)
                        self.distance_matrix[j][i] = float(weight)
    
    def get_index(self, module_id: str) -> Optional[int]:
        """Returns the index of a module in the list."""
        for i, mod in enumerate(self.module_list):
            if mod.id == module_id:
                return i
        return None
    
    def get_neighbors(self, module_id: str) -> List[str]:
        """Returns the neighbors of a module."""
        return self.adjacency_list.get(module_id, [])
    
    def get_weight(self, id1: str, id2: str) -> int:
        """Returns the weight of the connection between two modules."""
        if id1 == id2:
            return 0
        edge_key = self._get_edge_key(id1, id2)
        return self.edge_weights.get(edge_key, float('inf'))
    
    def get_module(self, module_id: str) -> Optional[Module]:
        """Returns a module by ID."""
        return self.modules.get(module_id)
    
    def get_module_count(self) -> int:
        """Returns the number of modules in the graph."""
        return len(self.module_list)
    
    def get_connection_count(self) -> int:
        """Returns the number of connections in the graph."""
        return sum(len(v) for v in self.adjacency_list.values()) // 2
    
    def get_modules_by_priority(self, min_priority: int) -> List[Module]:
        """Returns modules with priority greater than or equal to the specified value."""
        return [m for m in self.module_list if m.priority >= min_priority]
    
    def get_adjacency_matrix(self) -> List[List[float]]:
        """Returns the adjacency matrix."""
        return self.adjacency_matrix
    
    def get_distance_matrix(self) -> List[List[float]]:
        """Returns the distance matrix."""
        return self.distance_matrix
    
    def get_edge_weights(self) -> Dict[str, int]:
        """Returns the edge weights dictionary."""
        return self.edge_weights.copy()
    
    def to_dict(self) -> dict:
        """Converts the graph to dictionary."""
        return {
            'modules': [mod.to_dict() for mod in self.module_list],
            'connections': [
                {
                    'module1': id1,
                    'module2': id2,
                    'weight': self.edge_weights[self._get_edge_key(id1, id2)],
                    'type': self.connection_types.get(self._get_edge_key(id1, id2), 'energy')
                }
                for id1, neighbors in self.adjacency_list.items()
                for id2 in neighbors
                if id1 < id2  # Avoids duplicates
            ]
        }