# 本机连接

CLI：`D:\artcraft\gridcraft\GridCraft\gridcraft-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `gridcraft` 的 command/args 是实际启动配置。网关 `artcraft_session(app="gridcraft", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
usage:
  gridcraft-cli info <file> [--json]                      sheets, used ranges, tables, charts, names
  gridcraft-cli convert <in> <out> [--sheet NAME]         xlsx/csv/tsv/json/html/pdf by extension
  gridcraft-cli eval <formula> [--in FILE] [--sheet S] [--cell A1] [--json]
  gridcraft-cli cat <file> [--range A1:D20] [--sheet S] [--formulas] [--csv]
  gridcraft-cli check <file-or-dir>... [--json] [--tolerance 1e-9] [--max-report N]
                     cached-value calc oracle + XLSX round-trip fidelity (exit 1 on any difference)
  gridcraft-cli run [--in FILE | --sample NAME] [--cmd 'id={json}']... [--script FILE.jsonl]
                     [--out FILE] [--print RANGE] [--quiet]
                     a script line is id={json} or {"command": "id", "params": {…}};
                     blank lines and lines starting with # or // are skipped
  gridcraft-cli commands [--json] [--search X]
  gridcraft-cli functions [--json] [--search X] [--category C]
  gridcraft-cli mcp [--connect PORT] [--in FILE | --sample NAME]
  gridcraft-cli send <port> <method> [json]
  gridcraft-cli version
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
