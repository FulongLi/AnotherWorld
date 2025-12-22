"""
Decision Engine - Generates available actions based on person and world state
"""
from enum import Enum
from typing import List, Set
from models.person import PersonState, Personality
from models.world import WorldState


class Action(Enum):
    """Available actions a person can take"""
    STUDY = "study"
    WORK = "work"
    REST = "rest"
    MOVE = "move"  # Change location/career
    RISK = "risk"  # Take risks (entrepreneurship, etc.)
    RELATION = "relation"  # Build relationships


class DecisionEngine:
    """Generates and validates available actions"""
    
    def __init__(self, max_actions_per_year: int = 2):
        self.max_actions_per_year = max_actions_per_year
    
    def get_available_actions(
        self, 
        person: PersonState, 
        world: WorldState,
        personality: Personality
    ) -> List[Action]:
        """Get list of available actions based on current state"""
        available = []
        
        # STUDY - Available if young or low education
        if person.age < 30 or person.education_level < 0.8:
            if person.energy > 0.3:  # Need energy to study
                available.append(Action.STUDY)
        
        # WORK - Available if old enough and not too unhealthy
        if person.age >= 18 and person.health > 0.2:
            available.append(Action.WORK)
        
        # REST - Always available, but more important when stressed
        if person.stress > 0.5 or person.health < 0.5:
            available.append(Action.REST)
        elif person.energy < 0.3:
            available.append(Action.REST)
        
        # MOVE - Available if employment stability is low or personality allows
        if person.employment_stability < 0.5 or personality.risk_preference > 0.6:
            if person.age < 50:  # Less likely to move when older
                available.append(Action.MOVE)
        
        # RISK - Available if personality allows and economic conditions are good
        if personality.risk_preference > 0.5:
            if world is None or world.economic_cycle > 0 or person.wealth > 0.3:
                if person.age < 60:
                    available.append(Action.RISK)
        
        # RELATION - Available if not too lonely or personality is social
        if person.loneliness > 0.4 or personality.social_drive > 0.5:
            available.append(Action.RELATION)
        
        return available
    
    def select_actions(
        self,
        person: PersonState,
        world: WorldState,
        personality: Personality,
        user_choices: List[Action] = None
    ) -> List[Action]:
        """Select actions for the year"""
        available = self.get_available_actions(person, world, personality)
        
        if user_choices:
            # Validate user choices
            selected = [a for a in user_choices if a in available]
            # Limit to max actions
            selected = selected[:self.max_actions_per_year]
        else:
            # Auto-select based on personality and state
            selected = self._auto_select(available, person, personality)
        
        return selected
    
    def _auto_select(
        self,
        available: List[Action],
        person: PersonState,
        personality: Personality
    ) -> List[Action]:
        """Auto-select actions based on personality and state"""
        selected = []
        
        # Priority: address critical needs first
        if person.stress > 0.7 and Action.REST in available:
            selected.append(Action.REST)
        elif person.health < 0.3 and Action.REST in available:
            selected.append(Action.REST)
        
        # Then prioritize based on personality
        if personality.conscientiousness > 0.7:
            # Conscientious people prioritize work/study
            if Action.STUDY in available and person.education_level < 0.8:
                selected.append(Action.STUDY)
            elif Action.WORK in available:
                selected.append(Action.WORK)
        elif personality.social_drive > 0.7:
            # Social people prioritize relationships
            if Action.RELATION in available:
                selected.append(Action.RELATION)
        elif personality.risk_preference > 0.7:
            # Risk-takers prioritize risks
            if Action.RISK in available:
                selected.append(Action.RISK)
        
        # Fill remaining slots
        while len(selected) < self.max_actions_per_year and available:
            for action in available:
                if action not in selected:
                    selected.append(action)
                    break
        
        return selected[:self.max_actions_per_year]

