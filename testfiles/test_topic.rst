My Test Topic
=============

This is a test `reStructuredText`__ topic. It provides an example of reST
markup that can be used to test how docutils can transform reST into various
other formats.

.. __: http://docutils.sourceforge.net/rst.html

.. contents::


Lists
-----

Let's start by declaring a list. This is one of the simplest and most often
used elements in technical writing, besides sections, titles, and paragraphs
(which are already represented in this document's structure).

My list consists of a few items:

* red
* green
* blue

Those are great colors, aren't they? They can be combined in so many ways, too.

We have other types of items, too:

1. The first step.
2. The second step.
3. Watch that third step, it's a doozy!

Images
------

We frequently include images in technical writing to illustrate important
concepts, like this:

.. image:: test_img.png

He's a fine cat, that one.

Tables
------

You can easily create tables in reST.  Here's a quick one:

+----------------------+------------------------+-------------------+
| Common Name          | Classification         | Notes             |
+----------------------+------------------------+-------------------+
| Velvetleaf Blueberry | Vaccinium myrtilloides | look near bogs    |
+----------------------+------------------------+-------------------+
| Salmonberry          | Rubus spectabilis      | best when orange  |
+----------------------+------------------------+-------------------+
| Thimbleberry         | Rubus parviflorus      | don't eat wilted! |
+----------------------+------------------------+-------------------+

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

.. warning::

   This is a warning.

.. tip::

   This is a tip.

Includes
--------

reStructuredText supports the ``include`` directive, which can be used to
transclude other documents. Here's an example:

.. include:: test_topic_2.rst

