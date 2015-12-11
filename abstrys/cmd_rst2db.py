#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rst2db.py
# =========
#
# A reStructuredText to DocBook conversion tool, using Python's docutils
# library.
#
# by Eron Hennessey, with contributions from great people:
#
# * Aleksei Badyaev <aleksei.badyaev@gmail.com>
#

import os
import sys

from abstrys.docutils_ext.docbook_writer import DocBookWriter
from abstrys.common import printerr
from docutils.core import publish_string


USAGE = """
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


def print_usage_and_exit(return_code=0):
    print(USAGE)
    sys.exit(return_code)


def process_cmd_args():
    # get the command args
    params = {'input_filename': None,
              'output_filename': None,
              'template_filename': None,
              'root_element': 'section',
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
            elif last_switch == 'e':  # the root element
                params['root_element'] = arg
                last_switch = None
            else:  # the filename to process
                params['input_filename'] = arg
    return params


def process_with_template(contents, params, fields):
    """Process the results with a Jinja2-style template.

    The template variables can be specified as {{data.root_element}} and
    {{data.contents}}. You can use this to create a custom DocBook header for
    your final output."""
    try:
        import jinja2
    except ImportError:
        printerr("""Jinja2 is not installed: can't use template!""")
        sys.exit(1)
    fields['root_element'] = params['root_element']
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
    if params['output_filename'] != None:
        # If there's an output filename, use its basename as the root
        # element's ID.
        (path, filename) = os.path.split(params['output_filename'])
        (doc_id, ext) = os.path.splitext(filename)
        docutils_writer = DocBookWriter(params['root_element'], doc_id,
                output_xml_header=(params['template_filename'] == None))
    else:
        docutils_writer = DocBookWriter(params['root_element'],
                output_xml_header=(params['template_filename'] == None))
    # get the docbook output.
    overrides = {'input_encoding': 'utf-8',
                 'output_encoding': 'utf-8'}
    docbook_contents = publish_string(input_file_contents,
                                      writer=docutils_writer,
                                      settings_overrides=overrides)

    # process the output with a template if a template name was supplied.
    if params['template_filename'] != None:
        docbook_contents = process_with_template(docbook_contents.decode('utf-8'),
                                                 params,
                                                 docutils_writer.fields).encode('utf-8')
    # if there's an output file, write to that. Otherwise, write to stdout.
    if params['output_filename'] == None:
        output_file = sys.stdout
    else:
        output_file = open(params['output_filename'], 'w+')

    output_file.write(docbook_contents)
    # that's it, we're done here!
    sys.exit(0)

if __name__ == "__main__":
    run()
