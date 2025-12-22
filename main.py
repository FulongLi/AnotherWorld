"""
Main entry point for Life Trajectory Simulator
"""
import json
import random
from models.person import BirthProfile, Personality
from engine.simulator import LifeSimulator
from utils.helpers import generate_output_filename, save_json
from utils.rng import rng


def generate_random_birth_profile() -> BirthProfile:
    """Generate a random birth profile"""
    birth_year = random.randint(1950, 2000)
    regions = ['Urban', 'Suburban', 'Rural', 'Metropolitan']
    
    return BirthProfile(
        birth_year=birth_year,
        region=random.choice(regions),
        family_class=random.random(),
        parents_education=random.random(),
        family_stability=random.random(),
        genetic_health=0.5 + random.random() * 0.4,  # 0.5-0.9
        cognitive_potential=0.3 + random.random() * 0.5  # 0.3-0.8
    )


def generate_random_personality() -> Personality:
    """Generate a random personality"""
    return Personality(
        openness=random.random(),
        conscientiousness=random.random(),
        risk_preference=random.random(),
        social_drive=random.random(),
        resilience=random.random()
    )


def print_summary(result: dict):
    """Print a formatted summary to console"""
    summary = result['summary']
    
    print("\n" + "="*60)
    print("LIFE TRAJECTORY SIMULATION - SUMMARY")
    print("="*60)
    
    print(f"\n📖 Narrative:")
    print(f"   {summary['summary']}")
    
    print(f"\n⭐ Highlights:")
    for highlight in summary['highlights']:
        print(f"   • {highlight}")
    
    print(f"\n📊 Statistics:")
    stats = summary['statistics']
    print(f"   Total Events: {stats['total_events']}")
    print(f"   Events by Category:")
    for category, count in stats['event_by_category'].items():
        print(f"     - {category.capitalize()}: {count}")
    
    print(f"\n💰 Final State:")
    final = summary['final_state']
    print(f"   Age: {final['age']} years")
    print(f"   Health: {final['health']:.2f}")
    print(f"   Wealth: ${final['wealth']:,.2f}")
    print(f"   Income: ${final['income']:,.2f}")
    print(f"   Education: {final['education_level']:.2f}")
    print(f"   Social Capital: {final['social_capital']:.2f}")
    
    print(f"\n🎯 Key Events (first 5):")
    for event in summary['key_events'][:5]:
        print(f"   Age {event['age']}: {event['title']}")
        print(f"      {event['description']}")
    
    print("\n" + "="*60)


def main():
    """Main CLI interface"""
    print("="*60)
    print("LIFE TRAJECTORY SIMULATOR v1.0")
    print("="*60)
    print("\nThis system simulates a complete life trajectory.")
    print("It does NOT provide real-life advice.")
    print("="*60)
    
    # Get user preferences
    print("\nSimulation Options:")
    print("1. Random life (default)")
    print("2. Custom birth profile")
    
    choice = input("\nEnter choice (1 or 2, default 1): ").strip()
    
    if choice == "2":
        # Custom birth profile (simplified for MVP)
        print("\nUsing default custom profile...")
        birth = BirthProfile(
            birth_year=int(input("Birth year (1950-2000): ") or "1980"),
            region=input("Region (Urban/Suburban/Rural): ") or "Urban",
            family_class=float(input("Family class (0-1): ") or "0.5"),
            parents_education=float(input("Parents education (0-1): ") or "0.5"),
            family_stability=float(input("Family stability (0-1): ") or "0.7"),
            genetic_health=float(input("Genetic health (0.5-0.9): ") or "0.7"),
            cognitive_potential=float(input("Cognitive potential (0.3-0.8): ") or "0.6")
        )
    else:
        # Random birth profile
        seed = input("\nEnter random seed (or press Enter for random): ").strip()
        if seed:
            rng.set_seed(int(seed))
        birth = generate_random_birth_profile()
        print(f"\nGenerated random birth profile:")
        print(f"  Birth Year: {birth.birth_year}")
        print(f"  Region: {birth.region}")
        print(f"  Family Class: {birth.family_class:.2f}")
    
    # Generate personality
    personality = generate_random_personality()
    
    # Run simulation
    print("\n" + "-"*60)
    print("Running simulation...")
    print("-"*60)
    
    simulator = LifeSimulator(max_age=100)
    result = simulator.simulate(birth, personality)
    
    # Print summary
    print_summary(result)
    
    # Save results
    output_file = generate_output_filename()
    save_json(result, output_file)
    print(f"\n💾 Full results saved to: {output_file}")
    
    print("\n" + "="*60)
    print("Simulation complete!")
    print("="*60)


if __name__ == "__main__":
    main()

