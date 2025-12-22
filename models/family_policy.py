"""
Family Policy Module - One-Child Policy and Demography
Models family structure, resource allocation, and intergenerational pressure
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class FertilityPolicy(Enum):
    """Fertility policy periods"""
    PRE_CONTROL = (1949, 1970)  # 自然生育期
    SOFT_CONTROL = (1971, 1978)  # "晚稀少"过渡期
    ONE_CHILD = (1979, 2015)  # 严格独生子女时代
    TWO_CHILD = (2016, 2020)  # 全面二孩
    THREE_CHILD_PLUS = (2021, 9999)  # 鼓励生育


@dataclass
class FamilyPolicyState:
    """Family policy state for a given period"""
    policy: FertilityPolicy
    fertility_cap: float  # Expected number of children allowed
    enforcement_strength: float  # 0-1: Policy enforcement intensity
    penalty_cost: float  # 0-1: Cost of exceeding policy
    only_child_probability: float  # Probability of being only child
    urban_fertility_multiplier: float = 1.0  # Urban areas often stricter


@dataclass
class FamilyState:
    """Individual's family structure state"""
    siblings: int  # Number of siblings
    is_only_child: bool
    parental_pressure: float  # 0-1: Parental expectation pressure
    intergenerational_support: float  # 0-1: Support from extended family
    caregiver_burden: float  # 0-1: Burden of caring for aging parents
    family_wealth_per_child: float  # Wealth allocated per child


