"""
Dijkstra's algorithm implementation for finding the shortest path in a graph.
"""

import heapq
from typing import Dict, List, Tuple, Optional
from modules.grafo import InfrastructureGraph

class Dijkstra:
    """
    Implementation of the Dijkstra's algorithm for the shortest path possible.
    Utilizes heap (priority queue) for optimization and efficiency. 
    """
    
    def __init__(self, graph: InfrastructureGraph):
        self.graph = graph

    def shortest_path(self, start: str, end: str) -> Tuple[Optional[List[str]], Optional[float]]:
        """
        Finds the shortest path from start to end using Dijkstra's algorithm.
        
        Args:
            start (str): The starting module ID.
            end (str): The destination module ID.
        Returns:
            Tuple[Optional[List[str]], Optional[float]]: The shortest path as a list of module IDs and the total distance.
            
        """
        pass
        