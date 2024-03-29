# user settings --------------------------------------------------
SLASH = '/'
LIB_PATH = '/mnt/c/Users/titan/source/Library_py'
# LIB_PATH = 'C:\\Users\\titan\\source\\Library_py'
TO_LIB_PATH = '.'
#  ----------------------------------------------------------------

import sys
import pyperclip
import re

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
    if 'def' in line:
      for func_name in need_class:
        if line.startswith(f'def {func_name}'):
          print(f'import {func_name} OK.(function)')
          need_class.remove(func_name)

    if is_input:
      input_lines += 1
    if line.startswith('from titan_pylib'):
      _, s, _, *fs = line.split()
      fs = [x.rstrip(', ') for x in fs]
      s = s.replace('.', SLASH)
      s = f'{LIB_PATH}{SLASH}{s}.py'
      if s not in added_file:
        output += f'# {line}'
        try:
          f = open(s, 'r', encoding='utf-8')
        except FileNotFoundError:
          print(s)
          print(f'File \"{input_filename}\", line {input_lines}')
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
      output += f'# {line}'
      _, s, _, *fs = line.split()
      fs = [x.rstrip(', ') for x in fs]
      cnt = 0
      while s and s[0] == '.':
        s = s[1:]
        cnt += 1
      s = s.replace('.', SLASH)
      t = now_path
      for _ in range(cnt):
        i = len(t)-1
        while i >= 0 and t[i] != SLASH:
          i -= 1
        t = t[:i]
      s = f'{t}{SLASH}{s}.py'
      if s not in added_file:
        try:
          f = open(s, 'r', encoding='utf-8')
        except FileNotFoundError:
          print(s)
          print('FileNotFoundError')
          exit(1)
        get_code(s, f, fs)
        f.close()
        added_file.add(s)
    else:
      output += line
      # print(line, end='', file=output_file)
  if need_class:
    error_msg = ''
    for e in need_class:
      error_msg += f'  {e}\n'
    error_msg += 'ImportError: class not found.'
    print(error_msg)
    exit(1)

if __name__ == '__main__':

  input_filename = sys.argv[1]
  output_filename = sys.argv[2] if len(sys.argv) == 3 else 'clip'
  input_file = open(input_filename, 'r', encoding='utf-8')

  added_file = set()
  output = ''
  input_lines = 0

  get_code(TO_LIB_PATH, input_file, [], is_input=True)

  if output_filename in ['clip', 'CLIP', 'c', 'C']:
    output_filename = 'clipboard'
    pyperclip.copy(output)
  else:
    output_file = open(output_filename, 'w', encoding='utf-8')
    print(output, file=output_file)
    output_file.close()

  print()
  print('The process completed successfully.')
  print(f'Output file: \"{output_filename}\" .')
