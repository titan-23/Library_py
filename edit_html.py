import re
import os
from bs4 import BeautifulSoup

_pre = ''

def func(cur_dir, file):
  global _pre
  s = f'  {cur_dir}/{file}\r'
  print(' '*len(_pre) + '\r', end='')
  print(s, end='')
  _pre = s
  try:
    f = open(f'{cur_dir}/{file}', 'r', encoding='utf=8')
  except FileNotFoundError as e:
    print('\nError:', e)
    return
  lines = f.read()
  f.close()
  soup = BeautifulSoup(lines, 'html.parser')
  for text_node in soup.find_all(string=lambda s: s.startswith('titan_pylib')):
    if '_modules' in cur_dir and text_node.find_parent('span'):
      continue
    text_node.replace_with(re.sub(r'^.*\.', '', text_node))
  for text_node in soup.find_all(string=lambda s: 'package' in s):
    text_node.replace_with(re.sub(r'\s*package\s*$', '', text_node))
  for text_node in soup.find_all(string=lambda s: 'module' in s):
    text_node.replace_with(re.sub(r'\s*module\s*$', '', text_node))

  with open(f'{cur_dir}/{file}', 'w', encoding='utf-8') as output_file:
    output_file.write(str(soup))

if __name__ == '__main__':
  print('edit HTML.')

  path = "./docs/_build/"
  for cur_dir, dirs, files in os.walk(path):
    for file in files:
      if not file.endswith('.html'):
        continue
      func(cur_dir, file)

  print('\nprocess succeeded.')