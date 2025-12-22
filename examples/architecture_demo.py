"""
Demonstration of new architecture: Base World -> Country -> City
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.person import BirthProfile, Personality
from models.world_base import BaseWorldState
from models.country_china import ChinaCountryModel
from models.city import City, create_china_cities
from engine.simulator_v2 import LifeSimulatorV2, simulate_china_life


def demo_new_architecture():
    """Demonstrate new three-layer architecture"""
    print("="*70)
    print("NEW ARCHITECTURE DEMONSTRATION")
    print("Base World (Universal Laws) -> Country (Policies) -> City (Local Context)")
    print("="*70)
    
    birth = BirthProfile(
        birth_year=1990,
        region="Urban",
        family_class=0.6,
        parents_education=0.6,
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
    
    # Create base world (universal laws)
    base_world = BaseWorldState(year=birth.birth_year, base_year=1949)
    print(f"\nBase World (Universal Laws):")
    print(f"  Kondratiev Phase: {base_world.kondratiev_phase:.3f}")
    print(f"  Economic Cycle: {base_world.economic_cycle:.3f}")
    print(f"  Tech Level: {base_world.tech_level:.3f}")
    print(f"  Inequality: {base_world.inequality:.3f}")
    
    # Create China country model
    china_model = ChinaCountryModel(base_world, birth.birth_year)
    print(f"\nCountry Model (China Policies):")
    print(f"  Era: {china_model.current_era.name}")
    print(f"  Window Open: {china_model.window_open}")
    print(f"  Social Mobility: {china_model.get_effective_social_mobility():.3f}")
    print(f"  Education Return: {china_model.get_education_return():.3f}")
    print(f"  Family Policy: {china_model.family_policy_state.policy.name if china_model.family_policy_state else 'N/A'}")
    
    # Create cities
    china_cities = create_china_cities()
    
    print(f"\nCity Models (Local Context):")
    for city_name, city_config in china_cities.items():
        city = City(city_config, china_model)
        print(f"\n  {city_config.city_name}:")
        print(f"    Tier: {city_config.tier.value}")
        print(f"    Income Ceiling: {city_config.income_ceiling}")
        print(f"    Living Cost: {city_config.living_cost}")
        print(f"    Risk/Reward: {city_config.risk_reward_ratio:.2f}")
        print(f"    Mobility Threshold: {city_config.mobility_threshold}")
    
    # Run simulation for Shenzhen
    print(f"\n{'='*70}")
    print("Running Simulation: Shenzhen, China")
    print(f"{'='*70}")
    
    shenzhen_config = china_cities["shenzhen"]
    shenzhen = City(shenzhen_config, china_model)
    
    simulator = LifeSimulatorV2(max_age=50, seed=42)
    result = simulator.simulate(birth, personality, china_model, shenzhen)
    
    person = result['person']
    base_world_result = result['base_world']
    country_result = result['country']
    city_result = result['city']
    
    print(f"\nResults:")
    print(f"  Final Age: {person['age']}")
    print(f"  Final Wealth: ${person['wealth']:,.2f}")
    print(f"  Final Income: ${person['income']:,.2f}")
    print(f"  Education Level: {person['education_level']:.3f}")
    
    print(f"\nBase World Effects:")
    print(f"  Kondratiev Effect: {base_world.get_kondratiev_effect():.3f}x")
    print(f"  Economic Cycle: {base_world_result['economic_cycle']:.3f}")
    
    print(f"\nCountry Effects:")
    print(f"  Era: {country_result['era']}")
    print(f"  Social Mobility: {country_result['social_mobility']:.3f}")
    print(f"  Education Return: {country_result['education_return']:.3f}")
    
    print(f"\nCity Effects:")
    print(f"  City: {city_result['city_name']}")
    print(f"  Risk/Reward: {city_result['risk_reward_ratio']:.2f}")
    print(f"  Living Cost: {city_result['living_cost']}")


def compare_cities_new_architecture():
    """Compare different cities with new architecture"""
    print("\n" + "="*70)
    print("CITY COMPARISON - New Architecture")
    print("="*70)
    
    birth = BirthProfile(
        birth_year=1990,
        region="Urban",
        family_class=0.6,
        parents_education=0.6,
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
    
    base_world = BaseWorldState(year=birth.birth_year, base_year=1949)
    china_model = ChinaCountryModel(base_world, birth.birth_year)
    china_cities = create_china_cities()
    
    results = []
    
    for city_name, city_config in china_cities.items():
        city = City(city_config, china_model)
        
        simulator = LifeSimulatorV2(max_age=50, seed=42)
        result = simulator.simulate(birth, personality, china_model, city)
        
        person = result['person']
        results.append({
            'city': city_config.city_name,
            'wealth': person['wealth'],
            'income': person['income'],
            'education': person['education_level'],
            'risk_reward': city_config.risk_reward_ratio
        })
    
    print(f"\n{'City':<15} {'Wealth':<15} {'Income':<15} {'Education':<12} {'Risk/Reward'}")
    print("-"*70)
    
    for r in results:
        print(f"{r['city']:<15} ${r['wealth']:>12,.2f}  ${r['income']:>12,.2f}  {r['education']:>10.3f}  {r['risk_reward']:>10.2f}")


if __name__ == "__main__":
    demo_new_architecture()
    compare_cities_new_architecture()
    
    print("\n" + "="*70)
    print("ARCHITECTURE SUMMARY")
    print("="*70)
    print("""
Three-Layer Architecture:

1. Base World Layer (Universal Laws)
   - Pareto Principle (80/20 rule)
   - Kondratiev Cycles (long-term economic waves)
   - Economic cycles, technology, inequality
   - Applies to ALL countries

2. Country Layer (National Policies)
   - Country-specific policies (e.g., Reform & Opening, One-Child Policy)
   - Era transitions
   - Window mechanisms
   - Applies to ALL cities in that country

3. City Layer (Local Context)
   - City-specific characteristics
   - Income ceilings, living costs
   - Risk/reward ratios
   - Mobility thresholds
   - Unique to each city

Effects cascade: Base World -> Country -> City -> Person
    """)

