# effectcraft 工作方法

## 版本与证据

本机实测：`effectcraft-cli 0.22.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- 创建 comp.new → 添加图层 → 获取实际图层 ID/属性路径 → 关键帧与效果 → render_frame 检查 → save_project → 发现 renderQueue.add/renderQueue.render 或原生 CLI render 参数再导出。
- batch 是原子 undo 组，结果引用从 1 开始；command_batch 是逐条执行，失败时前面的步骤可能已生效。不要把 DesignCraft 的 $0 引用规则混进来。
- .ecproj/.ecprojx、.ectemplate、.ecpreset 属于本应用；上游不支持 AE .aep/.aepx/.ffx/.mogrt。某些效果有近似实现，不能承诺与 AE 像素一致；.xml 可能是工程或时间线，优先使用 .ecprojx 区分工程。
- 后台渲染的 CPU/GPU 与编码器能力需本机验证；通过原生资源读取合成状态和命令目录，不依赖上游效果数量。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [effectcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/effectcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
