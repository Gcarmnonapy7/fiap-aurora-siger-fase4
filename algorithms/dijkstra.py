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
        if start not in self.graph.modules or end not in self.graph.modules:
            return [],float('inf') # Return empty path and infinite distance if start or end module does not exist in the graph.
        
        if start == end:
            return [start],0.0
        
        distances = {module_id: float('inf') for module_id in self.graph.modules}
        distances[start] = 0
        previous_nodes = {start: None} # Keep track of the previous node for path reconstruction
        
        # Priority queue to store (distance, module_id) tuples
        
        priority_queue = [(0, start)]
        visited = set()
        
        print("=" * 60)
        print(f"Starting Dijkstra's algorithm from {start} to {end}")
        print("=" * 60)
        
        print("Processing edges:")
        
        while priority_queue: 
            
            current_distance, current_module = heapq.heappop(priority_queue)
            
            if start == end:
                break
            
            for neighbor in self.graph.adjacency_list[current_module]:
                
                if neighbor in visited:
                    continue
                
                edge_weight = self.graph.edges_weights.get(current_module , neighbor)
                
                if edge_weight == float('inf'):
                    continue
                
                new_distance = current_distance + edge_weight
                
                # Update the distance if a shorter path is found
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current_module
                    heapq.heappush(priority_queue, (new_distance, neighbor))
                    
                    print(f"Edge: {current_module} -> {neighbor}, Weight: {edge_weight}, New Distance: {new_distance}")
                    
                if distances[end] == float('inf'):
                    print(f"No path found from {start} to {end}.")
                    return [], float('inf')
                
                path = []
                current = end
                while current is not None: 
                    path.append(current)
                    current = previous_nodes.get(current)
                path.reverse()
                
                
                print(f"Shortest path from {start} to {end}: {' -> '.join(path)} with total distance: {distances[end]}")
                
                return (path, distances[end])
            
    def get_all_paths(self,start:str) -> Dict[str, Tuple[List[str], float]]:
        """
        Get the shortest paths from the start module to all other modules in the graph.
        
        Args:
            start (str): The starting module ID.
        Returns:
            Dict[str, Tuple[List[str], float]]: A dictionary where keys are module IDs and values are tuples containing the shortest path and its distance.
        """
        
        results = {}
        
        if start not in self.graph.modules:
            print(f"Start module {start} does not exist in the graph.")
            return results
        
        for end in self.graph.modules:
            if start != end:
                path, distance = self.shortest_path(start, end)
                results[end] = (path, distance)
        
        return results