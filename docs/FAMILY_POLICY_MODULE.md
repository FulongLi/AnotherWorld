# Family Policy Module - One-Child Policy and Demography

## Overview

The Family Policy Module models the one-child policy and its systemic effects on family structure, resource allocation, competition intensity, and intergenerational pressure. It is **not** just about "how many children," but about four critical dimensions:

1. **Family Sibling Distribution**
2. **Resource Density per Child**
3. **Peer Competition Intensity**
4. **Structural Pressure in Middle Age**

## Core Design Principle

> Family planning policy is not a "population control variable," but a **systemic constraint that deeply reshapes family structure, competition intensity, intergenerational resource allocation, and psychological state**.

## Policy Periods

### 1. Pre-Control (1949-1970)
- **Natural Fertility Period**
- No systematic restrictions
- Large families common

**Parameters:**
```yaml
fertility_cap: 4.5
enforcement_strength: 0.0
only_child_probability: 0.05
```

**System Effects:**
- Multiple children → resource dilution
- Weak peer competition
- Strong family support network
- Suitable for: "Group survival" in risk society

### 2. Soft Control (1971-1978)
- **"Late, Sparse, Few" Transition Period**
- Urban families begin to shrink
- Education resource density begins to rise

**Parameters:**
```yaml
fertility_cap: 2.8
enforcement_strength: 0.4
only_child_probability: 0.25
```

### 3. One-Child Strict (1979-2015) ⚠️ **CORE PERIOD**
- **Strict One-Child Policy Era**
- Most impactful period in the system

**Parameters:**
```yaml
fertility_cap: 1.1
enforcement_strength: 0.9
penalty_cost: 0.8
only_child_probability: 0.75
```

**Must-Link Variable Changes:**
```python
if is_only_child:
    education_investment *= 1.4
    parental_expectation += 0.3
    loneliness += 0.2
    resilience -= 0.1
```

**Intergenerational Structure Changes:**
- 4-2-1 family structure (4 grandparents, 2 parents, 1 child)
- Upward pressure concentrated on single individual
- Extremely low failure tolerance

📌 **This is the root module of involution and psychological pressure**

### 4. Two-Child (2016-2020)
- **Two-Child Policy Period**
- Policy relaxed, but structure not restored
- Urban birth intention still low

**Parameters:**
```yaml
fertility_cap: 1.6
enforcement_strength: 0.3
only_child_probability: 0.45
```

### 5. Three-Child+ (2021-present)
- **Three-Child and Low Fertility Trap**
- Policy allows more, but behavior doesn't match

**Parameters:**
```yaml
fertility_cap: 1.3
enforcement_strength: 0.1
only_child_probability: 0.55
```

📌 Policy allows ≠ behavior occurs  
📌 This is a **typical case of economic structure constraining policy**

## Family State Model

```python
@dataclass
class FamilyState:
    siblings: int
    is_only_child: bool
    parental_pressure: float  # 0-1
    intergenerational_support: float  # 0-1
    caregiver_burden: float  # 0-1
    family_wealth_per_child: float
```

## Direct Effects on Person State

### 1. Resource Allocation

```python
education_investment = family_wealth / (siblings + 0.5)
```

Only children receive **1.4x education investment multiplier**.

### 2. Psychological and Personality Adjustments

```python
if is_only_child:
    conscientiousness += 0.1
    social_drive -= 0.1
    loneliness += 0.15
```

(Not value judgments, but **statistical tendencies**)

### 3. Middle-Age Penalty (Very Important)

```python
if age > 45 and is_only_child:
    stress += 0.2
    caregiver_burden += 0.3
```

👉 **This is the structural source of only-child middle-age crisis**

### 4. Competition Intensity

```python
competition_intensity = base + only_child_effect + city_tier_effect + era_effect
```

- Only child: +0.2
- Tier 1 city: +0.3
- One-child era: +0.2
- Maximum: 1.0

## Integration with City Model

### Tier 1 City Amplification

```python
if city_level == "Tier1" and is_only_child:
    competition_intensity += 0.3
    marriage_pressure += 0.2
```

## Engineering-Level Conclusions

### ✅ China Model Must Include:

1. **Only-child marker (bool)**
2. **Sibling count**
3. **Intergenerational pressure variable**
4. **Structural penalty in middle age**

**Otherwise:**
- Involution cannot be explained
- Psychological state evolution doesn't hold
- China model will be "Western model with different skin"

## Implementation Files

- `models/family_policy.py`: Core family policy engine
- `models/world_china.py`: Integration with China world model
- `engine/simulator_china.py`: Application in simulation loop
- `examples/family_policy_demo.py`: Demonstration script

## Key Mechanisms

### Resource Allocation
- Only children: 1.4x education investment
- Multiple siblings: Resource divided

### Competition Intensity
- Combines family structure + city tier + era
- One-child era + Tier 1 city + only child = maximum competition (1.0)

### Caregiver Burden
- Increases when parents reach 60+
- Only children bear full burden
- Siblings share burden

### Middle-Age Structural Penalty
- Age > 45: Only children face +0.2 stress, +0.3 caregiver burden
- This creates the "middle-age crisis" for only children

## Usage Example

```python
from models.family_policy import FamilyPolicyEngine, FamilyState

# Generate family structure
family_state = FamilyPolicyEngine.generate_family_structure(
    birth_year=1990,
    family_wealth=100000,
    is_urban=True
)

# Apply only-child effects
FamilyPolicyEngine.apply_only_child_effects(
    person_state,
    personality,
    family_state,
    age=25,
    city_tier="tier1"
)

# Update caregiver burden
FamilyPolicyEngine.update_caregiver_burden(
    family_state,
    age=50,
    parent_age=78
)
```

