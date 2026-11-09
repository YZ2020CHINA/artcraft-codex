# 本机连接

CLI：`D:\artcraft\wordcraft\WordCraft\wordcraft-cli.exe`

实测版本信息：见项目 evidence/discovery.json。插件根目录 runtime.json 中 `wordcraft` 的 command/args 是实际启动配置。网关 `artcraft_session(app="wordcraft", action="close")` 会终止该应用的 headless 会话；先保存，再修改配置，再重新调用以启动新会话。其他应用不受影响。

原生启动/附着参数（来自已安装二进制的 --help；使用前核对当前帮助）：

```text
wordcraft-cli — WordCraft from the command line

USAGE:
  wordcraft-cli convert <in> <out> [--markup] [--update-fields] [--format wordml2003|flatopc]
                                              convert between formats (docx, doc [read], pdf, odt, rtf, html, md, tex, txt, json, png,
                                              xml); --update-fields refreshes unlocked fields before saving;
                                              an .xml file is a Word XML Document (Flat OPC), or with
                                              --format wordml2003 a Word 2003 XML Document;
                                              --markup (Print Markup): comments beside each page and
                                              tracked changes in pdf/png, a comment list in html/md/txt
  wordcraft-cli info <file>                   pages, words, paragraphs, properties (JSON)
  wordcraft-cli text <file>                   plain text
  wordcraft-cli inspect <file>                document structure (JSON)
  wordcraft-cli render <file> <out.png> [--page N] [--scale S]
  wordcraft-cli run [--file F | --template T] [--script FILE|-] --cmd 'id={json}' [--cmd …]
                    [--save OUT] [--print] [--author NAME]
                                              run commands headlessly, then save (--author names
                                              who tracked changes and comments are by).
                                              --script runs a JSON file (- is stdin) first:
                                              {"file"?, "template"?, "commands": [{"command": id,
                                              "params"?: {…}} | id, …], "save"?: [OUT, …]}; save
                                              formats follow the extension (docx and pdf in one run);
                                              relative paths resolve against the script's folder.
                                              file.new and file.open open another document and
                                              make it active; later commands and the saves work on
                                              the active one; view.switchWindows lists the open
                                              documents and with {"id": N} makes one active
  wordcraft-cli commands [--json]             list every command
  wordcraft-cli parity [--markdown]           feature-catalog parity
  wordcraft-cli mcp [--connect HOST:PORT | --author NAME] [--automation-read-root DIR] [--automation-write-root DIR]
                                              MCP server on stdio (headless, or bridged to the app).
                                              --automation-read-root / --automation-write-root confine
                                              the files the agent's commands read (open, insert text
                                              or picture, mail-merge data, templates…) and write (save,
                                              export, merge output…) to DIR, links followed; a root left
                                              out grants none of its access. They apply to the headless
                                              server and are an error with --connect.
  wordcraft-cli zotero <command> <file> [--cmd 'id={json}' …] [--save OUT] [--trace] [--port P]
                                              run a Zotero command on a document (Zotero must be
                                              running): addEditCitation, addEditBibliography,
                                              addNote, refresh, removeCodes, setDocPrefs
                                              (--cmd runs first, e.g. --cmd caret.docEnd)
  wordcraft-cli [<command>] -h | --help       this help
  wordcraft-cli --version

A password-protected Word file is opened with --password PASS, --password-file PATH or the
WORDCRAFT_PASSWORD environment variable; a password given on the command line is readable by
every other process, so the other two are better. A file opened with a password is written with
it again, as the app does. Exports that cannot carry a password (pdf, html, txt) stay plain.

Paper: documents created here, and HTML, Markdown and text files (which give no page size), use
the system region's paper (A4, or Letter in the US and other Letter regions), read from
LC_ALL / LC_PAPER / LANG or the platform. Set WORDCRAFT_REGION=en-US (or another tag) for the
same output on every machine.
```

可见窗口联动：仅用户需要时，按帮助用应用 exe 的 --control 启动明确的回环端口，使用匹配的 CLI --connect / --bridge / --attach。不要猜测统一端口或参数。PhotoCraft 可要求控制令牌；不要把令牌写入 skill 或聊天。带 roots 的 headless 配置通常与附着模式互斥，限制应在 GUI 启动时设置并核对。
