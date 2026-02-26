# Worktree 任务上下文：Phase P — RSS → Profile README

> **Branch:** `feature/rss-to-readme` → 合并目标：`njueeRay-profile/main`
> **仓库：** `njueeRay-profile`（GitHub 主页 README）
> **创建日期：** 2026-02-27
> **优先级：** P0（当前 Sprint 第一优先）
> **来源：** 2026-02-27 全体战略会议决议 #P

---

## ⚠️ 并行工作说明

当前并行运行的 worktree：

| Worktree 目录 | 仓库 | 分支 | 任务 |
|-------------|------|------|------|
| `njueeRay-profile/`（主） | njueeRay-profile | main | 主线 |
| **`njueeRay-rss/`（本窗口）** | njueeRay-profile | feature/rss-to-readme | **Phase P（当前）** |
| `njueeray-blog-authors/` | njueeray.github.io | feature/agent-blog-authors | Phase A（并行中） |

**与 Phase A 无冲突**（不同仓库）。
**Phase K 需等本分支合并后才能开始**（会修改同一 README.md）。

---

## 任务目标

将 `njueeray.github.io` 博客的最新文章自动同步展示到 GitHub Profile README 中。

### 具体工作项

- [ ] **GitHub Action**：定期拉取博客 RSS（`/rss.xml`），解析最新 N 篇文章标题 + 链接
- [ ] **README.md 占位区块**：在合适位置插入 `<!-- BLOG-POSTS:START -->...<!-- BLOG-POSTS:END -->` 标记
- [ ] **Action 自动写回**：解析结果写入占位区块，提交到主线
- [ ] **触发频率**：每日 UTC 08:00 + 手动触发（`workflow_dispatch`）
- [ ] **降级方案**：RSS 拉取失败时保留上次内容，不破坏 README 布局

### 技术选型（推荐，可自主决定）

- Action：`gautamkrishnar/blog-post-workflow`（成熟方案，Stars 众多）
- 备选：自写 Python/JS 脚本 + `actions/checkout` + commit
- 显示条数：最新 5 篇

### 关键参考

| 文件 | 用途 |
|------|------|
| `README.md` | 主要修改目标，找合适位置插入博客区块 |
| `njueeray.github.io` 的 `/rss.xml` | 数据源（确认 URL 格式） |
| `.github/workflows/` | 已有 Action 参考（3d-contrib.yml 等） |

---

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
