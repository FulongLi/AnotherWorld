# China World Model - Engineering Specification

## Overview

The China World Model implements a structured representation of major Chinese city development since 1949, based on engineering modeling principles rather than general historical narrative.

## Core Design Principle

> **"Highly window-dependent leap-type social environment"**

Key characteristics:
- **Centralized Development** (集中式发展)
- **Stage-based Leaps** (阶段性跃迁)
- **Path Dependence** (路径依赖)
- **Intergenerational Breaks** (代际断裂)

## Architecture

### 1. Six Distinct Eras (时间分段)

Each era represents a complete probability distribution shift:

#### Era 1: Establishment (1949-1957)
- **State Building Period | Low Mobility, Strong Organization**
- City function: Political/Industrial/Administrative
- Individual fate highly bound to organization
- Individual choice ≈ extremely low

**Parameters:**
```yaml
social_mobility: 0.15
inequality: 0.10
risk_reward_ratio: 0.2
education_return: 0.3
market_freedom: 0.2
```

**Key Variable:** Whether absorbed into the system

#### Era 2: Turbulence (1958-1977)
- **High Turbulence Period | Systemic Uncertainty**
- Urban development stagnated or regressed
- Education system ineffective
- Individual ability decoupled from returns

**Parameters:**
```yaml
social_mobility: 0.05
system_shock: 0.9
education_return: 0.1
health_risk: 0.8
```

**Key Insight:** Effort produces almost no positive feedback

#### Era 3: Reform Early (1978-1991)
- **Early Reform Period | First Window**
- Cities regain economic function
- Individual path choices emerge
- Urban-rural gap widens

**Parameters:**
```yaml
social_mobility: 0.45
risk_reward_ratio: 1.5
education_return: 0.8
inequality: 0.4
```

**Key Insight:** First generation of leap-makers born

#### Era 4: Urban Boom (1992-2007)
- **Urban Explosion Period | Golden Ascension Channel**
- Real estate / Manufacturing / Foreign trade
- Sharp city tier differentiation
- Education becomes core threshold

**Parameters:**
```yaml
social_mobility: 0.7
education_return: 1.2
asset_return: 1.8
inequality: 0.6
```

**Key Insight:** Most important leap window - missing this locks life trajectory

#### Era 5: Structure Solidify (2008-2019)
- **Structure Solidification | Declining Effort Returns**
- Housing prices become intergenerational barrier
- Highly concentrated urban resources
- Involution becomes explicit

**Parameters:**
```yaml
social_mobility: 0.35
education_return: 0.9
asset_entry_cost: 0.9
stress_factor: 0.7
```

**Key Insight:** Individual effort still matters, but wrong direction = ineffective

#### Era 6: New Uncertainty (2020-present)
- **Uncertain New Era | Risk Diffusion**
- Pandemic impact
- Industry volatility
- Stability becomes advantage again

**Parameters:**
```yaml
social_mobility: 0.25
system_volatility: 0.8
risk_penalty: 0.6
mental_health_weight: 1.2
```

**Key Insight:** Mental state becomes core survival variable

### 2. Four City Tiers (大城市分层)

#### Beijing (政治/资源中心)
- **Political/Resource Center**
- Advantages: Policy, education, system positions
- Limitations: High difficulty for non-locals

**Parameters:**
```yaml
policy_bonus: +0.4
market_freedom: -0.2
elite_competition: +0.6
income_ceiling: high
living_cost: very_high
mobility_threshold: high
```

**Suitable for:** System route, high education

#### Shanghai (金融/规则中心)
- **Financial/Rule Center**
- Advantages: Institutionalized, stable professional returns
- Limitations: Extremely high living costs

**Parameters:**
```yaml
income_ceiling: high
living_cost: very_high
mobility_threshold: high
risk_reward_ratio: 0.8
```

**Suitable for:** Professionals, long-termists

#### Shenzhen (技术/冒险中心)
- **Tech/Risk Center**
- Advantages: Non-origin friendly
- Limitations: High volatility, fast elimination

**Parameters:**
```yaml
risk_reward_ratio: +0.8
startup_success_rate: high_variance
age_penalty: after_35
mobility_threshold: low
```

**Suitable for:** High risk preference
**Note:** Easiest to get rich, fastest to fall

#### Guangzhou (商业/中庸型)
- **Commercial/Moderate**
- Advantages: Relatively low survival pressure
- Limitations: Difficult top-tier leap

**Parameters:**
```yaml
stability_bonus: +0.3
elite_path_probability: low
```

**Suitable for:** Stable life, multi-generational continuity

## Key Engineering Mechanisms

### 1. One-Time Window (一次性窗口)

```python
if window_open and missed:
    mobility *= 0.3  # Permanent reduction
```

**Implementation:**
- Windows open during Reform Early (1978-1991) and Urban Boom (1992-2007)
- Missing window creates permanent mobility multiplier reduction
- Once missed, cannot be recovered

### 2. Intergenerational Break (代际断裂)

**Key Variables:**
- `parent_assets`: Parent generation assets
- `property_owned`: Whether person owns property
- `property_value`: Property value

**Mechanism:**
- Parent assets ≠ child ability
- Property variable directly affects next generation starting point
- Property ownership provides intergenerational advantage (0-0.5 modifier)

### 3. City Selection = Probability Distribution Switch

Changing cities is not a numerical adjustment, but:

> **Switching entire probability distribution**

**Implementation:**
- Each city has distinct parameter set
- City change affects all action outcomes
- Mobility threshold, risk/reward, living costs all change

## Usage Example

```python
from models.person import BirthProfile, Personality
from models.world_china import ChinaCity
from engine.simulator_china import ChinaLifeSimulator

# Create birth profile
birth = BirthProfile(
    birth_year=1990,
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

# Run simulation
simulator = ChinaLifeSimulator(max_age=60, seed=42)
result = simulator.simulate(
    birth, 
    personality, 
    city=ChinaCity.SHENZHEN,
    parent_assets=50000
)

# Access results
china_world = result['china_world']
print(f"Era: {china_world['era']}")
print(f"Social Mobility: {china_world['social_mobility']}")
print(f"Window Missed: {china_world['window_missed']}")
print(f"Property Owned: {china_world['property_owned']}")
```

## Model Validation

The model demonstrates:

1. **Era Effects**: Different birth eras produce significantly different outcomes
2. **City Effects**: Shenzhen shows highest wealth accumulation (high risk/reward)
3. **Window Mechanism**: Missing window creates permanent mobility reduction
4. **Property Impact**: Property ownership significantly affects intergenerational advantage

## Files

- `models/world_china.py`: China world state model
- `engine/simulator_china.py`: China-specific simulator
- `examples/china_demo.py`: Demonstration script

## Notes

This model is based on engineering modeling principles and structured conclusions, not general historical narrative. It focuses on quantifiable parameters that directly affect life trajectories in the simulation system.

