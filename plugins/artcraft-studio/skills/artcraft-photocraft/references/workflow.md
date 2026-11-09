# photocraft 工作方法

## 版本与证据

本机实测：`photocraft-cli 0.21.0 (efb7ebd0c, 2026-11-06)`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- 用 doc_open/doc_new、doc_place、doc_save/doc_export 进行文件 I/O。上游明确区分受控文档工具与被 automation policy 拒绝的底层 file.* 命令；不要绕过专用工具用 command_run 猜路径参数。
- PSD 是交换格式，.pcraft 是原生工程。对外部 PSD 先另存副本、重开检查层树/蒙版/混合模式，视觉比对导入前后；不能承诺 Photoshop 无损往返。
- filter 或内容感知操作可能返回后台 job：看 isError、jobs_list 和实际图像再继续。若当前构建没有生成式功能，不能把传统抠图或修复算法说成 AI 生图。
- 导出透明素材时检查 alpha；做 PSD/PNG 交接前检查真实文件类型和尺寸。GUI bridge 的控制令牌与 roots 不等同于 headless roots，按当前 --help 配置。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [photocraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/photocraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
