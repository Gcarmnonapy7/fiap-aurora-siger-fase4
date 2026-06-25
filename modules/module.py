"""
Module Class - Represents a module of the Aurora Siger colony.
"""

class Module:
    """
    Class that represents a colony module.
    Uses tuple for fixed data and dictionary for dynamic attributes.
    """
    
    def __init__(self, module_id: str, name: str, energy_consumption: float, 
                 priority: int, storage_capacity: float, 
                 communication_need: int, status: str):
        """
        Initializes a colony module.
        
        Args:
            module_id: Unique module identifier
            name: Descriptive module name
            energy_consumption: Energy required for operation (kWh)
            priority: Importance level (1-10, where 10 is most important)
            storage_capacity: Storage capacity (kWh)
            communication_need: Communication frequency (1-10)
            status: 'active', 'maintenance', 'alert'
        """
        # Fixed attributes (as tuple)
        self._fixed_data = (
            module_id,
            name,
            energy_consumption,
            priority,
            storage_capacity,
            communication_need,
            status
        )
        
        # Dynamic attributes (as dictionary)
        self._attributes = {
            'position': None,
            'temperature': 20.0,
            'current_load': 0.0,
            'connections': []
        }
    
    # Properties for accessing fixed data
    @property
    def id(self) -> str:
        return self._fixed_data[0]
    
    @property
    def name(self) -> str:
        return self._fixed_data[1]
    
    @property
    def consumption(self) -> float:
        return self._fixed_data[2]
    
    @property
    def priority(self) -> int:
        return self._fixed_data[3]
    
    @property
    def capacity(self) -> float:
        return self._fixed_data[4]
    
    @property
    def communication(self) -> int:
        return self._fixed_data[5]
    
    @property
    def status(self) -> str:
        return self._fixed_data[6]
    
    # Getters and setters for dynamic attributes
    @property
    def position(self):
        return self._attributes['position']
    
    @position.setter
    def position(self, value):
        self._attributes['position'] = value
    
    @property
    def temperature(self):
        return self._attributes['temperature']
    
    @temperature.setter
    def temperature(self, value):
        self._attributes['temperature'] = value
    
    @property
    def load(self):
        return self._attributes['current_load']
    
    @load.setter
    def load(self, value):
        self._attributes['current_load'] = max(0, min(value, self.capacity))
    
    def __str__(self):
        return f"{self.name} (ID: {self.id}) - Priority: {self.priority}"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self) -> dict:
        """Converts module to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'consumption': self.consumption,
            'priority': self.priority,
            'capacity': self.capacity,
            'communication': self.communication,
            'status': self.status,
            'position': self.position,
            'temperature': self.temperature,
            'load': self.load
        }