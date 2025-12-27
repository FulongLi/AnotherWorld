"""
Life Simulator v2 - New architecture with Base World -> Country -> City
"""
from models.person import PersonState, BirthProfile, Personality
from models.world_base import BaseWorldState
from models.country_base import CountryModel
from models.country_china import ChinaCountryModel
from models.city import City, create_china_cities
from engine.decision_engine import DecisionEngine, Action
from engine.transition_engine import TransitionEngine
from narrative.life_events import LifeEventDetector
from narrative.summary_generator import SummaryGenerator
from utils.rng import rng
import copy


class LifeSimulatorV2:
    """Main simulator with new architecture: Base World -> Country -> City"""
    
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
        country_model: CountryModel,
        city: City = None,
        user_actions: dict = None
    ) -> dict:
        """Run a complete life simulation"""
        
        # Initialize person state from birth profile
        person = self._initialize_person(birth)
        
        # Initialize base world state (universal economic laws)
        # Use 1949 as base_year for China model compatibility
        base_world = BaseWorldState(
            year=birth.birth_year,
            base_year=1949
        )
        
        # Initialize country model (if not already initialized)
        if not hasattr(country_model, 'base_world') or country_model.base_world is None:
            country_model.base_world = base_world
        
        # Store previous state for event detection
        previous_state = None
        
        # Main simulation loop
        while person.age < self.max_age and person.health > 0:
            # Update base world (universal laws)
            base_world.update(birth.birth_year)
            
            # Update country model (country-specific policies)
            country_model.update(birth.birth_year + person.age)
            
            # Get actions for this year
            # Create world adapter for decision engine compatibility
            from models.world import WorldState
            world_adapter = WorldState(
                year=base_world.year,
                economic_cycle=base_world.economic_cycle,
                tech_level=base_world.tech_level,
                social_mobility=country_model.get_effective_social_mobility(),
                inequality=country_model.get_effective_inequality(),
                conflict_risk=0.1
            )
            
            year_actions = user_actions.get(person.age, []) if user_actions else None
            actions = self.decision_engine.select_actions(
                person, world_adapter, personality, year_actions
            )
            
            # Apply actions with new architecture
            previous_state = copy.deepcopy(person)
            self.transition_engine.apply_actions(
                person, base_world, country_model, city, personality, actions, birth
            )
            
            # Check for events
            self.event_detector.check_events(person, world_adapter, previous_state)
            
            # Age increment
            person.age += 1
            base_world.year = birth.birth_year + person.age
        
        # Generate summary
        events = self.event_detector.get_all_events()
        summary = self.summary_generator.generate_summary(
            person, birth, personality, world_adapter, events
        )
        
        return {
            'person': self._person_to_dict(person),
            'base_world': self._base_world_to_dict(base_world),
            'country': country_model.to_dict(),
            'city': city.to_dict() if city else None,
            'events': [self._event_to_dict(e) for e in events],
            'summary': summary
        }
    
    def _initialize_person(self, birth: BirthProfile) -> PersonState:
        """Initialize person state from birth profile"""
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
    
    def _base_world_to_dict(self, base_world: BaseWorldState) -> dict:
        """Convert base world state to dictionary"""
        return {
            'year': base_world.year,
            'kondratiev_phase': base_world.kondratiev_phase,
            'economic_cycle': base_world.economic_cycle,
            'tech_level': base_world.tech_level,
            'inequality': base_world.inequality,
            'social_mobility': base_world.social_mobility
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


# Convenience function for China simulation
def simulate_china_life(
    birth: BirthProfile,
    personality: Personality,
    city_name: str = "beijing",
    max_age: int = 100,
    seed: int = None
) -> dict:
    """Convenience function to simulate life in China"""
    # Create base world
    base_world = BaseWorldState(year=birth.birth_year, base_year=1949)
    
    # Create China country model
    china_model = ChinaCountryModel(base_world, birth.birth_year)
    
    # Create city
    china_cities = create_china_cities()
    if city_name not in china_cities:
        city_name = "beijing"  # Default
    
    city_config = china_cities[city_name]
    city = City(city_config, china_model)
    
    # Initialize family structure
    from models.family_policy import FamilyPolicyEngine
    family_wealth = birth.family_class * 100000
    family_state = FamilyPolicyEngine.generate_family_structure(
        birth.birth_year, family_wealth, True, rng
    )
    
    # Run simulation
    simulator = LifeSimulatorV2(max_age=max_age, seed=seed)
    result = simulator.simulate(birth, personality, china_model, city)
    
    # Add family state to result
    result['family_state'] = {
        'siblings': family_state.siblings,
        'is_only_child': family_state.is_only_child,
        'parental_pressure': family_state.parental_pressure,
        'caregiver_burden': family_state.caregiver_burden
    }
    
    return result

