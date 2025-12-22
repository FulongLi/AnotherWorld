"""
Person data models - Immutable birth profile and mutable state
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class BirthProfile:
    """Immutable birth parameters"""
    birth_year: int
    region: str
    family_class: float  # 0-1: Economic class
    parents_education: float  # 0-1: Parental education level
    family_stability: float  # 0-1: Family stability
    genetic_health: float  # 0-1: Genetic health potential
    cognitive_potential: float  # 0-1: Cognitive potential


@dataclass
class Personality:
    """Slow-changing personality traits"""
    openness: float  # 0-1: Openness to experience
    conscientiousness: float  # 0-1: Conscientiousness
    risk_preference: float  # 0-1: Risk tolerance
    social_drive: float  # 0-1: Social motivation
    resilience: float  # 0-1: Resilience to stress


@dataclass
class PersonState:
    """Mutable individual state"""
    # Basic attributes
    age: int = 0
    health: float = 1.0  # 0-1
    mental_health: float = 0.7  # 0-1
    energy: float = 0.8  # 0-1
    stress: float = 0.2  # 0-1
    
    # Education & Skills
    education_level: float = 0.0  # 0-1
    skill_depth: float = 0.0  # 0-1: Specialization depth
    skill_width: float = 0.0  # 0-1: Skill breadth
    learning_rate: float = 0.5  # 0-1: Learning ability
    
    # Economic
    income: float = 0.0
    wealth: float = 0.0
    occupation: Optional[str] = None
    employment_stability: float = 0.0  # 0-1
    
    # Social
    social_capital: float = 0.3  # 0-1
    loneliness: float = 0.3  # 0-1
    
    # Life events
    life_events: list = field(default_factory=list)
    
    def clamp_values(self):
        """Ensure all values stay within valid ranges"""
        self.health = max(0.0, min(1.0, self.health))
        self.mental_health = max(0.0, min(1.0, self.mental_health))
        self.energy = max(0.0, min(1.0, self.energy))
        self.stress = max(0.0, min(1.0, self.stress))
        self.education_level = max(0.0, min(1.0, self.education_level))
        self.skill_depth = max(0.0, min(1.0, self.skill_depth))
        self.skill_width = max(0.0, min(1.0, self.skill_width))
        self.learning_rate = max(0.0, min(1.0, self.learning_rate))
        self.employment_stability = max(0.0, min(1.0, self.employment_stability))
        self.social_capital = max(0.0, min(1.0, self.social_capital))
        self.loneliness = max(0.0, min(1.0, self.loneliness))

