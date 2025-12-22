# System Architecture - Three-Layer Design

## Overview

The system uses a **three-layer architecture** that separates universal economic laws from country-specific policies and city-level characteristics.

```
┌─────────────────────────────────────────┐
│      Layer 3: City (Local Context)     │
│  - Income ceilings, living costs        │
│  - Risk/reward ratios                  │
│  - Mobility thresholds                 │
│  - Unique to each city                  │
└─────────────────────────────────────────┘
                    ▲
┌─────────────────────────────────────────┐
│   Layer 2: Country (National Policies)   │
│  - Reform & Opening (China)             │
│  - One-Child Policy (China)             │
│  - Era transitions                      │
│  - Window mechanisms                    │
│  - Applies to ALL cities in country    │
└─────────────────────────────────────────┘
                    ▲
┌─────────────────────────────────────────┐
│  Layer 1: Base World (Universal Laws)   │
│  - Pareto Principle (80/20 rule)        │
│  - Kondratiev Cycles                    │
│  - Economic cycles                      │
│  - Technology, inequality               │
│  - Applies to ALL countries             │
└─────────────────────────────────────────┘
```

---

## Layer 1: Base World (Universal Laws)

**File**: `models/world_base.py`

### Purpose
Universal economic laws that apply to **all countries** regardless of political system or policies.

### Core Components

#### 1. Pareto Principle (80/20 Rule)
- **Wealth Distribution**: Top 20% get 4x multiplier (80% of wealth)
- **Opportunity Access**: Top 20% get 4x multiplier (80% of opportunities)
- **Technology Benefits**: Top 20% capture 80% of tech gains
- **Social Mobility**: Only 20% can achieve significant upward mobility

#### 2. Kondratiev Cycles
- **Long-term economic waves** (~50-60 years per cycle)
- **Four phases**:
  - Recovery (0.0-0.25): 1.0-1.2x multiplier
  - Expansion (0.25-0.5): 1.2-1.5x multiplier
  - Stagnation (0.5-0.75): 0.8-1.0x multiplier
  - Recession (0.75-1.0): 0.5-0.8x multiplier

#### 3. Economic Fundamentals
- **Economic Cycle**: Short-term cycles (10-year period)
- **Technology Level**: Generally increases over time
- **Inequality**: Tends to increase (Pareto reinforcement)
- **Social Mobility**: Inversely related to inequality

### Key Methods
- `get_wealth_multiplier(person_score)`: Pareto-based wealth accumulation
- `get_opportunity_multiplier(person_score)`: Pareto-based opportunity access
- `get_tech_benefit_multiplier(person_score)`: Pareto-based tech benefits
- `calculate_person_score(...)`: Determines elite status
- `get_kondratiev_effect()`: Long-wave economic effect

---

## Layer 2: Country (National Policies)

**File**: `models/country_base.py`, `models/country_china.py`

### Purpose
Country-specific policies and institutions that affect **all cities** within that country.

### Base Class: `CountryModel`
Abstract base class that all country models inherit from.

**Key Methods**:
- `get_era_for_year(year)`: Get current era
- `get_era_config(era)`: Get era-specific configuration
- `apply_country_modifiers(person, action_type)`: Apply country effects to actions
- `get_effective_social_mobility()`: Country-adjusted mobility
- `get_effective_inequality()`: Country-adjusted inequality

### China Implementation: `ChinaCountryModel`

#### Policies Implemented
1. **Reform & Opening (改革开放)**
   - Window periods: 1978-1991, 1992-2007
   - Permanent mobility reduction if window missed

2. **One-Child Policy (计划生育)**
   - Integrated via `FamilyPolicyEngine`
   - Affects family structure, competition intensity

3. **Era System**
   - 6 distinct eras with different parameters
   - Each era represents complete probability distribution shift

#### China-Specific Features
- **Window Mechanism**: One-time opportunities, permanent consequences
- **Era Transitions**: Complete parameter changes
- **Family Policy Integration**: Automatic family structure generation

---

## Layer 3: City (Local Context)

**File**: `models/city.py`

### Purpose
City-specific characteristics that create **local probability distributions** within the country framework.

### City Configuration

#### Economic Characteristics
- **Income Ceiling**: "low", "medium", "high"
- **Living Cost**: "low", "medium", "high", "very_high"

#### Policy Characteristics
- **Policy Bonus**: Level of policy support (0-1)
- **Market Freedom**: Relative to country base

#### Social Characteristics
- **Elite Competition**: Competition intensity (0-1)
- **Mobility Threshold**: "low", "medium", "high"

