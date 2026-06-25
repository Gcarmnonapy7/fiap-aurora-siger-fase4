"""
Helper utility functions.
"""

from typing import List, Dict, Any
import time

def format_time(seconds: float) -> str:
    """
    Formats time in seconds to a readable string.
    """
    if seconds < 60:
        return f"{seconds:.1f} segundos"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutos"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} horas"

def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """
    Calculates basic statistics for a list of numbers.
    """
    if not data:
        return {}
    
    return {
        'mean': sum(data) / len(data),
        'minimum': min(data),
        'maximum': max(data),
        'total': sum(data),
        'count': len(data)
    }

def validate_priority(value: int) -> bool:
    """
    Validates if the priority value is within the valid range (0-10).
    """
    return 0 <= value <= 10

def validate_status(status: str) -> bool:
    """
    Validates if the status value is valid.
    """
    valid_status = ['active', 'maintenance', 'alert', 'inactive']
    return status in valid_status