class FamilyPolicyEngine:
    """Engine for family policy effects"""
    
    @staticmethod
    def get_policy_for_year(year: int) -> FertilityPolicy:
        """Determine policy period based on year"""
        if year < 1971:
            return FertilityPolicy.PRE_CONTROL
        elif year < 1979:
            return FertilityPolicy.SOFT_CONTROL
        elif year < 2016:
            return FertilityPolicy.ONE_CHILD
        elif year < 2021:
            return FertilityPolicy.TWO_CHILD
        else:
            return FertilityPolicy.THREE_CHILD_PLUS
    
    @staticmethod
    def get_policy_config(policy: FertilityPolicy, is_urban: bool = True) -> FamilyPolicyState:
        """Get policy configuration for a period"""
        configs = {
            FertilityPolicy.PRE_CONTROL: FamilyPolicyState(
                policy=policy,
                fertility_cap=4.5,
                enforcement_strength=0.0,
                penalty_cost=0.0,
                only_child_probability=0.05,
                urban_fertility_multiplier=1.0
            ),
            FertilityPolicy.SOFT_CONTROL: FamilyPolicyState(
                policy=policy,
                fertility_cap=2.8,
                enforcement_strength=0.4,
                penalty_cost=0.3,
                only_child_probability=0.25,
                urban_fertility_multiplier=0.9
            ),
            FertilityPolicy.ONE_CHILD: FamilyPolicyState(
                policy=policy,
                fertility_cap=1.1,
                enforcement_strength=0.9,
                penalty_cost=0.8,
                only_child_probability=0.75,
                urban_fertility_multiplier=0.8  # Stricter in cities
            ),
            FertilityPolicy.TWO_CHILD: FamilyPolicyState(
                policy=policy,
                fertility_cap=1.6,
                enforcement_strength=0.3,
                penalty_cost=0.2,
                only_child_probability=0.45,
                urban_fertility_multiplier=0.85  # Still lower in cities
            ),
            FertilityPolicy.THREE_CHILD_PLUS: FamilyPolicyState(
                policy=policy,
                fertility_cap=1.3,  # Policy allows more, but behavior doesn't match
                enforcement_strength=0.1,
                penalty_cost=0.0,
                only_child_probability=0.55,  # Still high due to economic constraints
                urban_fertility_multiplier=0.7  # Economic structure constrains behavior
            )
        }
        
        config = configs[policy]
        
        # Urban areas have stricter enforcement
        if is_urban:
            config.only_child_probability *= (1 + config.urban_fertility_multiplier - 1.0)
            config.only_child_probability = min(1.0, config.only_child_probability)
        
        return config
    
    @staticmethod
    def generate_family_structure(
        birth_year: int,
        family_wealth: float,
        is_urban: bool = True,
        rng=None
    ) -> FamilyState:
        """Generate family structure based on policy and random factors"""
        import random
        if rng is None:
            rng = random
        
        policy = FamilyPolicyEngine.get_policy_for_year(birth_year)
        policy_config = FamilyPolicyEngine.get_policy_config(policy, is_urban)
        
        # Determine number of siblings based on policy
        # Use fertility_cap as expected value, add randomness
        expected_children = policy_config.fertility_cap
        
        # Add enforcement effect (stronger enforcement = closer to cap)
        if policy_config.enforcement_strength > 0.5:
            # Strong enforcement: most families at or below cap
            if rng.random() < policy_config.only_child_probability:
                siblings = 0  # Only child
            else:
                # 1-2 children mostly
                siblings = rng.choice([0, 1]) if expected_children < 1.5 else rng.choice([0, 1, 2])
        else:
            # Weak enforcement: more variation
            siblings = max(0, int(rng.gauss(expected_children, 0.8)))
            siblings = min(siblings, 5)  # Cap at 5
        
        is_only_child = (siblings == 0)
        
        # Calculate resource allocation per child
        total_children = siblings + 1  # Include self
        family_wealth_per_child = family_wealth / total_children
        
        # Parental pressure (higher for only children)
        if is_only_child:
            parental_pressure = 0.6 + rng.random() * 0.3  # 0.6-0.9
        else:
            parental_pressure = 0.3 + rng.random() * 0.3  # 0.3-0.6
        
        # Intergenerational support (weaker for only children)
        if is_only_child:
            intergenerational_support = 0.2 + rng.random() * 0.2  # 0.2-0.4
        else:
            intergenerational_support = 0.5 + rng.random() * 0.3  # 0.5-0.8
        
        # Initial caregiver burden (will increase with age)
        caregiver_burden = 0.0
        
        return FamilyState(
            siblings=siblings,
            is_only_child=is_only_child,
            parental_pressure=parental_pressure,
            intergenerational_support=intergenerational_support,
            caregiver_burden=caregiver_burden,
            family_wealth_per_child=family_wealth_per_child
        )
    
    @staticmethod
    def apply_only_child_effects(
        person_state,
        personality,
        family_state: FamilyState,
        age: int,
        city_tier: str = "medium"
    ):
        """Apply only-child specific effects to person state and personality"""
        if not family_state.is_only_child:
            return
        
        # Education investment multiplier (1.4x for only children)
        # This is already reflected in family_wealth_per_child, but affects learning rate
        if hasattr(person_state, 'learning_rate'):
            person_state.learning_rate *= 1.2  # Slight boost from focused investment
        
        # Personality adjustments (statistical tendencies, not value judgments)
        if hasattr(personality, 'conscientiousness'):
            personality.conscientiousness = min(1.0, personality.conscientiousness + 0.1)
        
        if hasattr(personality, 'social_drive'):
            personality.social_drive = max(0.0, personality.social_drive - 0.1)
        
        # Loneliness increase
        if hasattr(person_state, 'loneliness'):
            person_state.loneliness = min(1.0, person_state.loneliness + 0.15)
        
        # Resilience decrease (less exposure to sibling conflicts)
        if hasattr(personality, 'resilience'):
            personality.resilience = max(0.0, personality.resilience - 0.1)
        
        # Middle-age structural penalty (age > 45)
        if age > 45:
            if hasattr(person_state, 'stress'):
                person_state.stress = min(1.0, person_state.stress + 0.2)
            
            # Caregiver burden increases
            family_state.caregiver_burden = min(1.0, family_state.caregiver_burden + 0.3)
        
        # City tier amplification (Tier 1 cities)
        if city_tier in ["tier1", "Tier1", "beijing", "shanghai"]:
            # Competition intensity increase
            if hasattr(person_state, 'stress'):
                person_state.stress = min(1.0, person_state.stress + 0.1)
            
            # Marriage pressure (implicit in social pressure)
            if hasattr(person_state, 'social_capital'):
                # Higher social expectations
                pass  # Could add marriage_pressure attribute
    
    @staticmethod
    def calculate_competition_intensity(
        family_state: FamilyState,
        city_tier: str,
        era: str
    ) -> float:
        """Calculate competition intensity based on family structure and context"""
        base_intensity = 0.5
        
        # Only child effect
        if family_state.is_only_child:
            base_intensity += 0.2
        
        # City tier effect
        if city_tier in ["tier1", "Tier1", "beijing", "shanghai", "shenzhen"]:
            base_intensity += 0.3
        
        # Era effect (one-child era = highest competition)
        if era == "ONE_CHILD":
            base_intensity += 0.2
        
        return min(1.0, base_intensity)
    
    @staticmethod
    def update_caregiver_burden(
        family_state: FamilyState,
        age: int,
        parent_age: int = None
    ):
        """Update caregiver burden as person and parents age"""
        # Assume parents are ~25-30 years older
        if parent_age is None:
            parent_age = age + 28
        
        # Burden increases when parents reach old age (60+)
        if parent_age >= 60:
            # Only children bear full burden
            if family_state.is_only_child:
                burden_increase = 0.05 * (parent_age - 60) / 20  # Increases with parent age
            else:
                # Shared burden
                burden_increase = 0.02 * (parent_age - 60) / 20 / (family_state.siblings + 1)
            
            family_state.caregiver_burden = min(1.0, family_state.caregiver_burden + burden_increase)
        
        # Update stress based on burden
        return family_state.caregiver_burden

