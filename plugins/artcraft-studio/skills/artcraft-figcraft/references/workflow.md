# figcraft 工作方法

## 版本与证据

本机实测：`figcraft-cli 0.16.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- 使用 inspect_document 查页面与节点，create_node/set_properties 或发现的命令构建结构；批量对象操作前确认本应用引用规则，不沿用其他应用对象 ID。
- FigCraft 与在线 Figma 是独立应用。上游 .fig/.sketch 导入是 best effort；另存原生 .figcraft 并检查遮罩、字体、组件与约束，再交付。
- 上游某些章节对 .jam、Code Connect 的描述有新旧冲突；本机 CLI 已有 connect 命令，不能把旧“未实现”当现状。以实时注册表与实际文件验证为准。
- SVG/PNG/PDF 导出需检查图层边界、透明度与字体；FigCraft WASM 插件不能直接视作 Figma JavaScript 插件。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [figcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/figcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
