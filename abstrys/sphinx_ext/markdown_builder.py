# -*- coding: utf-8 -*-
#
# abstrys.sphinx_ext.markdown_builder
# -----------------------------------
#
# A Markdown builder for Sphinx, using rst2db's markdown writer.
#
# by Eron Hennessey

from abstrys.docutils_ext.markdown_writer import MarkdownWriter, MarkdownTranslator
from docutils.core import publish_from_doctree
from sphinx.builders.text import TextBuilder
import os, sys

class MarkdownBuilder(TextBuilder):
    """Build Markdown documents from a Sphinx doctree"""

    name = 'markdown'
    format = 'markdown'

    def __init__(self, app):
        TextBuilder.__init__(self, app)
        self.out_suffix = '.md'

    def prepare_writing(self, docnames):
        self.writer = MarkdownWriter()


def setup(app):
    global sphinx_app
    sphinx_app = app
    app.add_builder(MarkdownBuilder)

