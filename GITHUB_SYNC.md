# GitHub 同步工作流程

## 📌 重要规则

**所有代码修改必须同时同步到：**
1. ✅ 本地文件系统
2. ✅ GitHub远程仓库

## 🔄 标准工作流程

每次修改后，我都会执行：

```bash
# 1. 修改本地文件

# 2. Git 添加修改
git add .

# 3. Git 提交（包含清晰的提交信息）
git commit -m "feat/fix: 描述修改内容"

# 4. 推送到GitHub
git push origin main
```

## 📝 提交信息规范

使用清晰的提交信息：
- `feat:` 新功能
- `fix:` 错误修复
- `refactor:` 重构
- `docs:` 文档
- `style:` 格式调整
- `test:` 测试
- `chore:` 维护任务

## ✅ 已配置

- 远程仓库: https://github.com/seanmingw/ETFTradingBot
- 分支: main
- 代理: 已配置（127.0.0.1:7897）

## 🚀 快速命令

### 推送最新修改
```bash
git add . && git commit -m "更新说明" && git push origin main
```

### 检查状态
```bash
git status
```

### 查看提交历史
```bash
git log --oneline
```

## 📋 任务清单

- [x] 创建GitHub仓库
- [x] 配置远程仓库
- [x] 推送初始代码
- [x] 记录同步规则

---

**注意**: Token已配置为GitHub推送使用，后续推送无需重新认证。
