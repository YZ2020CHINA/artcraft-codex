# 本机连接

CLI：`D:\artcraft\photocraft\PhotoCraft\photocraft-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `photocraft` 的 command/args 是实际启动配置。网关 `artcraft_session(app="photocraft", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
photocraft-cli: headless PhotoCraft

Usage: photocraft-cli <COMMAND>

Commands:
  convert   Convert between formats (.pcraft, .psd, .png, .jpg, .tif, .webp, .exr, …)
  info      Print the document as JSON (size, mode, depth, layer tree)
  run       Open a file (or start a new document), run engine commands in order, save the result
  batch     Apply an action list to every image in a directory
  droplet   Run a droplet (File › Automate › Create Droplet) on images and folders
  commands  List the engine command registry
  mcp       Run the MCP server on stdio (headless engine, or bridge to a running `photocraft --control <port>`)
  serve     Keep one headless session open and answer JSON lines on stdio, or on 127.0.0.1:<PORT>
  help      Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
  -V, --version  Print version
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
