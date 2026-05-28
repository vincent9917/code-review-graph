---
name: review-mr
description: 使用知识图谱对 GitLab Merge Request 进行全面审查，并将结构化评审结果自动评论到对应 MR 上。
argument-hint: "[MR 编号或分支名称]"
---

# 审查 MR

使用知识图谱对 Merge Request 进行全面代码审查，并将结果自动发布到 GitLab MR 评论中。

**Token 优化：** 开始前调用 `get_docs_section_tool(section_name="review-mr")` 获取优化后的工作流程。除非用户明确要求，否则不要包含完整文件内容。

## 前置条件

- 已安装并认证 `glab` CLI（`glab auth status` 需显示已登录）
- 当前仓库的远程 origin 指向 GitLab

## 步骤

1. **识别 MR 并确定基准分支 `$BASE`**：
   - 如果提供了 MR 编号，记录该编号
   - 如果提供了分支名称，通过 `glab mr list --source-branch <branch>` 查找对应 MR 编号
   - 如果两者都未提供，通过 `glab mr view` 获取当前分支对应的 MR 信息
   - **确定基准分支**（按优先级）：
     1. 用户显式指定的基准分支（如用户说"对比 master"）
     2. 通过 `glab mr view <mr_number> -F json | jq -r .target_branch` 获取 MR 的目标分支（若无 `jq`，可用 `python3 -c "import sys,json; print(json.load(sys.stdin)['target_branch'])"`）
   - 将确定的基准分支记为 `$BASE`，后续所有步骤均使用 `$BASE`
   - 使用 `git diff $BASE...<branch>` 获取变更文件清单

2. **更新图谱**，调用 `build_or_update_graph_tool(base="$BASE")` 确保图谱反映当前状态。

3. **获取完整审查上下文**，调用 `get_review_context_tool(base="$BASE")`：
   - 使用 `$BASE` 作为 diff 基准
   - 返回 MR 中所有提交涉及的全部变更文件

4. **分析影响范围**，调用 `get_impact_radius_tool(base="$BASE")`：
   - 审查整个 MR 的爆炸半径
   - 识别高风险区域（被广泛依赖的代码）

5. **深入检查每个变更文件**：
   - 阅读有重大变更的文件的完整源码
   - 对高风险函数使用 `query_graph_tool(pattern="callers_of", target=<func>)` 查找调用者
   - 使用 `query_graph_tool(pattern="tests_for", target=<func>)` 验证测试覆盖
   - 检查公开 API 是否有破坏性变更

6. **生成结构化审查报告**：

   ```markdown
   ## 知识图谱代码审查报告

   ### 概述
   <1-3 句话的概览>

   ### 风险评估
   | 维度 | 结果 |
   |------|------|
   | 总体风险 | 低 / 中 / 高 |
   | 爆炸半径 | X 个文件，Y 个函数受影响 |
   | 测试覆盖 | N 个变更函数已覆盖 / M 个总数 |

   ### 文件逐项审查
   #### `<file_path>`
   - **变更内容**：<描述>
   - **影响范围**：<谁依赖此文件>
   - **问题**：<bug、风格、关注点，无则填 "无" >

   ### 缺失测试
   - `<function_name>` 在 `<file>` — 未找到测试覆盖

   ### 建议
   - <可操作的建议>
   - <可操作的建议>

   ---
   *由 code-review-graph 知识图谱自动生成*
   ```

7. **发布评论到 GitLab MR**：
   - 确认 `glab auth status` 显示已认证
   - 使用以下命令将审查报告发布为 MR 评论（避免重复发帖）：
     ```bash
     echo "<审查报告内容>" | glab mr note create <mr_number> --unique
     ```
   - 如果 `--unique` 不可用，先执行 `glab mr note list <mr_number>` 检查是否已有相同标题的评论，避免重复发布
   - 发布成功后，向用户汇报评论链接（`glab mr view <mr_number> --web` 或直接从输出中提取）

## 技巧

- 对于大型 MR，优先关注影响最大的文件（依赖者最多的）
- 使用 `semantic_search_nodes_tool` 查找 MR 可能遗漏的相关代码
- 检查重命名/移动的函数是否已更新所有调用方
- 使用 `--unique` 标志确保同一 MR 不会被重复评论
- 如果用户只需要本地查看报告而不发布，可在步骤 7 前询问确认
