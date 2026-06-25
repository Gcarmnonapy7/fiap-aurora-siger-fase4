"""
Standard data for Aurora Siger colony modules and connections.
"""

# ==================== MODULE DATA ====================
# Format: (id, name, energy_consumption, priority, storage_capacity, communication_need, status)
DEFAULT_MODULES = [
    # Critical infrastructure modules (high priority)
    ("HAB-01", "Habitacao", 85, 9, 30, 5, "active"),
    ("CTR-01", "Centro de Controle", 120, 10, 15, 10, "active"),
    ("ARM-01", "Armazenamento de Energia", 45, 8, 500, 3, "active"),
    ("OXI-01", "Producao de Oxigenio", 100, 10, 40, 4, "active"),
    ("MED-01", "Suporte Medico", 65, 9, 8, 7, "active"),
    
    # Support modules (medium priority)
    ("COM-01", "Comunicacao", 75, 8, 5, 10, "active"),
    ("AGR-01", "Agricultura", 95, 7, 20, 6, "active"),
    ("LAB-01", "Laboratorio Cientifico", 110, 6, 10, 8, "active"),
    
    # Additional modules (low priority)
    ("REC-01", "Centro de Recreacao", 40, 4, 2, 3, "active"),
    ("MAN-01", "Oficina de Manutencao", 50, 5, 5, 4, "active"),
]

# Dictionary with module positions for visualization
MODULE_POSITIONS = {
    "HAB-01": (0, 0),
    "CTR-01": (2, 0),
    "ARM-01": (1, 1),
    "AGR-01": (3, 0),
    "LAB-01": (4, 0),
    "COM-01": (0, 2),
    "MED-01": (2, 2),
    "OXI-01": (1, 3),
    "REC-01": (4, 2),
    "MAN-01": (3, 3),
}

# ==================== CONNECTION DATA ====================
# Format: (id1, id2, weight)
DEFAULT_CONNECTIONS = [
    # Main connections (critical)
    ("HAB-01", "CTR-01", 2),
    ("HAB-01", "MED-01", 1),
    ("HAB-01", "ARM-01", 3),
    ("CTR-01", "ARM-01", 2),
    ("CTR-01", "COM-01", 2),
    ("CTR-01", "LAB-01", 3),
    ("ARM-01", "OXI-01", 3),
    ("ARM-01", "AGR-01", 2),
    ("MED-01", "OXI-01", 2),
    
    # Secondary connections
    ("HAB-01", "AGR-01", 4),
    ("AGR-01", "LAB-01", 2),
    ("AGR-01", "OXI-01", 3),
    ("LAB-01", "COM-01", 3),
    ("COM-01", "MED-01", 3),
    ("CTR-01", "MED-01", 3),
    
    # Additional connections
    ("REC-01", "LAB-01", 2),
    ("REC-01", "COM-01", 3),
    ("MAN-01", "ARM-01", 2),
    ("MAN-01", "AGR-01", 3),
    ("MAN-01", "OXI-01", 2),
]

# Dictionary with connection types
CONNECTION_TYPES = {
    "HAB-01-CTR-01": "energy",
    "HAB-01-MED-01": "data",
    "HAB-01-ARM-01": "energy",
    "CTR-01-ARM-01": "energy",
    "CTR-01-COM-01": "data",
    "CTR-01-LAB-01": "data",
    "ARM-01-OXI-01": "energy",
    "ARM-01-AGR-01": "energy",
    "MED-01-OXI-01": "life",
    "HAB-01-AGR-01": "data",
    "AGR-01-LAB-01": "data",
    "AGR-01-OXI-01": "life",
    "LAB-01-COM-01": "data",
    "COM-01-MED-01": "data",
    "CTR-01-MED-01": "data",
}