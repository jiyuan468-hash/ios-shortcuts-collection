import os, re, json

disk_dirs = sorted([d for d in os.listdir('shortcuts') if os.path.isdir(os.path.join('shortcuts', d))])

with open('docs/js/app.js', encoding='utf-8') as f:
    js = f.read()

m = re.search(r'const catMap\s*=\s*\{([^}]+)\}', js, re.DOTALL)
cat_map_lines = m.group(1)

pairs = {}
for part in cat_map_lines.split(','):
    part = part.strip()
    if not part:
        continue
    if ':' in part:
        k, v = part.split(':', 1)
        k = k.strip().strip("'")
        v = v.strip().strip("'")
        pairs[k] = v

print('=== app.js catMap ===')
for k, v in sorted(pairs.items()):
    print(f'  {k}: {repr(v)} hex={v.encode("utf-8").hex()}')

print('\n=== Disk dirs ===')
for dd in disk_dirs:
    print(f'  {repr(dd)} hex={dd.encode("utf-8").hex()}')

print('\n=== JSON cat names ===')
d = json.load(open('docs/data/shortcuts.json', encoding='utf-8'))
for cat in d['categories']:
    print(f'  {cat["id"]}: {repr(cat["name"])} hex={cat["name"].encode("utf-8").hex()}')

# Check matches
print('\n=== Mismatches ===')
for cat_id, cat_name in [(cat['id'], cat['name']) for cat in d['categories']]:
    js_name = pairs.get(cat_id, '')
    if js_name != cat_name:
        print(f'  {cat_id}: JSON={repr(cat_name)} app.js={repr(js_name)}')
    else:
        # Check if this dir exists on disk
        if cat_name not in disk_dirs:
            print(f'  {cat_id}: OK (name matches) but dir "{cat_name}" NOT on disk!')
