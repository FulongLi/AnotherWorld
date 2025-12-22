"""
China World Model - Based on major city development since 1949
Engineering modeling perspective: structured conclusions for World Model
"""
from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum
import math
import random
from models.family_policy import (
    FamilyPolicyEngine, FamilyPolicyState, FamilyState, FertilityPolicy
)


class ChinaEra(Enum):
    """6 distinct eras in China's development"""
    ESTABLISHMENT = (1949, 1957)  # 国家建立期
    TURBULENCE = (1958, 1977)  # 高度动荡期
    REFORM_EARLY = (1978, 1991)  # 改革开放早期
    URBAN_BOOM = (1992, 2007)  # 城市爆发期
    STRUCTURE_SOLIDIFY = (2008, 2019)  # 结构固化期
    NEW_UNCERTAINTY = (2020, 9999)  # 不确定新时代


class ChinaCity(Enum):
    """4 representative city tiers"""
    BEIJING = "beijing"  # 政治/资源中心
    SHANGHAI = "shanghai"  # 金融/规则中心
    SHENZHEN = "shenzhen"  # 技术/冒险中心
    GUANGZHOU = "guangzhou"  # 商业/中庸型


@dataclass
class ChinaEraConfig:
    """Era-specific parameters"""
    era: ChinaEra
    social_mobility: float
    inequality: float
    risk_reward_ratio: float
    education_return: float
    system_shock: float = 0.0  # System disruption level
    health_risk: float = 0.0
    asset_return: float = 0.0
    asset_entry_cost: float = 0.0
    stress_factor: float = 0.0
    system_volatility: float = 0.0
    risk_penalty: float = 0.0
    mental_health_weight: float = 1.0
    market_freedom: float = 0.5
    elite_competition: float = 0.5


@dataclass
class ChinaCityConfig:
    """City-specific parameters"""
    city: ChinaCity
    policy_bonus: float = 0.0
    market_freedom: float = 0.5
    elite_competition: float = 0.5
    income_ceiling: str = "medium"  # low, medium, high
    living_cost: str = "medium"  # low, medium, high, very_high
    mobility_threshold: str = "medium"  # low, medium, high
    risk_reward_ratio: float = 1.0
    startup_success_rate: str = "medium"  # low, medium, high, high_variance
    age_penalty_age: int = 999  # Age when penalty starts
    stability_bonus: float = 0.0
    elite_path_probability: float = 0.5


