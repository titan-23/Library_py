import re
import os
from bs4 import BeautifulSoup

def func(cur_dir, file):
  print(f'  {cur_dir}{file}\r', end='')
  f = open(f'{cur_dir}{file}', 'r', encoding='utf=8')
  lines = f.read()
  f.close()
  soup = BeautifulSoup(lines, 'html.parser')
  for text_node in soup.find_all(string=lambda s: s.startswith('titan_pylib')):
    text_node.replace_with(re.sub(r'^.*\.', '', text_node))
  for text_node in soup.find_all(string=lambda s: 'package' in s):
    text_node.replace_with(re.sub(r'\s*package\s*$', '', text_node))
  for text_node in soup.find_all(string=lambda s: 'module' in s):
    text_node.replace_with(re.sub(r'\s*module\s*$', '', text_node))

  with open(f'{cur_dir}{file}', 'w', encoding='utf-8') as output_file:
    output_file.write(str(soup))

if __name__ == '__main__':
  print('edit HTML.')

  for file in os.listdir('./docs/_build/'):
    if not file.endswith('.html'):
      continue
    func('./docs/_build/', file)

  for cur_dir, dirs, files in os.walk('./docs/_build/titan_pylib_docs/'):
    for file in files:
      if not file.endswith('.html'):
        continue
      func(cur_dir, file)

  print('\nprocess succeeded.')
