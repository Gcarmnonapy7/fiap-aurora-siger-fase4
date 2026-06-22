"""
InfrastructureGraph Class - Represents the colony network as a graph.
Uses adjacency list and adjacency matrix.
"""

from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Set
from .module import Module


class InfrastructureGraph:
    """
    Class that represents the colony's infrastructure as a graph.
    """
    
    def __init__(self):
        """
        Initializes the graph with empty adjacency list and matrix.
        """
        
        self.adjacency_list: Dict[str,List[str]] = defaultdict(list)
        self.adjacency_matrix: Dict[Tuple[str, str], bool] = {}
        self.modules: Dict[str, Module] = {}
        self.list_of_modules: List[str] = []
        
        # weights edges
        self.edges_weights: Dict[str,int] = {}
        
        self.positions: Dict[str, Tuple[int,int]] = {}
        
        self.type_of_connection : Dict[Tuple[str, str], str] = {}
        
        self.matrix_distance = None
    
    def add_module(self,module : Module,position : Tuple[float,float] = None): 
        """
        Add a module to the graph
        
        Structure : use a dict for quick acess and list interaction.
        """
        
        if module is None : 
            raise ValueError(f"Module does not exists")
        
        if module.id in self.modules:
            raise ValueError(f"Module {module.id} already exists")
        
        self.modules[module.id] = module
        self.list_of_modules.append(module)
        self.adjacency_list[module.id] = []
        
        if position:
            self.positions[module.id] = position
            module.position = position
            
        # self update adjacency_matrix
        self._update_matrix()
        
    def add_connection(self,id1:str,id2:str,weight:float,type : str = "energy"):
        """
        Add connection between two modules(their ids) with a weight
        Args : 
            id1: first id
            id2: second i2
            weight : the wieght between the connection (distance,consume,type)
            type : type of connection (energy,communication,data)
        """
        if id1 not in self.modules or id2 not in self.modules:
            raise ValueError(f"One or both modules do not exist: {id1}, {id2}")
        
        if id1 == id2: 
            raise ValueError(f"Cannot connect module to itself: {id1}")
        
        # Update adjacency list
        
        if id2 not in self.adjacency_list[id1]:
            self.adjacency_list[id1].append(id2)
        if id1 not in self.adjacency_list[id2]:
            self.adjacency_list[id2].append(id1)
        
        # Storage the weight (normalize for id1,id2)
        key = tuple(sorted(id1,id2))
        self.edges_weights[key] = weight
        self.edges_weights[key] = type
        
        # self update matrix 
        self._update_matrix()
        
    def _update_matrix(self):
        """
        Update the adjacency_matrix based on the current adjacency_list 
        """
        
        n_of_modules = len(self.list_of_modules)
        
        self.adjacency_matrix = [[0] * n_of_modules for _ in range(n_of_modules)]
        
        # Map module ids to indices
        id_to_idx = {module.id: idx for idx,module in enumerate(self.list_of_modules)}
        
        for id1, neighbors in self.adjacency_list.items():
            if id1 in id_to_idx:
                idx1 = id_to_idx[id1]
                for id2 in neighbors:
                    if id2 in id_to_idx:
                        idx2 = id_to_idx[id2]
                        edge_key = self._get_edge_key(id1, id2)
                        weight = self.edges_weights.get(edge_key, 1)  # Default weight is 1
                        self.adjacency_matrix[idx1][idx2] = float(weight)
                        self.adjacency_matrix[idx2][idx1] = float(weight)  # Symmetric for undirected graph
                        
    def get_index(self,module_id:str) -> Optional[int]:
        """
        Get the index of a module in the adjacency matrix
        """
        for idx,module in enumerate(self.list_of_modules):
            if module.id == module_id:
                return idx
        return None
    
    def get_neighbors(self,module_id:str) -> List[str] : 
        """
        Get the neighbors of a module by its id
        """
        return self.adjacency_list.get(module_id, [])
    
    def get_module(self,module_id:str) -> Optional[Module]:
        """
        Get a module by its id
        """
        return self.modules.get(module_id, None)
    
    def get_weight(self,id1:str,id2:str) -> Optional[float]:
        """
        Get the weight of the connection between two modules
        """
        key = self._get_edge_key(id1, id2)
        return self.edges_weights.get(key, None)
    
    def get_connection_type(self,id1:str,id2:str) -> Optional[str]:
        """
        Get the type of connection between two modules
        """
        key = self._get_edge_key(id1, id2)
        return self.type_of_connection.get(key, None)
    
    def number_of_modules(self) -> int:
        """
        Get the number of modules in the graph
        """
        return len(self.list_of_modules)
    
    def _get_edge_key(self,id1:str,id2:str) -> Tuple[str,str]:
        """
        Get the edge key for two module ids (sorted tuple)
        """
        return tuple(sorted((id1, id2)))
    
    def to_dict(self) -> Dict:
        """
        Convert the graph to a dictionary representation
        """
        return {
            'modules': {module_id: module.__dict__ for module_id, module in self.modules.items()},
            'adjacency_list': dict(self.adjacency_list),
            'edges_weights': self.edges_weights,
            'type_of_connection': self.type_of_connection,
            'positions': self.positions
        }