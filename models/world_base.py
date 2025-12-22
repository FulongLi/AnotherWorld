"""
Base World Model - Universal Economic Laws
Underlying logic layer: Pareto Principle, Kondratiev Cycles, etc.
"""
from dataclasses import dataclass
from typing import Optional
import math
import random


@dataclass
class BaseWorldState:
    """Base world state with universal economic laws"""
    year: int
    
    # Kondratiev Cycle (康波周期) - Long-term economic waves (~50-60 years)
    kondratiev_phase: float  # 0-1: Position in long wave cycle
    kondratiev_cycle_length: int = 60  # Years per cycle
    
    # Pareto Principle (二八定律) - 80/20 rule
    PARETO_ELITE_THRESHOLD: float = 0.8  # Top 20% of population
    PARETO_WEALTH_SHARE: float = 0.8  # 80% of wealth
    PARETO_OPPORTUNITY_SHARE: float = 0.8  # 80% of opportunities
    
    # Economic fundamentals
    economic_cycle: float = 0.0  # -1 to 1: Short-term economic cycle
    tech_level: float = 0.5  # 0-1: Technological advancement
    inequality: float = 0.5  # 0-1: Economic inequality
    social_mobility: float = 0.5  # 0-1: Social mobility
    
    def __init__(self, year: int, base_year: int = 1950):
        self.year = year
        self.base_year = base_year
        self._initialize_kondratiev_cycle()
    
    def _initialize_kondratiev_cycle(self):
        """Initialize Kondratiev cycle position"""
        years_from_base = self.year - self.base_year
        # Calculate phase in cycle (0-1)
        self.kondratiev_phase = (years_from_base % self.kondratiev_cycle_length) / self.kondratiev_cycle_length
    
    def update(self, base_year: int = None):
        """Update base world state"""
        if base_year:
            self.base_year = base_year
        
        self.year += 1
        
        # Update Kondratiev cycle
        years_from_base = self.year - self.base_year
        self.kondratiev_phase = (years_from_base % self.kondratiev_cycle_length) / self.kondratiev_cycle_length
        
        # Short-term economic cycle (10-year cycle)
        cycle_period = 10
        years_passed = self.year - self.base_year
        self.economic_cycle = math.sin(years_passed / cycle_period * 2 * math.pi) * 0.8
        self.economic_cycle += random.gauss(0, 0.1)
        self.economic_cycle = max(-1.0, min(1.0, self.economic_cycle))
        
        # Technology generally increases
        tech_growth = random.gauss(0.01, 0.005)
        self.tech_level = max(0.0, min(1.0, self.tech_level + tech_growth))
        
        # Inequality tends to increase (Pareto reinforcement)
        inequality_growth = self.tech_level * 0.001
        inequality_change = random.gauss(inequality_growth, 0.01)
        self.inequality = max(0.0, min(1.0, self.inequality + inequality_change))
        
        # Social mobility inversely related to inequality
        mobility_change = random.gauss(0, 0.02)
        mobility_penalty = self.inequality * 0.3
        self.social_mobility = max(0.0, min(1.0, self.social_mobility + mobility_change - mobility_penalty))
    
    def get_kondratiev_effect(self) -> float:
        """
        Get Kondratiev cycle effect
        Returns multiplier based on cycle phase:
        - 0.0-0.25: Recovery (1.0-1.2x)
        - 0.25-0.5: Expansion (1.2-1.5x)
        - 0.5-0.75: Stagnation (0.8-1.0x)
        - 0.75-1.0: Recession (0.5-0.8x)
        """
        if self.kondratiev_phase < 0.25:
            # Recovery phase
            return 1.0 + (self.kondratiev_phase / 0.25) * 0.2
        elif self.kondratiev_phase < 0.5:
            # Expansion phase
            return 1.2 + ((self.kondratiev_phase - 0.25) / 0.25) * 0.3
        elif self.kondratiev_phase < 0.75:
            # Stagnation phase
            return 1.0 - ((self.kondratiev_phase - 0.5) / 0.25) * 0.2
        else:
            # Recession phase
            return 0.8 - ((self.kondratiev_phase - 0.75) / 0.25) * 0.3
    
    def is_in_elite_percentile(self, person_score: float) -> bool:
        """Determine if person is in top 20% (elite)"""
        return person_score >= self.PARETO_ELITE_THRESHOLD
    
    def get_wealth_multiplier(self, person_score: float) -> float:
        """
        Get wealth accumulation multiplier based on Pareto Principle
        Top 20% get 4x multiplier (80% of wealth / 20% of people = 4x)
        """
        if self.is_in_elite_percentile(person_score):
            return 4.0 * (1 + self.inequality * 0.5)
        else:
            return 0.25 * (1 - self.inequality * 0.3)
    
    def get_opportunity_multiplier(self, person_score: float) -> float:
        """Get opportunity access multiplier based on Pareto Principle"""
        if self.is_in_elite_percentile(person_score):
            return 4.0
        else:
            return 0.25
    
    def get_tech_benefit_multiplier(self, person_score: float) -> float:
        """Get technology benefit multiplier based on Pareto Principle"""
        if self.is_in_elite_percentile(person_score):
            return 1.0 + self.tech_level * 0.5
        else:
            return 0.3 + self.tech_level * 0.2
    
    def calculate_person_score(
        self,
        education: float,
        skill_depth: float,
        social_capital: float,
        wealth: float,
        birth_family_class: float
    ) -> float:
        """Calculate person's overall score to determine elite status"""
        import math
        normalized_wealth = min(1.0, math.log10(max(1, wealth / 1000) + 1) / 3.0)
        
        birth_weight = 0.2 + self.inequality * 0.3
        merit_weight = 1.0 - birth_weight
        
        score = (
            birth_family_class * birth_weight +
            (education * 0.3 + skill_depth * 0.4 + social_capital * 0.2 + normalized_wealth * 0.1) * merit_weight
        )
        
        if self.social_mobility > 0.5:
            score = max(score, (education * 0.3 + skill_depth * 0.4 + social_capital * 0.2) * self.social_mobility)
        
        return min(1.0, max(0.0, score))
    
    def get_social_mobility_chance(self, person_score: float) -> float:
        """Get chance of significant social mobility (only 20% can achieve)"""
        if person_score < 0.3:
            base_chance = self.social_mobility * 0.2
        elif person_score < 0.6:
            base_chance = self.social_mobility * 0.1
        else:
            base_chance = 0.05
        
        if person_score >= self.PARETO_ELITE_THRESHOLD:
            return 0.8
        else:
            return base_chance

