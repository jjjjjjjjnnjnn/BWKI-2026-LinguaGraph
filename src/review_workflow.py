"""
BWKI Review Workflow

可调用的审查工作流。在 Claude Code 中通过 /rw 命令触发。

用法：
    完整审查: /rw
    代码审查: /rw code
    科学审查: /rw science
    竞赛审查: /rw bwki
    红线检查: /rw redline
    版权检查: /rw ip
    可行性:   /rw business
"""

import json
from pathlib import Path
from datetime import datetime


# ===== 审查模板 =====

REVIEW_TEMPLATE = """
═══════════════════════════════════════════════
  BWKI REVIEW REPORT — {date}
═══════════════════════════════════════════════

{results}

综合评分: {total}/10
必须修复: {critical} 项
建议改进: {suggestions} 项
═══════════════════════════════════════════════
"""


# ===== 维度 1: 科学严谨性 =====
SCIENCE_CHECKLIST = """
## 维度 1: 科学严谨性 (Agent-A)

### 检查清单
- [ ] 研究问题是否清晰、可验证？
- [ ] 假设是否可证伪？
- [ ] 实验设计是否合理？（对照组、随机化、样本量）
- [ ] 是否有误差分析？
- [ ] 统计方法是否正确？
- [ ] 效应量和置信区间是否报告？
- [ ] 局限性是否诚实讨论？

### BWKI 评分标准 (#4 科学方法)
- 8-10: 严谨的科学方法，完整的设计
- 6-7: 方法基本正确，有小缺陷
- 4-5: 方法有明显缺陷
- 1-3: 缺乏科学方法
"""


# ===== 维度 2: 代码质量 =====
CODE_CHECKLIST = """
## 维度 2: 代码质量 (Agent-D)

### 检查清单
- [ ] 命名是否规范？（动词开头函数、描述性变量名）
- [ ] 函数是否短小？（< 50 行）
- [ ] 是否有文档字符串？
- [ ] 是否有类型注解？
- [ ] 错误处理是否完整？
- [ ] 是否有测试？（覆盖率 ≥ 75%）
- [ ] 代码是否可运行？
- [ ] 依赖是否明确？（requirements.txt）
- [ ] .gitignore 是否完整？
- [ ] README 是否完整？

### BWKI 评分标准 (#7 代码可读性)
- 8-10: 代码非常清晰，文档完整
- 6-7: 代码基本可读，有注释
- 4-5: 代码可读性一般
- 1-3: 代码混乱，难以理解
"""


# ===== 维度 3: BWKI 评分 =====
BWKI_CHECKLIST = """
## 维度 3: BWKI 竞赛评分 (Agent-BWIKI)

### 7 项标准逐项评估

| # | 标准 | 评分 | 说明 |
|---|------|:----:|------|
| 1 | 独立完成度 | __/10 | 核心想法是否独立？代码是否原创？ |
| 2 | 原创性与创意 | __/10 | 想法是否新颖？与现有工作的区别？ |
| 3 | 难度与工作量 | __/10 | 技术复杂性？投入时间？ |
| 4 | 科学方法 | __/10 | 实验设计？误差分析？文献调研？ |
| 5 | 前瞻性与洞见 | __/10 | 新知识？未来方向？局限性讨论？ |
| 6 | 实际应用价值 | __/10 | 目标用户？社会价值？可扩展性？ |
| 7 | 代码可读性 | __/10 | 代码清晰？注释完整？结构合理？ |

### 评分阈值
- 一等奖: 综合 ≥ 7.3, 无单项 < 6
- 二等奖: 综合 ≥ 6.0, 无单项 < 4
- 入围: 综合 ≥ 4.0
"""


