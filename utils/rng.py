"""
Random number generation utilities with seed support
"""
import random
import numpy as np
from typing import Optional


class RNG:
    """Centralized random number generator with seed support"""
    _instance: Optional['RNG'] = None
    _seed: Optional[int] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def set_seed(self, seed: int):
        """Set random seed for reproducibility"""
        self._seed = seed
        random.seed(seed)
        np.random.seed(seed)
    
    def normal(self, mean: float = 1.0, std: float = 0.15) -> float:
        """Generate normal distribution with mean and std"""
        return np.random.normal(mean, std)
    
    def uniform(self, low: float, high: float) -> float:
        """Generate uniform distribution"""
        return random.uniform(low, high)
    
    def random(self) -> float:
        """Generate random float 0-1"""
        return random.random()
    
    def choice(self, choices):
        """Random choice from list"""
        return random.choice(choices)
    
    def gauss(self, mu: float, sigma: float) -> float:
        """Generate gaussian distribution"""
        return random.gauss(mu, sigma)


# Global RNG instance
rng = RNG()

