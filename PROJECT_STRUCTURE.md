# AnotherWorld - 项目结构总览

## 📁 项目目录结构

```
AnotherWorld/
├── 📄 main.py                    # 主程序入口（通用世界模型）
├── 📄 test_run.py                # 快速测试脚本
├── 📄 requirements.txt           # Python依赖包
├── 📄 README.md                  # 项目说明文档
├── 📄 PROJECT_STRUCTURE.md       # 本文件 - 项目结构总览
│
├── 📂 models/                    # 数据模型层
│   ├── __init__.py
│   ├── person.py                 # 人物模型（出生档案、状态、性格）
│   ├── world.py                  # 通用世界模型（旧版，向后兼容）
│   ├── world_base.py             # 底层世界模型（二八定律、康波周期）
│   ├── country_base.py           # 国家模型基类
│   ├── country_china.py           # 中国国家模型（6个时代、政策）
│   ├── city.py                   # 城市模型（在国家框架下）
│   └── family_policy.py          # 计划生育政策模型（5个政策时期）
│
├── 📂 engine/                    # 核心引擎层
│   ├── __init__.py
│   ├── simulator.py              # 通用人生模拟器（旧版）
│   ├── simulator_v2.py           # 新架构模拟器（三层架构）
│   ├── simulator_china.py        # 中国版模拟器（旧版，向后兼容）
│   ├── decision_engine.py        # 决策引擎（行为选择）
│   └── transition_engine.py      # 状态转移引擎（支持新架构）
│
├── 📂 narrative/                 # 叙事生成层
│   ├── __init__.py
│   ├── life_events.py            # 人生事件检测
│   └── summary_generator.py      # 人生总结生成
│
├── 📂 utils/                     # 工具函数层
│   ├── __init__.py
│   ├── rng.py                    # 随机数生成器（支持种子）
│   └── helpers.py                # 辅助函数（数据保存、工具函数）
│
├── 📂 config/                    # 配置文件
│   └── constants.yaml            # 模拟常量配置
│
├── 📂 examples/                  # 示例和演示
│   ├── architecture_demo.py      # 新架构演示（三层架构）
│   ├── china_demo.py             # 中国模型演示（时代、城市对比）
│   ├── family_policy_demo.py     # 计划生育政策演示
│   └── pareto_demo.py            # 二八定律演示
│
├── 📂 docs/                      # 文档目录
│   ├── ARCHITECTURE.md           # 系统架构说明（三层设计）
│   ├── CHINA_WORLD_MODEL.md      # 中国世界模型详细说明
│   ├── FAMILY_POLICY_MODULE.md   # 计划生育政策模块说明
│   └── PARETO_PRINCIPLE.md       # 二八定律实现说明
│
├── 📂 output/                    # 输出结果目录
│   └── run_*.json                # 模拟结果JSON文件
│
└── 📂 [Web版本文件]              # 前端Web版本（可选）
    ├── index.html                # Web界面
    ├── styles.css                # 样式文件
    ├── game.js                   # Web版游戏逻辑
    ├── world-era.js              # 世界/时代模块
    ├── life-state.js             # 人生状态引擎
    ├── behavior-choice.js        # 行为选择模块
    └── narrative.js              # 叙事生成模块
```

---

## 🏗️ 系统架构

### 新三层架构设计（重构后）

```
┌─────────────────────────────────────────┐
│      Layer 3: City (城市层)              │
│  - 收入上限、生活成本                     │
│  - 风险/回报比                           │
│  - 流动性阈值                            │
│  - 每个城市独特的概率分布                  │
└─────────────────────────────────────────┘
                    ▲
┌─────────────────────────────────────────┐
│   Layer 2: Country (国家层)              │
│  - 改革开放（中国）                       │
│  - 计划生育（中国）                       │
│  - 时代转换                               │
│  - 窗口机制                               │
│  - 影响该国家所有城市                      │
└─────────────────────────────────────────┘
                    ▲
┌─────────────────────────────────────────┐
│  Layer 1: Base World (底层逻辑)          │
│  - 二八定律                               │
│  - 康波周期                               │
│  - 经济周期                               │
│  - 技术、不平等                           │
│  - 适用于所有国家                          │
└─────────────────────────────────────────┘
```

### 叙事和引擎层

