# 本机连接

CLI：`D:\artcraft\effectcraft\EffectCraft\effectcraft-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `effectcraft` 的 command/args 是实际启动配置。网关 `artcraft_session(app="effectcraft", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
usage: effectcraft-cli <info|commands|exec|run|props|get|set|render-frame|render|script|mcp> [args] [--json]
  info                                     project + engine summary
  commands [--filter TEXT] [--enabled]     list engine commands
  exec <command-id> [--params JSON]        run one engine command (exec --list: list them, as `commands`)
  run <id> <json> [<id> <json> ...]        run several commands in order
  run --args-file F                        the same, one argument per line of F (no command-line length limit)
  run --commands FILE|-                    steps from FILE, or standard input for -: a JSON array of
                                           {"command": ID, "params": {...}} (or "id" for "command"), or one
                                           such object per line (JSON Lines); at most 64 MiB and 100000 steps.
                                           Repeatable; run after the <id> <json> pairs and --args-file
  props <comp> <layer> [--flat] [--time S] a layer's property tree with paths
  get <comp> <layer> <path> [--time S]     read a property
  set <comp> <layer> <path> <value> [--time S] [--expression E]
  render-frame [--comp C] [--time S | --frame N] [--max-side PX | --scale K] [--out F.png] [--transparent]
  render [--comp C] --out FILE [--format F] [--start S] [--end S] [--work-area] [--fps N]
         [--resolution full|half|third|quarter|K] [--quality best|draft] [--channels rgb|rgba]
         [--jpeg-quality N] [--bitrate KBPS] [--prores PROFILE] [--audio auto|on|off]
         [--profile main|main10] [--level auto|4.1] [--rate-control bitrate|quality] [--video-quality N]
         [--keyint FRAMES] [--webm-codec vp9|av1] [--audio-bitrate KBPS] [--opus-app audio|voice]
         [--exr-compression C] [--exr-depth half|float] | --queue
                                           (formats h264|hevc|av1|prores|webm|png|jpeg|tiff|exr|tga|gif|wav|aiff;
                                           --profile..--keyint: HEVC / AV1, --audio-bitrate/--opus-app: WebM Opus;
                                           --exr-compression none|rle|zips|zip|piz|pxr24|b44|b44a|dwaa|dwab
                                           (default zip; pxr24 on float, b44/b44a on half and dwaa/dwab are lossy),
                                           --exr-depth (default float): OpenEXR)
                                           a relative --out is relative to the working directory
                                           --progress: progress lines on stderr when it is not a terminal
                                           (progress <frames done> <total> <seconds elapsed> <seconds left|->)
  render/render-frame --template T.ectemplate [--values V.json]   render one template instance
  bench [--comp C] [--time S] [--scale K] [--n N] [--play N] [--gpu [--adv3d]]   per-layer/effect render timings;
                                           --play N renders N consecutive frames with/without the layer cache;
                                           --gpu compares CPU and GPU ms/frame for every comp at Full and Half
  bench --ops [--small] [--layers N] [--comps N] [--footage N]
                                           everyday operations on a large generated project: startup, open,
                                           save, auto-save, edits + undo/redo, timeline, Project panel
  bench --roto [--frames N] [--sam2 FILE] [--mobilesam FILE] [--fixes] [--clip FRAMES_DIR --truth MASKS_DIR] [--json]
                                           Roto Brush trackers on synthetic clips with known mattes: movement,
                                           lighting change, occlusion, leaving and re-entering the frame
  script FILE.jsx [F.ecproj] | --eval CODE run JavaScript with the After Effects-style object model
                                           (app.project, comps, layers, properties…); prints writeLn
                                           output and the result; errors exit 1 with file:line:col
  mcp [--autosave | --bridge PORT]         MCP server (JSON-RPC over stdio); --autosave preserves unsaved headless work
      [--automation-read-root DIR] [--automation-write-root DIR]
                                           confine the agent's file access: reads under a read or write root,
                                           writes under a write root (each repeatable); scripts are refused
options: --project F.ecproj | --demo | --empty   --save | --save-as F   --bridge PORT   --json   --gpu
<comp>: id or name, '-' = active comp; <layer>: id, '#n' or name; <value>: JSON or bare string
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
