# -*- coding: utf-8 -*-
#
# #######################
# abstrys.markdown.writer
# #######################
#
# A module for docutils that converts from a doctree to Markdown output.
#
# Written by Eron Hennessey
#
# Much more information about the elements in this module can be found at:
#
# * http://docutils.sourceforge.net/docs/ref/doctree.html
#
import os
import sys

from docutils import nodes, writers
from textwrap import TextWrapper

LINE_WIDTH = 78

def _print_error(text, node = None):
    """Prints an error string and optionally, the node being worked on."""
    sys.stderr.write('\n%s: %s\n' % (__name__, text))
    if node:
        sys.stderr.write(u"  %s\n" % unicode(node))


class MarkdownWriter(writers.Writer):
    """A docutils writer for Markdown."""

    # class data
    supported = ('markdown',)
    output = None

    def __init__(self):
        """Initialize the writer. Takes the root element of the resulting
        Markdown output as its sole argument."""
        writers.Writer.__init__(self)
        self.translator_class = MarkdownTranslator

    def translate(self):
        visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()


class MarkdownTranslator(nodes.NodeVisitor):
    """A docutils translator for Markdown."""

    body_content = ""
    cur_para = ""
    section_level = 1
    indent = ""
    extra_indent = ""
    in_literal = False
    quote_level = 0
    enumerated_list = False
    deindent_first = False

    def __init__(self, document):
        """Initialize the translator."""
        nodes.NodeVisitor.__init__(self, document)
        self.wrapper = TextWrapper(width=LINE_WIDTH, break_long_words=False)

    def astext(self):
        return self.body_content

    #
    # some useful functions for formatting things.
    #

    def _get_line_prefix(self):
        return self.indent + ('> ' * self.quote_level)

    def _print_line_indented(self, text=""):
        """Prints a single line, indented (and possibly quoted)."""
        line = (self._get_line_prefix() + text.rstrip() + '\n')
        self.body_content += line

    def _print_lines_indented(self, text):
        """Prints a group of lines, indented (and possibly quoted)."""
        # split the lines
        lines = text.splitlines()
        for line in lines:
            if self.deindent_first:
                self.body_content += line
                self.deindent_first = False
            else:
                self._print_line_indented(line)

    def _wrap_lines_indented(self, text):
        """Wraps a group of lines, indented (and possibly quoted)."""
        line_prefix = self._get_line_prefix()
        self.wrapper.initial_indent = line_prefix
        self.wrapper.subsequent_indent = line_prefix + self.extra_indent
        wrapped_text = self.wrapper.fill(self.cur_para)
        if self.deindent_first:
            wrapped_text = wrapped_text[len(line_prefix):]
            self.deindent_first = False
        self.body_content += wrapped_text.rstrip() + '\n'

    def _start_admonition(self, node, title):
        self.quote_level += 1
        self._print_line_indented("**%s**" % title)
        self._print_line_indented()

    def _end_admonition(self, node):
        self.quote_level -= 1
        self._print_line_indented()

    #
    # the document itself
    #

    def visit_document(self, node):
        pass

    def depart_document(self, node):
        pass

    #
    # document parts
    #

    def visit_Text(self, node):
        self.cur_para += node.astext()

    def depart_Text(self, node):
        pass

    def visit_paragraph(self, node):
        # defar processing to depart_paragraph.
        pass

    def depart_paragraph(self, node):
        if self.in_literal:
            self._print_lines_indented(self.cur_para)
        else:
            self._wrap_lines_indented(self.cur_para)
        self._print_line_indented()
        # clear the collected para content.
        self.cur_para = ""

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1


    # block_quote
    def visit_block_quote(self, node):
        self.quote_level += 1

    def depart_block_quote(self, node):
        self.quote_level -= 1


    #
    # standard (bulleted/numbered) lists
    #

    def visit_bullet_list(self, node):
        pass

    def depart_bullet_list(self, node):
        pass

    def visit_enumerated_list(self, node):
        self.enumerated_list = True

    def depart_enumerated_list(self, node):
        self._print_line_indented()
        self.enumerated_list = False

    def visit_list_item(self, node):
        if self.enumerated_list:
            self.body_content += (self._get_line_prefix() + "1. ")
        else:
            self.body_content += (self._get_line_prefix() + "* ")
        self.indent += "    "
        self.deindent_first = True

    def depart_list_item(self, node):
        self.indent = self.indent[:-4]

    #
    # definition lists and associated nodes
    #

    def visit_definition_list(self, node):
        pass

    def depart_definition_list(self, node):
        pass

    def visit_definition_list_item(self, node):
        self.section_level += 1

    def depart_definition_list_item(self, node):
        self.section_level -= 1

    def visit_term(self, node):
        self.visit_title(node)

    def depart_term(self, node):
        self.depart_title(node)

    def visit_definition(self, node):
        self.visit_block_quote(node)

    def depart_definition(self, node):
        self.depart_block_quote(node)


    # description
    def visit_description(self, node):
        pass

    def depart_description(self, node):
        pass


    # emphasis
    def visit_emphasis(self, node):
        self.cur_para += "*"

    def depart_emphasis(self, node):
        self.cur_para += "*"

    # strong
    def visit_strong(self, node):
        self.cur_para += "**"

    def depart_strong(self, node):
        self.cur_para += "**"


    # field
    def visit_field(self, node):
        pass

    def depart_field(self, node):
        pass


    # field_body
    def visit_field_body(self, node):
        pass

    def depart_field_body(self, node):
        pass


    # field_list
    def visit_field_list(self, node):
        pass

    def depart_field_list(self, node):
        pass


    # field_name
    def visit_field_name(self, node):
        pass

    def depart_field_name(self, node):
        pass

    # image

    def _add_image(self, uri, alt_text="", caption=None):
        if caption:
            text = '![%s](%s "%s")' % (alt_text, uri, caption)
        else:
            text = '![%s](%s)' % (alt_text, uri)
        self._print_line_indented(text)
        self._print_line_indented()

    def _get_image_attrs(self, node):
        """Returns a tuple: (uri, alt)"""
        alt_text = ""
        uri = ""
        if 'alt' in node:
            alt_text = node['alt']
        if 'uri' in node:
            uri = node['uri']
        return (uri, alt_text)

    def visit_image(self, node):
        (uri, alt_text) = self._get_image_attrs(node)
        self._add_image(uri, alt_text)
        raise nodes.SkipNode

    def depart_image(self, node):
        pass

    # figure
    def visit_figure(self, node):
        caption = ""
        alt_text = ""
        uri = ""
        for c in node.children:
            if type(c).__name__ is 'caption':
                caption = c.astext()
            elif type(c).__name__ is 'image':
                (uri, alt_text) = self._get_image_attrs(c)
        self._add_image(uri, alt_text, caption)
        raise nodes.SkipNode

    def depart_figure(self, node):
        pass

    # caption
    def visit_caption(self, node):
        pass

    def depart_caption(self, node):
        pass


    #
    # notes and various other admonitions
    #

    def visit_note(self, node):
        self._start_admonition(node, "Note:")

    def depart_note(self, node):
        self._end_admonition(node)

    # tip
    def visit_tip(self, node):
        self._start_admonition(node, "Tip:")

    def depart_tip(self, node):
        self._end_admonition(node)

    # warning
    def visit_warning(self, node):
        self._start_admonition(node, "Warning:")

    def depart_warning(self, node):
        self._end_admonition(node)


    # literal inlines
    def visit_literal(self, node):
        self.cur_para += "`%s`" % node.astext()
        raise nodes.SkipNode

    def depart_literal(self, node):
        pass

    def visit_inline(self, node):
        self.visit_literal(node)

    def depart_inline(self, node):
        self.depart_literal(node)

    def visit_literal_strong(self, node):
        # not a normal reST element; this is added by Sphinx.
        self.cur_para += "**`%s`**" % node.astext()
        raise nodes.SkipNode

    def depart_literal_strong(self, node):
        pass


    # literal_block - uses GitHub syntax
    # https://help.github.com/articles/github-flavored-markdown/
    def visit_literal_block(self, node):
        code_class = ""
        if ('classes' in node) and ('code' in node['classes']):
            code_class = node['classes'][1]
        elif ('language' in node):
            code_class = node['language']
        self._print_line_indented("```" + code_class)
        self._print_lines_indented(node.astext())
        self._print_line_indented("```")
        self._print_line_indented()
        raise nodes.SkipNode

    def depart_literal_block(self, node):
        pass

    # option_list
    def visit_option(self, node):
        pass

    def depart_option(self, node):
        pass

    def visit_option_argument(self, node):
        pass

    def depart_option_argument(self, node):
        pass

    def visit_option_group(self, node):
        pass

    def depart_option_group(self, node):
        pass

    def visit_option_list(self, node):
        pass

    def depart_option_list(self, node):
        pass

    def visit_option_list_item(self, node):
        pass

    def depart_option_list_item(self, node):
        pass

    def visit_option_string(self, node):
        pass

    def depart_option_string(self, node):
        pass

    #
    # links and references
    #

    def visit_reference(self, node):
        text = ""
        if 'refuri' in node:
            text = ("[%s](%s)" % (node.astext(), node['refuri']))
        elif 'refid' in node:
            text = ("[%s](#%s)" % (node.astext(), node['refid']))
        else:
            text = node.astext()
        self.cur_para += text
        raise nodes.SkipNode

    def depart_reference(self, node):
        pass


    # table
    def visit_table(self, node):
        pass

    def depart_table(self, node):
        self._print_line_indented()

    def visit_tgroup(self, node):
        self.table_cols = int(node['cols'])
        self.table_col_widths = []

    def depart_tgroup(self, node):
        self.table_cols = 0

    def visit_colspec(self, node):
        self.table_col_widths.append(int(node['colwidth']))

    def depart_colspec(self, node):
        pass

    def visit_tbody(self, node):
        pass

    def depart_tbody(self, node):
        pass

    def visit_thead(self, node):
        pass

    def depart_thead(self, node):
        header_bar = self._get_line_prefix() + '| '
        for w in self.table_col_widths:
            header_bar += (('-' * w) + ' | ')
        header_bar = header_bar[:-1] + '\n'
        self.body_content += header_bar

    def visit_entry(self, node):
        pass

    def depart_entry(self, node):
        pass

    def visit_row(self, node):
        row_text = self._get_line_prefix() + '| '
        cur_entry = 0
        for entry in node.children:
            # remove any newlines in the entry's text.
            entry_text = ' '.join(entry.astext().splitlines())
            row_text += entry_text.ljust(self.table_col_widths[cur_entry]) + ' | '
            cur_entry += 1
        row_text = row_text[:-1] + '\n'
        self.body_content += row_text
        raise nodes.SkipNode

    def depart_row(self, node):
        pass


    # target
    def visit_target(self, node):
        # a target definition - skip (for now)
        raise nodes.SkipNode

    def depart_target(self, node):
        pass

    # title
    def visit_title(self, node):
        self.body_content += "\n%s %s\n\n" % (("#" * self.section_level), node.astext())
        raise nodes.SkipNode

    def depart_title(self, node):
        pass

    def visit_substitution_definition(self, node):
        # ignore these...
        raise nodes.SkipNode

    def depart_substitution_definition(self, node):
        pass

    def visit_index(self, node):
        pass

    def depart_index(self, node):
        pass

    def visit_topic(self, node):
        pass

    def depart_topic(self, node):
        pass

    def visit_comment(self, node):
        # ignore comments.
        raise nodes.SkipNode

    def depart_comment(self, node):
        pass

    def visit_compound(self, node):
        pass

    def depart_compound(self, node):
        pass

    def visit_compact_paragraph(self, node):
        self.visit_paragraph(node)

    def depart_compact_paragraph(self, node):
        self.depart_paragraph(node)

    # title_reference
    def visit_title_reference(self, node):
        pass

    def depart_title_reference(self, node):
        pass


    def visit_problematic(self, node):
        print("found problematic node!")

    def depart_problematic(self, node):
        pass

