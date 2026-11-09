# wordcraft 工作方法

## 版本与证据

本机实测：`wordcraft-cli 0.16.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- new_document/open_document → 结构检查 → 编辑 → 保存 DOCX → 重开 → render_page 或 PDF 检查分页。带 doc 参数时使用 list_documents 返回的真实 ID。
- 对外部 DOCX 用副本验证修订、注释、节、字段、表格、图表与 OLE；保留不代表可编辑。上游分页与 Word 不同，不能承诺逐页一致。
- .doc 读取不代表可以写回 .doc；模板 .dotx/.dotm 与文档保存入口不同。模板清单在 headless 需显式授权 dir，避免依赖 GUI 偏好。
- 原生资源状态可读，但 headless 没有桌面恢复保障；保存后再关闭，PDF 成品用 PDF 阅读/渲染工具校验，不能把 WordCraft 不支持重新打开 PDF 当导出失败。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [wordcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/wordcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
