start_time=$(date +%s)

# 既にあるファイルの駆除
echo "removing ./_docs/_build/"
eval $"rm ./_docs/_build/ -r"
echo "removing ./_docs/titan_pylib_docs/"
eval $"rm ./_docs/titan_pylib_docs/ -r"

eval $"sphinx-apidoc -f -e -d 1 -o ./_docs/titan_pylib_docs ./titan_pylib/"
eval $"sphinx-build -b html ./_docs ./_docs/_build"
eval $"pypy3 ./edit_html.py"
eval $"pypy3 ./all_expander.py"

# copy to docs
echo "copying"
cp -r ./_docs/_build/ ./docs/

end_time=$(date +%s)
elapsed_time=$((end_time - start_time))
echo "Time: ${elapsed_time}sec"
