import os
import re
import random
import sys  
from colorama import init, Fore, Style, Back



# Initialize Colorama
init(autoreset=True)

import ctypes

def set_window_title(title):
    # Encode the title to ANSI
    title_ansi = title.encode('ansi', 'ignore')
    ctypes.windll.kernel32.SetConsoleTitleA(title_ansi)

set_window_title('BwE Py Anti-Extractor')

def print_banner():
    print(Fore.CYAN + "*-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*")
    print(Fore.CYAN + "|" + Fore.WHITE + "            __________          __________               " + Fore.CYAN + "|")
    print(Fore.CYAN + "|" + Fore.WHITE + "            \\______   \\ __  _  _\\_   ____/               " + Fore.CYAN + "|")
    print(Fore.CYAN + ":" + Fore.WHITE + "             |    |  _//  \\/ \\/  /|  __)_                " + Fore.CYAN + ":")
    print(Fore.CYAN + "." + Fore.WHITE + "             |    |   \\\\        //       \\               " + Fore.CYAN + ".")
    print(Fore.CYAN + ":" + Fore.WHITE + "  (\\_/)      |______  / \\__/\\__//______  /               " + Fore.CYAN + ":")
    print(Fore.CYAN + "|" + Fore.WHITE + " ( x_x)             \\/" + Fore.CYAN + "Py Anti-Extractor" + Fore.WHITE + "\\/0.0.4           " + Fore.CYAN + "|")
    print(Fore.CYAN + "|" + Fore.WHITE + " (>  >)                                                  " + Fore.CYAN + "|")
    print(Fore.CYAN + "*-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*\n")

print_banner()

def find_search_string(data):
    patterns = [
        rb'<assemblyIdentity name="(.*?)"',
        rb'<assemblyIdentity type="win32" name="(.*?)"',
        rb'<assemblyIdentity type="win64" name="(.*?)"'
    ]
    matches = []

    for pattern in patterns:
        regex = re.compile(pattern)
        match = regex.search(data)
        if match:
            matches.append(match.group(1).decode('utf-8'))
    return matches[0] if matches else None

def search_and_replace(filename):
    with open(filename, 'rb') as file:
        data = file.read()
        search_str = find_search_string(data)
        print(filename)

        if search_str:
            print(f"\nFound Python App Name: {search_str}")

            ascii_search = search_str.encode('ascii')
            index = data.find(ascii_search)
            found_offsets = []
            found = False
            while index != -1:
                if (index == 0 or data[index - 1] != 0x22) and (index + len(ascii_search) == len(data) or data[index + len(ascii_search)] != 0x22):
                    if data[index + len(ascii_search):index + len(ascii_search) + 3] != b".py":
                        print(f"Name Found At: 0x{index:08X}")
                        found_offsets.append(index)
                        found = True
                    else:
                        print(f"Found '.py' immediately after the string, continuing to search.")
                    index = data.find(ascii_search, index + len(ascii_search) + 3)
                else:
                    index = data.find(ascii_search, index + 1)

            if found:
                print("\nFound Patchable Offsets:")
                for i, offset in enumerate(found_offsets):
                    print(f"{i + 1}. Offset: 0x{offset:08X}")
                selected_offset = int(input("\nSelect Offset To Patch: ")) - 1

                selected_offset = found_offsets[selected_offset]
                print(f"Selected Offset: 0x{selected_offset:08X}")

                length_hex = format(len(ascii_search), 'X')

                new_hex = '00 08 ' + ' '.join([format(random.randint(0, 31), '02X') for _ in range(0, len(ascii_search) - 2)])

                modified_data = data[:selected_offset] + bytes.fromhex(new_hex) + data[selected_offset + len(ascii_search):]

                backup_filename = filename.replace('.exe', '_backup.exe')

                print(Fore.YELLOW + "Modified Data: " + new_hex + Style.RESET_ALL)

                # Create a backup of the original file
                with open(backup_filename, 'wb') as backup_file:
                    backup_file.write(data)

                # Write modifications directly to the original file
                with open(filename, 'wb') as original_file:
                    original_file.write(modified_data)

                print("Original Program Backed Up As: " + backup_filename)
                print(Fore.GREEN + "File Patched Successfully!" + Style.RESET_ALL)

            else:
                print("{0:60}".format(Fore.RED + "\nNo Suitable Offset Found\n" + Style.RESET_ALL),'\r', end=' ')
        else:
            print("{0:60}".format(Fore.RED + "\nPython App Name Not Found\n" + Style.RESET_ALL),'\r', end=' ')

        print("\nPress Enter to Exit...")
        input()
        sys.exit(1)

exe_files = [file for file in os.listdir() if file.endswith('.exe')]
if not exe_files:
    print("No Programs Found In Current Directory!")
else:
    print("Executables Found:\n")
    for i, exe_file in enumerate(exe_files):
        print(f"{i + 1}. {exe_file}")

    choice = input("\nSelect Executable To Patch: ")

    try:
        choice = int(choice)
        if 1 <= choice <= len(exe_files):
            selected_file = exe_files[choice - 1]
            search_and_replace(selected_file)
        else:
            print("Invalid Choice.")
    except ValueError:
        print("Invalid Input.")
