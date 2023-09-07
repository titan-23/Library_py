import sys

input_filename = sys.argv[1]

output_filename = sys.argv[2] if len(sys.argv) == 3 else 'aa.py'

input_file = open(input_filename, 'r')
output_file = open(output_filename, 'w')

added_file = set()

def get_code(now_path, input_file):
  for line in input_file:
    if line.startswith('from Library_py'):
      _, s, _, *fs = line.split()
      s = s.replace('.', '\\')
      s = f'C:\\Users\\titan\\source\\{s}.py'
      if s not in added_file:
        f = open(s, 'r')
        get_code(s, f)
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
        f = open(s, 'r')
        get_code(s, f)
        f.close()
        added_file.add(s)
    else:
      print(line, end='', file=output_file)

get_code('./', input_file)
print(f'The process completed successfully.')
print(f'Output file: \"{output_filename}\" .')
