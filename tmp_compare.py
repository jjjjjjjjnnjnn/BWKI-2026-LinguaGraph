with open('README.md', 'r', encoding='utf-8') as f:
    en = f.read()
with open('README_DE.md', 'r', encoding='utf-8') as f:
    de = f.read()
with open('README_ZH.md', 'r', encoding='utf-8') as f:
    zh = f.read()

en_secs = []
for l in en.split('\n'):
    l = l.strip()
    if l.startswith('## ') and not l.startswith('### '):
        en_secs.append(l)
de_secs = [l.strip() for l in de.split('\n') if l.strip().startswith('## ') and not l.strip().startswith('### ')]
zh_secs = [l.strip() for l in zh.split('\n') if l.strip().startswith('## ') and not l.strip().startswith('### ')]

en_set = set(en_secs)
de_set = set(de_secs)
zh_set = set(zh_secs)

missing_de = en_set - de_set
missing_zh = en_set - zh_set

with open('/tmp/readme_diff.txt', 'w', encoding='utf-8') as f:
    f.write(f'EN sections: {len(en_secs)}\n')
    for s in en_secs:
        f.write(f'  {s}\n')
    f.write(f'\nDE sections: {len(de_secs)}\n')
    for s in de_secs:
        f.write(f'  {s}\n')
    f.write(f'\nMissing in DE ({len(missing_de)}):\n')
    for s in sorted(missing_de):
        f.write(f'  {s}\n')
    f.write(f'\nMissing in ZH ({len(missing_zh)}):\n')
    for s in sorted(missing_zh):
        f.write(f'  {s}\n')

print('Written to /tmp/readme_diff.txt')
