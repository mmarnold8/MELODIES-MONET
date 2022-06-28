# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config


# -- Project information -----------------------------------------------------

project = u'MELODIES-MONET'
copyright = u'2022, NCAR/UCAR, NOAA'
author = u'Rebecca Schwantes (NOAA), Barry Baker (NOAA), Louisa Emmons (NCAR), Rebecca Buchholz (NCAR)'

# The short X.Y version
version = u''
# The full version, including alpha/beta/rc tags
release = u''

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.extlinks',
    'myst_nb',
    'sphinx_design',
    'sphinx_click',
]

extlinks = {
    'issue': ('https://github.com/noaa-csl/melodies-monet/issues/%s', 'GH'),
    'pull': ('https://github.com/noaa-csl/melodies-monet/pull/%s', 'PR'),
}

autosummary_generate = True  # default in Sphinx v4

autodoc_default_options = {
    "members": True,
    "special-members": "__init__",
    # "undoc-members": True,
}
autodoc_member_order = "groupwise"

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_param = False
napoleon_use_rtype = False
napoleon_use_ivar = False  # True
napoleon_preprocess_types = True

nb_execution_timeout = 300  # in seconds, for each notebook cell (default: 30)
# nb_execution_mode = "auto"  # don't execute if all cells have output (default)
# nb_execution_mode = "cache"  # to speed build when working on other things
nb_execution_mode = "off"
nb_execution_excludepatterns = [
    "examples/airnow_wrfchem.ipynb",
]
nb_execution_show_tb = True

myst_enable_extensions = ["colon_fence"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = [
    u'_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints',
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'melodies-monetdoc'

html_theme_options = {
    'logo_only': True,
}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "../melodies_monet/data/MM_logo.png"

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'melodies-monet.tex', u'MELODIES-MONET Documentation', u'Rebecca Schwantes (NOAA) \\and Barry Baker (NOAA) \\and Louisa Emmons (NCAR) \\and Rebecca Buchholz (NCAR)', 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, 'melodies-monet', u'MELODIES-MONET Documentation', [author], 1)]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'melodies-monet', u'melodies-monet Documentation', author, 'melodies-monet', 'Analysis tool for atmopsheric chemistry modeling.', 'Miscellaneous'),
]

# -- Extension configuration -------------------------------------------------

linkcheck_ignore = [
    # Auth required:
    "https://rdhpcs-common-docs.rdhpcs.noaa.gov/wiki/index.php/Anaconda#Installation",
    "https://www2.cisl.ucar.edu/resources/conda-environments",
    # Sphinx 4.5 linkcheck having problem:
    "https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account",
]

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2
