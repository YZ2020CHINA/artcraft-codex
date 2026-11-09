# deckcraft 工作方法

## 版本与证据

本机实测：`deckcraft-cli 0.16.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- headless 可能没有文稿，先 new_presentation/open_presentation；检查主题、页面尺寸和布局，再插入形状/文字/图片。通过 inspect_slide 和 render_slide 逐页核对。
- 保存原生 .deckcraft/PPTX 和渲染图片使用不同入口：save_presentation 保存工程；图片用 export/render_slide。上游提醒用 file.save 给 .png/.jpg 路径可能写出原生 zip 字节，必须检查文件 magic。
- 外部 PPTX 的 SmartArt、动画、媒体、嵌入图表工作簿可能有往返损失；用副本检查，不覆盖输入。视频导出能力须查本机，不能按 PowerPoint 推断 MP4 可导出。
- 不带 path 的 save 可能只返回 needsPath，file.close 可能直接丢弃未保存内容。保存后验证实际文件与重新打开结果。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [deckcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/deckcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
