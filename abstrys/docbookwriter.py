# -*- coding: utf-8 -*-
#
# docbookwriter.py
# ================
#
# A module for docutils that converts from a doctree to DocBook output.
#
from docutils import nodes, writers

class DocBookWriter(writers.Writer):
    """A docutils writer for DocBook."""

    def __init__(self, root_element):
        """Initialize the writer. Takes the root element of the resulting
        DocBook output as its sole argument."""
        writers.Writer.__init__(self)
        self.document_type = root_element

    def translate(self):
        """Call the translator to translate the document"""
        self.visitor = DocBookTranslator(self.document, self.document_type)
        self.document.walkabout(self.visitor)
        self.output = self.visitor.astext()


class DocBookTranslator(nodes.NodeVisitor):
    """A docutils translator for DocBook."""

    def __init__(self, document, document_type):
        """Initialize the translator. Takes the root element of the resulting
        DocBook output as its sole argument."""
        nodes.NodeVisitor.__init__(self, document)
        self.settings = document.settings
        self.content = []
        self.document_type = document_type

        self.indent_level = 0
        self.indent_text = "  "

        self.in_code_block = False

    #
    # functions used by the translator.
    #
    def _add(self, string):
        """Adds the given string to the contents at the current indent
        level."""
        self.content.append(self.indent_text * self.indent_level)
        self.content.append(string)

    def _add_inline(self, string):
        self.content.append(string)

    def astext(self):
        return ''.join(self.content)

    #
    # document parts
    #

    def visit_document(self, node):
        if len(node['ids']) > 0:
            self._add('<%s id="%s">\n' % (self.document_type, ''.join(node['ids'])))
        else:
            self._add('<%s>\n' % self.document_type)
        self.indent_level +=1

    def depart_document(self, node):
        self.indent_level -= 1
        self._add('</%s>\n' % self.document_type)

    def visit_title(self, node):
        if len(node['ids']) > 0:
            self._add('<title id="%s">' % ''.join(node['ids']))
        else:
            self._add('<title>')

    def depart_title(self, node):
        self._add_inline('</title>\n')

    def visit_section(self, node):
        if len(node['ids']) > 0:
            self._add_inline('\n')
            self._add('<section id="%s">\n' % ''.join(node['ids']))
        else:
            self._add('<section>\n')
        self.indent_level += 1

    def depart_section(self, node):
        self.indent_level -= 1
        self._add('</section>\n')

    def visit_paragraph(self, node):
        self._add('<para>')

    def depart_paragraph(self, node):
        self._add_inline('</para>\n')

    def visit_contents(self, node):
        self._add('<para role="topiclist">')

    def visit_topic(self, node):
        self.visit_section(node)

    def depart_topic(self, node):
        self.depart_section(node)

    def visit_Text(self, node):
        if self.in_code_block or '\n' not in node:
            self._add_inline(node)
        else:
            first = True
            lines = node.split('\n')
            for line in lines:
                if first:
                    self._add_inline(line.rstrip())
                    first = False
                    self.indent_level += 1
                else:
                    self._add_inline('\n')
                    self._add('%s' % line.strip())
            self.indent_level -= 1


    def depart_Text(self, node):
        pass

    #
    # link parts
    #

    def visit_reference(self, node):
        if node.hasattr('refid'):
            self._add_inline('<link linkend="%s">' % node['refid'])
        elif node.hasattr('refuri'):
            self._add_inline('<ulink url="%s">' % node['refuri'])
        else:
            self._add_inline('<!-- FIXME: unknown reference: -->')

    def depart_reference(self, node):
        if node.hasattr('refid'):
            self._add_inline('</link>')
        elif node.hasattr('refuri'):
            self._add_inline('</ulink>')
        else:
            self._add_inline('<!-- end unknown reference -->')

    def visit_target(self, node):
        pass

    def depart_target(self, node):
        pass


    #
    # list parts
    #

    def visit_bullet_list(self, node):
        self._add("<itemizedlist>\n")
        self.indent_level += 1

    def depart_bullet_list(self, node):
        self.indent_level -= 1
        self._add("</itemizedlist>\n")

    def visit_enumerated_list(self, node):
        self._add("<orderedlist>\n")
        self.indent_level += 1

    def depart_enumerated_list(self, node):
        self.indent_level -= 1
        self._add("</orderedlist>\n")

    def visit_list_item(self, node):
        self._add("<listitem>\n")
        self.indent_level += 1

    def depart_list_item(self, node):
        self.indent_level -= 1
        self._add("</listitem>\n")

    #
    # image parts
    #

    def visit_image(self, node):
        self._add("<mediaobject>\n")
        self.indent_level += 1
        self._add("<imageobject>\n")
        self.indent_level += 1
        self._add('<imagedata fileref="%s"/>\n' % node['uri'])

    def depart_image(self, node):
        self.indent_level -= 1
        self._add("</imageobject>\n")
        self.indent_level -= 1
        self._add("</mediaobject>\n")

    #
    # table parts
    #

    def visit_table(self, node):
        self._add("<table>\n")
        self.indent_level += 1

    def depart_table(self, node):
        self.indent_level -= 1
        self._add("</table>\n")

    def visit_tgroup(self, node):
        self._add("<tgroup>\n")
        self.indent_level += 1

    def depart_tgroup(self, node):
        self.indent_level -= 1
        self._add("</tgroup>\n")

    def visit_colspec(self, node):
        self._add("<colspec>\n")
        self.indent_level += 1

    def depart_colspec(self, node):
        self.indent_level -= 1
        self._add("</colspec>\n")

    def visit_thead(self, node):
        self._add("<thead>\n")
        self.indent_level += 1

    def depart_thead(self, node):
        self.indent_level -= 1
        self._add("</thead>\n")

    def visit_row(self, node):
        self._add("<row>\n")
        self.indent_level += 1

    def depart_row(self, node):
        self.indent_level -= 1
        self._add("</row>\n")

    def visit_entry(self, node):
        self._add("<entry>\n")
        self.indent_level += 1

    def depart_entry(self, node):
        self.indent_level -= 1
        self._add("</entry>\n")

    def visit_tbody(self, node):
        self._add("<tbody>\n")
        self.indent_level += 1

    def depart_tbody(self, node):
        self.indent_level -= 1
        self._add("</tbody>\n")


    #
    # Character formatting
    #

    def visit_emphasis(self, node):
        self._add_inline('<emphasis>')

    def depart_emphasis(self, node):
        self._add_inline('</emphasis>')

    def visit_strong(self, node):
        self._add_inline('<emphasis role="strong">')

    def depart_strong(self, node):
        self._add_inline("</emphasis>")

    #
    # Code and such
    #

    def visit_literal_block(self, node):
        if node.hasattr('classes') and len(node['classes']) > 0:
            language = node['classes'][1]
            self._add('<programlisting language="%s">\n' % language)
        else:
            self._add("<programlisting>\n")
        self.in_code_block = True

    def depart_literal_block(self, node):
        self._add_inline("</programlisting>\n")
        self.in_code_block = False

    def visit_literal(self, node):
        self._add_inline('<code>')

    def depart_literal(self, node):
        self._add_inline('</code>')

    def visit_inline(self, node):
        pass

    def depart_inline(self, node):
        pass

    #
    # Admonitions
    #

    def visit_note(self, node):
        self._add("<note>\n")
        self.indent_level += 1

    def depart_note(self, node):
        self.indent_level -= 1
        self._add("</note>\n")

    def visit_warning(self, node):
        self._add("<warning>\n")
        self.indent_level += 1

    def depart_warning(self, node):
        self.indent_level -= 1
        self._add("</warning>\n")

    def visit_tip(self, node):
        self._add("<tip>\n")
        self.indent_level += 1

    def depart_tip(self, node):
        self.indent_level -= 1
        self._add("</tip>\n")

