"""
Quick test to verify the simulator works
"""
import sys
from models.person import BirthProfile, Personality
from engine.simulator import LifeSimulator

def test_simulation():
    """Run a quick test simulation"""
    print("Testing Life Trajectory Simulator...")
    
    # Create test birth profile
    birth = BirthProfile(
        birth_year=1980,
        region="Urban",
        family_class=0.6,
        parents_education=0.7,
        family_stability=0.8,
        genetic_health=0.75,
        cognitive_potential=0.65
    )
    
    # Create test personality
    personality = Personality(
        openness=0.7,
        conscientiousness=0.8,
        risk_preference=0.5,
        social_drive=0.6,
        resilience=0.7
    )
    
    # Run simulation
    print("Running simulation...")
    simulator = LifeSimulator(max_age=80, seed=42)
    result = simulator.simulate(birth, personality)
    
    # Check results
    assert result is not None
    assert 'person' in result
    assert 'summary' in result
    assert 'events' in result
    
    print(f"✓ Simulation completed successfully!")
    print(f"✓ Final age: {result['person']['age']}")
    print(f"✓ Total events: {len(result['events'])}")
    print(f"✓ Summary generated: {len(result['summary']['summary']) > 0}")
    
    print("\nTest passed! ✓")
    return True

if __name__ == "__main__":
    try:
        test_simulation()
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

