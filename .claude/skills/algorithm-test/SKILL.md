---
name: algorithm-test
description: "运行Python代码、语法检查、错误捕获。触发词：跑代码、运行python、代码测试、语法检查、algorithm test、执行py、code test、跑脚本。"
---

# /algorithm-test — 运行并验证 Python 算法代码

## 触发条件
用户说"测试代码"、"跑一下"、"验证代码"、"test algorithm"、"run code"时调用。

## 工作流

### 1. 定位代码文件
从用户输入或上下文中确定要测试的 `.py` 文件路径。

### 2. 预检（不运行）
```powershell
python -m py_compile "<file_path>" 2>&1
```
如果语法检查失败 → 报告错误，不继续执行。

### 3. 依赖检查
```powershell
python -c "import numpy, scipy, pandas, matplotlib, sklearn" 2>&1
```
缺依赖 → 提示 `pip install -r <file_path_parent>/requirements.txt`

### 4. 执行代码（限时 120 秒）
```powershell
cd "<file_directory>"
python "<file_name>" 2>&1
```

### 5. 结果报告
- 退出码 + 运行时长
- 如果报错：截取关键错误行（最后 10 行 stderr），标注错误类型（ImportError / SyntaxError / ValueError / FileNotFoundError / 其他）
- 如果成功：列出生成的文件（.png / .csv / .svg 等）
- 如果超时（>120s）：报告可能死循环，建议检查 while/递归
- 如果输出为空：标注"无输出，可能缺少 main guard 或 print"

### 6. 输出格式
```
## 代码测试报告
- 文件: xxx.py
- 语法检查: PASS / FAIL
- 运行状态: SUCCESS (12.3s) / ERROR / TIMEOUT
- 错误摘要: [如有]
- 产出文件: [列出]
```