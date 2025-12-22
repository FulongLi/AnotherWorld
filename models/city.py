"""
City Model - Cities within country framework
Cities are affected by country policies and show different development patterns
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict
from models.country_base import CountryModel


class CityTier(Enum):
    """City tier classification"""
    TIER1 = "tier1"  # First-tier cities
    TIER2 = "tier2"  # Second-tier cities
    TIER3 = "tier3"  # Third-tier cities


@dataclass
class CityConfig:
    """City-specific configuration"""
    city_name: str
    country: str
    tier: CityTier
    # Economic characteristics
    income_ceiling: str  # "low", "medium", "high"
    living_cost: str  # "low", "medium", "high", "very_high"
    # Policy characteristics
    policy_bonus: float  # Policy support level (0-1)
    market_freedom: float  # Market freedom relative to country base (0-1)
    # Social characteristics
    elite_competition: float  # Elite competition intensity (0-1)
    mobility_threshold: str  # "low", "medium", "high"
    # Risk characteristics
    risk_reward_ratio: float  # Risk/reward ratio multiplier
    startup_success_rate: str  # "low", "medium", "high", "high_variance"
    age_penalty_age: int  # Age when age penalty starts
    # Stability
    stability_bonus: float  # Stability bonus (0-1)
    elite_path_probability: float  # Probability of elite path (0-1)


class City:
    """City model within country framework"""
    
    def __init__(self, config: CityConfig, country_model: CountryModel):
        self.config = config
        self.country_model = country_model
    
    def get_city_modifier_for_action(self, action_type: str) -> float:
        """Get city-specific modifier for different actions"""
        modifiers = {
            "study": 1.0 + (self.config.policy_bonus * 0.5 if self.config.policy_bonus > 0.3 else 0),
            "work": 1.0 + (self.config.policy_bonus * 0.3),
            "risk": self.config.risk_reward_ratio,
            "relation": 1.0 + self.config.stability_bonus
        }
        return modifiers.get(action_type, 1.0)
    
    def get_income_multiplier(self) -> float:
        """Get income multiplier based on city tier"""
        multipliers = {
            "low": 0.7,
            "medium": 1.0,
            "high": 1.5
        }
        return multipliers.get(self.config.income_ceiling, 1.0)
    
    def get_living_cost_multiplier(self) -> float:
        """Get living cost multiplier"""
        multipliers = {
            "low": 0.5,
            "medium": 1.0,
            "high": 2.0,
            "very_high": 3.0
        }
        return multipliers.get(self.config.living_cost, 1.0)
    
    def get_mobility_modifier(self) -> float:
        """Get social mobility modifier"""
        modifiers = {
            "low": 1.2,  # Easier to move up
            "medium": 1.0,
            "high": 0.8  # Harder to move up
        }
        return modifiers.get(self.config.mobility_threshold, 1.0)
    
    def get_stress_modifier(self) -> float:
        """Get stress modifier from living cost"""
        cost_stress = {
            "low": 0.0,
            "medium": 0.1,
            "high": 0.2,
            "very_high": 0.3
        }
        return cost_stress.get(self.config.living_cost, 0.1)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'city_name': self.config.city_name,
            'country': self.config.country,
            'tier': self.config.tier.value,
            'income_ceiling': self.config.income_ceiling,
            'living_cost': self.config.living_cost,
            'mobility_threshold': self.config.mobility_threshold,
            'risk_reward_ratio': self.config.risk_reward_ratio
        }


# Predefined Chinese cities (within China country model)
def create_china_cities() -> Dict[str, CityConfig]:
    """Create predefined Chinese city configurations"""
    return {
        "beijing": CityConfig(
            city_name="Beijing",
            country="China",
            tier=CityTier.TIER1,
            income_ceiling="high",
            living_cost="very_high",
            policy_bonus=0.4,
            market_freedom=-0.2,  # Relative to country base
            elite_competition=0.6,
            mobility_threshold="high",
            risk_reward_ratio=0.6,
            startup_success_rate="low",
            age_penalty_age=999,
            stability_bonus=0.0,
            elite_path_probability=0.5
        ),
        "shanghai": CityConfig(
            city_name="Shanghai",
            country="China",
            tier=CityTier.TIER1,
            income_ceiling="high",
            living_cost="very_high",
            policy_bonus=0.2,
            market_freedom=0.1,
            elite_competition=0.7,
            mobility_threshold="high",
            risk_reward_ratio=0.8,
            startup_success_rate="medium",
            age_penalty_age=999,
            stability_bonus=0.0,
            elite_path_probability=0.6
        ),
        "shenzhen": CityConfig(
            city_name="Shenzhen",
            country="China",
            tier=CityTier.TIER1,
            income_ceiling="high",
            living_cost="high",
            policy_bonus=0.1,
            market_freedom=0.3,
            elite_competition=0.4,
            mobility_threshold="low",  # More accessible
            risk_reward_ratio=1.8,
            startup_success_rate="high_variance",
            age_penalty_age=35,
            stability_bonus=0.0,
            elite_path_probability=0.4
        ),
        "guangzhou": CityConfig(
            city_name="Guangzhou",
            country="China",
            tier=CityTier.TIER1,
            income_ceiling="medium",
            living_cost="medium",
            policy_bonus=0.1,
            market_freedom=0.2,
            elite_competition=0.5,
            mobility_threshold="medium",
            risk_reward_ratio=1.0,
            startup_success_rate="medium",
            age_penalty_age=999,
            stability_bonus=0.3,
            elite_path_probability=0.3
        )
    }

