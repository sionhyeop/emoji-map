#!/usr/bin/env python3
"""Parse Unicode emoji-test.txt + CLDR annotations into docs/emoji-data.js"""
import json, re, os

SRC = os.path.dirname(os.path.abspath(__file__))

def load_ann(*files):
    out = {}
    for f in files:
        d = json.load(open(os.path.join(SRC, f)))
        key = 'annotations' if 'annotations' in d else 'annotationsDerived'
        for ch, v in d[key]['annotations'].items():
            e = out.setdefault(ch, {'kw': [], 'tts': ''})
            e['kw'] += v.get('default', [])
            if v.get('tts') and not e['tts']:
                e['tts'] = v['tts'][0]
    return out

en = load_ann('ann-en.json', 'annd-en.json')
ko = load_ann('ann-ko.json', 'annd-ko.json')

SKIN = re.compile(r':?\s*(light|medium-light|medium|medium-dark|dark) skin tone')
groups = []
cur_group = cur_sub = None
by_key = {}  # base name -> emoji entry, for attaching skin variants
version = '?'

for line in open(os.path.join(SRC, 'emoji-test.txt'), encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('# Version:'):
        version = line.split(':', 1)[1].strip()
    if line.startswith('# group:'):
        cur_group = {'name': line.split(':', 1)[1].strip(), 'subs': []}
        groups.append(cur_group)
        continue
    if line.startswith('# subgroup:'):
        cur_sub = {'name': line.split(':', 1)[1].strip(), 'emoji': []}
        cur_group['subs'].append(cur_sub)
        continue
    if not line or line.startswith('#'):
        continue
    m = re.match(r'^([0-9A-F ]+?)\s*;\s*(\S[\S-]*)\s*#\s*(\S+)\s+E(\d+\.\d+)\s+(.*)$', line)
    if not m:
        continue
    codes, status, char, ever, name = m.groups()
    if status != 'fully-qualified' and status != 'component':
        continue
    if cur_group['name'] == 'Component':
        continue
    skin_m = SKIN.search(name)
    if skin_m:
        base_name = SKIN.sub('', name).replace(':,', ':').rstrip(': ,')
        # normalize: remove leftover ', ' artifacts
        base_name = re.sub(r':\s*(,\s*)+', ': ', base_name).rstrip(': ,')
        base = by_key.get(base_name)
        if base is not None:
            base.setdefault('s', []).append(char)
        continue
    ken = en.get(char, {})
    kko = ko.get(char, {})
    entry = {
        'c': char,
        'n': ken.get('tts') or name,
        'k': kko.get('tts') or '',
        'v': ever,
        'kw': ' '.join(dict.fromkeys(ken.get('kw', []) + kko.get('kw', []))),
    }
    by_key[name] = entry
    cur_sub['emoji'].append(entry)

groups = [g for g in groups if g['name'] != 'Component']
total = sum(len(s['emoji']) for g in groups for s in g['subs'])
skins = sum(len(e.get('s', [])) for g in groups for s in g['subs'] for e in s['emoji'])
print(f'version {version}, base emoji: {total}, skin variants: {skins}')

os.makedirs(os.path.join(SRC, 'docs'), exist_ok=True)
# split: core (render-critical) vs keywords (search-only, lazy loaded)
kw_map = {}
for g in groups:
    for s in g['subs']:
        for e in s['emoji']:
            if e['kw']:
                kw_map[e['c']] = e['kw']
            del e['kw']
with open(os.path.join(SRC, 'docs', 'emoji-data.js'), 'w', encoding='utf-8') as f:
    f.write('window.EMOJI_VERSION=' + json.dumps(version) + ';\n')
    f.write('window.EMOJI_DATA=' + json.dumps(groups, ensure_ascii=False, separators=(',', ':')) + ';\n')
with open(os.path.join(SRC, 'docs', 'emoji-kw.js'), 'w', encoding='utf-8') as f:
    f.write('window.EMOJI_KW=' + json.dumps(kw_map, ensure_ascii=False, separators=(',', ':')) + ';'
            + 'window.dispatchEvent(new Event("emoji-kw-ready"));\n')
for fn in ('emoji-data.js', 'emoji-kw.js'):
    print('wrote docs/' + fn, os.path.getsize(os.path.join(SRC, 'docs', fn)), 'bytes')
