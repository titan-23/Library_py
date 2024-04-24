import re
import os
from bs4 import BeautifulSoup

_pre = ''

def read_file(cur_dir, file):
  global _pre
  s = f'  {cur_dir}/{file}\r'
  print(' '*len(_pre) + '\r', end='')
  print(s, end='')
  _pre = s
  try:
    f = open(f'{cur_dir}/{file}', 'r', encoding='utf=8')
  except FileNotFoundError as e:
    print('\nError:', e)
    return None
  lines = f.read()
  f.close()
  return lines

def mainfunc(cur_dir, file):
  lines = read_file(cur_dir, file)
  soup = BeautifulSoup(lines, 'html.parser')
  for text_node in soup.find_all(string=lambda s: s.startswith('titan_pylib')):
    if '_modules' in cur_dir and text_node.find_parent('span'):
      continue
    if file == 'index.html' and text_node == "titan_pylib.data_structures.union_find.union_find":
      # index.html では、使用例で titan_pylib を使用している
      continue
    text_node.replace_with(re.sub(r'^.*\.', '', text_node))
  for text_node in soup.find_all(string=lambda s: 'package' in s):
    text_node.replace_with(re.sub(r'\s*package\s*$', '', text_node))
  for text_node in soup.find_all(string=lambda s: 'module' in s):
    text_node.replace_with(re.sub(r'\s*module\s*$', '', text_node))
  for text_node in soup.find_all(string=lambda s: 'ドキュメント' in s):
    text_node.replace_with(re.sub(r'\s*ドキュメント\s*$', '', text_node))

  with open(f'{cur_dir}/{file}', 'w', encoding='utf-8') as output_file:
    output_file.write(str(soup))

if __name__ == '__main__':
  print('edit HTML.')

  # all
  path = "./_docs/_build/"
  for cur_dir, dirs, files in os.walk(path):
    for file in files:
      if not file.endswith('.html'):
        continue
      mainfunc(cur_dir, file)

  print('\nprocess succeeded.')
