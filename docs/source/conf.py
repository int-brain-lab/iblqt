import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))

from iblqt import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'iblqt'
author = 'International Brain Laboratory'
copyright = f'{date.today().year}, International Brain Laboratory'
version = '.'.join(__version__.split('.')[:3])
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.linkcode',
    'sphinx_qt_documentation',
    # 'autoapi.extension',
    'myst_parser',
]
source_suffix = ['.rst', '.md']
templates_path = ['_templates']
exclude_patterns = []
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'one:': ('https://int-brain-lab.github.io/ONE/', None),
}
autodoc_typehints = 'none'
autoapi_dirs = ['../../iblqt']
autoapi_options = ['members', 'undoc-members', "show-module-summary", "special-members"]
autoapi_add_toctree_entry = True
autoapi_root = 'api'
# autoapi_own_page_level = 'class'
qt_documentation = 'Qt5'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'display_version': True,
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Napoleon Settings -------------------------------------------------------
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = True
napoleon_use_param = False
napoleon_use_rtype = False
napoleon_preprocess_types = True
napoleon_type_aliases = None
napoleon_attr_annotations = True


# -- linkcode Settings -------------------------------------------------------
def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    return "https://github.com/int-brain-lab/iblqt/blob/main/%s.py" % filename