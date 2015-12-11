#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rst2md.py
# =========
#
# A reStructuredText to Markdown conversion tool, using Python's docutils
# library.
#
# by Eron Hennessey
#

import os
import sys

from abstrys.docutils_ext.markdown_writer import MarkdownWriter
from abstrys.common import printerr
from docutils.core import publish_string


USAGE = """
rst2md - convert reStructuredText to Markdown

**Usage**::

 rst2md <filename> [-o output_file] [-t template_file]

Only the filename to process is required. All other settings are optional.

**Settings**:

-o *output_file*    set the output filename to write. If this is not
                    specified, then output will be sent to ``stdout``.

-t *template_file*  set a template file to use to dress the output. You must
                    have Jinja2 installed to use this feature.

                    Use {{data.contents}} to represent the output of this script
                    in your template.
        """


def print_usage_and_exit(return_code=0):
    print(USAGE)
    sys.exit(return_code)

def process_cmd_args():
    # get the command args
    params = {'input_filename': None,
              'output_filename': None,
              'template_filename': None,
              'switches': []}
    last_switch = None
    for arg in sys.argv[1:]:
        if arg[0] == '-':
            if arg[1] == 'h' or arg[1] == '?':
                print_usage_and_exit()
            params['switches'].append(arg[1])
            last_switch = arg[1]
        else:
            if last_switch == 'o':  # the output filename
                params['output_filename'] = arg
                last_switch = None
            elif last_switch == 't':  # the template filename
                params['template_filename'] = arg
                last_switch = None
            else:  # the filename to process
                params['input_filename'] = arg
    return params


def process_with_template(contents, params, fields):
    """Process the results with a Jinja2-style template.

    The template variables can be specified as {{data.root_element}} and
    {{data.contents}}. You can use this to create a custom Markdown header for
    your final output."""
    try:
        import jinja2
    except ImportError:
        printerr("""Jinja2 is not installed: can't use template!""")
        sys.exit(1)
    fields['contents'] = contents
    jinja2env = jinja2.Environment(loader=jinja2.FileSystemLoader('/'),
            trim_blocks=True)
    t = jinja2env.get_template(params['template_filename'])
    return t.render(data=fields)


def run():
    """The main procedure."""
    params = process_cmd_args()

    # check for the basics. Without these, we're lost...
    if params['input_filename'] == None:
        printerr("Wait, I need at *least* a filename to process!")
        print_usage_and_exit(1)

    if not os.path.exists(params['input_filename']):
        printerr("File doesn't exist: %s" % params['input_filename'])
        sys.exit(1)

    # get the file contents first
    input_file_contents = open(params['input_filename'], 'rb').read()

    docutils_writer = None
    # set up the writer
    docutils_writer = MarkdownWriter()

    # get the markdown output.
    overrides = {'input_encoding': 'utf-8',
                 'output_encoding': 'utf-8'}
    markdown_contents = publish_string(input_file_contents,
                                      writer=docutils_writer,
                                      settings_overrides=overrides)

    # process the output with a template if a template name was supplied.
    if params['template_filename'] != None:
        markdown_contents = process_with_template(markdown_contents.decode('utf-8'),
                                                 params,
                                                 docutils_writer.fields).encode('utf-8')
    # if there's an output file, write to that. Otherwise, write to stdout.
    if params['output_filename'] == None:
        output_file = sys.stdout
    else:
        output_file = open(params['output_filename'], 'w+')

    output_file.write(markdown_contents)
    # that's it, we're done here!
    sys.exit(0)

if __name__ == "__main__":
    run()
