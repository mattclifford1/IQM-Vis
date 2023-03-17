# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import IQM_Vis

sys.path.insert(0, os.path.abspath('..'))

project = 'IQM-Vis'
copyright = '2023, Matt Clifford'
author = 'Matt Clifford'
release = '0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    "nbsphinx",
    "sphinx_gallery.load_style",
]

templates_path = ['_templates']
exclude_patterns = ['_build',
                    'Thumbs.db',
                    '.DS_Store',
                    os.path.join('IQM_Vis', 'examples'),
                    os.path.join('IQM_Vis', 'image_metrics', 'expert'),
                    os.path.join('IQM_Vis', 'utils'),
                    os.path.join('IQM_Vis', 'image_loaders'),
                    os.path.join('IQM_Vis', 'UI')
                    ]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_theme = 'pydata_sphinx_theme'

# html_theme = 'furo'
html_theme = 'sphinx_rtd_theme'
html_theme = 'renku'
html_theme = 'cloud'
html_theme = 'sphinx_typo3_theme'
html_static_path = ['_static']

# notebook links
nbsphinx_prolog = """
View the whole notebook: https://github.com/mattclifford1/IQM-Vis/docs/{{ env.doc2path(env.docname, base=None) }}

----
"""
