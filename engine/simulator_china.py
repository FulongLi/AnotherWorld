"""
China-specific Life Simulator - Integrates China World Model
"""
from models.person import PersonState, BirthProfile, Personality
from models.world_china import ChinaWorldState, ChinaEra, ChinaCity
from models.family_policy import FamilyPolicyEngine
from engine.decision_engine import DecisionEngine, Action
from engine.transition_engine import TransitionEngine
from narrative.life_events import LifeEventDetector
from narrative.summary_generator import SummaryGenerator
from utils.rng import rng
import copy


class ChinaLifeSimulator:
    """Main simulator for China-specific life trajectories"""
    
    def __init__(self, max_age: int = 100, seed: int = None):
        self.max_age = max_age
        if seed is not None:
            rng.set_seed(seed)
        
        self.decision_engine = DecisionEngine()
        self.transition_engine = TransitionEngine()
        self.event_detector = LifeEventDetector()
        self.summary_generator = SummaryGenerator()
    
    def simulate(
        self,
        birth: BirthProfile,
        personality: Personality,
        city: ChinaCity = ChinaCity.BEIJING,
        parent_assets: float = 0.0,
        user_actions: dict = None
    ) -> dict:
        """Run a complete life simulation in China context"""
        
        # Initialize person state from birth profile
        person = self._initialize_person(birth)
        
        # Initialize China world state
        china_world = ChinaWorldState(
            year=birth.birth_year,
            era=ChinaEra.ESTABLISHMENT,  # Will be set correctly in __post_init__
            city=city
        )
        china_world.parent_assets = parent_assets
        
        # Initialize family structure
        family_wealth = birth.family_class * 100000  # Estimate family wealth
        china_world.initialize_family_structure(birth.birth_year, family_wealth, rng)
        
        # Apply only-child effects to initial person state
        if china_world.family_state:
            city_tier = "tier1" if city in [ChinaCity.BEIJING, ChinaCity.SHANGHAI, ChinaCity.SHENZHEN] else "tier2"
            FamilyPolicyEngine.apply_only_child_effects(
                person, personality, china_world.family_state, person.age, city_tier
            )
        
        # Store previous state for event detection
        previous_state = None
        
        # Main simulation loop
        while person.age < self.max_age and person.health > 0:
            # Update China world
            china_world.update(birth.birth_year)
            
            # Get actions for this year
            # Create a minimal world adapter for decision engine compatibility
            from models.world import WorldState
            world_adapter = WorldState(
                year=china_world.year,
                economic_cycle=0.0,  # Will be overridden by China-specific logic
                tech_level=0.5,
                social_mobility=china_world.get_social_mobility(),
                inequality=china_world.era_config.inequality,
                conflict_risk=0.1
            )
            
            year_actions = user_actions.get(person.age, []) if user_actions else None
            actions = self.decision_engine.select_actions(
                person, world_adapter, personality, year_actions
            )
            
            # Apply actions with China-specific modifiers
            previous_state = copy.deepcopy(person)
            self._apply_actions_china(person, china_world, personality, actions, birth)
            
            # Check for events
            # Note: Would need to adapt event detector for China context
            # self.event_detector.check_events(person, china_world, previous_state)
            
            # Age increment
            person.age += 1
            china_world.year = birth.birth_year + person.age
            
            # Update family policy state if era changed
            new_policy = FamilyPolicyEngine.get_policy_for_year(china_world.year)
            if china_world.family_policy_state is None or china_world.family_policy_state.policy != new_policy:
                is_urban = True
                china_world.family_policy_state = FamilyPolicyEngine.get_policy_config(new_policy, is_urban)
            
            # Update caregiver burden
            if china_world.family_state:
                FamilyPolicyEngine.update_caregiver_burden(
                    china_world.family_state, person.age
                )
                # Apply burden to stress
                person.stress = min(1.0, person.stress + china_world.family_state.caregiver_burden * 0.1)
            
            # Re-apply only-child effects (especially important for middle age)
            if china_world.family_state:
                city_tier = "tier1" if city in [ChinaCity.BEIJING, ChinaCity.SHANGHAI, ChinaCity.SHENZHEN] else "tier2"
                FamilyPolicyEngine.apply_only_child_effects(
                    person, personality, china_world.family_state, person.age, city_tier
                )
        
        # Generate summary
        events = self.event_detector.get_all_events()
        summary = self.summary_generator.generate_summary(
            person, birth, personality, None, events  # Pass None for world
        )
        
        return {
            'person': self._person_to_dict(person),
            'china_world': china_world.to_dict(),
            'events': [self._event_to_dict(e) for e in events],
            'summary': summary
        }
    
    def _initialize_person(self, birth: BirthProfile) -> PersonState:
        """Initialize person state from birth profile"""
        from models.person import PersonState
        
        person = PersonState()
        
        # Set initial values based on birth profile
        person.health = birth.genetic_health
        person.mental_health = 0.7 + birth.family_stability * 0.2
        person.energy = 0.8
        person.stress = 0.2 - birth.family_stability * 0.1
        
        # Education potential
        person.learning_rate = birth.cognitive_potential
        person.education_level = birth.parents_education * 0.3
        
        # Economic starting point
        person.wealth = birth.family_class * 10000
        person.income = 0
        
        # Social starting point
        person.social_capital = birth.family_stability * 0.3
        person.loneliness = 0.3 - birth.family_stability * 0.2
        
        return person
    
    def _apply_actions_china(
        self,
        person: PersonState,
        china_world: ChinaWorldState,
        personality: Personality,
        actions: list,
        birth: BirthProfile
    ):
        """Apply actions with China-specific modifiers"""
        from utils.helpers import apply_noise
        from utils.rng import rng
        
        for action in actions:
            if action == Action.STUDY:
                self._apply_study_china(person, china_world, personality)
            elif action == Action.WORK:
                self._apply_work_china(person, china_world, personality)
            elif action == Action.REST:
                self._apply_rest_china(person, china_world, personality)
            elif action == Action.MOVE:
                self._apply_move_china(person, china_world, personality)
            elif action == Action.RISK:
                self._apply_risk_china(person, china_world, personality)
            elif action == Action.RELATION:
                self._apply_relation_china(person, china_world, personality)
        
        # Natural aging
        self._apply_aging_china(person, china_world)
        
        # Check property opportunities
        if china_world.check_property_opportunity(person.wealth, person.age):
            success, remaining = china_world.apply_property_purchase(person.wealth)
            if success:
                person.wealth = remaining
        
        # Clamp values
        person.clamp_values()
    
    def _apply_study_china(self, person, china_world, personality):
        """Apply study with China modifiers"""
        from utils.helpers import apply_noise
        
        # Base gain
        base_gain = person.learning_rate * 0.05
        
        # Era modifier (education return)
        era_return = china_world.get_education_return()
        base_gain *= era_return
        
        # City modifier
        city_mod = china_world.get_city_modifier_for_action("study")
        base_gain *= city_mod
        
        # System shock penalty (turbulence era)
        if china_world.era == ChinaEra.TURBULENCE:
            base_gain *= (1 - china_world.era_config.system_shock * 0.5)
        
        gain = apply_noise(base_gain)
        
        person.education_level += gain
        person.skill_depth += gain * 0.8
        person.skill_width += gain * 0.3
        
        person.energy -= apply_noise(0.1)
        person.stress += apply_noise(0.02)
        
        if person.age >= 18:
            person.income *= 0.9
    
    def _apply_work_china(self, person, china_world, personality):
        """Apply work with China modifiers"""
        from utils.helpers import apply_noise
        
        # Base income calculation
        skill_factor = (person.skill_depth * 0.7 + person.skill_width * 0.3)
        education_factor = person.education_level
        
        # Era education return
        education_factor *= china_world.get_education_return()
        
        base_income = (skill_factor * 0.5 + education_factor * 0.3) * 1000
        
        # City modifier
        city_mod = china_world.get_city_modifier_for_action("work")
        base_income *= city_mod
        
        # City income ceiling
        if china_world.city_config.income_ceiling == "high":
            base_income *= 1.5
        elif china_world.city_config.income_ceiling == "low":
            base_income *= 0.7
        
        income_gain = apply_noise(base_income)
        person.income = max(person.income * 0.95, income_gain)
        
        # Wealth accumulation
        person.wealth += person.income * 0.3
        
        # Intergenerational advantage
        intergen_advantage = china_world.get_intergenerational_advantage()
        person.wealth += person.income * 0.1 * intergen_advantage
        
        # Costs
        person.energy -= apply_noise(0.15)
        
        # Stress from era and city
        stress_mod = china_world.get_stress_modifier()
        person.stress += apply_noise(0.05 + stress_mod * 0.1)
        
        # Mental health weight (new uncertainty era)
        if china_world.era == ChinaEra.NEW_UNCERTAINTY:
            mental_weight = china_world.get_mental_health_weight()
            if person.stress > 0.7:
                person.mental_health -= apply_noise(0.05 * mental_weight)
    
    def _apply_rest_china(self, person, china_world, personality):
        """Apply rest with China modifiers"""
        from utils.helpers import apply_noise
        
        recovery = 0.1 * (1 + personality.resilience)
        recovery = apply_noise(recovery)
        
        # Mental health weight in new uncertainty era
        if china_world.era == ChinaEra.NEW_UNCERTAINTY:
            mental_weight = china_world.get_mental_health_weight()
            recovery *= mental_weight
        
        person.energy += recovery
        person.stress -= recovery * 0.8
        person.health += recovery * 0.3
        person.mental_health += recovery * 0.2
        
        if person.income > 0:
            person.income *= 0.95
    
    def _apply_move_china(self, person, china_world, personality):
        """Apply move (city change) - switches entire probability distribution"""
        from utils.helpers import apply_noise
        from utils.rng import rng
        
        # City change is significant - it switches probability distributions
        # For simplicity, we'll model it as a risky but potentially rewarding move
        
        # Success depends on era and target city
        if china_world.era in [ChinaEra.REFORM_EARLY, ChinaEra.URBAN_BOOM]:
            # Window periods - moving is more rewarding
            success_chance = 0.7
        else:
            success_chance = 0.5
        
        # City accessibility
        if china_world.city_config.mobility_threshold == "low":
            success_chance += 0.2
        elif china_world.city_config.mobility_threshold == "high":
            success_chance -= 0.2
        
        if rng.random() < success_chance:
            # Successful move
            person.employment_stability += apply_noise(0.1)
            person.income *= apply_noise(1.2)
            person.social_capital += apply_noise(0.05)
        else:
            # Failed move
            person.employment_stability -= apply_noise(0.1)
            person.income *= apply_noise(0.8)
            person.stress += apply_noise(0.1)
        
        person.wealth -= apply_noise(500)
        person.energy -= apply_noise(0.2)
        person.stress += apply_noise(0.05)
    
    def _apply_risk_china(self, person, china_world, personality):
        """Apply risk with China modifiers"""
        from utils.helpers import apply_noise
        from utils.rng import rng
        
        # Risk/reward ratio from era and city
        risk_ratio = china_world.get_risk_reward_ratio()
        
        # City-specific risk characteristics
        if china_world.city == ChinaCity.SHENZHEN:
            # High variance in Shenzhen
            base_success = 0.4 + rng.random() * 0.4  # 0.4-0.8 range
        else:
            base_success = 0.5
        
        # Age penalty (especially in Shenzhen)
        if person.age > china_world.city_config.age_penalty_age:
            base_success *= 0.7
        
        # Window period bonus
        if china_world.window_open:
            base_success *= 1.3
        
        success_chance = base_success * risk_ratio
        success_chance = min(0.95, success_chance)
        
        if rng.random() < success_chance:
            # Success
            wealth_gain = apply_noise(5000 + person.wealth * 0.5)
            person.wealth += wealth_gain
            person.income *= apply_noise(1.5)
            person.social_capital += apply_noise(0.1)
        else:
            # Failure - risk penalty in new uncertainty era
            loss_mult = 1.0
            if china_world.era == ChinaEra.NEW_UNCERTAINTY:
                loss_mult = 1.0 + china_world.era_config.risk_penalty
            
            person.wealth -= apply_noise(person.wealth * 0.3 * loss_mult)
            person.stress += apply_noise(0.15)
            person.employment_stability -= apply_noise(0.1)
        
        person.energy -= apply_noise(0.2)
        person.stress += apply_noise(0.1)
    
    def _apply_relation_china(self, person, china_world, personality):
        """Apply relation with China modifiers"""
        from utils.helpers import apply_noise
        
        social_gain = 0.1 * (1 + personality.social_drive)
        social_gain = apply_noise(social_gain)
        
        # City stability bonus
        city_mod = china_world.get_city_modifier_for_action("relation")
        social_gain *= city_mod
        
        person.social_capital += social_gain
        person.loneliness -= social_gain * 0.8
        person.mental_health += social_gain * 0.3
        
        person.energy -= apply_noise(0.05)
        person.wealth -= apply_noise(100)
    
    def _apply_aging_china(self, person, china_world):
        """Apply aging with China-specific considerations"""
        from utils.helpers import apply_noise
        
        # Standard aging
        if person.age > 40:
            health_decline = (person.age - 40) * 0.002
            person.health -= apply_noise(health_decline)
        
        if person.age > 60:
            health_decline = 0.01
            person.health -= apply_noise(health_decline)
            person.energy -= apply_noise(0.01)
        
        # Health risk in turbulence era
        if china_world.era == ChinaEra.TURBULENCE:
            if rng.random() < china_world.era_config.health_risk * 0.1:
                person.health -= apply_noise(0.1)
        
        # Learning rate decreases
        if person.age > 30:
            person.learning_rate *= 0.995
        
        # Natural stress accumulation
        if person.stress < 0.5:
            person.stress += apply_noise(0.01)
    
    def _person_to_dict(self, person: PersonState) -> dict:
        """Convert person state to dictionary"""
        return {
            'age': person.age,
            'health': person.health,
            'mental_health': person.mental_health,
            'energy': person.energy,
            'stress': person.stress,
            'education_level': person.education_level,
            'skill_depth': person.skill_depth,
            'skill_width': person.skill_width,
            'learning_rate': person.learning_rate,
            'income': person.income,
            'wealth': person.wealth,
            'occupation': person.occupation,
            'employment_stability': person.employment_stability,
            'social_capital': person.social_capital,
            'loneliness': person.loneliness
        }
    
    def _event_to_dict(self, event) -> dict:
        """Convert event to dictionary"""
        return {
            'year': event.year,
            'age': event.age,
            'title': event.title,
            'description': event.description,
            'category': event.category
        }

