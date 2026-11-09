# 本机连接

CLI：`D:\artcraft\filmcraft\FilmCraft\filmcraft-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `filmcraft` 的 command/args 是实际启动配置。网关 `artcraft_session(app="filmcraft", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
filmcraft-cli: drive FilmCraft from the shell (headless engine, or the live app with --bridge)

USAGE
  filmcraft-cli [OPTIONS] <SUBCOMMAND> [ARGS]

SUBCOMMANDS
  exec <id> [key=value ...]     run one command; prints its result as JSON
  exec <id> '<json params>'     same, params as one JSON object
  run <script.jsonl | ->        run commands, one {"id","params"} per line (# comments ok), in
                                order: file.exportMedia waits for its file before the next line
                                (and before exit) unless its params say "wait": false
  commands [filter] [--json]    list commands (id, label, shortcut, params)
  describe <id>                 one command as JSON (menu, shortcut, params, enabled now)
  inspect [project|sequence]    project tree or active sequence as JSON (default: both)
  import <file>...              import media into the project
  export <out> [--preset name] [--format f] [--range r] [--start s --end s] [--settings json]
         [--gpu-rendering auto|off]
         [--scale f] [--quality 0-100] [--no-audio] [--queue] [--allow-offline]
                                export the active sequence and wait for it to finish: with an
                                export preset (`export --list-presets`; built-in or the user's), or
                                a format (h264|hevc|prores|dnxhr|apv|mjpeg|mxf-op1a|mxf-opatom|png|tiff|bmp|gif|wav|aiff|aac, guessed
                                from the extension); --range entire|inOut|workArea, or a custom
                                range in seconds; --settings is ExportSettings JSON merged over the
                                preset; --scale renders at a fraction of the frame size (0.5 =
                                half); --quality 0-100 for the formats that take one; --no-audio
                                leaves the sound out; --queue adds to the export queue and runs it
                                instead. Offline media (missing, made offline, unreadable) renders
                                as placeholder frames: the export then lists it in `offlineMedia`,
                                warns on stderr and exits 1, unless --allow-offline accepts it
  export --list-presets [query] list export presets (name, category, format) as JSON
  render --seconds S --out f.png [--scale 0.5] [--allow-offline]
                                render one Program frame to PNG (offline media: as for export)
  probe <media> [--image-sequence]
                                media info as JSON, with MXF / Ogg / BWF details; with
                                --image-sequence <media> is the first numbered still of a sequence
  bench-decode <media> [--frames N]
  mcp                           MCP server on stdio (headless, or --bridge to the live app)
  help                          this text
  --version                     print the version

OPTIONS
  --project <p.fcproj>          open this project first (headless)
  --demo                        open the built-in demo project (headless)
  --save                        save the project back to --project when done; runs saving one
                                project take turns, so each edits what the last one saved
  --save-as <p.fcproj>          save the project to this path when done
  --bridge <127.0.0.1:PORT>     send commands to the running app (`filmcraft --control PORT`)
  --data-dir <dir>              FilmCraft data directory for user export presets (headless;
                                default: the app's data directory)
  --keep-going                  `run`: report failing lines and continue
  --compact                     one-line JSON output

VALUES
  key=value parses value as JSON when it can (3.5, true, [1,2], {"a":1}), else as a string:
  `exec timeline.razor seconds=3.5`, `exec file.newBin name=Selects`.
  Times: 254016000000 ticks per second; most commands also take seconds=, frame= or timecode=.

EXIT STATUS
  0 success · 1 a command failed, or export/render drew offline media without --allow-offline
  · 2 usage error
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
