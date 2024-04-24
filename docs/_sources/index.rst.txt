.. titan\_pylib documentation master file, created by
   sphinx-quickstart on Thu Dec 28 00:22:05 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to titan\_pylib's documentation!
=========================================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   ./titan_pylib_docs/titan_pylib.algorithm.rst

   ./titan_pylib_docs/titan_pylib.data_structures.rst

   ./titan_pylib_docs/titan_pylib.graph.rst

   ./titan_pylib_docs/titan_pylib.io.rst

   ./titan_pylib_docs/titan_pylib.math.rst

   ./titan_pylib_docs/titan_pylib.string.rst


How to Use
----------

インストール方法
"""""""""""""""
pip を用いて以下のようにインストールできます。

.. code-block:: none

   pip install git+https://github.com/titan-23/Library_py.git@main

使用例
""""""

.. code-block:: python

   from titan_pylib.data_structures.union_find.union_find import UnionFind
   n = int(input())
   uf = UnionFind(n)


コード展開
""""""""""

オンラインジャッジに提出するときは、適切なパスを設定した上で ``expander.py`` を使用してください。

- 例1 ``a.py`` を展開してクリップボードにコピーする

.. code-block:: none

   python ./expander.py a.py


- 例2 ``b.py`` を展開して ``exp_b.py`` ファイルに書き出す

.. code-block:: none

   python ./expander.py a.py exp_b.py


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
