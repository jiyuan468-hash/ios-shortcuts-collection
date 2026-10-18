# 如何添加快捷指令文件

每个分类目录下都可以放入导出的 `.shortcut` 文件。

## 导出步骤

1. 打开 iOS「快捷指令」App
2. 找到你要导出的快捷指令
3. 长按指令 →「分享」→「保存到文件」
4. 选择本仓库对应目录
5. 文件会自动保存为 `.shortcut` 格式

## 命名规范

```
{类别}-{功能}.shortcut
```

示例：
- `morning-greeting.shortcut`
- `shopping-sign.shortcut`
- `lockscreen-todo.shortcut`

## 配合说明文档

每个目录都有 `SHORTCUT_SPEC.md`，详细描述了：
- 快捷指令的完整操作步骤
- 数据存储格式
- 自动化触发设置

创建快捷指令时参考 `SHORTCUT_SPEC.md` 即可。
