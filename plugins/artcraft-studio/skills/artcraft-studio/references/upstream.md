# 参考来源与本机适配

来源：[https://github.com/midasmatterhorn/artcraft-skills](https://github.com/midasmatterhorn/artcraft-skills)，固定提交 `042c5d4ddcd8e54178d72db3bc686a18658eee8d`，MIT，Copyright (c) 2026 midasmatterhorn。

这是一套应用技能资料，MCP 由各应用自身提供。仅整合本机 13 款应用的文档为 references，不安装重复顶层技能，不运行其安装器。README 声称的“evidence verified”代表作者在固定版本的审查，不等于本机所有业务操作已验证。

本机准确工具与参数优先，其次小文件实测，再参考相符的历史指南。指南以 macOS 为主，Windows 使用 runtime.json 的 D:/artcraft 路径；不要照抄 /Applications 或旧版 token 配置。存在历史章节自相矛盾时，实时工具结果优先。

| 应用 | 本机版本 | 适配入口 |
|---|---|---|
| filmcraft | filmcraft-cli 0.18.0 | [详细指南](../../artcraft-filmcraft/references/workflow.md) |
| effectcraft | effectcraft-cli 0.22.0 | [详细指南](../../artcraft-effectcraft/references/workflow.md) |
| photocraft | photocraft-cli 0.21.0 (efb7ebd0c, 2026-11-06) | [详细指南](../../artcraft-photocraft/references/workflow.md) |
| vectorcraft | vectorcraft-cli 0.22.0 | [详细指南](../../artcraft-vectorcraft/references/workflow.md) |
| designcraft | designcraft-cli 0.18.0 | [详细指南](../../artcraft-designcraft/references/workflow.md) |
| figcraft | figcraft-cli 0.16.0 | [详细指南](../../artcraft-figcraft/references/workflow.md) |
| soundcraft | soundcraft-cli 0.18.0 (windows x86_64) | [详细指南](../../artcraft-soundcraft/references/workflow.md) |
| lightcraft | lightcraft-cli 0.19.0 | [详细指南](../../artcraft-lightcraft/references/workflow.md) |
| deckcraft | deckcraft-cli 0.16.0 | [详细指南](../../artcraft-deckcraft/references/workflow.md) |
| gridcraft | gridcraft-cli 0.17.0 | [详细指南](../../artcraft-gridcraft/references/workflow.md) |
| wordcraft | wordcraft-cli 0.16.0 | [详细指南](../../artcraft-wordcraft/references/workflow.md) |
| pdfcraft | pdfcraft-cli 0.19.0 | [详细指南](../../artcraft-pdfcraft/references/workflow.md) |
| craftanything | craft-anything-cli 0.5.0 | [详细指南](../../artcraft-craftanything/references/workflow.md) |

未安装且未注册：CADCraft、SolidCraft、TextureCraft、MaterialCraft。GUI 附着未整体实测，不因文档提及便标为通过。
