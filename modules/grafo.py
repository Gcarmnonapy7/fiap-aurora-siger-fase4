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
        
        self.positions: Dict[str, Tuple[int,int]] = {}
        
        self.type_of_connection : Dict[Tuple[str, str], str] = {}
        
        self.matrix_distance = None
    
    def add_module(self,module : Module,position : Tuple[float,float] = None): 
        pass        