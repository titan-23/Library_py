sphinx-apidoc -f -e -o ./do .

sphinx-build -b html ./do ./do/_build
