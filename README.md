# iOS 快捷指令大全

> 把手机上的各种事情结合起来，靠快捷指令实现自动化操作。
> 整理自 [leecobaby/shortcuts](https://github.com/leecobaby/shortcuts)（1.7k stars）等开源项目，并补充更多实用场景。

---

## 目录结构

```
ios-shortcuts-collection/
├── daily-life/          # 🏠 生活日常
│   ├── morning/         #    早起 routine
│   ├── evening/         #    晚间 routine
│   └── sleep/           #    睡眠模式
├── shopping/            # 🛒 购物电商
│   ├── sign/            #    多平台签到
│   └── price-monitor/   #    价格监控提醒
├── social/              # 💬 社交通讯
│   └── wechat/          #    微信相关
├── productivity/        # 📝 效率办公
│   ├── todo/            #    待办清单管理
│   ├── meeting/         #    会议纪要
│   └── files/           #    文件整理
├── content/             # 📸 内容创作
│   └── photo/           #    照片处理
├── health/              # 🎯 健康监测
│   ├── water/           #    喝水提醒
│   └── exercise/        #    运动打卡
├── security/            # 🔒 安全隐私
│   └── lost/            #    丢失模式
├── lockscreen/          # 🌟 锁屏相关
│   ├── todo/            #    锁屏待办清单
│   └── widget/          #    锁屏 Widget
├── references/          # 📚 参考资料
│   ├── links/           #    参考项目链接
│   └── setup-guide/     #    使用教程
└── README.md
```

---

## 快速开始

### 1. 安装快捷指令 App

iOS 自带「快捷指令」App（iOS 10+），无需额外下载。如没有可在 App Store 搜索「快捷指令」。

### 2. 导入快捷指令

每个快捷指令目录下有 `.shortcut` 文件或说明，点击链接即可导入：

- 双击 `.shortcut` 文件 → 自动打开快捷指令 App → 点击「添加快捷指令」
- 或在快捷指令 App 中 → 点击右上角「+」→「从文件导入」

### 3. 添加到主屏 / 锁屏

- **主屏**：快捷指令 → 右上角「...」→「添加到主屏幕」
- **锁屏**：iOS 16+ 长按锁屏 →「自定义」→ 选择快捷指令
- **小组件**：长按主屏空白处 →「+」→ 搜索「快捷指令」

---

## 使用场景示例

### 场景一：早晨一键启动

触发方式：Siri「早上好」或锁屏图标

执行内容：
1. 播报今日天气 + 穿衣建议
2. 播报今日日程
3. 自动播放晨间音乐
4. 记录今日喝水目标（8 杯）

### 场景二：回家模式

触发方式：连接家中 WiFi 时自动运行

执行内容：
1. 关闭外出模式
2. 打开 HomeKit 灯光
3. 播报今日未读消息数
4. 记录到家时间

### 场景三：锁屏待办清单

触发方式：iOS 17+ Live Activity

执行内容：
1. 在锁屏显示今日最重要的 3 件事
2. 直接在锁屏勾选完成
3. 完成全部任务后自动关闭提醒

---

## 开发说明

### 添加新快捷指令

1. 在对应分类目录下创建新文件夹
2. 创建 `README.md` 描述使用方法
3. 导出快捷指令：快捷指令 App → 右上角「...」→「共享」→「保存至文件」
4. 将 `.shortcut` 文件放入目录
5. 更新主 README 的目录树

### 快捷指令文件格式

`.shortcut` 是 Apple 的快捷指令导出格式，可以直接双击导入。

---

## 参考项目

| 项目 | Stars | 说明 |
|------|-------|------|
| [leecobaby/shortcuts](https://github.com/leecobaby/shortcuts) | 1.7k | 最大的中文快捷指令集合，电商自动化为主 |
| [OwenYing/iphone-shortcut-library](https://github.com/OwenYing/iphone-shortcut-library) | 116 | Apple iOS 捷径库 |
| [heliomass/iOSShortcuts](https://github.com/heliomass/iOSShortcuts) | 84 | iOS Shortcuts 集合 |
| [leiting2327/LiveUp-LockScreenCards](https://github.com/leiting2327/LiveUp-LockScreenCards) | - | Live Activity + 快捷指令锁屏方案 |
| [kotadappe/ailis-mcp](https://github.com/kotadappe/ailis-mcp) | - | MCP Server，将 AI 对话保存到锁屏 |
| [dewang-mistry/focuscard](https://github.com/dewang-mistry/focuscard) | - | 锁屏单任务专注 |
| [nebuhtit/universal-task-manager](https://github.com/nebuhtit/universal-task-manager) | - | 本地优先任务管理 + 锁屏 Widget |

---

## 许可证

本项目基于各参考项目的开源协议。快捷指令文件本身不受版权保护，仅供个人学习使用。
