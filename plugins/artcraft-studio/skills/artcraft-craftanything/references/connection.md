# 本机连接

CLI：`D:\artcraft\craftanything\Craft Anything\craft-anything-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `craftanything` 的 command/args 是实际启动配置。网关 `artcraft_session(app="craftanything", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
Craft Anything on the command line: every tool, the MCP server, setup and doctor.

Usage: craft-anything-cli.exe [OPTIONS] <COMMAND>

Commands:
  mcp           Run the MCP server on stdin/stdout
  setup         Connect Craft Anything to your coding-agent apps
  doctor        Check the install, registrations, engines, AI backends and the MCP server
  uninstall     Remove Craft Anything's registrations and skill from agent apps
  commands      List every tool
  capabilities  What this install can do: toolsets, tool availability, engines
  triage        Open a file and run a first look at it
  report        Write a readable investigation report (Markdown or HTML) from findings and evidence
  chat          Ask the AI agent a question about a target (streams to stdout)
  rebuild       Study a website, app or game and have a coding agent rebuild it in a new project folder
  ai            Manage AI backends
  help          Print this message or the help of the given subcommand(s)

Options:
      --format <FORMAT>    Output format. `--output-format` always means this, even after a tool that has its own `--format` [default: json] [possible values: json, jsonl, md, text, csv, tsv]
      --json               Shorthand for --format json
      --project <PROJECT>  A project folder (`*.cany`): evidence, memory and the journal are kept there. Created if missing
      --allow-run          Allow tools that run code or change a device without asking
      --deep               Deep mode for this run only: tools may read a target's code, files and page source
      --clean-room         Clean room for this run only, whatever Settings say: nothing inside a target is read
  -h, --help               Print help
  -V, --version            Print version

Every tool is also a subcommand: `craft-anything-cli commands` lists them, `craft-anything-cli <tool> --help` shows its options.
When a tool has its own --format option (core-target-open, ...), --format after the tool name goes to the tool; pick the output with --output-format (or --format before the tool name). `report` has no format option of its own: use `report --html` for HTML.
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
