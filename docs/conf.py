# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'HomepageBuilder'
copyright = '2024, Light-Beacon'
author = 'Light-Beacon'
release = ''

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc','sphinx_copybutton']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_static_path = ['_static']
html_favicon = '_static/builder.ico'
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
    'custom.css'
]

language = 'zh'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#extensions.append("sphinx_wagtail_theme")
html_theme = 'furo' #press #sphinx_book_theme #sphinx_wagtail_theme #furo

html_theme_options = {
    "source_repository": "https://github.com/Light-Beacon/HomepageBuilder",
    "source_branch": "docs",
    "source_directory": "docs/",
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/Light-Beacon/HomepageBuilder",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-2x footer-icon",
        },
    ],
}
