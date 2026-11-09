"""Update integration evidence while retaining existing canvas state and user layout."""
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / 'project-blocks/data/project.json'


def main():
    data = json.loads(PATH.read_text(encoding='utf-8'))
    specs = [
        ('requirements', '13 款 ArtCraft 应用盘点', 'done', 'D:/artcraft 下 13 个 CLI 均原生支持 MCP；已记录实机版本与帮助。',
         ['evidence/discovery.json', 'evidence/native-mcp.json'], ['13/13 initialize 与 tools/list 成功，共 293 个原生工具。']),
        ('implementation', '统一 MCP 网关', 'done', '4 个入口按需启动 13 个原生 MCP；同一应用保留状态，支持工具发现、图片返回与显式关闭。',
         ['plugins/artcraft-studio/server.py', 'plugins/artcraft-studio/runtime.json'], ['13/13 经网关发现工具成功；原生错误可见；9 款应用设置工作区 roots。']),
        ('verification', '设计与剪辑流程验证', 'done', 'DesignCraft 编辑、保存、导出和重开；FilmCraft 导入该 PNG、插入时间线、输出 5 秒 H.264、保存和重开；0/2/4 秒画面已查看。',
         ['scripts/verify.py', 'evidence/gateway-verification.json', 'workspace/projects/connection-test.designcraft', 'workspace/projects/connection-test.fcproj', 'workspace/outputs/connection-test.mp4'], ['verify.py 完整通过；probe 确认 H.264、480×270、24fps、5秒。其他应用业务导出未逐项验证。']),
        ('skills', '插件与 14 个技能', 'done', '1 个协作总入口 + 13 个专属应用 skill，附实测工具 schema、原生 CLI 帮助与 GUI 联动说明；14/14 通过官方校验。',
         ['plugins/artcraft-studio/plugin.json', 'plugins/artcraft-studio/mcp.json', 'plugins/artcraft-studio/skills', '.agents/plugins/marketplace.json'], ['14 个 skill 均输出 Skill is valid!']),
        ('installation', '安装到 Codex', 'done', '本地 marketplace 已注册，artcraft-studio 1.0.0 安装并启用。重新打开 Codex 或新聊天加载新增工具。',
         ['plugins/artcraft-studio/mcp.json'], ['codex plugin list --marketplace artcraft-local --json：installed=true, enabled=true。当前聊天尚未热加载新增工具。']),
        ('delivery', '最终交付与使用说明', 'done', '已提供使用说明、应用技能、工作区、可编辑测试工程、视频和验证证据。默认 headless；GUI 联动与其余业务场景按后续任务验证。',
         ['README.md', 'workspace/outputs/connection-test.mp4'], ['项目画布与交付说明同步到实际结果。']),
    ]
    nodes = {n['id']: n for n in data['nodes']}
    for index, (ident, title, status, summary, files, evidence) in enumerate(specs):
        if ident not in nodes:
            node = {'id': ident, 'routeType': 'common', 'color': '#73d2b3',
                    'x': 60 + (index % 3) * 440, 'y': 80 + (index // 3) * 360,
                    'characters': 'Codex', 'choices': [], 'workflow': {}}
            data['nodes'].append(node)
            nodes[ident] = node
        node = nodes[ident]
        node.update({'title': title, 'summary': summary, 'location': '\n'.join(files), 'bgm': summary})
        node.setdefault('workflow', {}).update({'status': status, 'priority': 'P1', 'files': files,
                                              'acceptance': [summary], 'blockReason': '', 'evidence': evidence})
    edges = [('requirements', 'implementation'), ('implementation', 'verification'),
             ('implementation', 'skills'), ('skills', 'installation'), ('verification', 'delivery'), ('installation', 'delivery')]
    for source, dest in edges:
        choices = nodes[source].setdefault('choices', [])
        if not any(c.get('target') == dest for c in choices):
            choices.append({'id': f'{source}_{dest}', 'text': '前置依赖', 'tag': '前置依赖', 'target': dest})
    temp = PATH.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temp, PATH)
    print('Updated canvas: ' + str(PATH))


if __name__ == '__main__':
    main()
