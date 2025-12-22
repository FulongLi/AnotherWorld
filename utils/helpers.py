"""
Helper utility functions
"""
from typing import Any, Dict
import json
from datetime import datetime


def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))


def apply_noise(value: float, noise_factor: float = 0.15) -> float:
    """Apply random noise to a value"""
    from .rng import rng
    return value * rng.normal(1.0, noise_factor)


def save_json(data: Dict[str, Any], filepath: str):
    """Save data to JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(filepath: str) -> Dict[str, Any]:
    """Load data from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_output_filename(prefix: str = "run") -> str:
    """Generate output filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"output/{prefix}_{timestamp}.json"

