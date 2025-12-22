# Life Trajectory Simulator (LTS)

**Version**: v1.0  
**Status**: MVP - Runnable  
**Language**: Python 3.11+

A single-person, single-run life trajectory generation system that simulates a complete life from birth to death, with player choices at key stages, macro-environmental constraints, and structured life summaries.

## ⚠️ Important Note

> This system does **NOT** provide real-life advice.  
> Its output is for thought experiments and narrative generation only.

## Features

- **Complete Life Simulation**: From birth to death (0-100 years)
- **Player Choices**: Make decisions at key life stages
- **World State**: Dynamic economic cycles, technology, social mobility
- **Pareto Principle Integration**: 80/20 rule affects wealth, opportunities, and social mobility
- **Life Events**: Automatic detection of significant life events
- **Narrative Generation**: Comprehensive life summaries and highlights
- **Reproducible**: Seed-based random number generation

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Run a random life simulation
python main.py

# Follow the prompts to customize or use defaults
```

## Project Structure

```
/lts
 ├── main.py                 # CLI entry point
 ├── config/
 │    └── constants.yaml     # Configuration constants
 ├── models/
 │    ├── person.py          # Person data models
 │    └── world.py           # World state model
 ├── engine/
 │    ├── simulator.py       # Main simulation loop
 │    ├── decision_engine.py # Action generation
 │    └── transition_engine.py # State transitions
 ├── narrative/
 │    ├── life_events.py     # Event detection
 │    └── summary_generator.py # Summary generation
 ├── utils/
 │    ├── rng.py             # Random number generation
 │    └── helpers.py         # Utility functions
 └── output/
      └── run_*.json         # Simulation results
```

## Core Concepts

### Birth Profile (Immutable)
- Birth year, region, family class
- Parents' education, family stability
- Genetic health, cognitive potential

### Person State (Mutable)
- Health, mental health, energy, stress
- Education level, skills (depth/width)
- Income, wealth, occupation
- Social capital, loneliness

### Personality (Slow-changing)
- Openness, conscientiousness
- Risk preference, social drive
- Resilience

### World State
- Economic cycle (sine wave)
- Technology level (increasing)
- Social mobility, inequality
- Conflict risk
- **Pareto Principle (80/20 Rule)**: Integrated throughout
  - 80% of wealth held by top 20% of population
  - 80% of opportunities concentrated in top 20%
  - 80% of technology benefits captured by top 20%
  - Only 20% can achieve significant social mobility

### Actions
- **STUDY**: Increase education and skills
- **WORK**: Earn income, build career
- **REST**: Recover energy, reduce stress
- **MOVE**: Change location/career
- **RISK**: Take risks (entrepreneurship)
- **RELATION**: Build relationships

## Example Output

```json
{
  "summary": {
    "summary": "This was a life that spanned 78 years...",
    "highlights": [
      "High Education Achievement",
      "Career Breakthroughs",
      "Strong Social Network"
    ],
    "statistics": {
      "total_events": 12,
      "event_by_category": {
        "health": 2,
        "career": 3,
        "social": 1,
        "economic": 1,
        "milestone": 5
      }
    }
  }
}
```

## Pareto Principle (80/20 Rule)

The simulation incorporates the Pareto Principle throughout:

### Wealth Distribution
- **Top 20% (Elite)**: Receive 4x wealth multiplier (80% of wealth / 20% of people)
- **Bottom 80%**: Share remaining 20% of wealth (0.25x multiplier)
- Inequality amplifies this effect over time

### Opportunity Access
- **Top 20%**: 4x opportunity multiplier (80% of opportunities)
- **Bottom 80%**: 0.25x opportunity multiplier (20% of opportunities)
- Affects career moves, risk-taking, and social mobility

### Technology Benefits
- **Top 20%**: Full tech benefits + bonus (capture 80% of tech gains)
- **Bottom 80%**: Reduced tech benefits (share 20% of tech gains)
- Technology growth increases inequality

### Social Mobility
- Only 20% of population can achieve significant upward mobility
- Higher inequality = lower mobility (harder to break into elite)
- Birth class matters more in high-inequality worlds

### Person Score Calculation
Elite status determined by:
- Birth family class (weighted by inequality level)
- Education level
- Skill depth
- Social capital
- Current wealth

## Life Events

Events are automatically detected based on state thresholds:

| Event | Condition |
|-------|-----------|
| Burnout | stress > 0.8 |
| Career Breakthrough | skill_depth > 0.7 & economic_cycle > 0 |
| Social Isolation | loneliness > 0.9 |
| Economic Hardship | wealth < 0 & economic_cycle < -0.5 |
| Educational Achievement | education_level >= 0.8 |
| Health Crisis | health < 0.3 |

## Development

### Running Tests
```bash
# TODO: Add pytest tests
pytest
```

### Code Structure
- **Models**: Data structures (dataclasses)
- **Engine**: Core simulation logic
- **Narrative**: Event detection and summary generation
- **Utils**: Helper functions and RNG

## Version Roadmap

| Version | Content |
|---------|---------|
| v1.0 | Single-person complete life (current) |
| v1.1 | Narrative optimization |
| v2.0 | Multiple parallel lives |
| v3.0 | Novel/game integration |

## License

This project is for educational and experimental purposes.

## Contributing

This is an MVP implementation. Contributions welcome for:
- More sophisticated event detection
- Enhanced narrative generation
- Additional action types
- World state variations

---

**Remember**: This is a simulation, not real-life advice. Use responsibly.
