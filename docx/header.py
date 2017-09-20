# encoding: utf-8

"""
Page headers and footers.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from collections import Sequence
from .enum.header import WD_HEADER_FOOTER
from .blkcntnr import BlockItemContainer
from .shared import ElementProxy, lazyproperty


class _BaseHeaderFooter(ElementProxy):
    """
    Base class for header and footer objects.
    """

    __slots__ = '_hdr_ftr_ref'

    def __init__(self, element, parent, hdr_ftr_ref):
        super(_BaseHeaderFooter, self).__init__(element, parent)
        self._hdr_ftr_ref = hdr_ftr_ref

    @lazyproperty
    def body(self):
        """
        BlockItemContainer instance with contents of Header
        """
        if self._hdr_ftr_ref is None:
            return None
        return self.part.related_hdrftr_body(self._hdr_ftr_ref.rId)

    @property
    def is_linked_to_previous(self):
        """
        Boolean representing whether this Header is inherited from
        a previous section.
        """
        return self._hdr_ftr_ref is None


class Header(_BaseHeaderFooter):
    """
    One of the page headers for a section.
    """


class Footer(_BaseHeaderFooter):
    """
    One of the page footers for a section.
    """


class Headers(Sequence):
    """
    Sequence of |Footer| objects corresponding to the footers in the
    document. Supports ``len()``, iteration, and indexed access.
    """
    enum_list = [WD_HEADER_FOOTER.PRIMARY, WD_HEADER_FOOTER.FIRST_PAGE, WD_HEADER_FOOTER.EVEN_PAGES]

    def __init__(self, sectPr, parent):
        super(Headers, self).__init__()
        self._sectPr = sectPr
        self._parent = parent

    def __getitem__(self, key):
        return Header(self._sectPr, self._parent, self._sectPr.get_headerReference_of_type(key))

    def __iter__(self):
        for _type in Headers.enum_list:
            footer_ref = self._sectPr.get_headerReference_of_type(_type)
            yield Header(self._sectPr, self._parent, footer_ref)

    def __len__(self):
        return len(Headers.enum_list)


class Footers(Sequence):
    """
    Sequence of |Footer| objects corresponding to the footers in the
    document. Supports ``len()``, iteration, and indexed access.
    """
    enum_list = [WD_HEADER_FOOTER.PRIMARY, WD_HEADER_FOOTER.FIRST_PAGE, WD_HEADER_FOOTER.EVEN_PAGES]

    def __init__(self, sectPr, parent):
        super(Footers, self).__init__()
        self._sectPr = sectPr
        self._parent = parent

    def __getitem__(self, key):
        return Footer(self._sectPr, self._parent, self._sectPr.get_footerReference_of_type(key))

    def __iter__(self):
        for _type in Footers.enum_list:
            footer_ref = self._sectPr.get_footerReference_of_type(_type)
            yield Footer(self._sectPr, self._parent, footer_ref)

    def __len__(self):
        return len(Footers.enum_list)


class HeaderFooterBody(BlockItemContainer):
    """
    The rich-text body of a header or footer. Supports the same rich text
    operations as a document, such as paragraphs and tables.
    """
