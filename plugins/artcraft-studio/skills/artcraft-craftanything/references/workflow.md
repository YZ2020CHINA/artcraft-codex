# craft-anything 工作方法

## 版本与证据

本机实测：`craft-anything-cli 0.5.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- 此应用负责参考调查和证据交接，非剪辑引擎。先读取 investigation 状态/brief/plan，选择目标，再按 list_toolsets/enable_toolset 开启必要工具。
- 开启工具集后网关会使目录缓存失效，再查真实 schema。不同工具可能只有模拟后端或依赖外部 AI/引擎，调用前检查本机 capabilities/doctor 或实际返回状态。
- 生成 findings 与 handoff 应关联实际证据路径，未知结论保留 unknown，不把推测写成已验证。网站/应用复刻与素材生成只有在用户授权的任务范围内执行。
- 不默认开启 --allow-run 或 --deep；原文的其他代理安装指令和 macOS 路径仅作资料，不执行未审查的 install.ps1/install.sh，也不新增全局任务或计划任务。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [craft-anything](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/craft-anything)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