@dataclass
class ChinaWorldState:
    """China-specific world state"""
    year: int
    era: ChinaEra
    city: ChinaCity
    era_config: ChinaEraConfig = field(init=False)
    city_config: ChinaCityConfig = field(init=False)
    
    # Window mechanism (一次性窗口)
    window_open: bool = False
    window_missed: bool = False
    window_era: Optional[ChinaEra] = None
    
    # Intergenerational break (代际断裂)
    parent_assets: float = 0.0  # Parent generation assets
    property_owned: bool = False  # Whether person owns property
    property_value: float = 0.0
    
    # Family policy state
    family_policy_state: Optional[FamilyPolicyState] = None
    family_state: Optional[FamilyState] = None
    
    # Accumulated state
    mobility_multiplier: float = 1.0  # Permanent mobility modifier
    competition_intensity: float = 0.5  # Competition intensity (0-1)
    
    def __post_init__(self):
        """Initialize era and city configs"""
        self.era = self._get_era_for_year(self.year)
        self.era_config = self._get_era_config(self.era)
        self.city_config = self._get_city_config(self.city)
        self._check_window_status()
        # Family policy will be initialized when family structure is set
        # (needs birth_year which may not be available here)
    
    def _get_era_for_year(self, year: int) -> ChinaEra:
        """Determine era based on year"""
        if year < 1958:
            return ChinaEra.ESTABLISHMENT
        elif year < 1978:
            return ChinaEra.TURBULENCE
        elif year < 1992:
            return ChinaEra.REFORM_EARLY
        elif year < 2008:
            return ChinaEra.URBAN_BOOM
        elif year < 2020:
            return ChinaEra.STRUCTURE_SOLIDIFY
        else:
            return ChinaEra.NEW_UNCERTAINTY
    
    def _get_era_config(self, era: ChinaEra) -> ChinaEraConfig:
        """Get configuration for specific era"""
        configs = {
            ChinaEra.ESTABLISHMENT: ChinaEraConfig(
                era=era,
                social_mobility=0.15,
                inequality=0.10,
                risk_reward_ratio=0.2,
                education_return=0.3,
                market_freedom=0.2,
                elite_competition=0.3
            ),
            ChinaEra.TURBULENCE: ChinaEraConfig(
                era=era,
                social_mobility=0.05,
                inequality=0.15,
                risk_reward_ratio=0.1,
                education_return=0.1,
                system_shock=0.9,
                health_risk=0.8,
                market_freedom=0.1,
                elite_competition=0.2
            ),
            ChinaEra.REFORM_EARLY: ChinaEraConfig(
                era=era,
                social_mobility=0.45,
                inequality=0.4,
                risk_reward_ratio=1.5,
                education_return=0.8,
                market_freedom=0.6,
                elite_competition=0.4
            ),
            ChinaEra.URBAN_BOOM: ChinaEraConfig(
                era=era,
                social_mobility=0.7,
                inequality=0.6,
                risk_reward_ratio=1.2,
                education_return=1.2,
                asset_return=1.8,
                market_freedom=0.8,
                elite_competition=0.6
            ),
            ChinaEra.STRUCTURE_SOLIDIFY: ChinaEraConfig(
                era=era,
                social_mobility=0.35,
                inequality=0.7,
                risk_reward_ratio=0.8,
                education_return=0.9,
                asset_entry_cost=0.9,
                stress_factor=0.7,
                market_freedom=0.7,
                elite_competition=0.8
            ),
            ChinaEra.NEW_UNCERTAINTY: ChinaEraConfig(
                era=era,
                social_mobility=0.25,
                inequality=0.75,
                risk_reward_ratio=0.6,
                education_return=0.8,
                system_volatility=0.8,
                risk_penalty=0.6,
                mental_health_weight=1.2,
                market_freedom=0.6,
                elite_competition=0.9
            )
        }
        return configs[era]
    
    def _get_city_config(self, city: ChinaCity) -> ChinaCityConfig:
        """Get configuration for specific city"""
        configs = {
            ChinaCity.BEIJING: ChinaCityConfig(
                city=city,
                policy_bonus=0.4,
                market_freedom=-0.2,  # Relative to base
                elite_competition=0.6,
                income_ceiling="high",
                living_cost="very_high",
                mobility_threshold="high",
                risk_reward_ratio=0.6,  # Lower for risk-taking
                startup_success_rate="low"
            ),
            ChinaCity.SHANGHAI: ChinaCityConfig(
                city=city,
                policy_bonus=0.2,
                market_freedom=0.1,
                elite_competition=0.7,
                income_ceiling="high",
                living_cost="very_high",
                mobility_threshold="high",
                risk_reward_ratio=0.8,
                startup_success_rate="medium"
            ),
            ChinaCity.SHENZHEN: ChinaCityConfig(
                city=city,
                policy_bonus=0.1,
                market_freedom=0.3,
                elite_competition=0.4,
                income_ceiling="high",
                living_cost="high",
                mobility_threshold="low",  # More accessible
                risk_reward_ratio=1.8,  # High risk/reward
                startup_success_rate="high_variance",
                age_penalty_age=35
            ),
            ChinaCity.GUANGZHOU: ChinaCityConfig(
                city=city,
                policy_bonus=0.1,
                market_freedom=0.2,
                elite_competition=0.5,
                income_ceiling="medium",
                living_cost="medium",
                mobility_threshold="medium",
                risk_reward_ratio=1.0,
                startup_success_rate="medium",
                stability_bonus=0.3,
                elite_path_probability=0.3  # Lower chance of elite path
            )
        }
        return configs[city]
    
    def _check_window_status(self):
        """Check if we're in a window period or missed it"""
        # Key window periods
        if self.era == ChinaEra.REFORM_EARLY:
            self.window_open = True
            self.window_era = ChinaEra.REFORM_EARLY
        elif self.era == ChinaEra.URBAN_BOOM:
            self.window_open = True
            self.window_era = ChinaEra.URBAN_BOOM
        elif self.era in [ChinaEra.STRUCTURE_SOLIDIFY, ChinaEra.NEW_UNCERTAINTY]:
            # Window closed, check if missed
            if not self.window_missed and self.window_era in [ChinaEra.REFORM_EARLY, ChinaEra.URBAN_BOOM]:
                self.window_missed = True
                # Permanent mobility reduction
                self.mobility_multiplier *= 0.3
    
    def _initialize_family_policy(self):
        """Initialize family policy state"""
        # Use the year that was set (should be birth_year)
        policy = FamilyPolicyEngine.get_policy_for_year(self.year)
        is_urban = True  # Assume urban for major cities
        self.family_policy_state = FamilyPolicyEngine.get_policy_config(policy, is_urban)
    
    def initialize_family_structure(self, birth_year: int, family_wealth: float, rng=None):
        """Initialize family structure based on birth year"""
        # Initialize family policy state based on birth year
        policy = FamilyPolicyEngine.get_policy_for_year(birth_year)
        is_urban = True  # Major cities are urban
        self.family_policy_state = FamilyPolicyEngine.get_policy_config(policy, is_urban)
        
        # Generate family structure
        is_urban = True  # Major cities are urban
        self.family_state = FamilyPolicyEngine.generate_family_structure(
            birth_year, family_wealth, is_urban, rng
        )
        
        # Update competition intensity
        city_tier = "tier1" if self.city in [ChinaCity.BEIJING, ChinaCity.SHANGHAI, ChinaCity.SHENZHEN] else "tier2"
        era_name = self.era.name
        self.competition_intensity = FamilyPolicyEngine.calculate_competition_intensity(
            self.family_state, city_tier, era_name
        )
    
    def update(self, base_year: int):
        """Update China world state"""
        self.year += 1
        new_era = self._get_era_for_year(self.year)
        
        # Era transition
        if new_era != self.era:
            self.era = new_era
            self.era_config = self._get_era_config(self.era)
            self._check_window_status()
    
    def get_social_mobility(self) -> float:
        """Get effective social mobility with all modifiers"""
        base_mobility = self.era_config.social_mobility
        
        # Window effect
        if self.window_missed:
            base_mobility *= self.mobility_multiplier
        
        # City modifier
        if self.city_config.mobility_threshold == "high":
            base_mobility *= 0.8  # Harder to move up
        elif self.city_config.mobility_threshold == "low":
            base_mobility *= 1.2  # Easier to move up
        
        return max(0.0, min(1.0, base_mobility))
    
    def get_education_return(self) -> float:
        """Get education return with era and city modifiers"""
        base_return = self.era_config.education_return
        
        # City modifier (Beijing/Shanghai have better education resources)
        if self.city in [ChinaCity.BEIJING, ChinaCity.SHANGHAI]:
            base_return *= 1.2
        
        return base_return
    
    def get_risk_reward_ratio(self) -> float:
        """Get risk/reward ratio combining era and city"""
        era_ratio = self.era_config.risk_reward_ratio
        city_ratio = self.city_config.risk_reward_ratio
        
        # Combine (city modifies era base)
        combined = era_ratio * (1 + city_ratio - 1.0)
        
        # System volatility penalty (new uncertainty era)
        if self.era == ChinaEra.NEW_UNCERTAINTY:
            combined *= (1 - self.era_config.risk_penalty)
        
        return combined
    
    def get_asset_return(self) -> float:
        """Get asset return (mainly property)"""
        if self.era == ChinaEra.URBAN_BOOM:
            return self.era_config.asset_return  # 1.8x during boom
        elif self.era == ChinaEra.STRUCTURE_SOLIDIFY:
            return 0.5  # Slower growth
        else:
            return 0.2  # Minimal
    
    def get_property_entry_cost(self) -> float:
        """Get property entry cost (barrier to entry)"""
        if self.era == ChinaEra.STRUCTURE_SOLIDIFY:
            return self.era_config.asset_entry_cost  # 0.9 (very high)
        elif self.era == ChinaEra.NEW_UNCERTAINTY:
            return 0.8  # Still high
        else:
            return 0.3  # Lower barrier
    
    def check_property_opportunity(self, person_wealth: float, person_age: int) -> bool:
        """Check if person can enter property market"""
        # Age window for property purchase (typically 25-40)
        if person_age < 25 or person_age > 40:
            return False
        
        # Wealth threshold (depends on era and city)
        base_threshold = 50000  # Base threshold
        
        # City cost modifier
        cost_multiplier = {
            "low": 0.5,
            "medium": 1.0,
            "high": 2.0,
            "very_high": 3.0
        }.get(self.city_config.living_cost, 1.0)
        
        threshold = base_threshold * cost_multiplier * (1 + self.get_property_entry_cost())
        
        return person_wealth >= threshold
    
    def apply_property_purchase(self, person_wealth: float) -> tuple[bool, float]:
        """Apply property purchase and return (success, remaining_wealth)"""
        if not self.check_property_opportunity(person_wealth, 30):  # Assume age 30
            return False, person_wealth
        
        # Calculate property cost
        base_cost = 100000
        cost_multiplier = {
            "low": 0.5,
            "medium": 1.0,
            "high": 2.0,
            "very_high": 3.0
        }.get(self.city_config.living_cost, 1.0)
        
        property_cost = base_cost * cost_multiplier * (1 + self.get_property_entry_cost())
        
        if person_wealth >= property_cost:
            self.property_owned = True
            self.property_value = property_cost
            remaining = person_wealth - property_cost
            return True, remaining
        
        return False, person_wealth
    
    def get_intergenerational_advantage(self) -> float:
        """Calculate advantage from parent generation (代际断裂)"""
        # Property ownership is key intergenerational transfer
        if self.property_owned:
            # Property value provides starting advantage
            advantage = min(0.3, self.property_value / 1000000)  # Cap at 0.3
        else:
            advantage = 0.0
        
        # Parent assets also matter
        advantage += min(0.2, self.parent_assets / 500000)
        
        return min(0.5, advantage)  # Cap total advantage
    
    def get_city_modifier_for_action(self, action_type: str) -> float:
        """Get city-specific modifier for different actions"""
        modifiers = {
            "study": 1.0 + (self.city_config.policy_bonus * 0.5 if self.city == ChinaCity.BEIJING else 0),
            "work": 1.0 + (self.city_config.policy_bonus * 0.3),
            "risk": self.city_config.risk_reward_ratio,
            "relation": 1.0 + self.city_config.stability_bonus
        }
        return modifiers.get(action_type, 1.0)
    
    def get_stress_modifier(self) -> float:
        """Get stress modifier based on era and city"""
        base_stress = self.era_config.stress_factor
        
        # City living cost adds stress
        cost_stress = {
            "low": 0.0,
            "medium": 0.1,
            "high": 0.2,
            "very_high": 0.3
        }.get(self.city_config.living_cost, 0.1)
        
        return base_stress + cost_stress
    
    def get_mental_health_weight(self) -> float:
        """Get mental health importance weight"""
        return self.era_config.mental_health_weight
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        result = {
            'year': self.year,
            'era': self.era.name,
            'city': self.city.value,
            'window_open': self.window_open,
            'window_missed': self.window_missed,
            'property_owned': self.property_owned,
            'property_value': self.property_value,
            'mobility_multiplier': self.mobility_multiplier,
            'social_mobility': self.get_social_mobility(),
            'inequality': self.era_config.inequality,
            'risk_reward_ratio': self.get_risk_reward_ratio(),
            'education_return': self.get_education_return(),
            'competition_intensity': self.competition_intensity
        }
        
        # Add family policy info
        if self.family_policy_state:
            result['family_policy'] = {
                'policy': self.family_policy_state.policy.name,
                'fertility_cap': self.family_policy_state.fertility_cap,
                'only_child_probability': self.family_policy_state.only_child_probability
            }
        
        # Add family state info
        if self.family_state:
            result['family_state'] = {
                'siblings': self.family_state.siblings,
                'is_only_child': self.family_state.is_only_child,
                'parental_pressure': self.family_state.parental_pressure,
                'caregiver_burden': self.family_state.caregiver_burden,
                'family_wealth_per_child': self.family_state.family_wealth_per_child
            }
        
        return result