```
┌─────────────────────────────────────────┐
│          Narrative Layer                 │
│  (叙事生成层)                             │
│  - Life Events Detection                 │
│  - Summary Generation                    │
└─────────────────────────────────────────┘
                    ▲
┌─────────────────────────────────────────┐
│          Engine Layer                    │
│  (核心引擎层)                             │
│  - Simulator V2 (新架构)                  │
│  - Decision Engine (决策)                │
│  - Transition Engine (状态转移)           │
└─────────────────────────────────────────┘
```

---

## 📚 核心模块详解

### 1. Models（数据模型层）

#### `models/world_base.py` ⭐ **NEW**
- **BaseWorldState**: 底层世界模型
  - **二八定律**：财富分配、机会获取、技术收益
  - **康波周期**：长期经济波动（50-60年周期）
  - 经济周期、技术水平、不平等、社会流动性
  - **适用于所有国家**

#### `models/country_base.py` ⭐ **NEW**
- **CountryModel**: 国家模型基类（抽象类）
  - 定义国家模型的接口
  - 国家特定政策和制度
  - 时代转换机制

#### `models/country_china.py` ⭐ **NEW**
- **ChinaCountryModel**: 中国国家模型实现
  - **6个时代段**：国家建立期、动荡期、改革开放早期、城市爆发期、结构固化期、不确定新时代
  - **窗口机制**：一次性机会，错过永久影响
  - **政策集成**：改革开放、计划生育等

#### `models/city.py` ⭐ **NEW**
- **City**: 城市模型（在国家框架下）
  - 收入上限、生活成本
  - 风险/回报比
  - 流动性阈值
  - **概率分布切换**：换城市 = 切换整个概率分布

#### `models/person.py`
- **BirthProfile**: 不可变的出生档案
  - 出生年份、地区、家庭阶层
  - 父母教育、家庭稳定性
  - 遗传健康、认知潜力
- **Personality**: 性格特质（缓慢变化）
  - 开放性、尽责性、风险偏好、社交驱动、韧性
- **PersonState**: 可变的人物状态
  - 基础属性：健康、心理健康、能量、压力
  - 教育技能：教育水平、技能深度/广度、学习率
  - 经济：收入、财富、职业、就业稳定性
  - 社交：社会资本、孤独感

#### `models/world.py` (Legacy)
- **WorldState**: 旧版通用世界状态（向后兼容）
- 新项目应使用 `world_base.py`

#### `models/family_policy.py`
- **FamilyPolicyState**: 家庭政策状态
  - **5个政策时期**：
    1. 自然生育期 (1949-1970)
    2. "晚稀少"过渡期 (1971-1978)
    3. 严格独生子女时代 (1979-2015) ⚠️ 核心
    4. 全面二孩 (2016-2020)
    5. 三孩+鼓励生育 (2021-至今)
- **FamilyState**: 家庭结构状态
  - 兄弟姐妹数、独生子女标记
  - 父母压力、代际支持
  - 照护负担、人均家庭财富

---

### 2. Engine（核心引擎层）

#### `engine/simulator.py` (Legacy)
- **LifeSimulator**: 旧版通用模拟器（向后兼容）

#### `engine/simulator_v2.py` ⭐ **NEW**
- **LifeSimulatorV2**: 新架构模拟器
  - **三层架构**：Base World → Country → City
  - 支持任意国家模型
  - 支持任意城市配置
  - 效果级联：底层逻辑 → 国家政策 → 城市特征

#### `engine/simulator_china.py` (Legacy)
- **ChinaLifeSimulator**: 旧版中国模拟器（向后兼容）
- 新项目应使用 `simulator_v2.py` + `ChinaCountryModel`

#### `engine/decision_engine.py`
- **DecisionEngine**: 决策引擎
  - 生成可用行为列表
  - 根据状态和性格自动选择
  - 支持用户自定义选择
  - **6种行为类型**：
    - STUDY（学习）
    - WORK（工作）
    - REST（休息）
    - MOVE（移动/换城市）
    - RISK（冒险/创业）
    - RELATION（建立关系）

#### `engine/transition_engine.py`
- **TransitionEngine**: 状态转移引擎
  - 应用行为效果
  - 自然衰老
  - **支持新架构**：Base World + Country + City
  - **向后兼容**：仍支持旧版 WorldState
  - 效果级联：底层逻辑 → 国家政策 → 城市特征 → 人物状态

---

### 3. Narrative（叙事生成层）

#### `narrative/life_events.py`
- **LifeEventDetector**: 事件检测器
  - 基于状态阈值自动检测
  - 事件类型：健康、职业、社交、经济、里程碑
  - 应用事件影响

#### `narrative/summary_generator.py`
- **SummaryGenerator**: 总结生成器
  - 生成人生叙事
  - 识别关键节点
  - 计算成就统计
  - 生成关系总结
  - 生成遗产描述

