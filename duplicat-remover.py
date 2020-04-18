#!/usr/bin/env python3
from os import walk, makedirs, rename
from hashlib import sha1
from shutil import move
from time import time

files = []
hashes = []

for i in walk('.'):
    files.append(i)

##########################################
# Calculating hashes
##########################################

timer = time()
print(f"[ ] Calculating hashes", end='', flush=True)
for folder in files:
    if '/.' in folder[0] or folder == './duplicates':
        continue
    for fileName in folder[2]:
        path = folder[0]
        if fileName[0] == '.':
            continue
        with open(f'{path}/{fileName}', 'rb') as f:
            hasher = sha1()
            hasher.update(f.read())
            value = hasher.hexdigest()
        hashlist = [e['hash'] for e in hashes]
        newFile = {'path': path, 'filename': fileName}
        if value in hashlist:
            cluster = hashes[hashlist.index(value)]
            cluster['files'].append(newFile)
            cluster['len'] += 1
        else:
            hashes.append({'hash': value, 'len': 1, 'files': [newFile]})
print(f"\r[\u001b[32;1m*\u001b[0m] Calculating hashes     --> took {time() - timer:.4f}")

##########################################
# Calculating duplicates
##########################################

timer = time()
print(f"[ ] Calculating duplicates", end='', flush=True)
duplicates = [i for i in hashes if len(i['files']) > 1]
print(f"\r[\u001b[32;1m*\u001b[0m] Calculating duplicates --> took {time() - timer:.4f}")

filelen = 0
for i in duplicates:
    filelen += (i['len']-1)

print(f'Found {len(duplicates)} duplicates. Total Files to moved {filelen}')


##########################################
# Copping Files
##########################################

try:
    makedirs('duplicates')
except:
    pass
timer = time()
print(f"[ ] Copping Files", end='', flush=True)

for h in duplicates:
    for i, f in enumerate(h['files']):
        # print(f"{h['hash']} Nr {i+1} --> {f['path']}/{f['filename']}")
        try:
            if i == 0:
                pass
            else:
                move(f"{f['path']}/{f['filename']}", f"./duplicates/{h['hash']} Nr {i+1}")
        except:
            pass

print(f"\r[\u001b[32;1m*\u001b[0m] Copping Files          --> took {time() - timer:.4f}")
