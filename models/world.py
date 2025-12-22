"""
World state model - Global environment that evolves over time
Incorporates Pareto Principle (80/20 rule)
"""
from dataclasses import dataclass
import math
import random


@dataclass
class WorldState:
    """Global world state that affects individual lives"""
    year: int
    economic_cycle: float  # -1 to 1: Economic cycle position
    tech_level: float  # 0-1: Technological advancement
    social_mobility: float  # 0-1: Social mobility
    inequality: float  # 0-1: Economic inequality
    conflict_risk: float  # 0-1: Risk of conflict/war
    
    # Pareto Principle constants (80/20 rule)
    PARETO_ELITE_THRESHOLD: float = 0.8  # Top 20% of population
    PARETO_WEALTH_SHARE: float = 0.8  # 80% of wealth
    PARETO_OPPORTUNITY_SHARE: float = 0.8  # 80% of opportunities
    
    def update(self, base_year: int):
        """Update world state based on time"""
        years_passed = self.year - base_year
        
        # Economic cycle (sine wave with noise)
        cycle_period = 10
        self.economic_cycle = math.sin(years_passed / cycle_period * 2 * math.pi) * 0.8
        self.economic_cycle += random.gauss(0, 0.1)
        self.economic_cycle = max(-1.0, min(1.0, self.economic_cycle))
        
        # Technology generally increases
        tech_growth = random.gauss(0.01, 0.005)
        self.tech_level = max(0.0, min(1.0, self.tech_level + tech_growth))
        
        # Social mobility fluctuates (but constrained by Pareto Principle)
        # Higher inequality = lower mobility (harder to break into top 20%)
        mobility_change = random.gauss(0, 0.02)
        # Mobility inversely related to inequality (Pareto effect)
        mobility_penalty = self.inequality * 0.3
        self.social_mobility = max(0.0, min(1.0, self.social_mobility + mobility_change - mobility_penalty))
        
        # Inequality tends to increase over time (Pareto Principle reinforcement)
        # Technology growth can increase inequality (benefits elite more)
        inequality_growth = self.tech_level * 0.001  # Tech benefits elite disproportionately
        inequality_change = random.gauss(inequality_growth, 0.01)
        self.inequality = max(0.0, min(1.0, self.inequality + inequality_change))
        
        # Conflict risk can spike
        if random.random() < 0.05:  # 5% chance of conflict event
            self.conflict_risk = min(1.0, self.conflict_risk + random.uniform(0.1, 0.3))
        else:
            self.conflict_risk = max(0.0, self.conflict_risk - random.uniform(0, 0.02))
        
        self.year += 1
    
    def is_in_elite_percentile(self, person_score: float) -> bool:
        """
        Determine if person is in top 20% (elite) based on combined score
        Uses Pareto Principle: top 20% get 80% of benefits
        """
        # Elite threshold is at 80th percentile
        return person_score >= self.PARETO_ELITE_THRESHOLD
    
    def get_wealth_multiplier(self, person_score: float) -> float:
        """
        Get wealth accumulation multiplier based on Pareto Principle
        Top 20% get 4x multiplier (80% of wealth / 20% of people = 4x)
        Bottom 80% share remaining 20% of wealth
        """
        if self.is_in_elite_percentile(person_score):
            # Elite: 80% of wealth / 20% of people = 4x base rate
            return 4.0 * (1 + self.inequality * 0.5)  # Inequality amplifies elite advantage
        else:
            # Non-elite: 20% of wealth / 80% of people = 0.25x base rate
            return 0.25 * (1 - self.inequality * 0.3)  # Inequality reduces non-elite share
    
    def get_opportunity_multiplier(self, person_score: float) -> float:
        """
        Get opportunity access multiplier based on Pareto Principle
        Top 20% get 80% of opportunities
        """
        if self.is_in_elite_percentile(person_score):
            # Elite: 80% of opportunities / 20% of people = 4x
            return 4.0
        else:
            # Non-elite: 20% of opportunities / 80% of people = 0.25x
            return 0.25
    
    def get_tech_benefit_multiplier(self, person_score: float) -> float:
        """
        Get technology benefit multiplier based on Pareto Principle
        Top 20% capture 80% of technology benefits
        """
        if self.is_in_elite_percentile(person_score):
            # Elite: full tech benefits + bonus
            return 1.0 + self.tech_level * 0.5
        else:
            # Non-elite: reduced tech benefits
            return 0.3 + self.tech_level * 0.2
    
    def calculate_person_score(
        self,
        education: float,
        skill_depth: float,
        social_capital: float,
        wealth: float,
        birth_family_class: float
    ) -> float:
        """
        Calculate person's overall score to determine elite status
        Combines multiple factors weighted by current world state
        """
        # Normalize wealth (log scale to prevent extreme values)
        import math
        normalized_wealth = min(1.0, math.log10(max(1, wealth / 1000) + 1) / 3.0)
        
        # Weighted combination
        # In high inequality worlds, birth class matters more
        birth_weight = 0.2 + self.inequality * 0.3
        merit_weight = 1.0 - birth_weight
        
        score = (
            birth_family_class * birth_weight +
            (education * 0.3 + skill_depth * 0.4 + social_capital * 0.2 + normalized_wealth * 0.1) * merit_weight
        )
        
        # Social mobility affects how much merit can overcome birth
        if self.social_mobility > 0.5:
            # High mobility: merit can overcome birth disadvantage
            score = max(score, (education * 0.3 + skill_depth * 0.4 + social_capital * 0.2) * self.social_mobility)
        
        return min(1.0, max(0.0, score))
    
    def get_social_mobility_chance(self, person_score: float) -> float:
        """
        Get chance of significant social mobility based on Pareto Principle
        Only 20% of people can achieve significant upward mobility
        """
        # Base chance depends on current score and mobility level
        if person_score < 0.3:  # Starting from bottom
            # Low starting position: mobility chance depends on world mobility
            base_chance = self.social_mobility * 0.2  # Max 20% can move up significantly
        elif person_score < 0.6:  # Middle class
            # Middle: moderate chance
            base_chance = self.social_mobility * 0.1
        else:  # Already high
            # Already elite: maintain or slight improvement
            base_chance = 0.05
        
        # Pareto constraint: only 20% can be in elite
        if person_score >= self.PARETO_ELITE_THRESHOLD:
            # Already elite: high chance to maintain
            return 0.8
        else:
            # Not elite: chance to break in (limited by Pareto)
            return base_chance

