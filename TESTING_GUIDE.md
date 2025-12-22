# 测试指南 (Testing Guide)

## 📋 测试类型

项目包含以下类型的测试：

1. **快速测试脚本** (`test_run.py`) - 基础功能验证
2. **演示脚本** (`examples/`) - 功能演示和对比
3. **主程序** (`main.py`) - 交互式模拟

---

## 🚀 快速开始

### 1. 基础功能测试

```bash
# 运行快速测试脚本
python test_run.py
```

这会运行一个简单的人生模拟，验证核心功能是否正常。

**预期输出**：
```
Testing Life Trajectory Simulator...
Running simulation...
[OK] Simulation completed successfully!
[OK] Final age: 80
[OK] Total events: X
[OK] Summary generated: True

Test passed! [OK]
```

### 2. 运行所有测试（一键运行）

**Windows**:
```bash
# 双击运行或命令行执行
run_tests.bat
```

**Linux/Mac**:
```bash
# 添加执行权限后运行
chmod +x run_tests.sh
./run_tests.sh
```

这会依次运行所有测试和演示脚本。

### 2. 运行主程序（交互式）

```bash
# 交互式模拟
python main.py
```

按照提示输入参数或使用默认值。

---

## 📊 演示脚本

### 1. 新架构演示

```bash
# 演示三层架构（Base World -> Country -> City）
python examples/architecture_demo.py
```

**功能**：
- 展示底层逻辑（二八定律、康波周期）
- 展示国家模型（中国政策、时代）
- 展示城市模型（4个中国城市对比）
- 对比不同城市的结果

### 2. 中国模型演示

```bash
# 演示中国世界模型
python examples/china_demo.py
```

**功能**：
- 对比6个时代段
- 对比4个城市
- 展示窗口机制
- 展示代际断裂

### 3. 计划生育政策演示

```bash
# 演示计划生育政策影响
python examples/family_policy_demo.py
```

**功能**：
- 对比5个政策时期
- 展示独生子女效应
- 展示中年照护负担
- 展示竞争强度变化

### 4. 二八定律演示

```bash
# 演示二八定律影响
python examples/pareto_demo.py
```

**功能**：
- 展示财富分配
- 展示机会获取
- 展示技术收益
- 展示社会流动性

---

## 🧪 运行所有演示

### 方法1：使用测试脚本（推荐）

**Windows**:
```bash
run_tests.bat
```

**Linux/Mac**:
```bash
chmod +x run_tests.sh
./run_tests.sh
```

### 方法2：手动运行

**Windows (PowerShell)**:
```powershell
# 运行所有演示脚本
python examples/architecture_demo.py
python examples/china_demo.py
python examples/family_policy_demo.py
python examples/pareto_demo.py
```

**Linux/Mac**:
```bash
# 运行所有演示脚本
python examples/architecture_demo.py
python examples/china_demo.py
python examples/family_policy_demo.py
python examples/pareto_demo.py
```

---

## 🔍 验证测试

### 检查输出

所有演示脚本都会输出：
- ✅ 配置信息
- ✅ 模拟结果
- ✅ 对比数据
- ✅ 关键洞察

### 预期行为

1. **无错误输出**：所有脚本应正常运行，无异常
2. **可复现性**：使用相同种子应产生相同结果
3. **合理数值**：所有数值应在合理范围内（0-1或合理金额）

---

## 📝 自定义测试

### 创建自定义测试脚本

```python
# custom_test.py
from models.person import BirthProfile, Personality
from models.world_base import BaseWorldState
from models.country_china import ChinaCountryModel
from models.city import City, create_china_cities
from engine.simulator_v2 import LifeSimulatorV2

# 创建测试数据
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
    risk_preference=0.6,
    social_drive=0.6,
    resilience=0.7
)

# 创建模拟器
base_world = BaseWorldState(year=1990, base_year=1949)
china_model = ChinaCountryModel(base_world, 1990)
cities = create_china_cities()
city = City(cities["shenzhen"], china_model)

simulator = LifeSimulatorV2(max_age=50, seed=42)
result = simulator.simulate(birth, personality, china_model, city)

# 验证结果
assert result['person']['age'] == 50
assert result['person']['wealth'] >= -100000  # 合理范围
assert result['country']['era'] in ['ESTABLISHMENT', 'TURBULENCE', 'REFORM_EARLY', 
                                    'URBAN_BOOM', 'STRUCTURE_SOLIDIFY', 'NEW_UNCERTAINTY']

print("✅ 测试通过！")
```

运行：
```bash
python custom_test.py
```

---

## 🐛 调试测试

### 启用详细输出

在脚本中添加调试信息：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 检查中间状态

在模拟循环中添加打印：

```python
# 在 simulator_v2.py 的 simulate 方法中
if person.age % 10 == 0:
    print(f"Age {person.age}: Wealth={person.wealth:.2f}, "
          f"Education={person.education_level:.3f}")
```

### 使用固定种子

```python
# 使用固定种子确保可复现
simulator = LifeSimulatorV2(max_age=60, seed=42)
```

---

## 📊 性能测试

### 批量运行测试

```python
# performance_test.py
import time
from engine.simulator_v2 import simulate_china_life
from models.person import BirthProfile, Personality

birth = BirthProfile(1990, "Urban", 0.6, 0.6, 0.7, 0.7, 0.6)
personality = Personality(0.6, 0.7, 0.6, 0.6, 0.7)

start = time.time()
for i in range(100):
    result = simulate_china_life(birth, personality, "shenzhen", 60, i)
elapsed = time.time() - start

print(f"100次模拟耗时: {elapsed:.2f}秒")
print(f"平均每次: {elapsed/100:.3f}秒")
```

---

## ✅ 测试检查清单

运行测试前检查：

- [ ] Python 3.11+ 已安装
- [ ] 依赖已安装 (`pip install -r requirements.txt`)
- [ ] 在项目根目录运行
- [ ] 输出目录存在 (`output/`)

运行测试后验证：

- [ ] 所有脚本无错误运行
- [ ] 输出结果合理
- [ ] 数值在预期范围内
- [ ] 可复现性（相同种子 = 相同结果）

---

## 🔧 常见问题

### Q: 测试失败，提示模块未找到

**A**: 确保在项目根目录运行，或使用：
```bash
python -m pytest  # 如果安装了pytest
```

### Q: 输出结果不合理

**A**: 检查：
1. 种子是否正确设置
2. 参数是否在合理范围
3. 是否有随机性导致的极端值

### Q: 运行速度慢

**A**: 
- 减少 `max_age` 参数
- 减少模拟次数
- 检查是否有无限循环

---

## 📚 相关文档

- **项目结构**: `PROJECT_STRUCTURE.md`
- **快速参考**: `QUICK_REFERENCE.md`
- **架构说明**: `docs/ARCHITECTURE.md`
- **中国模型**: `docs/CHINA_WORLD_MODEL.md`
- **家庭政策**: `docs/FAMILY_POLICY_MODULE.md`

---

**提示**: 如果遇到问题，检查 `examples/` 目录下的演示脚本作为参考实现。

