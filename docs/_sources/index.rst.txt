Welcome to titan\_pylib's documentation!
=========================================

`titan23 <https://atcoder.jp/users/titan23>`_  が使用している、競技プログラミング用のライブラリです。 PyPy で動きます。
各 REAMDME はサボっています。また、ありえないバグを仕込んでたりします。ご注意ください。
誰かがバグに引っかかって WA を出してくれたら、筆者冥利に尽きます。

Library Overview
-----------------

.. toctree::
   :maxdepth: 1

   ./titan_pylib_docs/titan_pylib.algorithm.rst

   ./titan_pylib_docs/titan_pylib.data_structures.rst

   ./titan_pylib_docs/titan_pylib.graph.rst

   ./titan_pylib_docs/titan_pylib.io.rst

   ./titan_pylib_docs/titan_pylib.math.rst

   ./titan_pylib_docs/titan_pylib.string.rst


`view on github <https://github.com/titan-23/Library_py/tree/main>`_

----

How to Use
----------

インストール方法
"""""""""""""""
以下のように pip を用いてインストールできます。なお、更新頻度が高いため非推奨です。当サイト等からのコピペを想定しています。
また、バージョンは特に考えていないので注意してください。

.. code-block:: console

   $ pip install git+https://github.com/titan-23/Library_py.git@main

- アンインストール方法(時間がかかる可能性があります。書き方間違っているのかも)

.. code-block:: console

   $ pip uninstall titan_pylib


使用例
""""""

.. code-block:: python

   from titan_pylib.data_structures.union_find.union_find import UnionFind
   n = int(input())
   uf = UnionFind(n)


コード展開
""""""""""

オンラインジャッジに提出するときは、適切なパスを設定した上で ``expander.py`` を使用してください。

.. code-block:: console

   $ python ./expander.py <input_file> <output_file>

``<output_file>`` を省略または ``clip`` とするとクリップボードにコピーされます。


- 例1 ``./a.py`` を展開してクリップボードにコピーする

.. code-block:: console

   $ python ./expander.py ./a.py


- 例2 ``./b.py`` を展開して ``./exp_b.py`` ファイルに書き出す

.. code-block:: console

   $ python ./expander.py ./b.py ./exp_b.py

----

検索
-----

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
