# 待办清单管理

用快捷指令管理你的待办事项，支持锁屏查看。

---

## 功能

1. **添加任务** — 语音或文字快速添加
2. **完成任务** — 点击勾选完成任务
3. **查看今日任务** — 显示今天所有待办
4. **锁屏显示** — iOS 17+ Live Activity 展示在锁屏

---

## 方案一：纯快捷指令（本地存储）

使用快捷指令的「变量」或「文件」存储任务列表

```
添加任务：
1. 读取 tasks.json
2. 追加新任务
3. 保存回文件

完成任务：
1. 读取 tasks.json
2. 找到对应任务标记完成
3. 保存回文件

显示今日任务：
1. 读取 tasks.json
2. 筛选未完成的今日任务
3. 显示通知/Widget
```

---

## 方案二：Live Activity 锁屏显示

参考 [leiting2327/LiveUp-LockScreenCards](https://github.com/leiting2327/LiveUp-LockScreenCards)

```
iOS 17+ 使用 ActivityKit 实现
1. 启动 Live Activity 显示今日任务
2. 点击锁屏上的任务 → 标记完成
3. 全部完成后自动关闭 Live Activity
```

---

## 方案三：结合第三方服务

- **Things 3** — 通过 URL Scheme 添加任务
- **Todoist** — 支持快捷指令 API
- **滴答清单** — 有官方的快捷指令支持

---

## 相关文件

- `todo.sh` — 任务管理脚本（JSON 格式存储）
- `lockscreen-todo.shortcut` — 锁屏待办快捷指令
