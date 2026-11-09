# 本机连接

CLI：`D:\artcraft\soundcraft\SoundCraft\soundcraft-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `soundcraft` 的 command/args 是实际启动配置。网关 `artcraft_session(app="soundcraft", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
soundcraft-cli: SoundCraft without a window

Usage: soundcraft-cli <COMMAND>

Commands:
  info      Print an audio file's format as JSON, or a .scraft session's summary
  convert   Convert an audio file: resample, change the bit depth, normalize
  run       Run engine commands on a new, demo or saved session
  script    Run a file of engine commands, one `ID JSON` per line
  commands  List the engine commands
  describe  Print one engine command's details as JSON
  app       Call a running app's control channel
  mcp       Serve MCP on stdin and stdout
  parity    Print the parity report (markdown)
  plugins   List the built-in plugins
  help      Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
  -V, --version  Print version
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
