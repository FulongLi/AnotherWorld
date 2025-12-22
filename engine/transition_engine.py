"""
Transition Engine - Applies actions and updates person state
"""
from typing import List
from models.person import PersonState, Personality
from models.world import WorldState
from engine.decision_engine import Action
from utils.rng import rng
from utils.helpers import apply_noise


class TransitionEngine:
    """Applies state transitions based on actions"""
    
    def apply_actions(
        self,
        person: PersonState,
        world: WorldState,
        personality: Personality,
        actions: List[Action],
        birth_profile = None
    ):
        """Apply all actions and update person state"""
        for action in actions:
            self._apply_action(person, world, personality, action, birth_profile)
        
        # Natural aging effects
        self._apply_aging(person)
        
        # Clamp all values
        person.clamp_values()
    
    def _apply_action(
        self,
        person: PersonState,
        world: WorldState,
        personality: Personality,
        action: Action,
        birth_profile = None
    ):
        """Apply a single action"""
        if action == Action.STUDY:
            self._apply_study(person, world, personality, birth_profile)
        elif action == Action.WORK:
            self._apply_work(person, world, personality, birth_profile)
        elif action == Action.REST:
            self._apply_rest(person, personality)
        elif action == Action.MOVE:
            self._apply_move(person, world, personality, birth_profile)
        elif action == Action.RISK:
            self._apply_risk(person, world, personality, birth_profile)
        elif action == Action.RELATION:
            self._apply_relation(person, personality)
    
    def _apply_study(
        self,
        person: PersonState,
        world: WorldState,
        personality: Personality,
        birth_profile = None
    ):
        """Apply study action"""
        # Learning effectiveness depends on learning rate and tech level
        base_gain = person.learning_rate * (0.5 + world.tech_level * 0.5)
        
        # Apply Pareto Principle: tech benefits favor elite
        if birth_profile:
            person_score = world.calculate_person_score(
                person.education_level,
                person.skill_depth,
                person.social_capital,
                person.wealth,
                birth_profile.family_class
            )
            tech_multiplier = world.get_tech_benefit_multiplier(person_score)
            base_gain *= tech_multiplier
        
        gain = apply_noise(base_gain * 0.05)
        
        person.education_level += gain
        person.skill_depth += gain * 0.8
        person.skill_width += gain * 0.3
        
        # Costs
        person.energy -= apply_noise(0.1)
        person.stress += apply_noise(0.02)
        
        # Income might decrease if studying full-time
        if person.age >= 18:
            person.income *= 0.9
    
    def _apply_work(
        self,
        person: PersonState,
        world: WorldState,
        personality: Personality,
        birth_profile = None
    ):
        """Apply work action"""
        # Income depends on skills, education, and economic cycle
        skill_factor = (person.skill_depth * 0.7 + person.skill_width * 0.3)
        education_factor = person.education_level
        economic_factor = (world.economic_cycle + 1) / 2  # Convert -1 to 1 -> 0 to 1
        
        base_income = (skill_factor * 0.5 + education_factor * 0.3 + economic_factor * 0.2) * 1000
        
        # Apply Pareto Principle: wealth accumulation multiplier
        if birth_profile:
            person_score = world.calculate_person_score(
                person.education_level,
                person.skill_depth,
                person.social_capital,
                person.wealth,
                birth_profile.family_class
            )
            wealth_multiplier = world.get_wealth_multiplier(person_score)
            base_income *= wealth_multiplier
        
        income_gain = apply_noise(base_income)
        
        person.income = max(person.income * 0.95, income_gain)  # Slight decay or new income
        
        # Wealth accumulation also affected by Pareto
        if birth_profile:
            person_score = world.calculate_person_score(
                person.education_level,
                person.skill_depth,
                person.social_capital,
                person.wealth,
                birth_profile.family_class
            )
            wealth_multiplier = world.get_wealth_multiplier(person_score)
            person.wealth += person.income * 0.3 * wealth_multiplier  # Elite save more effectively
        else:
            person.wealth += person.income * 0.3  # Save 30% of income
        
        # Career progression
        if personality.conscientiousness > 0.6:
            person.employment_stability += apply_noise(0.02)
            person.skill_depth += apply_noise(0.01)
        
        # Costs
        person.energy -= apply_noise(0.15)
        person.stress += apply_noise(0.05)
        person.health -= apply_noise(0.01) if person.stress > 0.7 else 0
    
    def _apply_rest(
        self,
        person: PersonState,
        personality: Personality
    ):
        """Apply rest action"""
        # Recovery depends on resilience
        recovery = 0.1 * (1 + personality.resilience)
        recovery = apply_noise(recovery)
        
        person.energy += recovery
        person.stress -= recovery * 0.8
        person.health += recovery * 0.3
        person.mental_health += recovery * 0.2
        
        # Income might decrease
        if person.income > 0:
            person.income *= 0.95
    
    def _apply_move(
        self,
        person: PersonState,
        world: WorldState,
        personality: Personality,
        birth_profile = None
    ):
        """Apply move/change action"""
        # Calculate person score for opportunity access
        if birth_profile:
            person_score = world.calculate_person_score(
                person.education_level,
                person.skill_depth,
                person.social_capital,
                person.wealth,
                birth_profile.family_class
            )
            opportunity_mult = world.get_opportunity_multiplier(person_score)
            # Elite have better access to opportunities
            success_chance = 0.6 * opportunity_mult  # Elite: 0.6 * 4 = 2.4 (capped at 1.0)
            success_chance = min(0.95, success_chance)
        else:
            success_chance = 0.6
        
        # Moving can improve opportunities but is risky
        if rng.random() < success_chance:
            # Better opportunities
            person.employment_stability += apply_noise(0.1)
            income_mult = apply_noise(1.2)
            if birth_profile:
                income_mult *= world.get_wealth_multiplier(person_score)
            person.income *= income_mult
            person.social_capital += apply_noise(0.05)
        else:
            # Risky move didn't pay off
            person.employment_stability -= apply_noise(0.1)
            person.income *= apply_noise(0.8)
            person.stress += apply_noise(0.1)
        
        # Costs
        person.wealth -= apply_noise(500)  # Moving costs
        person.energy -= apply_noise(0.2)
        person.stress += apply_noise(0.05)
    
    def _apply_risk(
        self,
        person: PersonState,
        world: WorldState,
        personality: Personality,
        birth_profile = None
    ):
        """Apply risk-taking action (entrepreneurship, etc.)"""
        # Calculate person score for opportunity access
        if birth_profile:
            person_score = world.calculate_person_score(
                person.education_level,
                person.skill_depth,
                person.social_capital,
                person.wealth,
                birth_profile.family_class
            )
            opportunity_mult = world.get_opportunity_multiplier(person_score)
        else:
            person_score = 0.5
            opportunity_mult = 1.0
        
        # Success depends on skills, economic cycle, luck, and Pareto position
        base_success_chance = (
            person.skill_depth * 0.3 +
            person.social_capital * 0.2 +
            (world.economic_cycle + 1) / 2 * 0.3 +
            rng.random() * 0.2
        )
        
        # Elite get better opportunities (Pareto: 80% of opportunities to 20%)
        success_chance = base_success_chance * opportunity_mult
        success_chance = min(0.95, success_chance)  # Cap at 95%
        
        if success_chance > 0.5:
            # Success - wealth gain also affected by Pareto
            base_wealth_gain = apply_noise(5000 + person.wealth * 0.5)
            wealth_mult = world.get_wealth_multiplier(person_score)
            wealth_gain = base_wealth_gain * wealth_mult
            person.wealth += wealth_gain
            
            income_mult = apply_noise(1.5) * wealth_mult
            person.income *= income_mult
            person.social_capital += apply_noise(0.1)
        else:
            # Failure - but elite lose less
            loss_mult = 1.0 / opportunity_mult if opportunity_mult > 1 else 1.0
            person.wealth -= apply_noise(person.wealth * 0.3 * loss_mult)
            person.stress += apply_noise(0.15)
            person.employment_stability -= apply_noise(0.1)
        
        # Costs
        person.energy -= apply_noise(0.2)
        person.stress += apply_noise(0.1)
    
    def _apply_relation(
        self,
        person: PersonState,
        personality: Personality
    ):
        """Apply relationship-building action"""
        # Social gains
        social_gain = 0.1 * (1 + personality.social_drive)
        social_gain = apply_noise(social_gain)
        
        person.social_capital += social_gain
        person.loneliness -= social_gain * 0.8
        person.mental_health += social_gain * 0.3
        
        # Costs
        person.energy -= apply_noise(0.05)
        person.wealth -= apply_noise(100)  # Social activities cost money
    
    def _apply_aging(self, person: PersonState):
        """Apply natural aging effects"""
        # Health decline accelerates after 40
        if person.age > 40:
            health_decline = (person.age - 40) * 0.002
            person.health -= apply_noise(health_decline)
        
        if person.age > 60:
            health_decline = 0.01
            person.health -= apply_noise(health_decline)
            person.energy -= apply_noise(0.01)
        
        # Learning rate decreases with age
        if person.age > 30:
            person.learning_rate *= 0.995
        
        # Natural stress accumulation
        if person.stress < 0.5:
            person.stress += apply_noise(0.01)

