# 本机连接

CLI：`D:\artcraft\deckcraft\DeckCraft\deckcraft-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `deckcraft` 的 command/args 是实际启动配置。网关 `artcraft_session(app="deckcraft", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
deckcraft-cli works on DeckCraft presentations (.deckcraft, .pptx) without a window.

  info               print a presentation's slides, layouts and theme as JSON
  render             draw slides as PNG images
  render-transition  draw frames of the transition into a slide as PNG images
  convert            save a presentation in the format OUT's extension names
  run                run commands on a presentation, then save or export it
  commands           list the commands run can use, one per line
  describe           explain one command and its parameters
  app                run a command in the DeckCraft app started with --control
  mcp                serve the commands to an agent over MCP on stdio
  bench              time opening, drawing, saving and exporting a presentation
  links              print the DeckCraft community and project links
  --version          print the version

A presentation is edited by running commands on it:

  deckcraft-cli run --cmd 'slide.new={"title":"Q3 results"}' --save q3.deckcraft

`deckcraft-cli help SUBCOMMAND`, or `deckcraft-cli SUBCOMMAND --help`, explains one subcommand;
`deckcraft-cli help run` explains how to write a command.

If an output reader closes early, run, render, render-transition and convert continue; their exit
status reflects the work, not output delivery. Stop the process to cancel them.
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
