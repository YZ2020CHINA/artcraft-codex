# designcraft 工作方法

## 版本与证据

本机实测：`designcraft-cli 0.18.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- 使用 new_document 指定页面尺寸/边距/出血，再创建 frame、story 和样式。坐标为 points（72 pt = 1 inch）；页面工具通常 0-based，file.exportPdf 的 pages 规则须查命令说明。
- batch 的 $N.path 引用从 0 开始；有的步骤失败后前序编辑仍保留。检查 failedIndex/failedCommand/error，不要只看 JSON-RPC 请求成功。
- 文本偏移用 UTF-8 字节，中文不能按字符数直接计算 text.select 偏移；inspect/get_story 检查 overset 后调整框高、字号或分页。
- 印刷 PDF 应验证嵌入字体、出血和输出意图；本机 CLI validate-pdf 支持的标准以当前 --help 为准。headless 中 screenshot/dialog 等 GUI 专用工具可能不可用，用 render_page/export_png 验证。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [designcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/designcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
