import os
import subprocess
import re

F = ['Algorithm', 'DataStructures', 'Graph', 'IO', 'Math', 'MyClass', 'Others', 'String']
for f in F:
  for root, dirs, files in os.walk(f"..\\..\\Library_py\\{f}\\"):
    for filename in files:
      print(f'{filename=}')
      filename = str(filename)
      if filename.endswith('.py'):
        input_path = os.path.join(root, filename)
        output_dir = os.path.join(root)
        output_dir = output_dir[:len("..\\..\\Library_py\\")] + "gh-pages\\_src_expanded\\" + output_dir[len("..\\..\\Library_py\\"):]
        output_path = input_path[:len("..\\..\\Library_py\\")] + "gh-pages\\_src_expanded\\" + input_path[len("..\\..\\Library_py\\"):]
        if not os.path.exists(output_dir):
          print(output_dir)
          os.makedirs(output_dir)
        with open(output_path, 'w', encoding="utf-8") as output_file:
          f = input_path.lstrip("..\\..\\").replace("\\", ".")
          f = re.sub(r"\.py$", "", f)
          c = re.sub(r"\.py$", "", filename)
          print(f"from {f} import {c}", file=output_file)

        command = ["python", "..\\expander.py", output_path, output_path]
        try:
          result = subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
          print("展開に失敗しました:", f"from {f} import {c}")
          with open(output_path, 'w', encoding="utf-8") as output_file:
            with open(input_path, 'r', encoding="utf=8") as input_file:
              for line in input_file:
                print(line, end='', file=output_file)