---

### 4. Utils（工具函数层）

#### `utils/rng.py`
- **RNG**: 随机数生成器
  - 支持种子设置（可复现）
  - 正态分布、均匀分布、高斯分布

#### `utils/helpers.py`
- 辅助函数
  - 数值限制（clamp）
  - 噪声应用（apply_noise）
  - JSON保存/加载
  - 文件名生成

---

## 🔄 数据流

### 模拟流程

```
1. 初始化
   ├─ 创建 BirthProfile（出生档案）
   ├─ 生成 Personality（性格）
   ├─ 初始化 PersonState（人物状态）
   └─ 初始化 WorldState（世界状态）

2. 主循环（每年）
   ├─ 更新世界状态
   ├─ 生成可用行为
   ├─ 应用行为（状态转移）
   ├─ 检测人生事件
   └─ 年龄+1

3. 结束
   ├─ 生成人生总结
   ├─ 保存结果JSON
   └─ 输出统计信息
```

---

## 🎯 核心特性

### 1. 二八定律（Pareto Principle）
- **位置**: `models/world.py`
- **效果**:
  - 前20%获得4x财富乘数
  - 前20%获得4x机会乘数
  - 前20%获得更多技术收益
  - 仅20%能实现显著社会流动

### 2. 中国世界模型
- **位置**: `models/world_china.py`, `engine/simulator_china.py`
- **特性**:
  - 6个时代段，参数完全不同
  - 4个城市层级，概率分布切换
  - 窗口机制（一次性机会）
  - 代际断裂（房产、父代资产）

### 3. 计划生育政策
- **位置**: `models/family_policy.py`
- **特性**:
  - 5个政策时期
  - 独生子女效应（1.4x教育投资，但更高压力）
  - 竞争强度计算
  - 中年照护负担

---

## 📖 使用指南

### 快速开始

```python
# 通用模型
from models.person import BirthProfile, Personality
from engine.simulator import LifeSimulator

# 中国模型
from models.world_china import ChinaCity
from engine.simulator_china import ChinaLifeSimulator
```

### 运行示例

```bash
# 通用模型测试
python test_run.py

# 中国模型演示
python examples/china_demo.py

# 计划生育政策演示
python examples/family_policy_demo.py

# 二八定律演示
python examples/pareto_demo.py
```

---

## 📝 关键文件速查

| 文件 | 功能 | 关键类/函数 |
|------|------|------------|
| `main.py` | 主程序入口 | CLI界面 |
| `models/person.py` | 人物模型 | BirthProfile, PersonState, Personality |
| `models/world.py` | 通用世界 | WorldState, 二八定律 |
| `models/world_china.py` | 中国世界 | ChinaWorldState, 6时代4城市 |
| `models/family_policy.py` | 家庭政策 | FamilyPolicyEngine, FamilyState |
| `engine/simulator.py` | 通用模拟器 | LifeSimulator |
| `engine/simulator_china.py` | 中国模拟器 | ChinaLifeSimulator |
| `engine/decision_engine.py` | 决策引擎 | DecisionEngine, Action |
| `engine/transition_engine.py` | 状态转移 | TransitionEngine |
| `narrative/life_events.py` | 事件检测 | LifeEventDetector |
| `narrative/summary_generator.py` | 总结生成 | SummaryGenerator |

---

## 🔗 相关文档

- **README.md**: 项目总体说明
- **docs/CHINA_WORLD_MODEL.md**: 中国世界模型详细说明
- **docs/FAMILY_POLICY_MODULE.md**: 计划生育政策模块说明
- **docs/PARETO_PRINCIPLE.md**: 二八定律实现说明

---

## 🎨 Web版本（可选）

项目还包含一个Web前端版本，位于根目录：
- `index.html`: Web界面
- `game.js`: 游戏逻辑（集成MBTI）
- `world-era.js`: 世界/时代模块
- `life-state.js`: 人生状态引擎
- `behavior-choice.js`: 行为选择模块
- `narrative.js`: 叙事生成模块

---

## 📊 系统特点总结

1. **模块化设计**: 清晰的层次结构，易于扩展
2. **双模型支持**: 通用模型 + 中国专用模型
3. **可复现性**: 种子支持，结果可复现
4. **工程化建模**: 结构化参数，非历史叙述
5. **系统性影响**: 二八定律、时代窗口、家庭政策综合作用

---

**最后更新**: 2025年
**版本**: v1.0

