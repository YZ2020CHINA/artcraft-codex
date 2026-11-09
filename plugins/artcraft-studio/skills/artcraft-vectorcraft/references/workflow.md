# vectorcraft 工作方法

## 版本与证据

本机实测：`vectorcraft-cli 0.22.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- 绘制前 inspect 文档、画板和选择；draw_shape 的 fill/stroke 用显式值，避免继承上个对象外观。用真实几何背景对象得到导出底色，上游提醒画板显示背景可能不写入成品。
- 文本通过 add_text 或命令设置，检查 overflow；导出 SVG 后核对字体，跨机器交付可用 outlineText，仍保留未转曲原生工程。
- 外部 AI/EPS/PSD 输入先查 importWarnings 和实际对象结构，再另存 .vectorcraft；不要把合并预览当作可编辑图层，也不要声称写出了 Illustrator 原生编辑数据。
- 上游没有 Illustrator JSX 脚本运行时；优先 MCP 命令。格式支持以本机 document.formats 和实际打开结果为准。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [vectorcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/vectorcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
