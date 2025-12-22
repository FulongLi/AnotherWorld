"""
Life Events System - Detects and records significant life events
"""
from dataclasses import dataclass
from typing import List, Optional
from models.person import PersonState
from models.world import WorldState


@dataclass
class LifeEvent:
    """Represents a significant life event"""
    year: int
    age: int
    title: str
    description: str
    impact: dict
    category: str  # 'health', 'career', 'social', 'economic', 'milestone'


class LifeEventDetector:
    """Detects life events based on state thresholds"""
    
    def __init__(self):
        self.detected_events: List[LifeEvent] = []
    
    def check_events(
        self,
        person: PersonState,
        world: WorldState,
        previous_state: Optional[PersonState] = None
    ) -> List[LifeEvent]:
        """Check for new events based on current state"""
        new_events = []
        
        # Burnout event
        if person.stress > 0.8 and (not previous_state or previous_state.stress <= 0.8):
            new_events.append(LifeEvent(
                year=world.year,
                age=person.age,
                title="Burnout",
                description="Extreme stress leads to burnout. Health and productivity suffer.",
                impact={'health': -0.1, 'mental_health': -0.15, 'energy': -0.2},
                category='health'
            ))
        
        # Career breakthrough
        if (person.skill_depth > 0.7 and person.employment_stability > 0.6 and 
            world.economic_cycle > 0 and 
            (not previous_state or previous_state.skill_depth <= 0.7)):
            new_events.append(LifeEvent(
                year=world.year,
                age=person.age,
                title="Career Breakthrough",
                description="Your expertise and dedication pay off. Major career advancement.",
                impact={'income': person.income * 0.3, 'wealth': 2000, 'social_capital': 0.1},
                category='career'
            ))
        
        # Social collapse
        if person.loneliness > 0.9 and (not previous_state or previous_state.loneliness <= 0.9):
            new_events.append(LifeEvent(
                year=world.year,
                age=person.age,
                title="Social Isolation",
                description="Extreme loneliness takes its toll. Mental health deteriorates.",
                impact={'mental_health': -0.2, 'health': -0.05},
                category='social'
            ))
        
        # Economic hardship
        if (person.wealth < 0 and person.income < 500 and 
            world.economic_cycle < -0.5):
            new_events.append(LifeEvent(
                year=world.year,
                age=person.age,
                title="Economic Hardship",
                description="Financial difficulties during economic downturn.",
                impact={'stress': 0.15, 'mental_health': -0.1},
                category='economic'
            ))
        
        # Education milestone
        if person.education_level >= 0.8 and (not previous_state or previous_state.education_level < 0.8):
            new_events.append(LifeEvent(
                year=world.year,
                age=person.age,
                title="Educational Achievement",
                description="Reached high level of education. New opportunities open.",
                impact={'skill_depth': 0.1, 'income': person.income * 0.2},
                category='milestone'
            ))
        
        # Health crisis
        if person.health < 0.3 and (not previous_state or previous_state.health >= 0.3):
            new_events.append(LifeEvent(
                year=world.year,
                age=person.age,
                title="Health Crisis",
                description="Serious health problems emerge. Requires attention and resources.",
                impact={'wealth': -2000, 'energy': -0.3},
                category='health'
            ))
        
        # Apply event impacts
        for event in new_events:
            self._apply_event_impact(person, event)
            self.detected_events.append(event)
        
        return new_events
    
    def _apply_event_impact(self, person: PersonState, event: LifeEvent):
        """Apply event impacts to person state"""
        for key, value in event.impact.items():
            if hasattr(person, key):
                current_value = getattr(person, key)
                if isinstance(value, (int, float)):
                    if value < 0:
                        setattr(person, key, max(0, current_value + value))
                    else:
                        setattr(person, key, min(1.0 if key in ['health', 'mental_health', 'energy', 'stress'] else float('inf'), current_value + value))
                elif isinstance(value, (int, float)) and key in ['income', 'wealth']:
                    setattr(person, key, current_value + value)
    
    def get_all_events(self) -> List[LifeEvent]:
        """Get all detected events"""
        return self.detected_events

