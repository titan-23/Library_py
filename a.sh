apidoc_command="sphinx-apidoc -f -e -d 1 -o ./docs/titan_pylib_docs ./titan_pylib/"
eval $apidoc_command

build_command="sphinx-build -b html ./docs ./docs/_build"
eval $build_command
