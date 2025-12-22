"""
Demonstration of Pareto Principle effects in the simulation
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.person import BirthProfile, Personality
from engine.simulator import LifeSimulator


def compare_elite_vs_non_elite():
    """Compare simulation results for elite vs non-elite starting positions"""
    
    print("="*70)
    print("PARETO PRINCIPLE DEMONSTRATION")
    print("="*70)
    print("\nComparing Elite (Top 20%) vs Non-Elite (Bottom 80%) outcomes\n")
    
    # Elite birth profile (top 20%)
    elite_birth = BirthProfile(
        birth_year=1980,
        region="Metropolitan",
        family_class=0.9,  # High family class
        parents_education=0.85,
        family_stability=0.9,
        genetic_health=0.8,
        cognitive_potential=0.75
    )
    
    # Non-elite birth profile (bottom 80%)
    non_elite_birth = BirthProfile(
        birth_year=1980,
        region="Rural",
        family_class=0.2,  # Low family class
        parents_education=0.3,
        family_stability=0.5,
        genetic_health=0.6,
        cognitive_potential=0.5
    )
    
    # Same personality for fair comparison
    personality = Personality(
        openness=0.6,
        conscientiousness=0.7,
        risk_preference=0.5,
        social_drive=0.6,
        resilience=0.7
    )
    
    # Run simulations
    simulator = LifeSimulator(max_age=60, seed=42)
    
    print("Running Elite simulation...")
    elite_result = simulator.simulate(elite_birth, personality)
    
    simulator2 = LifeSimulator(max_age=60, seed=42)  # Same seed for comparison
    print("Running Non-Elite simulation...")
    non_elite_result = simulator2.simulate(non_elite_birth, personality)
    
    # Compare results
    print("\n" + "="*70)
    print("COMPARISON RESULTS")
    print("="*70)
    
    elite_person = elite_result['person']
    non_elite_person = non_elite_result['person']
    
    print(f"\n{'Metric':<25} {'Elite':<20} {'Non-Elite':<20} {'Ratio':<10}")
    print("-"*70)
    
    metrics = [
        ('Final Wealth', 'wealth', '$'),
        ('Final Income', 'income', '$'),
        ('Education Level', 'education_level', ''),
        ('Skill Depth', 'skill_depth', ''),
        ('Social Capital', 'social_capital', ''),
        ('Total Events', 'events', '')
    ]
    
    for name, key, prefix in metrics:
        if key == 'events':
            elite_val = len(elite_result['events'])
            non_elite_val = len(non_elite_result['events'])
        else:
            elite_val = elite_person[key]
            non_elite_val = non_elite_person[key]
        
        if elite_val > 0:
            ratio = elite_val / non_elite_val if non_elite_val > 0 else float('inf')
        else:
            ratio = 0
        
        if prefix == '$':
            elite_str = f"{prefix}{elite_val:,.2f}"
            non_elite_str = f"{prefix}{non_elite_val:,.2f}"
        else:
            elite_str = f"{elite_val:.3f}"
            non_elite_str = f"{non_elite_val:.3f}"
        
        ratio_str = f"{ratio:.2f}x" if ratio != float('inf') else "∞"
        
        print(f"{name:<25} {elite_str:<20} {non_elite_str:<20} {ratio_str:<10}")
    
    # Show Pareto effect
    print("\n" + "="*70)
    print("PARETO PRINCIPLE EFFECTS")
    print("="*70)
    
    wealth_ratio = elite_person['wealth'] / non_elite_person['wealth'] if non_elite_person['wealth'] > 0 else float('inf')
    income_ratio = elite_person['income'] / non_elite_person['income'] if non_elite_person['income'] > 0 else float('inf')
    
    print(f"\nWealth Ratio: {wealth_ratio:.2f}x")
    print(f"Income Ratio: {income_ratio:.2f}x")
    print(f"\nExpected (Pareto): ~4x multiplier for elite")
    print(f"Observed: Elite accumulates wealth {wealth_ratio:.2f}x faster")
    
    # Show world state
    elite_world = elite_result['world']
    print(f"\nFinal World State:")
    print(f"  Inequality: {elite_world['inequality']:.3f}")
    print(f"  Social Mobility: {elite_world['social_mobility']:.3f}")
    print(f"  Technology Level: {elite_world['tech_level']:.3f}")
    
    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)
    print("""
1. Elite (top 20%) accumulate wealth ~4x faster due to Pareto multiplier
2. Non-elite (bottom 80%) share remaining 20% of wealth (0.25x multiplier)
3. Higher inequality reduces social mobility
4. Technology benefits favor elite disproportionately
5. Birth class matters more in high-inequality worlds
    """)


if __name__ == "__main__":
    compare_elite_vs_non_elite()

