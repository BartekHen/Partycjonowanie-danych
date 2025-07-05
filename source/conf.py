# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'BazyDanych'
copyright = '2025, Bartosz Potoczny'
author = 'Bartosz Potoczny'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'pl'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Opcje dla wyjścia LaTeX ---------------------------------------------

latex_elements = {
    # Użyj silnika xelatex, który lepiej radzi sobie z Unicode (polskie znaki)
    'preamble': r'''
\usepackage{fontspec}
\usepackage{polyglossia}
\setdefaultlanguage{polish}
\setotherlanguage{english}
''',
    'pointsize': '11pt',
    'papersize': 'a4paper',
    'figure_align': 'htbp',
    'fontpkg': '',
    'fncychap': r'\usepackage[Lenny]{fncychap}',
    'babel': '', # Wyłączamy stary babel
    'extrapackages': r'\usepackage{tabularx}',
}

latex_engine = 'xelatex'

