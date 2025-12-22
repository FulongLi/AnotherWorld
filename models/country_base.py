"""
Country Model Base - National-level policies and institutions
Country models inherit from this and implement country-specific logic
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, List
from models.world_base import BaseWorldState


@dataclass
class CountryConfig:
    """Country-specific configuration"""
    country_name: str
    base_year: int
    political_system: str  # e.g., "democracy", "authoritarian", "mixed"
    economic_system: str  # e.g., "market", "planned", "mixed"
    social_mobility_base: float  # Base social mobility
    inequality_trend: float  # Inequality trend (-1 to 1)


class CountryModel(ABC):
    """Base class for country models"""
    
    def __init__(self, config: CountryConfig, base_world: BaseWorldState):
        self.config = config
        self.base_world = base_world
        self.policies: Dict[str, any] = {}
        self.eras: List[Dict] = []
    
    @abstractmethod
    def get_era_for_year(self, year: int) -> str:
        """Get current era name for given year"""
        pass
    
    @abstractmethod
    def get_era_config(self, era: str) -> Dict:
        """Get configuration for specific era"""
        pass
    
    @abstractmethod
    def apply_country_modifiers(self, person_state, action_type: str) -> float:
        """Apply country-specific modifiers to actions"""
        pass
    
    def update(self, year: int):
        """Update country state"""
        self.base_world.update(self.config.base_year)
        # Country-specific updates can be added here
    
    def get_effective_social_mobility(self) -> float:
        """Get effective social mobility (base world + country modifiers)"""
        base = self.base_world.social_mobility
        # Country-specific adjustments
        return max(0.0, min(1.0, base * self.config.social_mobility_base))
    
    def get_effective_inequality(self) -> float:
        """Get effective inequality (base world + country trend)"""
        base = self.base_world.inequality
        # Apply country trend
        return max(0.0, min(1.0, base + self.config.inequality_trend * 0.1))

