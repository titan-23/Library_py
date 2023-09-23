from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from markdown import markdown
import glob
import os

class HTMLMaker():

  def __init__(self):
    pass

  def set(self, filename) -> bool:
    self.filename = filename
    self.input_file_flag = False
    self.output_file_flag = False
    self.code_file_flag = False

    try:
      self.input_file = open(f'..\\Library_py\\docs_md\\{filename}.md', 'r', encoding='utf-8')
      self.input_file_flag = True
    except FileNotFoundError:
      print(f'..\\Library_py\\docs_md\\{filename}.md is not found.')
      return False

    try:
      self.code_file = open(f'..\\Library_py\\{filename}.py', 'r', encoding='utf-8')
      self.code_file_flag = True
    except FileNotFoundError:
      # print(f'..\\Library_py\\{filename}.py is not found.')
      # return False
      pass

    try:
      self.output_file = open(f'..\\Library_py\\docs\\{filename}.html', 'w', encoding='utf-8')
      self.output_file_flag = True
    except FileNotFoundError:
      print(f'..\\Library_py\\docs\\{filename}.html is not found.')
      return False

    return True

  def output_code(self):
    # Monokaiテーマを指定してHTMLに変換してシンタックスハイライト
    print('<button id=\"copyButton\">コピー</button>', file=self.output_file)
    print('<script src=https://github.com/titanium-22/Library_py/blob/main/docs/js/copy.js\n"></script>', file=self.output_file)
    formatter = HtmlFormatter(style="monokai")
    the_css = formatter.get_style_defs()
    code = ''
    for line in self.code_file:
      code += str(line)
    html_code = highlight(code, PythonLexer(), formatter)
    print(html_code, file=self.output_file)

  def write(self, title):
    cnt = self.filename.count("\\")
    style_path = '../' * cnt + 'style.css'
    line = f'''<!DOCTYPE html>\n<html>\n<head>\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<link rel=\"stylesheet\" type=\"text/css\" href={style_path}\">\n<title>{title}</title>\n</head>\n<body>'''
    html_output = line
    print(html_output, file=self.output_file)

    for line in self.input_file:
      line = str(line)
      if line.endswith(".md)\n"):
        line = line.replace('.md', '.html')
      html_output = markdown(line)
      print(html_output, end='', file=self.output_file)
      if self.code_file_flag and '](https://github.com/titanium-22/Library_py/blob/main/' in line and line.endswith('.py)\n'):
        print(filename)
        self.output_code()

    line = '''\n</body>\n</html>'''
    html_output = line
    print(html_output, file=self.output_file)

    self.input_file.close()
    self.output_file.close()
    if self.code_file_flag:
      self.code_file.close()


maker = HTMLMaker()

for root, dirs, files in os.walk("..\\Library_py\\docs_md\\"):
  for filename in files:
    filename = str(filename)
    if filename.endswith('.md'):
      filename = filename.removesuffix('.md')
      path = os.path.join(root, filename).removeprefix('..\\Library_py\\docs_md\\')
      if not maker.set(path):
        continue
      maker.write(title=filename)
