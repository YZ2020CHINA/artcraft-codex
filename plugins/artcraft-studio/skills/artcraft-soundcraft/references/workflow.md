# soundcraft 工作方法

## 版本与证据

本机实测：`soundcraft-cli 0.18.0 (windows x86_64)`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- new_session/open_session → import_audio → inspect_session 确认轨道/片段 → 编辑与 DSP → save_session → bounce_mix。编辑前确认 seconds/frames/samples 的单位。
- 与视频交接优先输出 WAV，按接收端确认采样率（常用 48000Hz）与声道；检查长度、实际音轨、削波并试听。不要因能解码 MP3/AAC 就承诺可导出该格式。
- 上游提示源音频可能整段解码到 RAM，大素材先用小片段验证。MIDI 硬件、外部同步、Atmos、AAF/OMF/PTX 及第三方插件宿主能力均需查当前版本，不能按 Pro Tools 的功能推断。
- 音频创作/编辑与音乐生成区分：SoundCraft 负责已有音频的编辑混音；AI 生成需使用用户已授权且实际可用的生成工具。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [soundcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/soundcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
