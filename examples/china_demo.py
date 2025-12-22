"""
Demonstration of China World Model - Era transitions and city effects
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.person import BirthProfile, Personality
from models.world_china import ChinaCity, ChinaEra
from engine.simulator_china import ChinaLifeSimulator


def compare_eras():
    """Compare different birth eras in China"""
    print("="*70)
    print("CHINA WORLD MODEL - ERA COMPARISON")
    print("="*70)
    
    eras_to_test = [
        (1950, "Establishment Era (1950)"),
        (1965, "Turbulence Era (1965)"),
        (1980, "Reform Early Era (1980)"),
        (1995, "Urban Boom Era (1995)"),
        (2010, "Structure Solidify Era (2010)"),
        (2022, "New Uncertainty Era (2022)")
    ]
    
    results = []
    
    for birth_year, era_name in eras_to_test:
        print(f"\n{'='*70}")
        print(f"Testing: {era_name}")
        print(f"{'='*70}")
        
        # Same birth profile, different eras
        birth = BirthProfile(
            birth_year=birth_year,
            region="Urban",
            family_class=0.5,
            parents_education=0.5,
            family_stability=0.7,
            genetic_health=0.7,
            cognitive_potential=0.6
        )
        
        personality = Personality(
            openness=0.6,
            conscientiousness=0.7,
            risk_preference=0.6,
            social_drive=0.6,
            resilience=0.7
        )
        
        simulator = ChinaLifeSimulator(max_age=min(80, 2024 - birth_year), seed=42)
        result = simulator.simulate(birth, personality, ChinaCity.BEIJING, parent_assets=0)
        
        person = result['person']
        china_world = result['china_world']
        
        print(f"Final Age: {person['age']}")
        print(f"Final Wealth: ${person['wealth']:,.2f}")
        print(f"Final Income: ${person['income']:,.2f}")
        print(f"Education Level: {person['education_level']:.3f}")
        print(f"Social Mobility: {china_world['social_mobility']:.3f}")
        print(f"Window Missed: {china_world['window_missed']}")
        print(f"Property Owned: {china_world['property_owned']}")
        
        results.append({
            'era': era_name,
            'wealth': person['wealth'],
            'income': person['income'],
            'education': person['education_level'],
            'mobility': china_world['social_mobility'],
            'window_missed': china_world['window_missed']
        })
    
    # Summary comparison
    print("\n" + "="*70)
    print("ERA COMPARISON SUMMARY")
    print("="*70)
    print(f"{'Era':<30} {'Wealth':<15} {'Mobility':<12} {'Window Missed'}")
    print("-"*70)
    
    for r in results:
        print(f"{r['era']:<30} ${r['wealth']:>12,.2f}  {r['mobility']:>10.3f}  {r['window_missed']}")


def compare_cities():
    """Compare different cities in same era"""
    print("\n" + "="*70)
    print("CHINA WORLD MODEL - CITY COMPARISON")
    print("="*70)
    
    cities_to_test = [
        (ChinaCity.BEIJING, "Beijing - Political/Resource Center"),
        (ChinaCity.SHANGHAI, "Shanghai - Financial/Rule Center"),
        (ChinaCity.SHENZHEN, "Shenzhen - Tech/Risk Center"),
        (ChinaCity.GUANGZHOU, "Guangzhou - Commercial/Stable")
    ]
    
    birth = BirthProfile(
        birth_year=1990,  # Urban boom era
        region="Urban",
        family_class=0.5,
        parents_education=0.5,
        family_stability=0.7,
        genetic_health=0.7,
        cognitive_potential=0.6
    )
    
    personality = Personality(
        openness=0.6,
        conscientiousness=0.7,
        risk_preference=0.6,
        social_drive=0.6,
        resilience=0.7
    )
    
    results = []
    
    for city, city_name in cities_to_test:
        print(f"\n{'='*70}")
        print(f"Testing: {city_name}")
        print(f"{'='*70}")
        
        simulator = ChinaLifeSimulator(max_age=60, seed=42)
        result = simulator.simulate(birth, personality, city, parent_assets=0)
        
        person = result['person']
        china_world = result['china_world']
        
        print(f"Final Wealth: ${person['wealth']:,.2f}")
        print(f"Final Income: ${person['income']:,.2f}")
        print(f"Education Level: {person['education_level']:.3f}")
        print(f"Risk/Reward Ratio: {china_world['risk_reward_ratio']:.3f}")
        print(f"Property Owned: {china_world['property_owned']}")
        
        results.append({
            'city': city_name,
            'wealth': person['wealth'],
            'income': person['income'],
            'risk_reward': china_world['risk_reward_ratio']
        })
    
    # Summary
    print("\n" + "="*70)
    print("CITY COMPARISON SUMMARY")
    print("="*70)
    print(f"{'City':<35} {'Wealth':<15} {'Risk/Reward':<12}")
    print("-"*70)
    
    for r in results:
        print(f"{r['city']:<35} ${r['wealth']:>12,.2f}  {r['risk_reward']:>10.3f}")


def window_mechanism_demo():
    """Demonstrate window mechanism (一次性窗口)"""
    print("\n" + "="*70)
    print("WINDOW MECHANISM DEMONSTRATION")
    print("="*70)
    print("\nComparing people who caught vs missed the window period\n")
    
    # Person who caught the window (born 1980, active during 1992-2007)
    birth_caught = BirthProfile(
        birth_year=1980,
        region="Urban",
        family_class=0.5,
        parents_education=0.5,
        family_stability=0.7,
        genetic_health=0.7,
        cognitive_potential=0.6
    )
    
    # Person who missed the window (born 1995, too late for urban boom)
    birth_missed = BirthProfile(
        birth_year=1995,
        region="Urban",
        family_class=0.5,
        parents_education=0.5,
        family_stability=0.7,
        genetic_health=0.7,
        cognitive_potential=0.6
    )
    
    personality = Personality(
        openness=0.6,
        conscientiousness=0.7,
        risk_preference=0.6,
        social_drive=0.6,
        resilience=0.7
    )
    
    simulator1 = ChinaLifeSimulator(max_age=60, seed=42)
    result_caught = simulator1.simulate(birth_caught, personality, ChinaCity.SHENZHEN, 0)
    
    simulator2 = ChinaLifeSimulator(max_age=30, seed=42)
    result_missed = simulator2.simulate(birth_missed, personality, ChinaCity.SHENZHEN, 0)
    
    print(f"{'Metric':<25} {'Caught Window':<20} {'Missed Window':<20} {'Ratio'}")
    print("-"*70)
    
    caught_person = result_caught['person']
    missed_person = result_missed['person']
    caught_world = result_caught['china_world']
    missed_world = result_missed['china_world']
    
    metrics = [
        ('Wealth', 'wealth', '$'),
        ('Income', 'income', '$'),
        ('Social Mobility', 'social_mobility', ''),
        ('Window Missed', 'window_missed', '')
    ]
    
    for name, key, prefix in metrics:
        if key == 'social_mobility':
            caught_val = caught_world[key]
            missed_val = missed_world[key]
        elif key == 'window_missed':
            caught_val = 1 if caught_world[key] else 0
            missed_val = 1 if missed_world[key] else 0
        else:
            caught_val = caught_person[key]
            missed_val = missed_person[key]
        
        if prefix == '$':
            caught_str = f"{prefix}{caught_val:,.2f}"
            missed_str = f"{prefix}{missed_val:,.2f}"
        else:
            caught_str = f"{caught_val:.3f}" if isinstance(caught_val, float) else str(caught_val)
            missed_str = f"{missed_val:.3f}" if isinstance(missed_val, float) else str(missed_val)
        
        if isinstance(caught_val, (int, float)) and isinstance(missed_val, (int, float)) and missed_val > 0:
            ratio = caught_val / missed_val
            ratio_str = f"{ratio:.2f}x"
        else:
            ratio_str = "N/A"
        
        print(f"{name:<25} {caught_str:<20} {missed_str:<20} {ratio_str}")
    
    print("\n" + "="*70)
    print("KEY INSIGHT: Window mechanism creates permanent mobility reduction")
    print("="*70)


if __name__ == "__main__":
    compare_eras()
    compare_cities()
    window_mechanism_demo()

