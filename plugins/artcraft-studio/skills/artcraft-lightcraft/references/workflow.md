# lightcraft 工作方法

## 版本与证据

本机实测：`lightcraft-cli 0.19.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- 显式 import/query_photos/select_photos 后读取 get_develop 与 list_controls；修改后分别核对原始文件、照片选择和导出结果。库持久化需要配置授权项目内 --library。
- RAW 可能解码传感器也可能仅使用嵌入预览；先检查本机文件信息与实际像素。PSD 可能只有合并图，需分层交付时转到 PhotoCraft。
- AI 降噪和 SAM 类抠图可能需要用户另装权重；先查模型/后端状态，不能承诺模型已存在或擅自下载。Lightroom 参数迁移不保证相同色彩。
- 原生资源提供 library、photos、photo/active、develop/active、controls，先 list 再读取准确 URI，按需用其中一种避免重复读取整个库。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [lightcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/lightcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
