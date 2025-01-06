# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'APOalpyca'
copyright = '2025, Jon Holtzman'
author = 'Jon Holtzman'

import sys
import os
sys.path.insert(0, os.path.abspath('../device/'))


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]
napoleon_use_ivar = True

source_suffix = '.txt'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'nature'
html_static_path = ['_static']

# https://sphinx-themes.org/sample-sites/sphinx-rtd-theme/
html_theme = 'sphinx_rtd_theme'

#
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
#
html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': -1,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
    'style_nav_header_background': '#000040',
    'vcs_pageview_mode': 'edit',
}

#

