import os

class Bundler():

  def __init__(self):
    self.HEAD: str = '''https://titanium-22.github.io/Library_py/'''


F = ['Algorithm', 'DataStructures', 'Graph', 'Math', 'MyClass', 'Others', 'String']
for f in F:
  for root, dirs, files in os.walk(f"../../Library_py\\{f}\\"):
    for filename in files:
      filename = str(filename)
      if filename.endswith('.py'):
        input_path = f"{root}{filename}"
        print(input_path)
        input_file = open(input_path, 'r', encoding="utf-8")
        output_path = input_path[:len("../../Library_py")] + "_src_expanded/" + input_path[len("../../Library_py"):]
        output_file = open(output_path, 'w', encoding="utf-8")
        

