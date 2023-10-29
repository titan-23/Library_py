'''
builder.py

事前に適切なブランチからプルする

>> python builder.py
で AllExpander 、 HTMLMaker を実行
'''

import subprocess

# expand したものを生成
command_expaned = ["python", "./AllExpander.py"]
try:
  result = subprocess.run(command_expaned, stdout=subprocess.PIPE, text=True, check=True)
  print(result.stdout)
except subprocess.CalledProcessError as e:
  print('Error: ExpandError')
  print('Try: >>> python AllExpander.py')
  exit(1)
print('AllExpander.py Finished.')

# HTML ファイルを生成
command_html = ["python", "./HTMLMaker.py"]
try:
  result = subprocess.run(command_html, capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
  print('Error: HTMLError')
  print('Try: >>> python HTMLMaker.py')
  exit(1)
print('HTMLMaker.py Finished.')

print('The build was successful.')
