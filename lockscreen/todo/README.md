# 锁屏待办清单

把重要的事钉在 iPhone 锁屏上，iOS 17+ Live Activity 方案。

---

## 方案一：Live Activity（推荐）

iOS 17+ 支持 Live Activity，可以直接在锁屏显示动态内容。

### 参考项目

- [leiting2327/LiveUp-LockScreenCards](https://github.com/leiting2327/LiveUp-LockScreenCards) — LiveUp 复刻，把任务钉到锁屏

### 实现思路

```
1. 创建 SwiftData 模型存储任务
2. 使用 ActivityKit 创建 Live Activity
3. 快捷指令添加/完成任务
4. 锁屏实时更新显示
```

### 快捷指令配合

- 「添加任务」快捷指令 → 写入 SwiftData → 触发 Live Activity 更新
- 「完成任务」快捷指令 → 标记完成 → 从锁屏移除

---

## 方案二：WidgetKit 锁屏小组件

iOS 16+ 支持锁屏 Widget，但交互能力有限。

### 特点
- 可以在锁屏左右滑动查看
- 点击可跳转到 App
- 需要用户手动添加到锁屏

### 实现
```
1. 创建 Widget Extension
2. 使用 TimelineProvider 提供任务数据
3. 支持点击跳转
4. 可配置样式
```

---

## 方案三：纯快捷指令方案

不写代码，纯用快捷指令实现基础功能。

```
1. 创建「查看今日任务」快捷指令
2. 添加到锁屏快捷入口
3. 按下电源键 → 点击图标 → 查看任务
4. 配合「添加任务」快捷指令使用
```

---

## 快速开始

### 最低配置方案
1. 创建一个「查看今日待办」快捷指令
2. 将其添加到锁屏（iOS 16+）
3. 配合文本备忘录存储任务

### 完整方案
参考 [LiveUp-LockScreenCards](https://github.com/leiting2327/LiveUp-LockScreenCards) 项目，需要 Xcode 开发环境。
