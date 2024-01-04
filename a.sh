start_time=$(date +%s)

# 既にあるファイルの駆除
echo "removing ./docs/_build/"
eval $"rm ./docs/_build/ -r"
echo "removing ./docs/titan_pylib_docs/"
eval $"rm ./docs/titan_pylib_docs/ -r"

eval $"sphinx-apidoc -f -e -d 1 -o ./docs/titan_pylib_docs ./titan_pylib/"
eval $"sphinx-build -b html ./docs ./docs/_build"
eval $"pypy3 ./edit_html.py"
eval $"pypy3 ./all_expander.py"

end_time=$(date +%s)
elapsed_time=$((end_time - start_time))
echo "Time: ${elapsed_time}sec"
