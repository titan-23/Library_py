import os

def change_root_name():
  '''
  replace('titanium-22', 'titan-23')
  '''
  for root, dirs, files in os.walk("../docs_md/"):
    for filename in files:
      filename = str(filename)
      if filename.endswith('.md'):
        filename = filename.removesuffix('.md')
        path = os.path.join(root, filename)
        file_name = f'{path}.md'
        with open(file_name, encoding="utf-8") as f:
          data_lines = f.readlines()
        out_lines = ''
        for line in data_lines:
          s = str(line)
          s = s.replace('titanium-22', 'titan-23')
          out_lines += s
        with open(file_name, mode="w", encoding="utf-8") as f:
          f.write(out_lines)

change_root_name()
