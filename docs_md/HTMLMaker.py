# python src_expand.py
# python HTMLMaker.py

import re
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from markdown import markdown
import os


class HTMLMaker():

  def __init__(self):
    self.HEAD: str = '''https://titanium-22.github.io/Library_py/'''

  def set(self, filename) -> bool:
    self.filename = filename
    self.input_file_flag = False
    self.output_file_flag = False
    self.code_file_flag = False

    try:
      self.input_file = open(f'..\\..\\Library_py\\docs_md\\{filename}.md', 'r', encoding='utf-8')
      self.input_file_flag = True
    except FileNotFoundError:
      print(f'..\\..\\Library_py\\docs_md\\{filename}.md is not found.')
      return False

    try:
      self.code_file = open(f'..\\..\\Library_py\\{filename}.py', 'r', encoding='utf-8')
      self.code_file_flag = True
    except FileNotFoundError:
      if self.filename and self.filename[-1] == '_':
        try:
          self.code_file = open(f'..\\..\\Library_py\\{filename[:-1]}.py', 'r', encoding='utf-8')
          self.code_file_flag = True
        except FileNotFoundError:
          print(f'code {filename} not found.')
          pass

    try:
      self.output_file = open(f'..\\..\\Library_py\\docs\\{filename}.html', 'w', encoding='utf-8')
      self.output_file_flag = True
    except FileNotFoundError:
      print(f'..\\Library_py\\docs\\{filename}.html is not found.')
      return False

    return True

  def output_code(self, code, copy: bool):
    # Monokaiテーマを指定してHTMLに変換してシンタックスハイライト
    print("<div class=\"code-block\">", file=self.output_file)

    if copy:
      print("<div class=\"button-group\">", file=self.output_file)
      print('<button id=\"copyButton\">コピー</button>', file=self.output_file)
      print('<button id=\"ShowFullCodeButton\">全表示</button>', file=self.output_file)
      print('<button id=\"toggleCodeButton\">展開</button>', file=self.output_file)
      print('</div>', file=self.output_file)
    formatter = HtmlFormatter(style="monokai")
    # the_css = formatter.get_style_defs()
    outs = ''
    for line in code:
      outs += str(line)
    html_code = highlight(outs, PythonLexer(), formatter)
    html_code = html_code.replace('<div class=\"highlight\">', '<div class=\"highlight\" id=\"codeContainer1\">')
    assert html_code.endswith('</div>\n')

    if copy:
      # expand
      exp_filepath = f'..\\..\\Library_py\\_src_expanded\\{self.filename}.py'
      with open(exp_filepath, 'r', encoding="utf-8") as exp_code:
        outs = ''
        for line in exp_code:
          outs += str(line)
        html_code2 = highlight(outs, PythonLexer(), formatter)
        assert html_code2.startswith('<div class=\"highlight\">')
        html_code2 = html_code2.replace('<div class=\"highlight\">', '<div class=\"highlight\" id=\"codeContainer2\" style=\"display: none;\">')
        html_code += html_code2
    print(html_code, file=self.output_file)
    print("</div>", file=self.output_file)

  def out(self, s: str) -> None:
    html_output = markdown(s)
    html_output = re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', html_output)
    print(html_output, file=self.output_file)

  def write(self, title):
    # print(title)
    cnt = self.filename.count("\\")
    style_path = '../' * cnt + 'style.css'
    t = 'Library_py-' + self.filename.replace('\\', '-')
    if title == 'index':
      t = 'Library_py'
    
    # header
    line = f'''<!DOCTYPE html>\n<html>\n<head>\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n'''
    self.out(line)
    line = f'''<link href=\"https://fonts.googleapis.com/css?family=Inconsolata\" rel=\"stylesheet\" type=\"text/css\">\n'''
    self.out(line)
    line = f'''<link rel=\"stylesheet\" type=\"text/css\" href=\"{style_path}\">\n'''
    self.out(line)

    cnt = self.filename.count("\\")
    script_js_path = '../' * cnt + 'script.js'
    line = f'''<script src="{script_js_path}"></script>\n'''
    self.out(line)

    line = f'''<title>{t}</title>\n</head>\n<body>'''
    self.out(line)

    # Home
    line = f'''### [Home]({self.HEAD})\n\n'''
    line += f'''_____\n'''
    self.out(line)

    # body
    code_flag = False
    outs = ''
    for line in self.input_file:
      line = str(line)
      if self.code_file_flag and line.startswith("<!-- code=https://github.com/titanium-22/Library_py/blob/main/"):
        self.out(outs)
        self.output_code(code=self.code_file, copy=True)
        outs = ''
        continue
      if (not code_flag) and line == "```python\n":
        code_flag = True
        self.out(outs)
        outs = ''
        continue
      if code_flag and line == "```\n":
        code_flag = False
        self.output_code(code=outs, copy=False)
        outs = ''
        continue

      if line.endswith(".md)\n"):
        line = line.replace('.md', '.html')
      if line.startswith("  - "):
        line = "\t" + line[2:]
      outs += line
    self.out(outs)

    line = "\n</body>\n</html>"
    self.out(line)

    self.input_file.close()
    self.output_file.close()
    if self.code_file_flag:
      self.code_file.close()


maker = HTMLMaker()

for root, dirs, files in os.walk("../../Library_py\\docs_md\\"):
  for filename in files:
    filename = str(filename)
    if filename.endswith('.md'):
      filename = filename.removesuffix('.md')
      path = os.path.join(root, filename).removeprefix('../../Library_py\\docs_md\\')
      if not maker.set(path):
        continue
      maker.write(title=filename)

# for root, dirs, files in os.walk("../../Library_py\\docs_md\\"):
#   for filename in files:
#     filename = str(filename)
#     if filename.endswith('.md'):
#       filename = filename.removesuffix('.md')
#       path = os.path.join(root, filename).removeprefix('../../Library_py\\docs_md\\')
#       file_name = f'{path}.md'
#       with open(file_name, encoding="utf-8") as f:
#         data_lines = f.readlines()
#       out_lines = ''
#       x = False
#       for line in data_lines:
#         s = str(line)
#         if '`](https://github.com/titanium-22/Library_py/tree/main/' in s:
#           if s.startswith('- ') or s.startswith('\t- '):
#             out_lines += s
#             continue
#           assert not x
#           x = True
#           print('aaaaaaaaaa', s)
#           out_lines += s.replace('/Library_py/tree/main/', '/Library_py/blob/main/')
#           out_lines += f'''<!-- code=https://github.com/titanium-22/Library_py/blob/main/{path}.py -->'''
#           out_lines += '\n'
#         else:
#           out_lines += s
#       with open(file_name, mode="w", encoding="utf-8") as f:
#         f.write(out_lines)
