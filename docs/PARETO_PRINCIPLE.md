# Pareto Principle (80/20 Rule) Integration

## Overview

The Life Trajectory Simulator incorporates the Pareto Principle (80/20 rule) throughout the world model and action system. This creates a realistic representation of how wealth, opportunities, and benefits are distributed in society.

## Implementation Details

### 1. Wealth Distribution

**Formula**: `wealth_multiplier = get_wealth_multiplier(person_score)`

- **Elite (Top 20%)**: 
  - Base multiplier: 4.0x
  - With inequality: `4.0 * (1 + inequality * 0.5)`
  - Represents: 80% of wealth / 20% of people = 4x average

- **Non-Elite (Bottom 80%)**:
  - Base multiplier: 0.25x
  - With inequality: `0.25 * (1 - inequality * 0.3)`
  - Represents: 20% of wealth / 80% of people = 0.25x average

**Applied in**:
- `_apply_work()`: Income and wealth accumulation
- `_apply_risk()`: Success wealth gains

### 2. Opportunity Access

**Formula**: `opportunity_multiplier = get_opportunity_multiplier(person_score)`

- **Elite**: 4.0x multiplier (80% of opportunities)
- **Non-Elite**: 0.25x multiplier (20% of opportunities)

**Applied in**:
- `_apply_move()`: Success chance for career/location changes
- `_apply_risk()`: Success chance for entrepreneurship

### 3. Technology Benefits

**Formula**: `tech_multiplier = get_tech_benefit_multiplier(person_score)`

- **Elite**: `1.0 + tech_level * 0.5` (full benefits + bonus)
- **Non-Elite**: `0.3 + tech_level * 0.2` (reduced benefits)

**Applied in**:
- `_apply_study()`: Learning effectiveness from technology

### 4. Social Mobility

**Formula**: `mobility_chance = get_social_mobility_chance(person_score)`

- Only 20% of population can achieve significant upward mobility
- Mobility inversely related to inequality
- Higher inequality = lower mobility (harder to break into elite)

**Constraints**:
- Starting from bottom (< 0.3): Max 20% can move up significantly
- Middle class (0.3-0.6): Moderate chance
- Already elite (≥ 0.8): High chance to maintain

### 5. Person Score Calculation

**Formula**: `person_score = calculate_person_score(...)`

Combines:
- Birth family class (weighted by inequality: 0.2 + inequality * 0.3)
- Education level (30%)
- Skill depth (40%)
- Social capital (20%)
- Normalized wealth (10%)

**Elite Threshold**: Score ≥ 0.8 (top 20%)

## World State Effects

### Inequality Growth
- Technology growth increases inequality (benefits elite more)
- Inequality reduces social mobility
- Higher inequality = birth class matters more

### Social Mobility
- Mobility inversely related to inequality
- High mobility worlds: merit can overcome birth disadvantage
- Low mobility worlds: birth class dominates

## Code Locations

- **World Model**: `models/world.py`
  - `is_in_elite_percentile()`
  - `get_wealth_multiplier()`
  - `get_opportunity_multiplier()`
  - `get_tech_benefit_multiplier()`
  - `calculate_person_score()`
  - `get_social_mobility_chance()`

- **Transition Engine**: `engine/transition_engine.py`
  - All action methods apply Pareto multipliers

## Example Scenarios

### Scenario 1: Elite Person
- Person score: 0.85 (elite)
- Wealth multiplier: 4.0x
- Opportunity multiplier: 4.0x
- Tech multiplier: 1.5x
- Result: Rapid wealth accumulation, better opportunities

### Scenario 2: Non-Elite Person
- Person score: 0.4 (non-elite)
- Wealth multiplier: 0.25x
- Opportunity multiplier: 0.25x
- Tech multiplier: 0.5x
- Result: Slower progress, limited opportunities

### Scenario 3: High Inequality World
- Inequality: 0.9
- Elite advantage amplified: 4.0 * 1.45 = 5.8x
- Non-elite disadvantage: 0.25 * 0.73 = 0.18x
- Social mobility: Very low
- Result: Extreme wealth concentration

## Mathematical Foundation

The Pareto Principle states that roughly 80% of effects come from 20% of causes. In this simulation:

- **80% of wealth** → **20% of people** = **4x multiplier** for elite
- **20% of wealth** → **80% of people** = **0.25x multiplier** for non-elite
- **80% of opportunities** → **20% of people** = **4x multiplier** for elite
- **20% of opportunities** → **80% of people** = **0.25x multiplier** for non-elite

This creates a realistic power-law distribution where small advantages compound over time, and breaking into the elite becomes increasingly difficult as inequality grows.

