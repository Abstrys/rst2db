#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rst2db.py
# =========
#
# A reStructuredText to DocBook conversion tool, using Python's docutils
# library.
#
# by Eron Hennessey

import sys
import os
from docutils.core import publish_string
from docutils.core import publish_cmdline
from docutils.core import publish_file
from abstrys.docutils.docbook_writer import DocBookWriter

def printerr(error_text):
    """Prints an error message to stderr"""
    sys.stderr.write("ERROR -- %s\n" % error_text)

def __init__(self):
    self.USAGE = """
rst2db - convert reStructuredText to DocBook

**Usage:**

:
rst2db <filename> [-e root_element] [-o output_file] [-t template_file]

Only the filename to process is required. All other settings are optional.

**Settings:**

-e *root_element*   set the root element of the resulting docbook file. If this
                  is not specified, then 'section' will be used by default.

-o *output_file*    set the output filename to write. If this is not
                  specified, then output will be sent to ``stdout``.

-t *template_file*  set a template file to use to dress the output. You must
                  have Jinja2 installed to use this feature.

                  Use {{data.root_element}} and {{data.contents}} to
                  represent the output of this script in your template.
        """
    self.input_filename = None
    self.output_filename = None
    self.template_filename = None
    self.root_element = 'section'
    self.switches = []

def print_usage_and_exit(self, return_code=0):
    print(self.USAGE)
    sys.exit(return_code)

def process_cmd_args(self):
    # get the command args
    last_switch = None
    for arg in sys.argv[1:]:
        if arg[0] == '-':
            if arg[1] == 'h' or arg[1] == '?':
                self.print_usage_and_exit()
            self.switches.append(arg[1])
            last_switch = arg[1]
        else:
            if last_switch == 'o': # the output filename
                self.output_filename = arg
                last_switch = None
            elif last_switch == 't': # the template filename
                self.template_filename = arg
                last_switch = None
            elif last_switch == 'e': # the root element
                self.root_element = arg
                last_switch = None
            else: # the filename to process
                self.input_filename = arg


def process_with_template(self, contents):
    """Process the results with a Jinja2-style template.

    The template variables can be specified as {{data.root_element}} and
    {{data.contents}}. You can use this to create a custom DocBook header for
    your final output."""
    try:
        import jinja2
    except ImportError:
        printerr("""Jinja2 is not installed: can't use template!""")
        sys.exit(1)

    if not os.path.exists(self.template_filename):
        printerr("Template file doesn't exist: %s" %
                self.template_filename)
        sys.exit(1)

    data = { 'root_element': self.root_element,
             'contents': contents }

    jinja2env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'),
            trim_blocks=True)

    t = jinja2env.get_template(self.template_filename)
    return t.render(data=data)


def run(self):
    """The main procedure."""
    self.process_cmd_args()

    # check for the basics. Without these, we're lost...
    if self.input_filename == None:
        printerr("Wait, I need at *least* a filename to process!")
        self.print_usage_and_exit(1)

    if not os.path.exists(self.input_filename):
        printerr("File doesn't exist: %s" % self.input_filename)
        sys.exit(1)

    # get the file contents first
    input_file_contents = open(self.input_filename, 'r').read()

    docutils_writer = None
    # set up the writer
    if self.output_filename != None:
        # If there's an output filename, use its basename as the root
        # element's ID.
        (path, filename) = os.path.split(self.output_filename)
        (doc_id, ext) = os.path.splitext(filename)
        docutils_writer = DocBookWriter(self.root_element, doc_id,
                output_xml_header=(self.template_filename == None))
    else:
        docutils_writer = DocBookWriter(self.root_element,
                output_xml_header=(self.template_filename == None))

    # get the docbook output.
    docbook_contents = publish_string(input_file_contents,
            writer=docutils_writer)

    # process the output with a template if a template name was supplied.
    if self.template_filename != None:
        docbook_contents = self.process_with_template(docbook_contents)

    # if there's an output file, write to that. Otherwise, write to stdout.
    if self.output_filename == None:
        output_file = sys.stdout
    else:
        output_file = open(self.output_filename, 'w+')

    output_file.write(docbook_contents)

    # that's it, we're done here!
    sys.exit(0)

if __name__ == "__main__":
    run()

