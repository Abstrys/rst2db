#########
rst2db.py
#########

A number of tools for reStructuredText (reST) and Sphinx, including:

* A reST to DocBook converter (``rst2db``) with an included Sphinx builder
  (abstrys.spinx_ext.docbook_builder).

* A reST to Markdown converter (``rst2md``) with an included Sphinx builder
  (abstrys.sphinx_ext.markdown_builder).

Prerequisites
=============

Before installing rst2db, you'll need the following prerequisites:

* libxml2 and headers (**libxml2** and **libxml2-dev**)
* Python bindings for libxml2 (**python-lxml** or **python3-lxml**)
* libxslt1 headers (**libxslt1-dev**)
* Python headers (**python-dev** or **python3-dev**)

**You can install these on Ubuntu / Debian** by running::

 sudo apt-get install libxml2 libxml2-dev libxslt1-dev

and *one* of the following, depending on your Python version::

 sudo apt-get install python3-lxml python3-dev

 sudo apt-get install python-lxml python-dev


Using the command-line utilities
================================

::

 rst2db <filename> [-e root_element] [-o output_file] [-t template_file]

 rst2md <filename> [-o output_file]

Only the *filename* to process is required. All other settings are optional.

**Settings:**

.. list-table::
   :widths: 1 3

   * - -e root_element
     - set the root element of the resulting docbook file. If this is not specified, then 'section'
       will be used.

   * - -o output_file
     - set the output filename to write. If this is not specified, then output will be sent to
       stdout.

   * - -t template_file
     - set a template file to use to dress the output. You must have Jinja2 installed to use this
       feature.


DocBook template files
----------------------

When using a DocBook template file, use {{data.root_element}} and {{data.contents}} to represent the
root element (chapter, section, etc.) and {{data.contents}} to represent the transformed contents of
your ``.rst`` source.

For example, you could use a template that looks like this:

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <!DOCTYPE {{data.root_element}} PUBLIC "-//OASIS//DTD DocBook XML V4.1.2//EN"
             "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd">
   <{{data.root_element}}>
       {{data.contents}}
   </{{data.root_element}}>

A template is only necessary if you want to customize the output. A standard DocBook XML header will
be included in each output file by default.


Using the Sphinx builders
=========================

Docbook output
--------------

To build DocBook output with Sphinx, add `abstrys.sphinx_ext.docbook_builder` to the *extensions*
list in ``conf.py``::

 extensions = [
    ... other extensions here ...
    abstrys.sphinx_ext.docbook_builder
    ]

There are two configurable parameters for ``conf.py`` that correspond to
``rst2db.py`` parameters:


.. list-table::
   :widths: 1 3

   * - *docbook_template_file*
     - template file that will be used to position the document parts. This should be a valid
       DocBook .xml file that contains  Requires Jinja2 to be
       installed if specified.

   * - *docbook_default_root_element*
     - default root element for a file-level document.  Default is 'section'.

For example:

.. code:: python

   docbook_template_file = 'dbtemplate.xml'
   docbook_default_root_element = chapter

Then, build your project using ``sphinx-build`` with the ``-b docbook`` option::

 sphinx-build source output -b docbook


Markdown output
---------------

To build Markdown output with Sphinx, add ``abstrys.sphinx_ext.docbook_builder`` to the *extensions*
list in ``conf.py``::

 extensions = [
    ... other extensions here ...
    abstrys.sphinx_ext.markdown_builder
    ]

There aren't any configurable options yet. Just build your project with ``-b markdown`` as the
output type::

 sphinx-build source output -b markdown


License
-------

This software is provided under the `BSD 3-Clause`__ license. See the
`LICENSE`__ file for more details.

.. __: http://opensource.org/licenses/BSD-3-Clause
.. __: https://github.com/Abstrys/abstrys-toolkit/blob/master/LICENSE

For more information
--------------------

Contact: Eron Hennessey <eron@abstrys.com>