#### Risk Characteristics
- **Risk/Reward Ratio**: Multiplier for risk-taking
- **Startup Success Rate**: "low", "medium", "high", "high_variance"
- **Age Penalty Age**: Age when age penalty starts

### Key Concept: Probability Distribution Switch

> **Changing cities is not a numerical adjustment, but switching entire probability distributions.**

When a person moves from one city to another:
- Income ceiling changes
- Living costs change
- Risk/reward ratios change
- Mobility thresholds change
- All action outcomes are recalculated

### Predefined Chinese Cities

| City | Type | Key Characteristics |
|------|------|---------------------|
| Beijing | Political/Resource | High policy bonus, high competition, very high cost |
| Shanghai | Financial/Rule | High income ceiling, very high cost, high competition |
| Shenzhen | Tech/Risk | High risk/reward (1.8x), low mobility threshold, age penalty at 35 |
| Guangzhou | Commercial/Stable | Medium income, medium cost, stability bonus |

---

## Data Flow

### Effect Cascade

```
Base World (Universal)
    ↓
    ├─→ Pareto multipliers applied
    ├─→ Kondratiev effects applied
    └─→ Economic cycles affect outcomes
    
Country Model (National)
    ↓
    ├─→ Era-specific modifiers
    ├─→ Policy effects (e.g., education return)
    ├─→ Window mechanisms
    └─→ Family policy integration
    
City Model (Local)
    ↓
    ├─→ Income ceiling multipliers
    ├─→ Living cost modifiers
    ├─→ Risk/reward adjustments
    └─→ Mobility threshold effects
    
Final Person State
```

### Example: Work Action

```python
# 1. Base calculation
base_income = (skill * 0.5 + education * 0.3 + economy * 0.2) * 1000

# 2. Base World effects
base_income *= kondratiev_effect  # Long-wave cycle
base_income *= pareto_wealth_multiplier  # 80/20 rule

# 3. Country effects
base_income *= country_era_modifier  # Era-specific return
base_income *= country_policy_modifier  # Policy effects

# 4. City effects
base_income *= city_income_multiplier  # Income ceiling
base_income *= city_policy_bonus  # City policy support

# Final income
person.income = base_income
```

---

## Implementation Files

### Base Layer
- `models/world_base.py`: `BaseWorldState` - Universal laws

### Country Layer
- `models/country_base.py`: `CountryModel` - Base class
- `models/country_china.py`: `ChinaCountryModel` - China implementation
- `models/family_policy.py`: `FamilyPolicyEngine` - Family policy (country-level)

### City Layer
- `models/city.py`: `City`, `CityConfig` - City models

### Engine Integration
- `engine/transition_engine.py`: Applies all three layers
- `engine/simulator_v2.py`: New architecture simulator

---

## Usage Example

```python
from models.world_base import BaseWorldState
from models.country_china import ChinaCountryModel
from models.city import City, create_china_cities
from engine.simulator_v2 import LifeSimulatorV2

# 1. Create base world (universal laws)
base_world = BaseWorldState(year=1990, base_year=1949)

# 2. Create country model (China policies)
china_model = ChinaCountryModel(base_world, 1990)

# 3. Create city (local context)
china_cities = create_china_cities()
shenzhen = City(china_cities["shenzhen"], china_model)

# 4. Run simulation
simulator = LifeSimulatorV2(max_age=60, seed=42)
result = simulator.simulate(birth, personality, china_model, shenzhen)
```

---

## Design Principles

### 1. Separation of Concerns
- **Universal laws** are separate from **country policies**
- **Country policies** are separate from **city characteristics**
- Each layer can be modified independently

### 2. Extensibility
- Add new countries by implementing `CountryModel`
- Add new cities by creating `CityConfig`
- Base world laws remain constant

### 3. Cascading Effects
- Effects cascade from base → country → city
- Each layer modifies the previous layer's output
- Final outcome is product of all layers

### 4. Probability Distribution Switching
- Cities represent different probability distributions
- Moving cities = switching distributions
- Not just numerical adjustments

---

## Future Extensions

### Adding New Countries
1. Create new country model class inheriting from `CountryModel`
2. Implement country-specific policies
3. Define country eras and transitions
4. Create country-specific cities

### Adding New Cities
1. Create `CityConfig` with city characteristics
2. Add to country's city dictionary
3. City automatically integrates with country model

### Adding New Universal Laws
1. Add to `BaseWorldState`
2. Automatically applies to all countries
3. All country models inherit the effect

---

**This architecture ensures that universal economic laws, country-specific policies, and city-level characteristics are properly separated and can be extended independently.**

