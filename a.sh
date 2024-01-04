# 自分用メモ：
# ./a.sh
# を実行すればすべてがOK

start_time=$(date +%s)

# 既にあるファイルの駆除
echo "removing ./docs/"
rm ./docs/ -r
echo "removing ./_docs/_build/"
rm ./_docs/_build/ -r
echo "removing ./_docs/titan_pylib_docs/"
rm ./_docs/titan_pylib_docs/ -r

pypy3 ./all_expander.py
sphinx-apidoc -f -e -d 1 -o ./_docs/titan_pylib_docs ./titan_pylib/
pypy3 ./edit_rst.py
sphinx-build -b html ./_docs ./_docs/_build
pypy3 ./edit_html.py

# copy to docs
echo "copying"
cp -r ./_docs/_build/ ./docs/

end_time=$(date +%s)
elapsed_time=$((end_time - start_time))
echo "Time: ${elapsed_time}sec"
