"""
Summary Generator - Creates narrative summaries of a life
"""
from typing import List, Dict, Any
from models.person import PersonState, BirthProfile, Personality
from models.world import WorldState
from narrative.life_events import LifeEvent


class SummaryGenerator:
    """Generates life summaries and narratives"""
    
    def generate_summary(
        self,
        person: PersonState,
        birth: BirthProfile,
        personality: Personality,
        world: WorldState,
        events: List[LifeEvent]
    ) -> Dict[str, Any]:
        """Generate comprehensive life summary"""
        
        # Categorize events
        event_categories = {
            'health': [e for e in events if e.category == 'health'],
            'career': [e for e in events if e.category == 'career'],
            'social': [e for e in events if e.category == 'social'],
            'economic': [e for e in events if e.category == 'economic'],
            'milestone': [e for e in events if e.category == 'milestone']
        }
        
        # Generate narrative
        narrative = self._generate_narrative(person, events, event_categories)
        
        # Identify highlights
        highlights = self._identify_highlights(person, events)
        
        # Calculate statistics
        stats = self._calculate_statistics(person, events)
        
        return {
            'summary': narrative,
            'highlights': highlights,
            'statistics': stats,
            'final_state': self._get_final_state_dict(person),
            'key_events': [self._event_to_dict(e) for e in events[:20]],  # Top 20 events
            'birth_profile': {
                'birth_year': birth.birth_year,
                'region': birth.region,
                'family_class': birth.family_class
            },
            'personality': {
                'openness': personality.openness,
                'conscientiousness': personality.conscientiousness,
                'risk_preference': personality.risk_preference,
                'social_drive': personality.social_drive,
                'resilience': personality.resilience
            }
        }
    
    def _generate_narrative(
        self,
        person: PersonState,
        events: List[LifeEvent],
        event_categories: Dict[str, List[LifeEvent]]
    ) -> str:
        """Generate narrative text"""
        narratives = []
        
        # Opening
        if person.age < 50:
            narratives.append(f"This was a life cut short at age {person.age}.")
        else:
            narratives.append(f"This was a life that spanned {person.age} years.")
        
        # Economic narrative
        if person.wealth > 0.5:
            narratives.append("Financial success was achieved through dedication and opportunity.")
        elif person.wealth < 0:
            narratives.append("Financial struggles were a constant challenge throughout life.")
        else:
            narratives.append("Financial stability was maintained through careful management.")
        
        # Career narrative
        if len(event_categories['career']) > 0:
            narratives.append("Significant career milestones were reached.")
        if person.skill_depth > 0.7:
            narratives.append("Deep expertise was developed in chosen fields.")
        
        # Social narrative
        if person.loneliness > 0.7:
            narratives.append("Social isolation was a recurring theme.")
        elif person.social_capital > 0.7:
            narratives.append("Strong social connections were built and maintained.")
        
        # Health narrative
        if len(event_categories['health']) > 2:
            narratives.append("Health challenges were faced multiple times.")
        elif person.health > 0.7:
            narratives.append("Good health was maintained throughout most of life.")
        
        # Closing
        if person.mental_health > 0.7 and person.life_events:
            narratives.append("Overall, this was a life marked by resilience and adaptation.")
        elif person.stress > 0.7:
            narratives.append("This life was characterized by high stress and constant challenges.")
        else:
            narratives.append("This was a life of relative stability and gradual progress.")
        
        return " ".join(narratives)
    
    def _identify_highlights(
        self,
        person: PersonState,
        events: List[LifeEvent]
    ) -> List[str]:
        """Identify key life highlights"""
        highlights = []
        
        # Education
        if person.education_level > 0.8:
            highlights.append("High Education Achievement")
        
        # Career
        career_events = [e for e in events if e.category == 'career']
        if len(career_events) > 0:
            highlights.append("Career Breakthroughs")
        
        # Wealth
        if person.wealth > 100000:
            highlights.append("Significant Wealth Accumulation")
        elif person.wealth < -10000:
            highlights.append("Financial Hardship")
        
        # Social
        if person.social_capital > 0.8:
            highlights.append("Strong Social Network")
        elif person.loneliness > 0.8:
            highlights.append("Chronic Loneliness")
        
        # Health
        health_events = [e for e in events if e.category == 'health']
        if len(health_events) > 3:
            highlights.append("Multiple Health Challenges")
        
        return highlights if highlights else ["Ordinary Life"]
    
    def _calculate_statistics(
        self,
        person: PersonState,
        events: List[LifeEvent]
    ) -> Dict[str, Any]:
        """Calculate life statistics"""
        return {
            'total_events': len(events),
            'event_by_category': {
                'health': len([e for e in events if e.category == 'health']),
                'career': len([e for e in events if e.category == 'career']),
                'social': len([e for e in events if e.category == 'social']),
                'economic': len([e for e in events if e.category == 'economic']),
                'milestone': len([e for e in events if e.category == 'milestone'])
            },
            'peak_wealth': person.wealth,
            'final_income': person.income,
            'education_level': person.education_level,
            'skill_depth': person.skill_depth
        }
    
    def _get_final_state_dict(self, person: PersonState) -> Dict[str, Any]:
        """Convert final state to dictionary"""
        return {
            'age': person.age,
            'health': person.health,
            'mental_health': person.mental_health,
            'energy': person.energy,
            'stress': person.stress,
            'education_level': person.education_level,
            'skill_depth': person.skill_depth,
            'skill_width': person.skill_width,
            'income': person.income,
            'wealth': person.wealth,
            'social_capital': person.social_capital,
            'loneliness': person.loneliness
        }
    
    def _event_to_dict(self, event: LifeEvent) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            'year': event.year,
            'age': event.age,
            'title': event.title,
            'description': event.description,
            'category': event.category
        }

