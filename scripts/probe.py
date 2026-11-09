"""Exercise native MCP initialize + tools/list; save exact schemas for authoring."""
import concurrent.futures
import json
import pathlib
import queue
import subprocess
import threading
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]


class Client:
    def __init__(self, command):
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        self.lines = queue.Queue()
        self.errors = []
        self.counter = 0
        threading.Thread(target=self.read, daemon=True).start()
        threading.Thread(target=self.drain_errors, daemon=True).start()

    def read(self):
        for line in self.proc.stdout:
            try:
                self.lines.put(json.loads(line))
            except (ValueError, UnicodeError):
                pass

    def drain_errors(self):
        for line in self.proc.stderr:
            self.errors.append(line.decode('utf-8', errors='replace'))

    def send(self, obj):
        self.proc.stdin.write((json.dumps(obj, ensure_ascii=False) + '\n').encode('utf-8'))
        self.proc.stdin.flush()

    def request(self, method, params=None, timeout=45):
        self.counter += 1
        ident = self.counter
        self.send({'jsonrpc': '2.0', 'id': ident, 'method': method, 'params': params or {}})
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            response = self.lines.get(timeout=max(.01, end - time.monotonic()))
            if response.get('id') == ident:
                if 'error' in response:
                    raise RuntimeError(str(response['error']))
                return response.get('result', {})
        raise TimeoutError(method)

    def initialize(self):
        result = self.request('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {},
                                             'clientInfo': {'name': 'artcraft-local-check', 'version': '1.0'}})
        self.send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        return result

    def close(self):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def check(item):
    name, data = item
    args = ['mcp']
    if name == 'vectorcraft':
        args += ['--headless']
    if name in ('lightcraft', 'pdfcraft'):
        args += ['--compact']
    client = Client([data['cli'], *args])
    try:
        init = client.initialize()
        tools = []
        params = {}
        while True:
            page = client.request('tools/list', params)
            tools.extend(page.get('tools', []))
            if not page.get('nextCursor'):
                break
            params = {'cursor': page['nextCursor']}
        result = {'ok': True, 'command': data['cli'], 'args': args, 'initialize': init, 'tools': tools}
    except Exception as exc:
        result = {'ok': False, 'error': repr(exc), 'stderr': ''.join(client.errors)[-4000:]}
    finally:
        client.close()
    print(name, result.get('ok'), len(result.get('tools', [])), result.get('error', ''), flush=True)
    return name, result


if __name__ == '__main__':
    discovery = json.loads((ROOT / 'evidence/discovery.json').read_text(encoding='utf-8'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = dict(pool.map(check, discovery.items()))
    (ROOT / 'evidence/native-mcp.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
