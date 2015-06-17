# -*- coding: utf-8 -*-
#
# abstrys.docbook.writer
# ----------------------
#
# A module for docutils that converts from a doctree to DocBook output.
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

import lxml.etree as etree


def _print_error(text, node = None):
    """Prints an error string and optionally, the node being worked on."""
    sys.stderr.write('\n%s: %s\n' % (__name__, text))
    if node:
        sys.stderr.write(u"  %s\n" % unicode(node))


class DocBookWriter(writers.Writer):
    """A docutils writer for DocBook."""

    def __init__(self, root_element, document_id = None, output_xml_header=True):
        """Initialize the writer. Takes the root element of the resulting
        DocBook output as its sole argument."""
        writers.Writer.__init__(self)
        self.document_type = root_element
        self.document_id = document_id
        self.output_xml_header = output_xml_header

    def translate(self):
        """Call the translator to translate the document"""
        self.visitor = DocBookTranslator(self.document, self.document_type,
                self.document_id, self.output_xml_header)
        self.document.walkabout(self.visitor)
        self.output = self.visitor.astext()
        self.fields = self.visitor.fields


class DocBookTranslator(nodes.NodeVisitor):
    """A docutils translator for DocBook."""

    def __init__(self, document, document_type, document_id = None,
                 output_xml_header=True):
        """Initialize the translator. Takes the root element of the resulting
        DocBook output as its sole argument."""
        nodes.NodeVisitor.__init__(self, document)
        self.settings = document.settings
        self.content = []
        self.document_type = document_type
        self.document_id = document_id
        self.in_first_section = False
        self.output_xml_header = output_xml_header

        self.in_pre_block = False
        self.in_figure = False
        self.skip_text_processing = False
        self.next_element_id = None

        # self.estack is a stack of etree nodes. The bottom of the stack should
        # always be the base element (the document). The top of the stack is
        # the element currently being processed.
        self.estack = []
        self.tb = etree.TreeBuilder()
        self.fields = {}
        self.current_field_name = None
        self.nsmap = {'xml': 'http://www.w3.org/XML/1998/namespace',
                      'xlink': 'http://www.w3.org/1999/xlink',
                      'xi': 'http://www.w3.org/2001/XInclude',
                      'svg': 'http://www.w3.org/2000/svg',
                      'xhtml': 'http://www.w3.org/1999/xhtml',
                      'mathml': 'http://www.w3.org/1998/Math/MathML',
                      None: 'http://docbook.org/ns/docbook'}


    #
    # functions used by the translator.
    #

    def astext(self):
        doc = self.tb.close()
        et = etree.ElementTree(doc)
        if self.output_xml_header:
            rep = etree.tostring(et, encoding="utf-8", standalone=True,
                    pretty_print=True)
        else:
            rep = etree.tostring(et, encoding="utf-8", pretty_print=True)
        return rep


    def _add_element_title(self, title_name, title_attribs = {}):
        """Add a title to the current element."""
        self._push_element('title', title_attribs)
        self.tb.data(title_name)
        return self.tb_end('title')


    def _push_element(self, name, attribs = {}):
        if self.next_element_id:
            attribs['{http://www.w3.org/XML/1998/namespace}id'] = self.next_element_id
            self.next_element_id = None
        elif '{http://www.w3.org/XML/1998/namespace}id' in attribs and attribs['{http://www.w3.org/XML/1998/namespace}id'] is None:
            del attribs['{http://www.w3.org/XML/1998/namespace}id']
        e = self.tb.start(name, attribs, self.nsmap)
        self.estack.append(e)
        return e


    def _pop_element(self):
        e = self.estack.pop()
        return self.tb.end(e.tag)


    #
    # document parts
    #

    def visit_abstract(self, node):
        self._push_element('abstract')


    def depart_abstract(self, node):
        self._pop_element()


    def visit_address(self, node):
        self.visit_literal_block(node)


    def depart_address(self, node):
        self.depart_literal_block(node)


    def visit_block_quote(self, node):
        self._push_element('blockquote')


    def depart_block_quote(self, node):
        self._pop_element()


    def visit_comment(self, node):
        # ignore comments in the output.
        _print_error("ignoring comment:", node)
        self.skip_text_processing = True


    def depart_comment(self, node):
        self.skip_text_processing = False


    def visit_compact_paragraph(self, node):
        self.visit_paragraph(node)


    def depart_compact_paragraph(self, node):
        self.depart_paragraph(node)


    def visit_compound(self, node):
        pass


    def depart_compound(self, node):
        pass


    def visit_docinfo(self, node):
        _print_error("docinfo", node)
        pass


    def depart_docinfo(self, node):
        pass


    def visit_document(self, node):
        """Create the document itself."""
        pass


    def depart_document(self, node):
        pass


    def visit_include(self, node):
        """Include as an xi:include"""


    def visit_index(self, node):
        pass
        #self._push_element('indexterm')


    def depart_index(self, node):
        pass
        #self._pop_element()


    def visit_literal_strong(self, node):
        self._push_element('command')


    def depart_literal_strong(self, node):
        self._pop_element()


    def visit_paragraph(self, node):
        if self.current_field_name is None:
            self._push_element('para')


    def depart_paragraph(self, node):
        if self.current_field_name is None:
            self._pop_element()


    def visit_section(self, node):
        attribs = {}
        # Do something special if this is the very first section in the
        # document.
        if self.in_first_section == False:
            node['ids'][0] = self.document_id
            self._push_element(self.document_type,
                               {'{http://www.w3.org/XML/1998/namespace}id': self.document_id,
                                'version': '5.0'})
            self.in_first_section = True
            return

        if self.next_element_id:
            node['ids'][0] = self.next_element_id
            attribs['{http://www.w3.org/XML/1998/namespace}id'] = self.next_element_id
            self.next_element_id = None
        else:
            if len(node['ids']) > 0:
                attribs['{http://www.w3.org/XML/1998/namespace}id'] = unicode(node['ids'][0])

        self._push_element('section', attribs)
        # TODO - Collect other attributes.


    def depart_section(self, node):
        self._pop_element()


    def visit_substitution_definition(self, node):
        # substitution references don't seem to be caught by the processor.
        # Otherwise, I'd have this code here:
        # sub_name = node['names'][0]
        # sub_text = unicode(node.children[0])
        # if sub_text[0:2] == '\\u':
        #     sub_text = '&#%s;' % sub_text[2:]
        # self.subs.append('<!ENTITY %s "%s">' % (sub_name, sub_text))
        self.skip_text_processing = True


    def depart_substitution_definition(self, node):
        self.skip_text_processing = False


    def visit_substitution_reference(self, node):
        #self.tb.data('&%s;' % unicode(node))
        self.skip_text_processing = True


    def depart_substitution_reference(self, node):
        self.skip_text_processing = False


    def visit_subtitle(self, node):
        self._push_element('subtitle')


    def depart_subtitle(self, node):
        self._pop_element()


    def visit_title(self, node):
        attribs = {}
        # first check to see if an {http://www.w3.org/XML/1998/namespace}id was supplied.
        if len(node['ids']) > 0:
            attribs['{http://www.w3.org/XML/1998/namespace}id'] = unicode(node['ids'][0])
        elif len(node.parent['ids']) > 0:
            # If the parent node has an ID, we can use that and add '.title' at
            # the end to make a deterministic title ID.
            attribs['{http://www.w3.org/XML/1998/namespace}id'] = '%s.title' % unicode(node.parent['ids'][0])
        self._push_element('title', attribs)


    def depart_title(self, node):
        self._pop_element()


    def visit_title_reference(self, node):
        self._push_element('citetitle')


    def depart_title_reference(self, node):
        self._pop_element()


    def visit_titleabbrev(self, node):
        self._push_element('titleabbrev')


    def depart_titleabbrev(self, node):
        self._pop_element()


    def visit_topic(self, node):
        self.visit_section(node)


    def depart_topic(self, node):
        self.depart_section(node)


    def visit_Text(self, node):
        if self.skip_text_processing:
            return
        self.tb.data(unicode(node))


    def depart_Text(self, node):
        pass


    #
    # link parts
    #

    def visit_reference(self, node):
        internal_ref = False

        # internal ref style #1: it declares itself internal
        if node.hasattr('internal'):
            internal_ref = node['internal']

        # internal ref style #2: it hides as an external ref, with strange
        # qualities.
        if (node.hasattr('anonymous') and (node['anonymous'] == 1) and
                node.hasattr('refuri') and (node['refuri'][0] == '_')):
            internal_ref = True
            node['refuri'] = node['refuri'][1:]

        if node.hasattr('refid'):
            self._push_element('link', {'linkend': node['refid']})
        elif node.hasattr('refuri'):
            if internal_ref:
                ref_name = os.path.splitext(node['refuri'])[0]
                self._push_element('link', {'linkend': ref_name})
            else:
                self._push_element('link', {'{http://www.w3.org/1999/xlink}href': node['refuri']})
        else:
            _print_error('unknown reference', node)


    def depart_reference(self, node):
        if node.hasattr('refid') or node.hasattr('refuri'):
            self._pop_element()


    def visit_target(self, node):
        if node.hasattr('refid'):
            if node['refid'] == 'index-0':
                return
            else:
                self.next_element_id = node['refid']


    def depart_target(self, node):
        #self._pop_element()
        pass


    #
    # list parts
    #

    def visit_bullet_list(self, node):
        self._push_element('itemizedlist')


    def depart_bullet_list(self, node):
        self._pop_element()


    def visit_enumerated_list(self, node):
        self._push_element('orderedlist')


    def depart_enumerated_list(self, node):
        self._pop_element()


    def visit_list_item(self, node):
        self._push_element('listitem')


    def depart_list_item(self, node):
        self._pop_element()


    def visit_definition_list(self, node):
        self._push_element('variablelist')


    def depart_definition_list(self, node):
        self._pop_element()


    def visit_definition_list_item(self, node):
        self._push_element('varlistentry')


    def depart_definition_list_item(self, node):
        self._pop_element()


    def visit_term(self, node):
        self._push_element('term')


    def depart_term(self, node):
        self._pop_element()


    def visit_definition(self, node):
        self.visit_list_item(node)


    def depart_definition(self, node):
        self.depart_list_item(node)


    def visit_field_list(self, node):
        self._push_element('info')


    def depart_field_list(self, node):
        self._pop_element()  # info


    def visit_field(self, node):
        pass


    def depart_field(self, node):
        pass


    def visit_field_name(self, node):
        name = node.astext()
        if name == 'author':
            self._push_element('author')
            self._push_element('personname')
        elif name == 'date':
            self._push_element('pubdate')
        self.current_field_name = name
        self.skip_text_processing = True


    def depart_field_name(self, node):
        self.skip_text_processing = False


    def visit_field_body(self, node):
        if self.current_field_name:
            value = node.astext()
            self.fields[self.current_field_name] = value
        else:
            node.clear()


    def depart_field_body(self, node):
        if self.current_field_name:
            if self.current_field_name == 'author':
                self._pop_element()  # personname
                self._pop_element()  # author
            elif self.current_field_name == 'date':
                self._pop_element()  # pubdate
            self.current_field_name = None

    #
    # image parts
    #

    def visit_image(self, node):
        # if not in an enclosing figure, then we need to start a mediaobject
        # here.
        if self.in_figure == False:
            self._push_element('mediaobject')

        self._push_element('imageobject')

        # Many options are supported for imagedata
        imagedata_attribs = {}

        if node.hasattr('uri'):
            imagedata_attribs['fileref'] = node['uri']
        else:
            # unknown attribute
            imagedata_attribs['eek'] = unicode(node)

        if node.hasattr('height'):
            pass # not in docbook

        if node.hasattr('width'):
            pass # not in docbook

        if node.hasattr('scale'):
            imagedata_attribs['scale'] = unicode(node['scale'])

        if node.hasattr('align'):
            alignval = node['align']
            if (alignval == 'top' or alignval == 'middle' or alignval ==
                'bottom'):
              # top, middle, bottom all refer to the docbook 'valign'
              # attribute.
              imagedata_attribs['valign'] = alignval
            else:
              # left, right, center stay as-is
              imagedata_attribs['align'] = alignval

        if node.hasattr('target'):
            _print_error('no target attribute supported for images!')

        self._push_element('imagedata', imagedata_attribs)
        self._pop_element()

        # alt text?
        if node.hasattr('alt'):
            self._push_element('textobject')
            self._push_element('phrase')
            self.tb.data(node['alt'])
            self._pop_element() # phrase
            self._pop_element() # textobject


    def depart_image(self, node):
        self._pop_element() # imageobject
        # if not in an enclosing figure, then we need to close the mediaobject
        # here.
        if self.in_figure == False:
            self._pop_element() # mediaobject


    def visit_figure(self, node):
        self._push_element('mediaobject')
        self.in_figure = True


    def depart_figure(self, node):
        self._pop_element()
        self.in_figure = False


    def visit_caption(self, node):
        self._push_element('caption')
        self.visit_paragraph(node)


    def depart_caption(self, node):
        self.depart_paragraph(node)
        self._pop_element()


    #
    # table parts
    #

    def visit_table(self, node):
        self._push_element('table')


    def depart_table(self, node):
        self._pop_element()


    def visit_tgroup(self, node):
        attribs = {}

        if node.hasattr('cols'):
            attribs['cols'] =  unicode(node['cols'])

        self._push_element('tgroup', attribs)


    def depart_tgroup(self, node):
        self._pop_element()


    def visit_colspec(self, node):
        attribs = {}

        if node.hasattr('colwidth'):
            attribs['colwidth'] = unicode(node['colwidth'])

        self._push_element('colspec', attribs)


    def depart_colspec(self, node):
        self._pop_element()


    def visit_thead(self, node):
        self._push_element('thead')


    def depart_thead(self, node):
        self._pop_element()


    def visit_row(self, node):
        self._push_element('row')


    def depart_row(self, node):
        self._pop_element()


    def visit_entry(self, node):
        self._push_element('entry')


    def depart_entry(self, node):
        self._pop_element()


    def visit_tbody(self, node):
        self._push_element('tbody')


    def depart_tbody(self, node):
        self._pop_element()


    #
    # Character formatting
    #

    def visit_emphasis(self, node):
        self._push_element('emphasis')


    def depart_emphasis(self, node):
        self._pop_element()


    def visit_strong(self, node):
        self._push_element('emphasis', {'role': 'strong'})


    def depart_strong(self, node):
        self._pop_element()


    def visit_subscript(self, node):
        self._push_element('subscript')


    def depart_subscript(self, node):
        self._pop_element()


    def visit_superscript(self, node):
        self._push_element('superscript')


    def depart_superscript(self, node):
        self._pop_element()


    #
    # Code and such
    #

    def visit_literal_block(self, node):
        attribs = {}

        if node.hasattr('language'):
            if node.hasattr('classes') and len(node['classes']) > 0:
                attribs['language'] = node['classes'][1]
            else:
                attribs['language'] = node['language']

        self._push_element("programlisting", attribs)
        self.in_pre_block = True


    def depart_literal_block(self, node):
        self._pop_element()
        self.in_pre_block = False


    def visit_literal(self, node):
        self._push_element('code')


    def depart_literal(self, node):
        self._pop_element()


    def visit_inline(self, node):
        pass


    def depart_inline(self, node):
        pass

    #
    # Admonitions
    #

    def visit_admonition(self, node):
        # generic admonitions will just use the 'note' conventions, but will
        # set the title.
        self.visit_note(node)


    def depart_admonition(self, node):
        self.depart_note(node)


    def visit_attention(self, node):
        self.visit_important(node)
        self._add_element_title('Attention')


    def depart_attention(self, node):
        self.depart_important(node)


    def visit_caution(self, node):
        self._push_element('caution')


    def depart_caution(self, node):
        self._pop_element()


    def visit_danger(self, node):
        self.visit_warning(node)
        self._add_element_title('Danger')


    def depart_danger(self, node):
        self.depart_warning(node)


    def visit_error(self, node):
        self.visit_important(node)
        self._add_element_title('Error')


    def depart_error(self, node):
        self.depart_important(node)


    def visit_hint(self, node):
        self.visit_tip(node)
        self._add_element_title('Hint')


    def depart_hint(self, node):
        self.depart_tip(node)


    def visit_important(self, node):
        self._push_element('important')


    def depart_important(self, node):
        self._pop_element()


    def visit_note(self, node):
        self._push_element('note')


    def depart_note(self, node):
        self._pop_element()


    def visit_tip(self, node):
        self._push_element('tip')


    def depart_tip(self, node):
        self._pop_element()


    def visit_warning(self, node):
        self._push_element('warning')


    def depart_warning(self, node):
        self._pop_element()

    #
    # Error encountered...
    #

    def visit_problematic(self, node):
        _print_error('problematic node', node)

    def depart_problematic(self, node):
        pass

    def visit_system_message(self, node):
        _print_error('system message', node)

    def depart_system_message(self, node):
        pass

