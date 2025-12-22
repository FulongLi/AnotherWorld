"""
Main Life Simulator - Orchestrates the simulation loop
"""
from models.person import PersonState, BirthProfile, Personality
from models.world import WorldState
from engine.decision_engine import DecisionEngine, Action
from engine.transition_engine import TransitionEngine
from narrative.life_events import LifeEventDetector
from narrative.summary_generator import SummaryGenerator
from utils.rng import rng
import copy


class LifeSimulator:
    """Main simulator that runs a complete life"""
    
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
        user_actions: dict = None  # {year: [Action, ...]}
    ) -> dict:
        """Run a complete life simulation"""
        
        # Initialize person state from birth profile
        person = self._initialize_person(birth)
        world = WorldState(
            year=birth.birth_year,
            economic_cycle=0.0,
            tech_level=0.3 + birth.birth_year % 100 / 100 * 0.4,  # Tech level based on birth year
            social_mobility=0.5,
            inequality=0.5,
            conflict_risk=0.1
        )
        
        # Store previous state for event detection
        previous_state = None
        
        # Main simulation loop
        while person.age < self.max_age and person.health > 0:
            # Update world
            world.update(birth.birth_year)
            
            # Get actions for this year
            year_actions = user_actions.get(person.age, []) if user_actions else None
            actions = self.decision_engine.select_actions(
                person, world, personality, year_actions
            )
            
            # Apply actions
            previous_state = copy.deepcopy(person)
            self.transition_engine.apply_actions(person, world, personality, actions)
            
            # Check for events
            self.event_detector.check_events(person, world, previous_state)
            
            # Age increment
            person.age += 1
            world.year = birth.birth_year + person.age
        
        # Generate summary
        events = self.event_detector.get_all_events()
        summary = self.summary_generator.generate_summary(
            person, birth, personality, world, events
        )
        
        return {
            'person': self._person_to_dict(person),
            'world': self._world_to_dict(world),
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
    
    def _world_to_dict(self, world: WorldState) -> dict:
        """Convert world state to dictionary"""
        return {
            'year': world.year,
            'economic_cycle': world.economic_cycle,
            'tech_level': world.tech_level,
            'social_mobility': world.social_mobility,
            'inequality': world.inequality,
            'conflict_risk': world.conflict_risk
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

