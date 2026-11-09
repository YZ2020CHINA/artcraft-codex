"""Read local ArtCraft CLI help without changing application documents."""
import concurrent.futures
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]


def inspect(exe):
    def run(*args):
        p = subprocess.run([str(exe), *args], capture_output=True, timeout=20,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        return (p.stdout + p.stderr).decode('utf-8', errors='replace')
    name = exe.parent.parent.name
    return name, {'cli': str(exe), 'help': run('--help'), 'version': run('--version')}


if __name__ == '__main__':
    (ROOT / 'evidence').mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        apps = dict(pool.map(inspect, pathlib.Path('D:/artcraft').rglob('*-cli.exe')))
    (ROOT / 'evidence' / 'discovery.json').write_text(
        json.dumps(apps, ensure_ascii=False, indent=2), encoding='utf-8')
    for name, data in apps.items():
        print(name, data['version'].strip(), '\n', data['help'], '\n')
