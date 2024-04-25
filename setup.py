from glob import glob
from os.path import basename, splitext
from setuptools import setup, find_packages

def _requires_from_file(filename: str):
    return open(filename).read().splitlines()

setup(
  name="titan_pylib",
  version="0.1.0",
  license="ライセンス",
  description="パッケージの説明",
  author="titan23",
  url="https://github.com/titan-23/Library_py",
  packages=find_packages("titan_pylib"),
  package_dir={"": "titan_pylib"},
  py_modules=[splitext(basename(path))[0] for path in glob('titan_pylib/*.py')],
  include_package_data=True,
  zip_safe=False,
  install_requires=_requires_from_file('requirements.txt'),
)
