---
name: review-mr
description: 使用知识图谱对 GitLab Merge Request 或分支差异进行全面审查。输出包含爆炸半径分析的结构化评审结果。
argument-hint: "[MR 编号或分支名称]"
---

# 审查 MR

使用知识图谱对 Merge Request 或分支差异进行全面代码审查。

**Token 优化：** 开始前调用 `get_docs_section_tool(section_name="review-mr")` 获取优化后的工作流程。除非用户明确要求，否则不要包含完整文件内容。

## 步骤

1. **识别 MR 的变更**：
   - 如果提供了 MR 编号或分支，使用 `git diff master...<branch>` 获取变更文件
   - 否则从当前分支与 master 的差异自动检测

2. **更新图谱**，调用 `build_or_update_graph_tool(base="master")` 确保图谱反映当前状态。

3. **获取完整审查上下文**，调用 `get_review_context_tool(base="master")`：
   - 使用 `master`（或指定的基准分支）作为 diff 基准
   - 返回 MR 中所有提交涉及的全部变更文件

4. **分析影响范围**，调用 `get_impact_radius_tool(base="master")`：
   - 审查整个 MR 的爆炸半径
   - 识别高风险区域（被广泛依赖的代码）

5. **深入检查每个变更文件**：
   - 阅读有重大变更的文件的完整源码
   - 对高风险函数使用 `query_graph_tool(pattern="callers_of", target=<func>)` 查找调用者
   - 使用 `query_graph_tool(pattern="tests_for", target=<func>)` 验证测试覆盖
   - 检查公开 API 是否有破坏性变更

6. **生成结构化审查输出**：

   ```
   ## MR 审查：<title>

   ### 概述
   <1-3 句话的概览>

   ### 风险评估
   - **总体风险**：低 / 中 / 高
   - **爆炸半径**：X 个文件，Y 个函数受影响
   - **测试覆盖**：N 个变更函数已覆盖 / M 个总数

   ### 文件逐项审查
   #### <file_path>
   - 变更内容：<描述>
   - 影响范围：<谁依赖此文件>
   - 问题：<bug、风格、关注点>

   ### 缺失测试
   - <function_name> 在 <file> - 未找到测试覆盖

   ### 建议
   - <可操作的建议>
   - <可操作的建议>
   ```

## 技巧

- 对于大型 MR，优先关注影响最大的文件（依赖者最多的）
- 使用 `semantic_search_nodes_tool` 查找 MR 可能遗漏的相关代码
- 检查重命名/移动的函数是否已更新所有调用方
