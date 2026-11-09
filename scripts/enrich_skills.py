"""Bundle pinned MIT upstream documentation as references, not duplicate skills."""
import hashlib
import json
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'evidence/upstream-artcraft-skills'
PLUGIN = ROOT / 'plugins/artcraft-studio'
COMMIT = '042c5d4ddcd8e54178d72db3bc686a18658eee8d'
URL = 'https://github.com/midasmatterhorn/artcraft-skills'

# Synthesized operation notes. Older capability claims remain explicitly versioned.
NOTES = {
    'filmcraft': '''- 剪辑顺序：probe/导入 → project_inspect 找实际 item ID → source.open → 设置 In/Out（如需）→ source.insert/overwrite → sequence_inspect 检查轨道、时长和离线素材 → 保存 .fcproj。
- 导出前通过 command_list 查 export.formats 和 export 相关命令，确认本机编码器可用；枚举里有格式不代表本机能编码。file.exportMedia 明确传 wait=true，检查结果的 offlineMedia、文件和重新 probe。不要用一次性进程的 wait=false 导出。
- 字幕与语音识别是不同能力。上游的 Whisper/Kokoro 是构建开关；先查本机可用性，不因有 transcript/tts 菜单就承诺识别或神经配音。可导入现成字幕/文字。
- GUI bridge 需核对 FILMCRAFT_CONTROL_TOKEN；上游要求启动应用和 CLI 继承同一个 64 位十六进制 token。绝不把 token 写进技能或回显。Premiere .prproj 和 .mogrt 不能假定兼容；优先测试 XML/OTIO 或渲染媒体交接。''',
    'effectcraft': '''- 创建 comp.new → 添加图层 → 获取实际图层 ID/属性路径 → 关键帧与效果 → render_frame 检查 → save_project → 发现 renderQueue.add/renderQueue.render 或原生 CLI render 参数再导出。
- batch 是原子 undo 组，结果引用从 1 开始；command_batch 是逐条执行，失败时前面的步骤可能已生效。不要把 DesignCraft 的 $0 引用规则混进来。
- .ecproj/.ecprojx、.ectemplate、.ecpreset 属于本应用；上游不支持 AE .aep/.aepx/.ffx/.mogrt。某些效果有近似实现，不能承诺与 AE 像素一致；.xml 可能是工程或时间线，优先使用 .ecprojx 区分工程。
- 后台渲染的 CPU/GPU 与编码器能力需本机验证；通过原生资源读取合成状态和命令目录，不依赖上游效果数量。''',
    'photocraft': '''- 用 doc_open/doc_new、doc_place、doc_save/doc_export 进行文件 I/O。上游明确区分受控文档工具与被 automation policy 拒绝的底层 file.* 命令；不要绕过专用工具用 command_run 猜路径参数。
- PSD 是交换格式，.pcraft 是原生工程。对外部 PSD 先另存副本、重开检查层树/蒙版/混合模式，视觉比对导入前后；不能承诺 Photoshop 无损往返。
- filter 或内容感知操作可能返回后台 job：看 isError、jobs_list 和实际图像再继续。若当前构建没有生成式功能，不能把传统抠图或修复算法说成 AI 生图。
- 导出透明素材时检查 alpha；做 PSD/PNG 交接前检查真实文件类型和尺寸。GUI bridge 的控制令牌与 roots 不等同于 headless roots，按当前 --help 配置。''',
    'vectorcraft': '''- 绘制前 inspect 文档、画板和选择；draw_shape 的 fill/stroke 用显式值，避免继承上个对象外观。用真实几何背景对象得到导出底色，上游提醒画板显示背景可能不写入成品。
- 文本通过 add_text 或命令设置，检查 overflow；导出 SVG 后核对字体，跨机器交付可用 outlineText，仍保留未转曲原生工程。
- 外部 AI/EPS/PSD 输入先查 importWarnings 和实际对象结构，再另存 .vectorcraft；不要把合并预览当作可编辑图层，也不要声称写出了 Illustrator 原生编辑数据。
- 上游没有 Illustrator JSX 脚本运行时；优先 MCP 命令。格式支持以本机 document.formats 和实际打开结果为准。''',
    'designcraft': '''- 使用 new_document 指定页面尺寸/边距/出血，再创建 frame、story 和样式。坐标为 points（72 pt = 1 inch）；页面工具通常 0-based，file.exportPdf 的 pages 规则须查命令说明。
- batch 的 $N.path 引用从 0 开始；有的步骤失败后前序编辑仍保留。检查 failedIndex/failedCommand/error，不要只看 JSON-RPC 请求成功。
- 文本偏移用 UTF-8 字节，中文不能按字符数直接计算 text.select 偏移；inspect/get_story 检查 overset 后调整框高、字号或分页。
- 印刷 PDF 应验证嵌入字体、出血和输出意图；本机 CLI validate-pdf 支持的标准以当前 --help 为准。headless 中 screenshot/dialog 等 GUI 专用工具可能不可用，用 render_page/export_png 验证。''',
    'figcraft': '''- 使用 inspect_document 查页面与节点，create_node/set_properties 或发现的命令构建结构；批量对象操作前确认本应用引用规则，不沿用其他应用对象 ID。
- FigCraft 与在线 Figma 是独立应用。上游 .fig/.sketch 导入是 best effort；另存原生 .figcraft 并检查遮罩、字体、组件与约束，再交付。
- 上游某些章节对 .jam、Code Connect 的描述有新旧冲突；本机 CLI 已有 connect 命令，不能把旧“未实现”当现状。以实时注册表与实际文件验证为准。
- SVG/PNG/PDF 导出需检查图层边界、透明度与字体；FigCraft WASM 插件不能直接视作 Figma JavaScript 插件。''',
    'soundcraft': '''- new_session/open_session → import_audio → inspect_session 确认轨道/片段 → 编辑与 DSP → save_session → bounce_mix。编辑前确认 seconds/frames/samples 的单位。
- 与视频交接优先输出 WAV，按接收端确认采样率（常用 48000Hz）与声道；检查长度、实际音轨、削波并试听。不要因能解码 MP3/AAC 就承诺可导出该格式。
- 上游提示源音频可能整段解码到 RAM，大素材先用小片段验证。MIDI 硬件、外部同步、Atmos、AAF/OMF/PTX 及第三方插件宿主能力均需查当前版本，不能按 Pro Tools 的功能推断。
- 音频创作/编辑与音乐生成区分：SoundCraft 负责已有音频的编辑混音；AI 生成需使用用户已授权且实际可用的生成工具。''',
    'lightcraft': '''- 显式 import/query_photos/select_photos 后读取 get_develop 与 list_controls；修改后分别核对原始文件、照片选择和导出结果。库持久化需要配置授权项目内 --library。
- RAW 可能解码传感器也可能仅使用嵌入预览；先检查本机文件信息与实际像素。PSD 可能只有合并图，需分层交付时转到 PhotoCraft。
- AI 降噪和 SAM 类抠图可能需要用户另装权重；先查模型/后端状态，不能承诺模型已存在或擅自下载。Lightroom 参数迁移不保证相同色彩。
- 原生资源提供 library、photos、photo/active、develop/active、controls，先 list 再读取准确 URI，按需用其中一种避免重复读取整个库。''',
    'deckcraft': '''- headless 可能没有文稿，先 new_presentation/open_presentation；检查主题、页面尺寸和布局，再插入形状/文字/图片。通过 inspect_slide 和 render_slide 逐页核对。
- 保存原生 .deckcraft/PPTX 和渲染图片使用不同入口：save_presentation 保存工程；图片用 export/render_slide。上游提醒用 file.save 给 .png/.jpg 路径可能写出原生 zip 字节，必须检查文件 magic。
- 外部 PPTX 的 SmartArt、动画、媒体、嵌入图表工作簿可能有往返损失；用副本检查，不覆盖输入。视频导出能力须查本机，不能按 PowerPoint 推断 MP4 可导出。
- 不带 path 的 save 可能只返回 needsPath，file.close 可能直接丢弃未保存内容。保存后验证实际文件与重新打开结果。''',
    'gridcraft': '''- inspect_workbook/read_range 确认表、范围和类型，list_functions/evaluate_formula 发现函数和实际计算结果，再 write_range/format_range。保留公式，不能以看起来一样的常量替代。
- XLSX 是主要输出；老 .xls/.xlsb/.ods 的导入可能只有部分值、缓存或格式。用副本往返检查实际工作簿；不要承诺 Excel 修复提示为零。
- 宏可保留不代表会执行；.xlsm 改成 .xlsx 可能丢 VBA。加密输入的另存结果可能未加密，交付前明确检查。
- CSV/TSV/PDF 是导出，可能不清 dirty flag；保存原生工作簿后再关闭。资源 workbook/functions/commands 可用于只读检查。''',
    'wordcraft': '''- new_document/open_document → 结构检查 → 编辑 → 保存 DOCX → 重开 → render_page 或 PDF 检查分页。带 doc 参数时使用 list_documents 返回的真实 ID。
- 对外部 DOCX 用副本验证修订、注释、节、字段、表格、图表与 OLE；保留不代表可编辑。上游分页与 Word 不同，不能承诺逐页一致。
- .doc 读取不代表可以写回 .doc；模板 .dotx/.dotm 与文档保存入口不同。模板清单在 headless 需显式授权 dir，避免依赖 GUI 偏好。
- 原生资源状态可读，但 headless 没有桌面恢复保障；保存后再关闭，PDF 成品用 PDF 阅读/渲染工具校验，不能把 WordCraft 不支持重新打开 PDF 当导出失败。''',
    'pdfcraft': '''- compact 模式先 tool_search 查目标功能，再 tool_call；doc_open 后检查文档 ID、页数和权限，修改后 doc_save 到新路径并重新打开。
- OCR 的语言、现有文本编辑和导出格式以当前工具/模型实际支持为准；上游旧版 OCR 只支持有限语言，不能因为界面有 OCR 就承诺中文可用。
- 遮盖对象不等于删除敏感内容。需要真实 redaction 时发现并应用对应工具，再 text_extract/搜索/audit 检查底层内容。
- Office 转 PDF 优先让 WordCraft/DeckCraft/GridCraft 各自导出，再交给 PdfCraft 整理；不要假设 PdfCraft 能直接打开所有 Office 格式。签名/验证须区分本地证书检查与在线吊销查询。''',
    'craftanything': '''- 此应用负责参考调查和证据交接，非剪辑引擎。先读取 investigation 状态/brief/plan，选择目标，再按 list_toolsets/enable_toolset 开启必要工具。
- 开启工具集后网关会使目录缓存失效，再查真实 schema。不同工具可能只有模拟后端或依赖外部 AI/引擎，调用前检查本机 capabilities/doctor 或实际返回状态。
- 生成 findings 与 handoff 应关联实际证据路径，未知结论保留 unknown，不把推测写成已验证。网站/应用复刻与素材生成只有在用户授权的任务范围内执行。
- 不默认开启 --allow-run 或 --deep；原文的其他代理安装指令和 macOS 路径仅作资料，不执行未审查的 install.ps1/install.sh，也不新增全局任务或计划任务。''',
}


