# AnotherWorld - 快速参考手册

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行通用模型
python main.py

# 运行中国模型演示
python examples/china_demo.py
```

---

## 📂 核心文件速查

### 模型层 (Models)
| 文件 | 核心类 | 说明 |
|------|--------|------|
| `person.py` | `BirthProfile`, `PersonState`, `Personality` | 人物数据模型 |
| `world.py` | `WorldState` | 通用世界模型 + 二八定律 |
| `world_china.py` | `ChinaWorldState`, `ChinaEra`, `ChinaCity` | 中国世界模型（6时代4城市） |
| `family_policy.py` | `FamilyPolicyEngine`, `FamilyState` | 计划生育政策模型 |

### 引擎层 (Engine)
| 文件 | 核心类 | 说明 |
|------|--------|------|
| `simulator.py` | `LifeSimulator` | 通用人生模拟器 |
| `simulator_china.py` | `ChinaLifeSimulator` | 中国版模拟器 |
| `decision_engine.py` | `DecisionEngine`, `Action` | 行为决策引擎 |
| `transition_engine.py` | `TransitionEngine` | 状态转移引擎 |

### 叙事层 (Narrative)
| 文件 | 核心类 | 说明 |
|------|--------|------|
| `life_events.py` | `LifeEventDetector`, `LifeEvent` | 人生事件检测 |
| `summary_generator.py` | `SummaryGenerator` | 人生总结生成 |

---

## 🎯 关键概念

### 二八定律 (Pareto Principle)
- **位置**: `models/world.py`
- **效果**: 前20%获得4x财富/机会乘数
- **文档**: `docs/PARETO_PRINCIPLE.md`

### 中国世界模型
- **位置**: `models/world_china.py`
- **6个时代**: 1949-1957, 1958-1977, 1978-1991, 1992-2007, 2008-2019, 2020+
- **4个城市**: 北京、上海、深圳、广州
- **窗口机制**: 错过窗口永久降低流动性
- **文档**: `docs/CHINA_WORLD_MODEL.md`

### 计划生育政策
- **位置**: `models/family_policy.py`
- **5个时期**: Pre-Control, Soft Control, One-Child, Two-Child, Three-Child+
- **独生子女效应**: 1.4x教育投资，但更高压力
- **文档**: `docs/FAMILY_POLICY_MODULE.md`

---

## 🔧 常用操作

### 创建人物
```python
from models.person import BirthProfile, Personality

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
    risk_preference=0.5,
    social_drive=0.6,
    resilience=0.7
)
```

### 运行通用模拟
```python
from engine.simulator import LifeSimulator

simulator = LifeSimulator(max_age=80, seed=42)
result = simulator.simulate(birth, personality)
```

### 运行中国模拟
```python
from engine.simulator_china import ChinaLifeSimulator
from models.world_china import ChinaCity

simulator = ChinaLifeSimulator(max_age=60, seed=42)
result = simulator.simulate(birth, personality, ChinaCity.SHENZHEN, parent_assets=0)
```

---

## 📊 行为类型 (Actions)

| 行为 | 说明 | 主要效果 |
|------|------|----------|
| `STUDY` | 学习 | 提升教育、技能 |
| `WORK` | 工作 | 增加收入、财富 |
| `REST` | 休息 | 恢复能量、降低压力 |
| `MOVE` | 移动/换城市 | 改变机会（中国模型：切换概率分布） |
| `RISK` | 冒险/创业 | 高风险高回报 |
| `RELATION` | 建立关系 | 提升社交资本 |

---

## 🏙️ 中国城市特性

| 城市 | 类型 | 特点 |
|------|------|------|
| 北京 | 政治/资源中心 | 政策加成高，竞争激烈 |
| 上海 | 金融/规则中心 | 收入上限高，生活成本极高 |
| 深圳 | 技术/冒险中心 | 高风险高回报，年龄惩罚明显 |
| 广州 | 商业/中庸型 | 稳定性加成，精英路径概率低 |

---

## 📈 时代特征速查

| 时代 | 年份 | 社会流动性 | 关键特征 |
|------|------|-----------|----------|
| 国家建立期 | 1949-1957 | 0.15 | 低流动、强组织 |
| 高度动荡期 | 1958-1977 | 0.05 | 系统冲击、教育失效 |
| 改革开放早期 | 1978-1991 | 0.45 | 第一轮窗口 ⭐ |
| 城市爆发期 | 1992-2007 | 0.70 | 黄金窗口 ⭐⭐ |
| 结构固化期 | 2008-2019 | 0.35 | 努力回报下降 |
| 不确定新时代 | 2020+ | 0.25 | 心理健康权重增加 |

---

## 🔑 关键机制

### 窗口机制（一次性机会）
- **触发时代**: 1978-1991, 1992-2007
- **错过后果**: 流动性永久降低 ×0.3
- **代码位置**: `models/world_china.py` → `_check_window_status()`

### 代际断裂
- **房产影响**: 拥有房产提供0-0.3优势
- **父代资产**: 提供0-0.2优势
- **代码位置**: `models/world_china.py` → `get_intergenerational_advantage()`

### 独生子女效应
- **教育投资**: 1.4x乘数
- **父母压力**: +0.3
- **孤独感**: +0.15
- **中年负担**: 45+岁，压力+0.2，照护负担+0.3
- **代码位置**: `models/family_policy.py` → `apply_only_child_effects()`

---

## 📝 输出格式

### 模拟结果结构
```python
{
    'person': {
        'age': 60,
        'wealth': 50000,
        'education_level': 0.8,
        # ... 其他属性
    },
    'china_world': {
        'era': 'URBAN_BOOM',
        'city': 'shenzhen',
        'social_mobility': 0.7,
        'window_missed': False,
        'family_state': {
            'is_only_child': True,
            'siblings': 0,
            'parental_pressure': 0.8
        }
    },
    'events': [...],
    'summary': {...}
}
```

---

## 🐛 调试技巧

1. **使用固定种子**: `LifeSimulator(seed=42)` 确保可复现
2. **查看中间状态**: 在模拟循环中添加打印
3. **检查政策时期**: `FamilyPolicyEngine.get_policy_for_year(year)`
4. **验证窗口状态**: `china_world.window_open`, `china_world.window_missed`

---

## 📚 完整文档

- **项目结构**: `PROJECT_STRUCTURE.md` - 详细结构说明
- **中国模型**: `docs/CHINA_WORLD_MODEL.md`
- **家庭政策**: `docs/FAMILY_POLICY_MODULE.md`
- **二八定律**: `docs/PARETO_PRINCIPLE.md`

---

**快速更新**: 查看 `PROJECT_STRUCTURE.md` 获取完整信息

