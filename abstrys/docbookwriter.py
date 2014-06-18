# -*- coding: utf-8 -*-
#
# docbookwriter.py
# ================
#
# A module for docutils that converts from a doctree to DocBook output.
#
# Written by Eron Hennessey
#
# Much more information about the elements in this module can be found at:
#
# * http://docutils.sourceforge.net/docs/ref/doctree.html
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

        self.in_pre_block = False
        self.in_figure = False

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

    def visit_block_quote(self, node):
        self._add('<blockquote>\n')
        self.indent_level += 1

    def depart_block_quote(self, node):
        self.indent_level -= 1
        self._add('</blockquote>\n')

    def visit_topic(self, node):
        self.visit_section(node)

    def depart_topic(self, node):
        self.depart_section(node)

    def visit_Text(self, node):
        if self.in_pre_block or '\n' not in node:
            self._add_inline(node)
        else:
            first = True
            lines = node.split('\n')
            for line in lines:
                if first:
                    self._add_inline('%s' % line.strip())
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

    def visit_definition_list(self, node):
        self._add('<variablelist>\n')
        self.indent_level += 1

    def depart_definition_list(self, node):
        self.indent_level -= 1
        self._add('</variablelist>\n')

    def visit_definition_list_item(self, node):
        self._add('<varlistentry>\n')
        self.indent_level += 1

    def depart_definition_list_item(self, node):
        self.indent_level -= 1
        self._add('</varlistentry>\n')

    def visit_term(self, node):
        self._add('<term>')

    def depart_term(self, node):
        self._add_inline('</term>\n')

    def visit_definition(self, node):
        self.visit_list_item(node)

    def depart_definition(self, node):
        self.depart_list_item(node)

    #
    # image parts
    #

    def start_mediaobject(self):
        self._add("<mediaobject>\n")
        self.indent_level += 1

    def end_mediaobject(self):
        self.indent_level -= 1
        self._add("</mediaobject>\n")

    def visit_image(self, node):
        # images can exist outside of figures in the doctree, but figures
        # always contain an image.
        if not self.in_figure:
            self.start_mediaobject()

        self._add("<imageobject>\n")
        self.indent_level += 1

        # Many options are supported for imagedata
        imagedata_parts = ['<imagedata']

        if node.hasattr('uri'):
            imagedata_parts.append('fileref="%s"' % node['uri'])
        else:
            imagedata_parts.append('eek="%s"' % str(node))

        if node.hasattr('height'):
            pass
        if node.hasattr('width'):
            pass
        if node.hasattr('scale'):
            imagedata_parts.append('scale="%s"' % node['scale'])
        if node.hasattr('align'):
            alignval = node['align']
            if (alignval == 'top' or alignval == 'middle' or alignval ==
                'bottom'):
              # top, middle, bottom all refer to the docbook 'valign'
              # attribute.
              imagedata_parts.append('valign="%s"' % alignval)
            else:
              # left, right, center stay as-is
              imagedata_parts.append('align="%s"' % alignval)
        if node.hasattr('target'):
            pass
        self._add(' '.join(imagedata_parts))
        self._add_inline('>\n')
        # alt text?
        if node.hasattr('alt'):
            self._add('<textobject>\n')
            self.indent_level += 1
            self._add('<phrase>%s</phrase>\n' % node['alt'])
            self.indent_level -= 1
            self._add('</textobject>\n')

    def depart_image(self, node):
        self.indent_level -= 1
        self._add("</imageobject>\n")
        if not self.in_figure:
            self.end_mediaobject()

    def visit_figure(self, node):
        self.start_mediaobject()

    def depart_figure(self, node):
        self.end_mediaobject()

    def visit_caption(self, node):
        self._add('<caption>\n')
        self.indent_level += 1
        self.visit_paragraph(node)

    def depart_caption(self, node):
        self.depart_paragraph(node)
        self.indent_level -= 1
        self._add('</caption>\n')

    #
    # table parts
    #

    def visit_table(self, node):
        self._add('<table>\n')
        self.indent_level += 1

    def depart_table(self, node):
        self.indent_level -= 1
        self._add("</table>\n")

    def visit_tgroup(self, node):
        if node.hasattr('cols'):
            self._add('<tgroup cols="%s">\n' % node['cols'])
        else:
            self._add("<tgroup>\n")
        self.indent_level += 1

    def depart_tgroup(self, node):
        self.indent_level -= 1
        self._add("</tgroup>\n")

    def visit_colspec(self, node):
        if node.hasattr('colwidth'):
            self._add('<colspec colwidth="%s"/>\n' % node['colwidth'])
        else:
            self._add('<colspec/>\n')

    def depart_colspec(self, node):
        pass

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
        self._add_inline(' <emphasis>')

    def depart_emphasis(self, node):
        self._add_inline('</emphasis>')

    def visit_strong(self, node):
        self._add_inline('<emphasis role="strong">')

    def depart_strong(self, node):
        self.depart_emphasis(node)

    def visit_subscript(self, node):
        self._add_inline('<subscript>')

    def depart_subscript(self, node):
        self._add_inline('</subscript>')

    def visit_superscript(self, node):
        self._add_inline('<superscript>')

    def depart_superscript(self, node):
        self._add_inline('</superscript>')

    #
    # Code and such
    #

    def visit_literal_block(self, node):
        if node.hasattr('classes') and len(node['classes']) > 0:
            language = node['classes'][1]
            self._add('<programlisting language="%s">\n' % language)
        else:
            self._add("<programlisting>\n")
        self.in_pre_block = True

    def depart_literal_block(self, node):
        self._add_inline("</programlisting>\n")
        self.in_pre_block = False

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