# ===== 维度 4: 红线检查 =====
REDLINE_CHECKLIST = """
## 维度 4: 红线检查 (Agent-Redline)

### 绝对红线（违反即淘汰）
- [ ] 是否有抄袭？（代码/论文/想法）
- [ ] 是否有虚假数据？
- [ ] 是否有未声明的 AI 生成内容？
- [ ] 是否有伦理问题？（未经同意的数据收集）
- [ ] 是否有安全问题？（API key 泄露、敏感数据）
- [ ] 是否有歧视性内容？

### 高风险项（严重扣分）
- [ ] 是否过度声称？（"首次""唯一""最佳"）
- [ ] 是否忽视局限性？
- [ ] 是否有利益冲突未声明？
- [ ] 引用是否规范？

### 安全检查
- [ ] 代码中是否有硬编码的 API key？
- [ ] .env 文件是否在 .gitignore 中？
- [ ] 是否有敏感信息泄露？
"""


# ===== 维度 5: 版权/知识产权 =====
IP_CHECKLIST = """
## 维度 5: 版权/知识产权 (Agent-IP)

### 代码许可
- [ ] 使用的库是否有兼容许可证？
- [ ] 自己的代码使用什么许可证？
- [ ] 是否有 GPL 代码需要开源？

### 数据来源
- [ ] 学生数据是否有知情同意？
- [ ] 公开数据集是否有使用限制？
- [ ] 是否有版权争议的素材？

### 引用规范
- [ ] 论文引用是否完整？
- [ ] 代码引用是否注明来源？
- [ ] 图片/设计是否有版权？

### BWKI 特定
- [ ] 教师指导是否声明？
- [ ] 团队成员贡献是否说明？
"""


# ===== 维度 6: 商业化/可行性 =====
BUSINESS_CHECKLIST = """
## 维度 6: 商业化/可行性 (Agent-Business)

### 资源评估
- [ ] 时间是否充足？（距离截止日期）
- [ ] 预算是否足够？
- [ ] 团队能力是否匹配？
- [ ] 外部依赖是否可控？

### 风险评估
- [ ] 技术风险（LLM 准确性、性能）
- [ ] 数据风险（招募、质量、数量）
- [ ] 时间风险（开发、测试、展示）
- [ ] 人员风险（伙伴参与度）

### 可行性
- [ ] MVP 是否可在截止日前完成？
- [ ] Demo 是否可现场运行？
- [ ] 视频是否可按时录制？
- [ ] 报告是否可按时撰写？

### 资源清单
| 资源 | 状态 | 缺口 |
|------|------|------|
| LLM API | [有/无] | |
| 学生数据 | [有/无] | |
| 标注数据 | [有/无] | |
| 代码 | [有/无] | |
| 可视化 | [有/无] | |
| 视频设备 | [有/无] | |
"""


# ===== 工作流入口 =====
def run_review(dimensions: str = "all"):
    """
    运行审查工作流。

    Args:
        dimensions: 审查维度，可选值：
            - "all": 全部 6 维度
            - "code": 仅代码质量
            - "science": 仅科学严谨性
            - "bwki": 仅竞赛评分
            - "redline": 仅红线检查
            - "ip": 仅版权/知识产权
            - "business": 仅商业化/可行性
    """
    date = datetime.now().strftime("%Y-%m-%d")
    
    checks = {
        "science": SCIENCE_CHECKLIST,
        "code": CODE_CHECKLIST,
        "bwki": BWKI_CHECKLIST,
        "redline": REDLINE_CHECKLIST,
        "ip": IP_CHECKLIST,
        "business": BUSINESS_CHECKLIST,
    }
    
    if dimensions == "all":
        selected = checks.values()
    elif dimensions in checks:
        selected = [checks[dimensions]]
    else:
        print(f"Unknown dimension: {dimensions}")
        print(f"Available: all, {', '.join(checks.keys())}")
        return
    
    report = REVIEW_TEMPLATE.format(
        date=date,
        results="\n".join(selected),
        total="__",
        critical="__",
        suggestions="__"
    )
    
    print(report)
    return report


if __name__ == "__main__":
    import sys
    dim = sys.argv[1] if len(sys.argv) > 1 else "all"
    run_review(dim)
