# 本机连接

CLI：`D:\artcraft\figcraft\FigCraft\figcraft-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `figcraft` 的 command/args 是实际启动配置。网关 `artcraft_session(app="figcraft", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
FigCraft without a window

Files: .figcraft (native), .penpot (Penpot 2.x), .json (FigCraft or REST API file JSON), .fig (best effort; `info` lists what wasn't imported), .sketch (Sketch 48 or newer, best effort), .svg, .png/.jpg/.webp/.gif/.bmp (open as an image layer).

Usage: figcraft-cli [OPTIONS] <COMMAND>

Commands:
  info      Pages, node counts, top-level frames, style/variable/image counts
  export    Export frames, a layer or the whole file
  convert   Convert by extension (.figcraft, .json, .svg, .png, .jpg, .webp, .pdf, .fig, .penpot)
  render    Render the whole page with its background as png, jpg or webp
  run       Run a script of commands in a headless session, one JSON result line per step
  commands  List every command with its label, shortcut, undoable flag (*) and parameters
  mcp       Serve MCP on stdio: headless, or attached to a running app
  plugin    Publish plugins to a server's plugin directory
  connect   Publish a code repository's component mappings (code connect) to a design file
  perf      Measure the hot paths on synthetic documents and print Markdown tables
  help      Print this message or the help of the given subcommand(s)

Options:
      --no-system-fonts
          Lay text out with the fonts built into FigCraft only, for renders that match on every machine (or set FIGCRAFT_NO_SYSTEM_FONTS=1). Otherwise installed fonts are indexed the first time text is laid out, as in the app

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version

See docs/cli.md and docs/mcp.md.
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
