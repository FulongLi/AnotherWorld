# 项目更新日志

## 2025年更新

### 已完成的更新

1. **engine/__init__.py**
   - ✅ 添加了 `LifeSimulatorV2` 和 `simulate_china_life` 的导出
   - 现在可以从 `engine` 包直接导入新架构模拟器

2. **engine/simulator_v2.py**
   - ✅ 修复了 `base_year` 参数，统一使用 1949 作为中国模型的基准年
   - ✅ 改进了 `_event_to_dict` 方法，添加了安全的属性访问（使用 `getattr`）

3. **app.py**
   - ✅ 改进了错误处理，添加了详细的错误日志（仅在 debug 模式下）
   - ✅ 改进了 `_generate_trajectory` 函数，添加了更多轨迹数据
   - ✅ 添加了启动信息提示

4. **static/app.js**
   - ✅ 改进了事件显示，添加了类别信息
   - ✅ 改进了事件渲染的安全性

5. **PROJECT_STRUCTURE.md**
   - ✅ 更新了项目结构，添加了 Web 相关文件
   - ✅ 区分了新旧 Web 版本文件

6. **README.md**
   - ✅ 添加了 Web 界面使用说明

7. **.gitignore**
   - ✅ 创建了 `.gitignore` 文件，排除不必要的文件

### 架构说明

项目现在使用三层架构：
- **Layer 1**: Base World (底层逻辑 - 二八定律、康波周期)
- **Layer 2**: Country (国家模型 - 中国政策、时代)
- **Layer 3**: City (城市层 - 4个中国城市)

### Web 界面

- Flask 后端 (`app.py`)
- 前端模板 (`templates/index.html`)
- 静态文件 (`static/style.css`, `static/app.js`)

### 依赖

所有依赖已更新到 `requirements.txt`：
- Flask 和 Flask-CORS 用于 Web 界面
- 其他核心依赖保持不变

### 注意事项

1. 运行 Web 界面前需要安装所有依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 确保在项目根目录运行 `app.py`

3. Web 界面默认运行在 `http://localhost:5000`

4. 所有模块导入路径已检查并更新

### 待优化项（可选）

1. 添加更多国家模型支持
2. 添加轨迹可视化图表
3. 添加批量模拟功能
4. 添加结果导出功能
5. 添加用户自定义参数预设

