# 锁屏待办清单 快捷指令

**指令名称**：查看今日任务

**触发方式**：锁屏图标 / Siri「我的待办」

---

## 方案一：纯快捷指令版（推荐入门）

使用 JSON 文件存储任务，无需开发环境。

### 数据文件格式

在「文件」App 中创建 `tasks.json`：

```json
{
  "date": "2024-01-15",
  "tasks": [
    { "id": 1, "text": "早上开会", "done": false, "time": "09:00" },
    { "id": 2, "text": "午休健身", "done": false, "time": "12:30" },
    { "id": 3, "text": "晚上聚餐", "done": true, "time": "19:00" }
  ]
}
```

### 快捷指令步骤

**查看今日任务：**

| 步骤 | 动作 | 参数 |
|------|------|------|
| 1 | 读取文件 | 路径：`tasks.json` |
| 2 | 获取日期 | 格式：YYYY-MM-DD |
| 3 | 如果 | 文件日期 == 当前日期 |
| 4 | 过滤列表 | 条件：done == false |
| 5 | 组合文本 | `今日待办（{{数量}}项）：\n{{任务列表}}` |
| 6 | 显示通知 | 从上方文本 |

**添加任务：**

| 步骤 | 动作 | 参数 |
|------|------|------|
| 1 | 获取输入 | 文本 |
| 2 | 读取文件 | `tasks.json` |
| 3 | 追加到列表 | 新任务加入 tasks |
| 4 | 写入文件 | 更新 `tasks.json` |
| 5 | 显示通知 | `已添加：{{输入文本}}` |

**完成任务：**

| 步骤 | 动作 | 参数 |
|------|------|------|
| 1 | 获取输入 | 任务编号 |
| 2 | 读取文件 | `tasks.json` |
| 3 | 设置变量 | 将对应任务 done 设为 true |
| 4 | 写入文件 | 保存 |
| 5 | 显示通知 | `✅ 已完成：{{任务文本}}` |

---

## 方案二：Live Activity 版（iOS 17+，需要 Xcode）

参考 [leiting2327/LiveUp-LockScreenCards](https://github.com/leiting2327/LiveUp-LockScreenCards)

### 需要的组件

1. iOS App（SwiftUI）
2. WidgetExtension（ActivityKit）
3. SwiftData 数据模型
4. 快捷指令通过 App Intents 触发

### 快捷指令与 App 的交互

```
1. 快捷指令 → 调用 App Intent「添加任务」
2. App Intent → 写入 SwiftData
3. SwiftData → 通知 Widget 更新
4. Live Activity → 锁屏实时更新
```

---

## 快速开始

1. 先使用方案一，在「文件」App 创建 `tasks.json`
2. 在快捷指令 App 中按上述步骤创建三个指令
3. 将「查看今日任务」添加到锁屏
