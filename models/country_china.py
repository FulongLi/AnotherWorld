"""
China Country Model - Implements country-specific policies and institutions
Based on China's policies: Reform & Opening, One-Child Policy, etc.
"""
from dataclasses import dataclass, field
from typing import Dict, Optional, List
from enum import Enum
from models.country_base import CountryModel, CountryConfig
from models.world_base import BaseWorldState
from models.family_policy import FamilyPolicyEngine, FamilyPolicyState, FamilyState, FertilityPolicy


class ChinaEra(Enum):
    """6 distinct eras in China's development"""
    ESTABLISHMENT = (1949, 1957)  # 国家建立期
    TURBULENCE = (1958, 1977)  # 高度动荡期
    REFORM_EARLY = (1978, 1991)  # 改革开放早期
    URBAN_BOOM = (1992, 2007)  # 城市爆发期
    STRUCTURE_SOLIDIFY = (2008, 2019)  # 结构固化期
    NEW_UNCERTAINTY = (2020, 9999)  # 不确定新时代


@dataclass
class ChinaEraConfig:
    """Era-specific parameters"""
    era: ChinaEra
    social_mobility: float
    inequality: float
    risk_reward_ratio: float
    education_return: float
    system_shock: float = 0.0
    health_risk: float = 0.0
    asset_return: float = 0.0
    asset_entry_cost: float = 0.0
    stress_factor: float = 0.0
    system_volatility: float = 0.0
    risk_penalty: float = 0.0
    mental_health_weight: float = 1.0
    market_freedom: float = 0.5
    elite_competition: float = 0.5


class ChinaCountryModel(CountryModel):
    """China-specific country model"""
    
    def __init__(self, base_world: BaseWorldState, year: int = 1950):
        config = CountryConfig(
            country_name="China",
            base_year=1949,
            political_system="authoritarian",
            economic_system="mixed",  # Market socialism
            social_mobility_base=0.6,  # Moderate base mobility
            inequality_trend=0.3  # Increasing inequality trend
        )
        super().__init__(config, base_world)
        
        self.current_era = self._get_era_for_year(year)
        self.era_config = self._get_era_config(self.current_era)
        
        # Window mechanism (一次性窗口)
        self.window_open: bool = False
        self.window_missed: bool = False
        self.window_era: Optional[ChinaEra] = None
        self.mobility_multiplier: float = 1.0
        
        # Family policy state
        self.family_policy_state: Optional[FamilyPolicyState] = None
        self._initialize_family_policy(year)
        
        self._check_window_status()
    
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
    
    def get_era_for_year(self, year: int) -> str:
        """Get era name as string"""
        era = self._get_era_for_year(year)
        return era.name
    
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
    
    def get_era_config(self, era: str) -> Dict:
        """Get era configuration as dict"""
        era_enum = ChinaEra[era]
        config = self._get_era_config(era_enum)
        return {
            'social_mobility': config.social_mobility,
            'inequality': config.inequality,
            'risk_reward_ratio': config.risk_reward_ratio,
            'education_return': config.education_return,
            'system_shock': config.system_shock,
            'health_risk': config.health_risk,
            'asset_return': config.asset_return,
            'asset_entry_cost': config.asset_entry_cost,
            'stress_factor': config.stress_factor,
            'system_volatility': config.system_volatility,
            'risk_penalty': config.risk_penalty,
            'mental_health_weight': config.mental_health_weight,
            'market_freedom': config.market_freedom,
            'elite_competition': config.elite_competition
        }
    
    def _check_window_status(self):
        """Check if we're in a window period or missed it"""
        if self.current_era == ChinaEra.REFORM_EARLY:
            self.window_open = True
            self.window_era = ChinaEra.REFORM_EARLY
        elif self.current_era == ChinaEra.URBAN_BOOM:
            self.window_open = True
            self.window_era = ChinaEra.URBAN_BOOM
        elif self.current_era in [ChinaEra.STRUCTURE_SOLIDIFY, ChinaEra.NEW_UNCERTAINTY]:
            if not self.window_missed and self.window_era in [ChinaEra.REFORM_EARLY, ChinaEra.URBAN_BOOM]:
                self.window_missed = True
                self.mobility_multiplier *= 0.3
    
    def _initialize_family_policy(self, year: int):
        """Initialize family policy state"""
        policy = FamilyPolicyEngine.get_policy_for_year(year)
        is_urban = True  # Major cities are urban
        self.family_policy_state = FamilyPolicyEngine.get_policy_config(policy, is_urban)
    
    def update(self, year: int):
        """Update China country model"""
        super().update(year)
        
        # Check era transition
        new_era = self._get_era_for_year(year)
        if new_era != self.current_era:
            self.current_era = new_era
            self.era_config = self._get_era_config(self.current_era)
            self._check_window_status()
        
        # Update family policy if needed
        new_policy = FamilyPolicyEngine.get_policy_for_year(year)
        if self.family_policy_state is None or self.family_policy_state.policy != new_policy:
            is_urban = True
            self.family_policy_state = FamilyPolicyEngine.get_policy_config(new_policy, is_urban)
    
    def apply_country_modifiers(self, person_state, action_type: str) -> float:
        """Apply China-specific modifiers to actions"""
        modifier = 1.0
        
        # Era-specific modifiers
        if action_type == "study":
            modifier *= self.era_config.education_return
        elif action_type == "risk":
            modifier *= self.era_config.risk_reward_ratio
            if self.current_era == ChinaEra.NEW_UNCERTAINTY:
                modifier *= (1 - self.era_config.risk_penalty)
        
        # Window effect
        if self.window_missed and action_type in ["risk", "move"]:
            modifier *= self.mobility_multiplier
        
        return modifier
    
    def get_effective_social_mobility(self) -> float:
        """Get effective social mobility with window effect"""
        base = super().get_effective_social_mobility()
        era_mobility = self.era_config.social_mobility
        
        # Combine base world mobility with era-specific mobility
        combined = (base + era_mobility) / 2
        
        # Apply window effect
        if self.window_missed:
            combined *= self.mobility_multiplier
        
        return max(0.0, min(1.0, combined))
    
    def get_education_return(self) -> float:
        """Get education return with era modifier"""
        return self.era_config.education_return
    
    def get_risk_reward_ratio(self) -> float:
        """Get risk/reward ratio"""
        base = self.era_config.risk_reward_ratio
        if self.current_era == ChinaEra.NEW_UNCERTAINTY:
            base *= (1 - self.era_config.risk_penalty)
        return base
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'country': 'China',
            'era': self.current_era.name,
            'window_open': self.window_open,
            'window_missed': self.window_missed,
            'mobility_multiplier': self.mobility_multiplier,
            'social_mobility': self.get_effective_social_mobility(),
            'inequality': self.get_effective_inequality(),
            'education_return': self.get_education_return(),
            'risk_reward_ratio': self.get_risk_reward_ratio(),
            'family_policy': self.family_policy_state.policy.name if self.family_policy_state else None
        }

