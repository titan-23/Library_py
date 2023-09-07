import sys
import pyperclip
import re
import io
import sys

LIB_PATH = 'C:\\Users\\titan\\source'

input_filename = sys.argv[1]
output_filename = sys.argv[2] if len(sys.argv) == 3 else 'aa.py'
input_file = open(input_filename, 'r', encoding='utf-8')

added_file = set()
output = ''
input_lines = 0

def get_code(now_path, input_file, need_class, is_input=False):
  global input_lines, output

  for line in input_file:

    if 'class' in line:
      match = re.search(r'class\s+(\w+)', line)
      if match:
        class_name = match.group(1)
        if class_name in need_class:
          print(f'import {class_name} OK.')
          need_class.remove(class_name)

    if is_input:
      input_lines += 1
    if line.startswith('from Library_py'):
      _, s, _, *fs = line.split()
      s = s.replace('.', '\\')
      s = f'{LIB_PATH}\\{s}.py'
      if s not in added_file:
        try:
          f = open(s, 'r', encoding='utf-8')
        except FileNotFoundError:
          print(f'  File \"{input_filename}\", line {input_lines}')
          error_line = line.rstrip()
          error_underline = '^' * len(error_line)
          print(f'    {error_line}')
          print(f'    {error_underline}')
          print('ImportError')
          exit(1)
        get_code(s, f, fs)
        f.close()
        added_file.add(s)
    elif line.startswith('from .'):
      _, s, _, *fs = line.split()
      cnt = 0
      while s and s[0] == '.':
        s = s[1:]
        cnt += 1
      s = s.replace('.', '\\')
      t = now_path
      for _ in range(cnt):
        i = len(t)-1
        while t[i] != '\\':
          i -= 1
        t = t[:i]
      s = f'{t}\\{s}.py'
      if s not in added_file:
        f = open(s, 'r', encoding='utf-8')
        get_code(s, f, fs)
        f.close()
        added_file.add(s)
    else:
      output += line
      # print(line, end='', file=output_file)
  if need_class:
    for e in need_class:
      print(f'  {e}')
    print('ImportError: class not found.')
    exit(1)

get_code('./', input_file, [], is_input=True)

if output_filename in ['clip', 'CLIP', 'c', 'C']:
  output_filename = 'clipboard'
  pyperclip.copy(output)
else:
  output_file = open(output_filename, 'w', encoding='utf-8')
  print(output, file=output_file)
  output_file.close()

print()
print(f'The process completed successfully.')
print(f'Output file: \"{output_filename}\" .')
