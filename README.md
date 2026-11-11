# ArtCraft × Codex 本地创作工作台

已将 `D:\artcraft` 的 13 个原生 MCP 服务封装成一个本地 Codex 插件。

插件：`artcraft-studio@artcraft-local`，版本 `1.1.0`。已通过 Codex CLI 安装并确认 `installed: true`、`enabled: true`。包含 14 个 skill：一个协作入口和 13 个应用 skill。使用本机 Python 标准库，不需要 API key、云服务或新增运行依赖。PyYAML 仅在 `.validation-deps` 中用于官方技能校验器。

## Codex 中使用 Claude / GPT 调用插件（2026-11-11 更新）

这次更新后，**在 Codex 里切换到 Claude 模型（例如通过 Magpie 等中转站接入的 Claude API）也可以正常调用本插件的工具和 skill**，与使用 GPT 模型时一致。

- 已在 Codex 桌面版（Windows）实测：修复后 Claude 与 GPT 会话都能加载这组本地插件的 MCP 工具，并实际调用了 Blender、Aseprite、Flux、Stable Audio 的状态工具。
- 原因：Codex 读取插件 `mcp.json` 时只接受 `type`、`command`、`args`、`env`、`cwd`，`command` 必须是裸可执行名，并会拒绝 `startup_timeout_sec`、`tool_timeout_sec` 等字段；旧格式导致部分模型会话里插件工具不出现。
- 现在构建脚本生成的 `mcp.json` 统一使用 `cmd.exe` 调用插件目录内的 `launch-mcp.cmd`，本机 Python/Node 的绝对路径和环境变量写在启动器里。
- 已安装旧版本的用户：重新运行安装/构建脚本后，**新开一个 Codex 聊天或重启 Codex** 即可生效。
- 长任务需要更长超时时，可在 `~/.codex/config.toml` 对应的 `[mcp_servers.<名称>]` 中设置 `tool_timeout_sec`。

## 开始使用

重新打开 Codex 或新建本地聊天以加载新增插件。当前聊天的工具目录不会因写入配置而自动获得新工具；若没有 ArtCraft 工具，先检查插件启用状态并重载。

可以直接说：

- “使用 $artcraft-studio，帮我做一张海报，保留可编辑工程。”
- “使用 $artcraft-filmcraft 剪辑这组视频，用 $artcraft-soundcraft 处理音频。”
- “使用 $artcraft-effectcraft 做一个标题动画，再交给 FilmCraft 合成。”
- “使用 $artcraft-photocraft 编辑这张图，导出 PNG 和分层文件。”

网关提供 `artcraft_apps`、`artcraft_tools`、`artcraft_call`、`artcraft_resources`、`artcraft_session` 五个入口。先按任务查询实际工具 schema，再调用原生工具；所有 293 个原生工具均可按需发现，不必启动全部应用。

## 目录和保存

- `workspace/assets`：本次任务的输入素材。
- `workspace/projects`：原生可编辑工程。
- `workspace/outputs`：导出成品。
- `plugins/artcraft-studio`：插件源码、网关和 14 个技能。
- `evidence`：实机版本、工具 schema、验证记录。
- `project-blocks`：积木工坊独立程序和项目画布。

**当前是 headless 模式**：后台使用应用原生引擎，不会自动编辑桌面窗口正在打开的文档。GUI 联动参数因软件而异；各应用 skill 的 `references/connection.md` 保存了本机帮助，按需切换 `--bridge`、`--connect` 或 `--attach`。切换前先保存再关闭对应会话。

9 款应用的文件读写被原生 automation roots 限制在 workspace。FilmCraft、GridCraft、LightCraft、Craft Anything 的当前启动模式未设置原生文件根隔离，调用仍只使用当前任务授权路径。导入其他项目素材时，把文件放入 assets，或在有权限时按任务修改 `runtime.json` 中相应根目录并重启该应用会话；不要默认开放整盘。

