"""
Demonstration of Family Policy effects in China World Model
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.person import BirthProfile, Personality
from models.world_china import ChinaCity
from engine.simulator_china import ChinaLifeSimulator


def compare_only_child_vs_siblings():
    """Compare only child vs multiple siblings"""
    print("="*70)
    print("FAMILY POLICY DEMONSTRATION - Only Child vs Siblings")
    print("="*70)
    
    # Same birth profile, but different family structures
    birth = BirthProfile(
        birth_year=1990,  # One-child policy era
        region="Urban",
        family_class=0.6,
        parents_education=0.6,
        family_stability=0.7,
        genetic_health=0.7,
        cognitive_potential=0.6
    )
    
    personality = Personality(
        openness=0.6,
        conscientiousness=0.6,  # Will be modified by only-child effect
        risk_preference=0.5,
        social_drive=0.6,  # Will be modified by only-child effect
        resilience=0.6  # Will be modified by only-child effect
    )
    
    # Note: Family structure is randomly generated, so we'll run multiple times
    # and compare statistics
    print("\nRunning simulations (family structure is randomly determined)...")
    print("Note: In one-child policy era, ~75% chance of being only child\n")
    
    results_only_child = []
    results_siblings = []
    
    for seed in range(10):
        simulator = ChinaLifeSimulator(max_age=50, seed=seed)
        result = simulator.simulate(birth, personality, ChinaCity.BEIJING, 0)
        
        china_world = result['china_world']
        if china_world.get('family_state', {}).get('is_only_child', False):
            results_only_child.append(result)
        else:
            results_siblings.append(result)
    
    if not results_only_child or not results_siblings:
        print("Not enough variation in family structure. Running with fixed seeds...")
        # Force different family structures by manipulating the random generation
        # This is a simplified demonstration
        return
    
    # Compare averages
    print(f"\nOnly Child Results (n={len(results_only_child)}):")
    avg_wealth_oc = sum(r['person']['wealth'] for r in results_only_child) / len(results_only_child)
    avg_education_oc = sum(r['person']['education_level'] for r in results_only_child) / len(results_only_child)
    avg_stress_oc = sum(r['person']['stress'] for r in results_only_child) / len(results_only_child)
    
    print(f"  Average Wealth: ${avg_wealth_oc:,.2f}")
    print(f"  Average Education: {avg_education_oc:.3f}")
    print(f"  Average Stress: {avg_stress_oc:.3f}")
    
    print(f"\nSiblings Results (n={len(results_siblings)}):")
    avg_wealth_sib = sum(r['person']['wealth'] for r in results_siblings) / len(results_siblings)
    avg_education_sib = sum(r['person']['education_level'] for r in results_siblings) / len(results_siblings)
    avg_stress_sib = sum(r['person']['stress'] for r in results_siblings) / len(results_siblings)
    
    print(f"  Average Wealth: ${avg_wealth_sib:,.2f}")
    print(f"  Average Education: {avg_education_sib:.3f}")
    print(f"  Average Stress: {avg_stress_sib:.3f}")


def compare_policy_eras():
    """Compare different policy eras"""
    print("\n" + "="*70)
    print("FAMILY POLICY DEMONSTRATION - Policy Era Comparison")
    print("="*70)
    
    eras_to_test = [
        (1960, "Pre-Control (1960)"),
        (1985, "One-Child Strict (1985)"),
        (2018, "Two-Child (2018)"),
        (2023, "Three-Child+ (2023)")
    ]
    
    results = []
    
    for birth_year, era_name in eras_to_test:
        print(f"\n{'='*70}")
        print(f"Testing: {era_name}")
        print(f"{'='*70}")
        
        birth = BirthProfile(
            birth_year=birth_year,
            region="Urban",
            family_class=0.6,
            parents_education=0.6,
            family_stability=0.7,
            genetic_health=0.7,
            cognitive_potential=0.6
        )
        
        personality = Personality(
            openness=0.6,
            conscientiousness=0.6,
            risk_preference=0.5,
            social_drive=0.6,
            resilience=0.6
        )
        
        simulator = ChinaLifeSimulator(max_age=min(40, 2024 - birth_year), seed=42)
        result = simulator.simulate(birth, personality, ChinaCity.BEIJING, 0)
        
        person = result['person']
        china_world = result['china_world']
        family_state = china_world.get('family_state', {})
        family_policy = china_world.get('family_policy', {})
        
        print(f"Family Policy: {family_policy.get('policy', 'N/A')}")
        print(f"Only Child: {family_state.get('is_only_child', False)}")
        print(f"Siblings: {family_state.get('siblings', 0)}")
        print(f"Parental Pressure: {family_state.get('parental_pressure', 0):.3f}")
        print(f"Competition Intensity: {china_world.get('competition_intensity', 0):.3f}")
        print(f"Final Education: {person['education_level']:.3f}")
        print(f"Final Stress: {person['stress']:.3f}")
        if person['age'] > 45:
            print(f"Caregiver Burden: {family_state.get('caregiver_burden', 0):.3f}")
        
        results.append({
            'era': era_name,
            'only_child': family_state.get('is_only_child', False),
            'siblings': family_state.get('siblings', 0),
            'competition': china_world.get('competition_intensity', 0),
            'education': person['education_level'],
            'stress': person['stress']
        })
    
    # Summary
    print("\n" + "="*70)
    print("POLICY ERA COMPARISON SUMMARY")
    print("="*70)
    print(f"{'Era':<30} {'Only Child':<12} {'Siblings':<10} {'Competition':<12} {'Education':<12} {'Stress'}")
    print("-"*70)
    
    for r in results:
        print(f"{r['era']:<30} {str(r['only_child']):<12} {r['siblings']:<10} {r['competition']:<12.3f} {r['education']:<12.3f} {r['stress']:.3f}")


def middle_age_caregiver_demo():
    """Demonstrate caregiver burden in middle age"""
    print("\n" + "="*70)
    print("FAMILY POLICY DEMONSTRATION - Middle Age Caregiver Burden")
    print("="*70)
    print("\nComparing only child vs siblings at age 50+\n")
    
    birth = BirthProfile(
        birth_year=1970,  # Will be in one-child era when they have children
        region="Urban",
        family_class=0.6,
        parents_education=0.6,
        family_stability=0.7,
        genetic_health=0.7,
        cognitive_potential=0.6
    )
    
    personality = Personality(
        openness=0.6,
        conscientiousness=0.6,
        risk_preference=0.5,
        social_drive=0.6,
        resilience=0.6
    )
    
    simulator = ChinaLifeSimulator(max_age=55, seed=42)
    result = simulator.simulate(birth, personality, ChinaCity.BEIJING, 0)
    
    person = result['person']
    china_world = result['china_world']
    family_state = china_world.get('family_state', {})
    
    print(f"Age: {person['age']}")
    print(f"Is Only Child: {family_state.get('is_only_child', False)}")
    print(f"Siblings: {family_state.get('siblings', 0)}")
    print(f"Caregiver Burden: {family_state.get('caregiver_burden', 0):.3f}")
    print(f"Stress: {person['stress']:.3f}")
    print(f"Mental Health: {person['mental_health']:.3f}")
    
    if family_state.get('is_only_child', False):
        print("\n⚠️  Only child bears full caregiver burden - structural stress source")
    else:
        print(f"\n[OK] Burden shared among {family_state.get('siblings', 0) + 1} siblings")


if __name__ == "__main__":
    compare_policy_eras()
    middle_age_caregiver_demo()
    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)
    print("""
1. One-child policy era (1979-2015) creates highest competition intensity
2. Only children receive 1.4x education investment but face higher stress
3. Middle age (45+) brings structural penalty for only children (caregiver burden)
4. Competition intensity combines family structure + city tier + era
5. Parental pressure is significantly higher for only children
    """)

