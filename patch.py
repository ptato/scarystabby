#!/usr/bin/env python3
import re, os, sys

# Step 1: Find the executable's path 
path_to_dd = None

if os.name == 'nt':
    # Attempt to get steam path from registry
    import winreg
    steam_path = None
    try:
        steam_reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam')
        for i in range(winreg.QueryInfoKey(steam_reg)[1]):
            kname, kvalue, ktype = winreg.EnumValue(steam_reg, i)
            if kname == 'SteamPath':
                steam_path = kvalue
                break
    except: 
        print("Cant't read Windows Registry")

    # Check if any of the possible executable paths exist
    if steam_path is not None:
        maybe_path = steam_path + r'\steamapps\common\devildaggers\dd.exe'
        if os.path.isfile(maybe_path):
            path_to_dd = maybe_path

    elif os.path.isfile('.\dd.exe'):
        path_to_dd = r'.\dd.exe'

    elif os.path.isfile(r'C:\Program Files (x86)\Steam\steamapps\common\devildaggers\dd.exe'):
        path_to_dd = r'C:\Program Files (x86)\Steam\steamapps\common\devildaggers\dd.exe'

elif os.name == 'posix':
    print('Posix not yet implemented')
else:
    print(os.name + ' not yet implemented')

# The Final Test
if path_to_dd is None:
    print('Devil Daggers executable not found.')
    print('Run this script from the directory where the executable is located', flush=True)
    sys.exit(0)
else:
    print('Found dd.exe path: ' + path_to_dd, flush=True)

# Step 2: Make a backup
try:
    import shutil
    shutil.copy2(path_to_dd, path_to_dd + '.backup')
except:
    print("Can't backup executable. Restore file with steam in case of errors")

# Step 3: Patch the executable
with open(path_to_dd, 'r+b') as executable:
    contents = executable.read()

    ddrepl = lambda m: b'http://localhost:8081/backend15/' + m.group(1) + b'\00\00'
    pattern = b'http:\/\/dd\.hasmodai\.com\/backend15\/([a-z\._]*)\00'
    contents = re.sub(pattern, ddrepl, contents)

    executable.seek(0)
    executable.write(contents)
