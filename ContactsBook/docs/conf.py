from dotenv import load_dotenv
import sys
import os

load_dotenv()

sys.path.append(os.path.abspath('..'))
project = 'ContactsBook'
copyright = '2024, SSergiy'
author = 'SSergiy'
release = '0.1.0'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']
