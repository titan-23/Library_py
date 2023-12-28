import subprocess
import sys
import os

com = ['sphinx-apidoc', '-f', '-e', '-o', './do/data_structures', '.']
subprocess.run(com)
