"""End-to-end MCP checks using only generated files under the local workspace."""
import base64
import json
import pathlib
import sys

from probe import Client

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORK = ROOT / 'workspace'
LOG = []


def unpack(result):
    for item in result.get('content', []):
        if item['type'] == 'text':
            try:
                return json.loads(item['text'])
            except ValueError:
                return item['text']
    return result


def main():
    c = Client([sys.executable, str(ROOT / 'plugins/artcraft-studio/server.py')])
    active = set()

    def gateway(name, args):
        result = c.request('tools/call', {'name': name, 'arguments': args}, timeout=120)
        LOG.append({'gateway': name, 'arguments': args, 'result': {
            **result, 'content': [{k: (f'<{len(v)} base64 chars>' if k == 'data' else v)
                                  for k, v in item.items()} for item in result.get('content', [])]}})
        if result.get('isError'):
            raise AssertionError(result)
        return result

    def call(app, tool, **args):
        active.add(app)
        result = gateway('artcraft_call', {'app': app, 'tool': tool, 'arguments': args})
        return unpack(result)

    try:
        assert c.initialize()['serverInfo']['name'] == 'artcraft-studio'
        assert len(c.request('tools/list')['tools']) == 5
        apps = unpack(gateway('artcraft_apps', {}))['apps']
        assert len(apps) == 13 and all(a['available'] for a in apps.values())
        for app in apps:
            active.add(app)
            result = unpack(gateway('artcraft_tools', {'app': app}))
            assert result['tools'], app
            print(app, len(result['tools']), 'gateway tools OK', flush=True)
            resources = unpack(gateway('artcraft_resources', {'app': app, 'action': 'list'}))['resources']
            assert resources, app
            uri = next((r['uri'] for r in resources if r['uri'].endswith('://commands')),
                       resources[-1]['uri'])
            resource = unpack(gateway('artcraft_resources', {'app': app, 'action': 'read', 'uri': uri}))
            assert resource.get('contents'), (app, resource)
            print(app, len(resources), 'native resources; read OK', flush=True)

        # Reads and calls reuse tool schema, while explicit refresh reloads it.
        status = unpack(gateway('artcraft_session', {'app': 'filmcraft', 'action': 'status'}))
        count = status['toolListRequests']
        brief = unpack(gateway('artcraft_tools', {'app': 'filmcraft', 'detail': 'summary', 'query': 'inspect'}))
        assert brief['tools'] and all('inputSchema' not in t for t in brief['tools'])
        call('filmcraft', 'project_inspect')
        same = unpack(gateway('artcraft_session', {'app': 'filmcraft', 'action': 'status'}))
        assert same['toolListRequests'] == count
        gateway('artcraft_tools', {'app': 'filmcraft', 'refresh': True})
        refreshed = unpack(gateway('artcraft_session', {'app': 'filmcraft', 'action': 'status'}))
        assert refreshed['toolListRequests'] == count + 1
        refused = c.request('tools/call', {'name': 'artcraft_resources', 'arguments': {
            'app': 'filmcraft', 'action': 'read', 'uri': 'file:///unadvertised'}})
        assert refused.get('isError') is True
        print('Schema cache / explicit refresh / compact discovery / resource URI boundary OK', flush=True)
        before = unpack(gateway('artcraft_tools', {'app': 'craftanything', 'detail': 'summary'}))['total']
        call('craftanything', 'enable_toolset', toolset='formats')
        enabled = unpack(gateway('artcraft_tools', {'app': 'craftanything', 'detail': 'summary'}))
        assert enabled['total'] > before, enabled
        print('Dynamic toolset cache invalidation OK:', before, '->', enabled['total'], flush=True)

        # Stateful design, native save, PNG export, new document, reopen and verify persisted text.
        call('designcraft', 'new_document', width=480, height=270, title='ArtCraft MCP verified', intent='web')
        call('designcraft', 'execute', command='frame.create', params={
            'rect': [24, 24, 420, 100], 'content': 'text', 'text': 'ArtCraft + Codex\nMCP connection verified'})
        project = WORK / 'projects/connection-test.designcraft'
        preview = WORK / 'outputs/connection-test.png'
        call('designcraft', 'save_document', path=str(project))
        call('designcraft', 'export_png', path=str(preview), scale=1)
        assert project.stat().st_size > 100 and preview.stat().st_size > 100
        call('designcraft', 'new_document', title='temporary')
        call('designcraft', 'open_document', path=str(project))
        doc = call('designcraft', 'inspect_document')
        assert 'MCP connection verified' in json.dumps(doc)
        print('DesignCraft create/edit/save/export/reopen OK', flush=True)

        # Cross-app real media import, sequence, save, frame render and reopen.
        call('filmcraft', 'command_run', id='file.newProject', params={'name': 'ArtCraft MCP test'})
        call('filmcraft', 'command_run', id='file.newSequence', params={
            'name': 'Connection Test', 'width': 480, 'height': 270, 'fps': 24, 'video': 1, 'audio': 1})
        call('filmcraft', 'media_import', paths=[str(preview)])
        commands = call('filmcraft', 'command_list', filter='insert')
        (ROOT / 'evidence/filmcraft-insert-commands.json').write_text(json.dumps(commands, ensure_ascii=False, indent=2), encoding='utf-8')
        project_state = call('filmcraft', 'project_inspect')
        (ROOT / 'evidence/filmcraft-project-state.json').write_text(json.dumps(project_state, ensure_ascii=False, indent=2), encoding='utf-8')
        media = next(x['item'] for x in project_state['root']['children'] if x['type'] == 'Still Image')
        call('filmcraft', 'command_run', id='source.open', params={'item': media})
        call('filmcraft', 'command_run', id='source.insert', params={})
        sequence = call('filmcraft', 'sequence_inspect')
        assert 'connection-test' in json.dumps(sequence), sequence
        video = WORK / 'outputs/connection-test.mp4'
        call('filmcraft', 'command_run', id='file.exportMedia', params={
            'path': str(video), 'format': 'h264', 'audio': False,
            'width': 480, 'height': 270, 'fps': 24, 'wait': True})
        assert video.stat().st_size > 1000
        for seconds in (0, 2, 4):
            result = gateway('artcraft_call', {'app': 'filmcraft', 'tool': 'render_frame',
                                             'arguments': {'seconds': seconds, 'max_side': 480}})
            image = next(x for x in result['content'] if x['type'] == 'image')
            (WORK / f'outputs/video-frame-{seconds}.png').write_bytes(base64.b64decode(image['data']))
        film = WORK / 'projects/connection-test.fcproj'
        call('filmcraft', 'command_run', id='file.saveAs', params={'path': str(film)})
        assert film.stat().st_size > 100
        call('filmcraft', 'command_run', id='file.open', params={'path': str(film)})
        assert 'Connection Test' in json.dumps(call('filmcraft', 'project_inspect'))
        print('FilmCraft sequence/import/insert/H264 export/3 frames/save/reopen OK', flush=True)

        # Native error and unknown backend errors must remain visible to the caller.
        bad = c.request('tools/call', {'name': 'artcraft_call', 'arguments': {
            'app': 'filmcraft', 'tool': 'not_a_real_tool', 'arguments': {}}})
        assert bad.get('isError') is True
        print('Error propagation OK', flush=True)
    finally:
        for app in active:
            gateway('artcraft_session', {'app': app, 'action': 'close'})
        c.proc.stdin.close()
        assert c.proc.wait(timeout=10) == 0
        (ROOT / 'evidence/gateway-verification.json').write_text(json.dumps(LOG, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
