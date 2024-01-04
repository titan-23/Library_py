from typing import List
import os
import subprocess
import re

def get_class_names(file_name: str) -> List[str]:
  # モジュール名の、
  # 先頭大文字、
  # アンダーバー消してその次大文字にする
  file_name = file_name.removesuffix('.py')
  if file_name.startswith('get_'):
    return file_name
  if file_name == 'bubble_sort':
    return 'bubble_sort'
  if file_name == 'quick_sort':
    return 'quick_sort'
  if file_name == 'merge_sort':
    return 'merge_sort'
  if file_name == 'csr_array':
    return 'CSRArray'
  if file_name == 'lazy_rbst':
    return 'LazyRBST'
  if file_name == 'safe_hash':
    return 'HashSet'
  if file_name == 'lca':
    return 'LCA'
  res = ''
  i = 0
  while i < len(file_name):
    if i == 0:
      res += file_name[i].capitalize()
      i += 1
    if file_name[i] == '_' and i+1 < len(file_name):
      res += file_name[i+1].capitalize()
      i += 2
    else:
      res += file_name[i]
      i += 1
  res = res.replace('Avl', 'AVL')
  res = res.replace('Bst', 'BST')
  res = res.replace('Wb', 'WB')
  res = res.replace('FastIo', 'FastIO')
  res = res.replace('Hld', 'HLD')
  return res

if __name__ == '__main__':
  banned_name = {'__init__.py', 'expander.py'}
  banned_dirs = {'./titan_pylib/data_structures/_arcive', './titan_pylib/others/machine'}

  for cur_dir, dirs, files in os.walk('./titan_pylib/'):
    for file in files:
      if not file.endswith('.py'):
        continue
      if file in banned_name:
        continue
      if cur_dir in banned_dirs:
        continue
      input_path = os.path.join(cur_dir, file)
      output_dir = os.path.join(cur_dir)
      output_dir = "./docs/_build/_expanded/" + output_dir[len("./titan_pylib/"):]
      output_path = "./docs/_build/_expanded/" + input_path[len("./titan_pylib/"):]
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)

      with open(output_path, 'w', encoding="utf-8") as output_file:
        f = input_path.lstrip("./").replace("/", ".")
        f = re.sub(r"\.py$", "", f)
        class_name = get_class_names(file)
        print(f"from {f} import {class_name}", file=output_file)

      command = ["pypy3", "./titan_pylib/expander.py", output_path, output_path]
      try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
      except subprocess.CalledProcessError:
        with open(output_path, 'w', encoding="utf-8") as output_file:
          f = input_path.lstrip("./").replace("/", ".")
          f = re.sub(r"\.py$", "", f)
          class_name = file.removesuffix('.py')
          print(f"from {f} import {class_name}", file=output_file)
          command = ["pypy3", "./titan_pylib/expander.py", output_path, output_path]
        try:
          result = subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
          print(f'{cur_dir=}')
          print("展開に失敗しました:", f"from {f} import {class_name}")
          with open(output_path, 'w', encoding="utf-8") as output_file:
            with open(input_path, 'r', encoding="utf=8") as input_file:
              for line in input_file:
                print(line, end='', file=output_file)
