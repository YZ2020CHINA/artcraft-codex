# filmcraft 工作方法

## 版本与证据

本机实测：`filmcraft-cli 0.18.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- 剪辑顺序：probe/导入 → project_inspect 找实际 item ID → source.open → 设置 In/Out（如需）→ source.insert/overwrite → sequence_inspect 检查轨道、时长和离线素材 → 保存 .fcproj。
- 导出前通过 command_list 查 export.formats 和 export 相关命令，确认本机编码器可用；枚举里有格式不代表本机能编码。file.exportMedia 明确传 wait=true，检查结果的 offlineMedia、文件和重新 probe。不要用一次性进程的 wait=false 导出。
- 字幕与语音识别是不同能力。上游的 Whisper/Kokoro 是构建开关；先查本机可用性，不因有 transcript/tts 菜单就承诺识别或神经配音。可导入现成字幕/文字。
- GUI bridge 需核对 FILMCRAFT_CONTROL_TOKEN；上游要求启动应用和 CLI 继承同一个 64 位十六进制 token。绝不把 token 写进技能或回显。Premiere .prproj 和 .mogrt 不能假定兼容；优先测试 XML/OTIO 或渲染媒体交接。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [filmcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/filmcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
