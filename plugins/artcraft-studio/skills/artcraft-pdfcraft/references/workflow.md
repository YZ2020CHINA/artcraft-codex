# pdfcraft 工作方法

## 版本与证据

本机实测：`pdfcraft-cli 0.19.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- compact 模式先 tool_search 查目标功能，再 tool_call；doc_open 后检查文档 ID、页数和权限，修改后 doc_save 到新路径并重新打开。
- OCR 的语言、现有文本编辑和导出格式以当前工具/模型实际支持为准；上游旧版 OCR 只支持有限语言，不能因为界面有 OCR 就承诺中文可用。
- 遮盖对象不等于删除敏感内容。需要真实 redaction 时发现并应用对应工具，再 text_extract/搜索/audit 检查底层内容。
- Office 转 PDF 优先让 WordCraft/DeckCraft/GridCraft 各自导出，再交给 PdfCraft 整理；不要假设 PdfCraft 能直接打开所有 Office 格式。签名/验证须区分本地证书检查与在线吊销查询。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [pdfcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/pdfcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
