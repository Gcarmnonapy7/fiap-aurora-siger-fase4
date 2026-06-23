"""
Default data for the colony Aurora Siger.
"""

DEFAULT_MODULES = [
    ("HAB-01", "Habitação", 85, 9, 30, 5, "ativo"),
    ("CTR-01", "Centro de Controle", 120, 10, 15, 10, "ativo"),
    ("ARM-01", "Armazenamento de Energia", 45, 8, 500, 3, "ativo"),
    ("OXI-01", "Produção de Oxigênio", 100, 10, 40, 4, "ativo"),
    ("MED-01", "Suporte Médico", 65, 9, 8, 7, "ativo"),
    
    ("COM-01", "Comunicação", 75, 8, 5, 10, "ativo"),
    ("AGR-01", "Agricultura", 95, 7, 20, 6, "ativo"),
    ("LAB-01", "Laboratório Científico", 110, 6, 10, 8, "ativo"),

    ("REC-01", "Centro de Recreação", 40, 4, 2, 3, "ativo"),
    ("MAN-01", "Oficina de Manutenção", 50, 5, 5, 4, "ativo"),
]

POSITIONS_MODULES = {
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

CONNECTIONS_DEFAULT = [
    ("HAB-01", "CTR-01", 2),
    ("HAB-01", "MED-01", 1),
    ("HAB-01", "ARM-01", 3),
    ("CTR-01", "ARM-01", 2),
    ("CTR-01", "COM-01", 2),
    ("CTR-01", "LAB-01", 3),
    ("ARM-01", "OXI-01", 3),
    ("ARM-01", "AGR-01", 2),
    ("MED-01", "OXI-01", 2),
    
    ("HAB-01", "AGR-01", 4),
    ("AGR-01", "LAB-01", 2),
    ("AGR-01", "OXI-01", 3),
    ("LAB-01", "COM-01", 3),
    ("COM-01", "MED-01", 3),
    ("CTR-01", "MED-01", 3),
    
    ("REC-01", "LAB-01", 2),
    ("REC-01", "COM-01", 3),
    ("MAN-01", "ARM-01", 2),
    ("MAN-01", "AGR-01", 3),
    ("MAN-01", "OXI-01", 2),
]

TYPES_CONNECTIONS = {
    "HAB-01-CTR-01": "energia",
    "HAB-01-MED-01": "dados",
    "HAB-01-ARM-01": "energia",
    "CTR-01-ARM-01": "energia",
    "CTR-01-COM-01": "dados",
    "CTR-01-LAB-01": "dados",
    "ARM-01-OXI-01": "energia",
    "ARM-01-AGR-01": "energia",
    "MED-01-OXI-01": "vida",
    "HAB-01-AGR-01": "dados",
    "AGR-01-LAB-01": "dados",
    "AGR-01-OXI-01": "vida",
    "LAB-01-COM-01": "dados",
    "COM-01-MED-01": "dados",
    "CTR-01-MED-01": "dados",
}