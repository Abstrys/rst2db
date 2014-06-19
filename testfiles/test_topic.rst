My Test Topic
=============

This is a test `reStructuredText`__ topic. It provides an example of reST
markup that can be used to test how docutils can transform reST into various
other formats.

.. __: http://docutils.sourceforge.net/rst.html

.. contents::

Simple Lists
------------

Let's start by declaring a list. This is one of the simplest and most often
used elements in technical writing, besides sections, titles, and paragraphs
(which are already represented in this document's structure).

My list consists of a few items:

* red
* green
* blue

Those are great colors, aren't they? They can be combined in so many ways, too.

We have some numbered items, too:

1. The first step.
2. The second step.
3. Watch that third step, it's a doozy!


Extended Lists
--------------

In addition to simple list types (itemized and ordered), there are other common
list types. Most used in DocBook is one called a *variable list*, which is
analagous to a definition list. Here's an example.

Term 1:
    Term 1 has a description

Term 2:
    Term 2 also has a description

Term 3:
    Term 3 was lost in a maze of twisty passages, all different.


Linking
-------

There are all sorts of link types in reStructuredText:

* **Anonymous links**::

    This is an `anonymous link`__.

    .. __: lists

  This is an `anonymous link`__.

.. __: lists

* **Named links**::

    This is a `named link`_.

    .. _`named link`: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html

  This is a `named link`_.

.. _`named link`: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html

* **Indirect links**::

    This is an `indirect link`__.

    .. __: `named link`_

  This is an `indirect link`__.

.. __: `named link`_


Images
------

We frequently include images in technical writing to illustrate important
concepts, like this:

.. image:: test_img.png
   :scale: 50
   :align: center
   :alt: Purrmenides

He's a fine cat, that one.

.. figure:: test_img.png
   :alt: Purrmenides

   This figure has both alt text and a caption!


Tables
------

You can easily create tables in reST.  Here's a quick one:

+----------------------+----------------------------+-------------------+
| Common Name          | Classification             | Notes             |
+======================+============================+===================+
| Velvetleaf Blueberry | * Vaccinium look near bogs                     |
|                      |                                                |
+----------------------+----------------------------+-------------------+
| Salmonberry          | Rubus spectabilis          | best when orange  |
+----------------------+----------------------------+-------------------+
| Thimbleberry         | Rubus parviflorus          | don't eat wilted! |
+----------------------+----------------------------+-------------------+
| Catberry             |                            |                   |
+----------------------+----------------------------+-------------------+

Code
----

Code blocks can be included a number of ways:

**Method 1**

::

  # this is a code block
  a = "hello world"
  print a

**Method 2**

.. code:: python

    # this is a code block
    a = "hello world"
    print a

You can also have inline code fragments, such as: ``a = "hello world"``.

Admonitions and such
--------------------

Here's an admonition:

.. note::

    This is a note.

    This is still part of the note.

This is no longer part of the note.

.. warning::

   This is a warning.

.. tip::

   This is a tip.

Includes
--------

reStructuredText supports the ``include`` directive, which can be used to
transclude other documents. Here's an example:

.. include:: test_topic_2.rst