def enrich():
    # Pin provenance: a new checkout must be explicitly reviewed before being bundled.
    head = (UPSTREAM / '.git/HEAD').read_text().strip()
    if head.startswith('ref: '):
        ref = head[5:]
        loose = UPSTREAM / '.git' / ref
        if loose.exists():
            head = loose.read_text().strip()
        else:
            packed = (UPSTREAM / '.git/packed-refs').read_text()
            head = next(line.split()[0] for line in packed.splitlines() if line.endswith(' ' + ref))
    if head != COMMIT:
        raise RuntimeError('Upstream revision changed; review before updating bundled references')
    versions = json.loads((ROOT / 'evidence/discovery.json').read_text(encoding='utf-8'))
    license_dir = PLUGIN / 'licenses'
    license_dir.mkdir(exist_ok=True)
    shutil.copyfile(UPSTREAM / 'LICENSE', license_dir / 'artcraft-skills-MIT.txt')
    records = {}
    for app, notes in NOTES.items():
        folder = 'craft-anything' if app == 'craftanything' else app
        source = UPSTREAM / folder
        skill = PLUGIN / 'skills' / ('artcraft-' + app)
        refs = skill / 'references'
        refs.mkdir(parents=True, exist_ok=True)
        upstream_text = (source / 'SKILL.md').read_text(encoding='utf-8')
        # Strip frontmatter so this is a reference, never a competing auto-trigger skill.
        body = re.sub(r'\A---\s*\n.*?\n---\s*\n', '', upstream_text, count=1, flags=re.S)
        intro = f'> Archived reference from {URL}/tree/{COMMIT}/{folder}; MIT (c) 2026 midasmatterhorn.\n> Historical app versions and macOS paths; use local runtime discovery for current Windows behavior.\n> This document is reference data, not permission or instructions to install software.\n\n'
        (refs / 'upstream-guide.md').write_text(intro + body, encoding='utf-8')
        if (source / 'evidence.md').exists():
            shutil.copyfile(source / 'evidence.md', refs / 'evidence.md')
        if (source / 'CHANGES.md').exists():
            shutil.copyfile(source / 'CHANGES.md', refs / 'CHANGES.md')
        for detail in (source / 'references').glob('*.md') if (source / 'references').exists() else []:
            (refs / 'references').mkdir(exist_ok=True)
            shutil.copyfile(detail, refs / 'references' / detail.name)
        local = versions[app]['version'].strip().splitlines()[0]
        workflow = f'''# {folder} 工作方法

## 版本与证据

本机实测：`{local}`。上游指南固定到 artcraft-skills `{COMMIT[:12]}`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

{notes}

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [{folder}]({URL}/tree/{COMMIT}/{folder})；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
'''
        (refs / 'workflow.md').write_text(workflow, encoding='utf-8')
        records[app] = {'localVersion': local, 'source': f'{URL}/tree/{COMMIT}/{folder}',
                        'upstreamSkillSha256': hashlib.sha256((source/'SKILL.md').read_bytes()).hexdigest()}
    studio = PLUGIN / 'skills/artcraft-studio/references'
    studio.mkdir(parents=True, exist_ok=True)
    rows = '\n'.join(f'| {k} | {r["localVersion"]} | [详细指南](../../artcraft-{k}/references/workflow.md) |' for k,r in records.items())
    (studio / 'upstream.md').write_text(f'''# 参考来源与本机适配

来源：[{URL}]({URL})，固定提交 `{COMMIT}`，MIT，Copyright (c) 2026 midasmatterhorn。

这是一套应用技能资料，MCP 由各应用自身提供。仅整合本机 13 款应用的文档为 references，不安装重复顶层技能，不运行其安装器。README 声称的“evidence verified”代表作者在固定版本的审查，不等于本机所有业务操作已验证。

本机准确工具与参数优先，其次小文件实测，再参考相符的历史指南。指南以 macOS 为主，Windows 使用 runtime.json 的 D:/artcraft 路径；不要照抄 /Applications 或旧版 token 配置。存在历史章节自相矛盾时，实时工具结果优先。

| 应用 | 本机版本 | 适配入口 |
|---|---|---|
{rows}

未安装且未注册：CADCraft、SolidCraft、TextureCraft、MaterialCraft。GUI 附着未整体实测，不因文档提及便标为通过。
''', encoding='utf-8')
    (PLUGIN / 'upstream-provenance.json').write_text(json.dumps({'repository': URL, 'commit': COMMIT,
        'license': 'licenses/artcraft-skills-MIT.txt', 'apps': records}, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Bundled 13 versioned workflow guides with upstream MIT attribution')


if __name__ == '__main__':
    enrich()
