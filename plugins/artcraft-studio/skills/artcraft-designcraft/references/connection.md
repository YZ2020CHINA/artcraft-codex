# 本机连接

CLI：`D:\artcraft\designcraft\DesignCraft\designcraft-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `designcraft` 的 command/args 是实际启动配置。网关 `artcraft_session(app="designcraft", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
usage: designcraft-cli run [--in FILE | --sample] [--cmd ID[=JSON]]... [--page N] [--scale S] [--pdf-options JSON] [--export OUT] [--all-pages DIR]
         (--page, --scale and --pdf-options apply to the exports that follow them)
       designcraft-cli commands [FILTER]
       designcraft-cli describe COMMAND
       designcraft-cli script [FILE|-] [--in FILE | --sample] [--connect PORT] [--save OUT] [--export OUT] [--keep-going]
       designcraft-cli app [--port PORT] COMMAND [JSON] | --method METHOD [JSON]
       designcraft-cli mcp [--connect PORT] [--sample] [--automation-read-root DIR]... [--automation-write-root DIR]...
         the roots confine every file the agent's commands read (open, placed images, data sources, libraries) and
         write (save, export, package) to those folders, links followed. Each may be given more than once; a kind
         left out grants none of its access.
         They run the in-process server, so they conflict with --connect (a running app is not confined by them).
       designcraft-cli perf [--pages N] [--runs N] [--strict]
       designcraft-cli bench FILE [--runs N]
       designcraft-cli validate-pdf FILE.pdf [--standard x4|x1a]  # built-in PDF/X checks (including visible unembedded fonts; the standard defaults to the file's own)
       designcraft-cli thumbnail FILE.designcraft OUT.png [SIZE]  # the saved first-page preview, at most SIZE px
       designcraft-cli links
       designcraft-cli --version

Community: https://discord.gg/artcraft  ·  https://getartcraft.com/apps/designcraft  ·  https://github.com/storytold/designcraft
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
