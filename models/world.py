"""
World state model - Global environment that evolves over time
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
        
        # Social mobility fluctuates
        mobility_change = random.gauss(0, 0.02)
        self.social_mobility = max(0.0, min(1.0, self.social_mobility + mobility_change))
        
        # Inequality can increase or decrease
        inequality_change = random.gauss(0, 0.01)
        self.inequality = max(0.0, min(1.0, self.inequality + inequality_change))
        
        # Conflict risk can spike
        if random.random() < 0.05:  # 5% chance of conflict event
            self.conflict_risk = min(1.0, self.conflict_risk + random.uniform(0.1, 0.3))
        else:
            self.conflict_risk = max(0.0, self.conflict_risk - random.uniform(0, 0.02))
        
        self.year += 1

