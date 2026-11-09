# 本机连接

CLI：`D:\artcraft\pdfcraft\PdfCraft\pdfcraft-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `pdfcraft` 的 command/args 是实际启动配置。网关 `artcraft_session(app="pdfcraft", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
pdfcraft-cli info   <file.pdf> [--password PW]            document summary as JSON
                                                          (includes any declared PDF/A or PDF/UA level)
pdfcraft-cli render <file.pdf> --page N [--dpi 96] --out x.png   (.png, .jpg, .tif or .pam)
pdfcraft-cli text   <file.pdf> [--page N]                  extracted text (pages separated by form feeds)
pdfcraft-cli edit   <in.pdf> --out out.pdf [--rotate 1,3:90] [--delete 2,4] [--move 5:1]
                      [--insert-blank 1] [--title T] [--author A] [--full]
                      (options run in order; page numbers refer to the document after the earlier options)
pdfcraft-cli combine <a.pdf> <b.pdf> … --out combined.pdf
pdfcraft-cli extract <in.pdf> --pages 1,3,5-8 --out out.pdf    (pages and ranges, in the order given)
pdfcraft-cli split   <in.pdf> (--every N | --before 3,7) [--out-dir DIR]
pdfcraft-cli check  <files or dirs…> [--timeout 20] [--dpi 36] [--json out.json]
pdfcraft-cli audit  <file.pdf> [--password PW]            find faux redactions (fails when found)
pdfcraft-cli batch <files or dirs...> --steps convert,ocr,optimize --out-dir DIR
                      [--recursive] [--root DIR] [--stop-on-error]
                      [--ppi 150] [--quality 60] [--dpi 300] [--language en] [--ocr-all-pages]
pdfcraft-cli tools                                       automation tools and their JSON Schemas
pdfcraft-cli run    <tool> [key=value …] [--root DIR] [--out image.png]
pdfcraft-cli run    --script steps.json [--root DIR] [--report]
                      [{"tool": "doc_open", "args": {…}}, …]; --report prints one JSON document for the run
pdfcraft-cli mcp    [--root DIR] [--compact] [--automation-read-root DIR] [--automation-write-root DIR]
                                                           MCP server on stdin/stdout (opt-in)
                                                           --compact lists a core set of tools plus tool_search and tool_call
                                                           --automation-read-root / --automation-write-root confine the files the
                                                           agent's tools read (open, combine, import, fonts, certificates…) and
                                                           write (save, export, extract, split, reports…) to DIR, links followed;
                                                           a root left out grants none of its access. --root, when also given,
                                                           applies as well
pdfcraft-cli ui     --control FILE <method> [key=value …] [--out shot.png]
                                                           drive a running app started with --control FILE
help and feedback: https://discord.gg/artcraft
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
