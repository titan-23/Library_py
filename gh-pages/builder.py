import subprocess

command_expaned = ["python", "./AllExpander.py"]
command_html = ["python", "./HTMLMaker.py"]
try:
  result = subprocess.run(command_expaned, capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
  print('Error: ExpandError')
  print('Try: python AllExpander.py')
  exit(1)

try:
  result = subprocess.run(command_html, capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
  print('Error: HTMLError')
  print('Try: python HTMLMaker.py')
  exit(1)