本地 marketplace 和 MCP 启动参数引用本项目路径，因此请保留此目录。若移动项目、升级 Codex 后 Python 路径改变，需重新生成配置并重新注册安装；`scripts/build_plugin.py` 使用实际运行它的 Python 路径生成 mcp.json。

## 已验证

2026-11-07（Asia/Shanghai）：

- 13/13 原生 MCP 完成 initialize、tools/list，合计 293 个工具。
- 13/13 通过统一网关完成工具发现；会话维持状态，未知工具错误能传回调用方。
- DesignCraft 创建文字版式，保存 `.designcraft`、导出 PNG，重新打开后文字保留。
- FilmCraft 导入上述 PNG，插入 24 fps、480 × 270 时间线，导出 5 秒 H.264 MP4，保存和重新打开 `.fcproj`。
- 实际查看 0、2、4 秒预览帧，画面与源图一致；原生 probe 确认 MP4 为 H.264、480 × 270、24 fps、5 秒，无音轨。
- 14/14 skill 通过官方 quick_validate.py。
- Codex plugin list 确认插件已安装并启用。

这验证了接入和代表性的设计→剪辑交接；其余应用尚未逐项完成业务编辑、导出、GUI 附着或音频试听验证。测试图片只用于检查连通性。

## 维护

从项目目录使用本机 Python 运行：

```text
scripts/discover.py       读取所有应用的版本与帮助
scripts/probe.py          原生 MCP 握手与工具发现
scripts/build_plugin.py   按探测结果重新生成插件配置和技能
scripts/verify.py         网关与设计→剪辑端到端检查
```

重新生成会替换生成的 skill；保留已有 runtime.json（工作根、GUI 附着参数与照片库路径不会被重置）。先保存有意定制的技能内容。网关 server.py 不是生成文件。

注册与安装：

```powershell
codex plugin marketplace add 'E:\ams 工作室（成品）\一些项目\AI\本地大模型mcp\artcraft-codex' --json
codex plugin add 'artcraft-studio@artcraft-local' --json
codex plugin list --marketplace artcraft-local --json
```

配置依据：[OpenAI MCP 文档](https://developers.openai.com/codex/mcp/) 和 [插件构建文档](https://developers.openai.com/codex/plugins/build/)。

## 1.1.0 优化

参考 [midasmatterhorn/artcraft-skills](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d) 固定版本，为本机 13 款应用加入 workflow.md 和可按需阅读的原文参考。保留 MIT 许可与来源，不执行其安装脚本；未安装的四款应用未被注册。历史指南版本较旧，不把旧限制当作当前行为。

- 新增 artcraft_resources：读取原生文档/命令/照片库/显影/调查资源。13 款共发现 38 个资源，每款读取一个代表性资源验证通过。
- artcraft_tools 支持 detail=summary 与 query；完整 schema 按需查询。会话缓存减少重复 tools/list，refresh=true 可强制更新；动态工具集与 list_changed 通知使缓存失效。
- 分应用加入保存/导出区别、字幕与语音识别区别、原生/交换格式、批次索引、GUI 认证、往返检查等操作要点；具体旧版限制仍需本机验证。
- 重建插件保留 runtime.json 定制连接和工作根；官方 Logo 保持原文件。
- 回归包含 13 应用工具与资源读取、缓存/刷新/动态工具集、新建保存重开、设计 PNG→FilmCraft 时间线→H.264 导出与 14 技能校验。

## GitHub 源码与许可

源码仓库：https://github.com/YZ2020CHINA/artcraft-codex

自有代码使用 [MIT License](LICENSE)，第三方组件、软件、模型与素材保留各自许可。开发、分支和发布流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

首次安装先运行 `python scripts/discover.py`、`python scripts/probe.py`，再运行 `python scripts/build_plugin.py` 生成本机 MCP 配置；这些命令读取你已安装的 ArtCraft，原生软件不包含在仓库内。
