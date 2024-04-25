import os
import re

_pre = ''

def func(cur_dir: str, file: str) -> None:
  global _pre
  s = f'{cur_dir}{file}'
  print(' '*len(_pre) + '\r', end='')
  _pre = ' '*2 + s + '\r'
  print(_pre, end='')
  try:
    f = open(s, 'r', encoding='utf=8')
  except FileNotFoundError as e:
    print('\nError:', e)
    return
  lines = f.read().split('\n')
  f.close()

  if lines and lines[0].endswith('module'):
    expanded_file = file[len('titan_pylib.'):-len('.rst')].replace('.', '/')

    url = file.replace('.', '/')[:-len('/rst')] + '.py'
    frm_name = file[:-len('/rst')]

    class_name = []
    with open(url, 'r', encoding='utf-8') as f:
      for line in f:
        match = re.search(r'class\s+(\w+)', line)
        if line.startswith('class ') and match:
          class_name.append(match.group(1))

    if not class_name:
      with open(url, 'r', encoding='utf-8') as f:
        for line in f:
          match = re.search(r'def\s+(\w+)', line)
          if line.startswith('def ') and match:
            class_name.append(match.group(1))

    codes = '''
.. code-block:: python

'''
    for name in class_name:
      imp_str = f'''
  from {frm_name} import {name}'''
      codes += imp_str

    new_paragraph = f'''
ソースコード
^^^^^^^^^^^^

{codes}

`view on github <https://github.com/titan-23/Library_py/tree/main/{url}>`_

展開済みコード
""""""""""""""

.. literalinclude:: ../_build/_expanded/{expanded_file}.py
   :language: python
   :linenos:

仕様
^^^^^^^^^^^^^^^^'''
    lines.insert(3, new_paragraph)
    with open(s, 'w', encoding='utf=8') as f:
      for i, line in enumerate(lines):
        if line.endswith('module'):
          line = line[:-len('module')]
        if line.endswith('package'):
          line = line[:-len('package')]
        lines[i] = line
      print(*lines, sep='\n', file=f)

if __name__ == '__main__':
  print('edit rst.')

  path = "./_docs/titan_pylib_docs/"
  for cur_dir, dirs, files in os.walk(path):
    for file in files:
      if not file.endswith('.rst'):
        continue
      func(cur_dir, file)

  print('\nprocess succeeded.')
