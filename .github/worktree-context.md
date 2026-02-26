# Worktree 任务上下文：Phase K — Team Knowledge Graph

> **Branch:** `feature/knowledge-graph` → 合并目标：`njueeRay-profile/main`
> **仓库：** `njueeRay-profile`（GitHub 主页 README）
> **创建日期：** 2026-02-27
> **优先级：** P2（Phase P 已完成，本任务现在可执行）
> **来源：** 2026-02-27 全体战略会议决议 #K

---

## ⚠️ 并行工作说明

| Worktree 目录 | 仓库 | 分支 | 状态 |
|-------------|------|------|------|
| `njueeRay-profile/`（主） | njueeRay-profile | main | Phase P ✅ 已合并 |
| **`njueeray-kg/`（本窗口）** | njueeRay-profile | feature/knowledge-graph | **Phase K（当前）** |

**本分支起点包含 Phase P 的所有变更**（RSS 区块已在 README.md 中）。
**Phase A（njueeray.github.io）** 已独立完成，与本任务无冲突。

---

## 任务目标

在 GitHub Profile README 中嵌入**团队知识图谱 SVG**，让访客能直观看到 AI-native 团队的认知结构。

---

## 知识图谱设计规范

### 节点分类（3 层）

```
Layer 1 — 核心人物（大圆，金色 #f0e68c）
  njueeRay（中心）

Layer 2 — Agent 团队（中圆，蓝色 #1f6feb）
  Brain · PM · Dev · Researcher · Code-Reviewer · Brand

Layer 3 — 核心概念（圆角矩形，灰色 #30363d 边框）
  AI-native · Playbook · Worktree · Build-in-Public
  Knowledge-Graph · Blog · Profile-README · L2-Patterns
```

### 视觉规范

- **背景**：`#0d1117`（GitHub Dark）
- **Agent 节点**：蓝色系 `#58a6ff`
- **概念节点**：灰色 `#8b949e`
- **整体尺寸**：900×500 px

### 插入位置（README.md 现有结构）

```
...
[3D 贡献图 <details>]   ← 现有
[知识图谱 <details>]    ← 本次新增
[Connect 区]           ← 现有
```

---

## 具体工作项

- [ ] 创建 `assets/team-knowledge-graph.svg`（手写 SVG，暗色背景）
- [ ] 在 README.md 的 3D 贡献图折叠区**之后**插入展示区块：

```html
<!-- ===== TEAM KNOWLEDGE GRAPH ===== -->
<details>
<summary>🧠 Team Knowledge Graph — AI-native 团队认知图谱</summary>
<br/>
<div align="center">
  <img src="assets/team-knowledge-graph.svg" alt="Team Knowledge Graph" width="900"/>
</div>
</details>
```

---

## DoD（完成标准）

- [ ] `assets/team-knowledge-graph.svg` 已创建（包含全部节点和边）
- [ ] README.md `<details>` 区块插入完成，位于 3D 图之后
- [ ] SVG 在 GitHub dark mode 下渲染正常（背景 #0d1117）
- [ ] SVG 文件大小 < 100KB
- [ ] 节点标签清晰可读

---

## 提交规范

```
feat(profile): add Team Knowledge Graph SVG (Phase K)

Co-authored-by: GitHub Copilot <copilot@github.com>
```

---

## 完成后：向主窗口（OpenProfile）汇报

```
feature/knowledge-graph worktree 任务已完成。
变更摘要：[描述改动]
请在 njueeRay-profile 仓库执行合并流程。
```

主窗口执行：
```bash
git -C "..\njueeRay-profile" merge feature/knowledge-graph
git -C "..\njueeRay-profile" push origin main
git -C "..\njueeRay-profile" worktree remove ..\njueeray-kg
git -C "..\njueeRay-profile" branch -d feature/knowledge-graph
git -C "..\njueeRay-profile" push origin --delete feature/knowledge-graph
```

## 提交规范

```
feat(profile): add RSS blog posts auto-sync

Co-authored-by: GitHub Copilot <copilot@github.com>
```

---

## DoD（完成标准）

- [ ] GitHub Action 文件创建（`.github/workflows/blog-posts.yml`）
- [ ] README.md 含占位标记并有初始内容（手动触发 Action 后验证）
- [ ] Action 在 GitHub Actions 页面成功运行一次
- [ ] 降级方案已实现（RSS 失败不破坏 README）
- [ ] README 暗色模式下渲染正常

---

## 完成后：向主窗口（OpenProfile）汇报

```
feature/rss-to-readme worktree 任务已完成。
变更摘要：[描述主要改动]
请在 njueeRay-profile 仓库执行合并流程。
```

主窗口执行：
```bash
git -C "..\njueeRay-profile" merge feature/rss-to-readme
git -C "..\njueeRay-profile" push origin main
git -C "..\njueeRay-profile" worktree remove ..\njueeRay-rss
git -C "..\njueeRay-profile" branch -d feature/rss-to-readme
git -C "..\njueeRay-profile" push origin --delete feature/rss-to-readme
```

**合并完成后**，可立即开启 Phase K（知识图谱）。
