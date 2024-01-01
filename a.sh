eval $"sphinx-apidoc -f -e -d 1 -o ./docs/titan_pylib_docs ./titan_pylib/"
eval $"sphinx-build -b html ./docs ./docs/_build"
eval $"pypy3 ./a.py"
