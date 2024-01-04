# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../titan_pylib/'))
sys.path.insert(0, os.path.abspath('../titan_pylib/algorithm/'))
sys.path.insert(0, os.path.abspath('../titan_pylib/data_structures/'))
sys.path.insert(0, os.path.abspath('../titan_pylib/graph/'))
sys.path.insert(0, os.path.abspath('../titan_pylib/io/'))
sys.path.insert(0, os.path.abspath('../titan_pylib/math/'))
sys.path.insert(0, os.path.abspath('../titan_pylib/string/'))
autodoc_typehints = 'description'  # 型ヒントを有効
# autoclass_content = 'both'         # __init__()も出力
autodoc_default_options = {
    'private-members': False,
    'show-inheritance': False,
    'members': None,
    'maxdepth': 1,
}

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'titan_pylib'
copyright = '2023, titan'
author = 'titan'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'recommonmark',
    'sphinx.ext.githubpages',
    'sphinx_copybutton',
]

# sphinx_copybutton設定
copybutton_prompt_text = ">>> "

viewcode_line_numbers = True

# Napoleon settings
napoleon_google_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_js_files = ['_static/script.js']
html_css_files = ['_static/style.css', '_static/codeblock.css', '_static/dammy.css']
