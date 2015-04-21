# -*- coding: utf-8 -*-
#
# abstrys.sphinx.docbook_builder
# ------------------------------
#
# A DocBook builder for Sphinx, using rst2db's docbook writer.
#
# by Eron Hennessey

from abstrys.docutils.docbook_writer import DocBookWriter
from docutils.core import publish_from_doctree
from sphinx.builders.text import TextBuilder
import os, sys

class DocBookBuilder(TextBuilder):
    """Build DocBook documents from a Sphinx doctree"""
    name = 'docbook'

    def process_with_template(self, contents):
        """Process the results with a moustache-style template.

        The template variables can be specified as {{data.root_element}} and
        {{data.contents}}. You can use this to create a custom DocBook header
        for your final output."""
        try:
            import jinja2
        except ImportError:
            sys.stderr.write("DocBookBuilder -- Jinja2 is not installed: can't use template!\n")
            sys.exit(1)

        full_template_path = os.path.join(sphinx_app.env.srcdir,
                        sphinx_app.config.docbook_template_file)

        if not os.path.exists(full_template_path):
            sys.stderr.write(
                    "DocBookBuilder -- template file doesn't exist: %s\n" %
                    full_template_path)
            sys.exit(1)

        data = { 'root_element': self.root_element,
                 'contents': contents }

        jinja2env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(sphinx_app.env.srcdir),
                trim_blocks=True)

        try:
            t = jinja2env.get_template(self.template_filename)
            t.render(data=data)
        except:
            sys.stderr.write(
                    "DocBookBuilder -- Jinja2 couldn't load template at: %s" %
                    full_template_path)
            sys.exit(1)

        return t.render(data=data)


    def get_target_uri(self, docname, typ=None):
       return './%s.xml' % docname


    def prepare_writing(self, docnames):
        self.root_element = sphinx_app.config.docbook_default_root_element
        self.template_filename = sphinx_app.config.docbook_template_file


    def write_doc(self, docname, doctree):

        # If there's an output filename, use its basename as the root
        # element's ID.
        #(path, filename) = os.path.split(self.output_filename)
        #(doc_id, ext) = os.path.splitext(filename)

        docutils_writer = DocBookWriter(self.root_element, docname,
                output_xml_header=(self.template_filename == None))

        # get the docbook output.
        docbook_contents = publish_from_doctree(doctree,
                writer=docutils_writer)

        # process the output with a template if a template name was supplied.
        if self.template_filename != None:
            docbook_contents = self.process_with_template(docbook_contents)

        output_file = open(os.path.join(self.outdir, '%s.xml' % docname), 'w+')
        output_file.write(docbook_contents)


def setup(app):
    global sphinx_app
    sphinx_app = app
    app.add_config_value('docbook_default_root_element', 'section', 'env')
    app.add_config_value('docbook_template_file', None, 'env')
    app.add_builder(DocBookBuilder)

