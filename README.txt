rst2db.py
=========

A reStructuredText to DocBook converter using Python's docutils.

rst2db.py will convert simple reStructuredText markup to DocBook. Not all tags
are yet supported, but it is easy to add new ones thanks to docutils.

Usage
-----

::

  rst2db <filename> [-e root_element] [-o output_file] [-t template_file]

Only the filename to process is required. All other settings are optional.

Settings:

  -e root_element   set the root element of the resulting docbook file. If this
                    is not specified, then 'section' will be used.

  -o output_file    set the output filename to write. If this is not specified,
                    then output will be sent to stdout.

  -t template_file  set a template file to use to dress the output. You must
                    have Jinja2 installed to use this feature.

                    Use {{data.root_element}} and {{data.contents}} to
                    represent the output of this script in your template.

License
-------

This software is provided under the `BSD
3-Clause <http://opensource.org/licenses/BSD-3-Clause>`__ license. See
the `LICENSE
file <https://github.com/Abstrys/abstrys-toolkit/blob/master/LICENSE>`__
for more details.

For more information
--------------------

Contact `eron@abstrys.com <mailto:eron@abstrys.com?Subject=rst2db>`__
