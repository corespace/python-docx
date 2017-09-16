# encoding: utf-8

"""
|HeaderPart|, |FooterPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..header import HeaderFooterBody
from ..opc.part import XmlPart


class HeaderPart(XmlPart):
    @property
    def body(self):
        """
        A |HeaderFooterBody| proxy object for the `w:hdr` element in this part,
        """
        # TODO: how to access parent here? is it necessary? self?
        return HeaderFooterBody(self.element, None)


class FooterPart(XmlPart):
    @property
    def body(self):
        """
        A |HeaderFooterBody| proxy object for the `w:ftr` element in this part,
        """
        # TODO: how to access parent here? is it necessary? self?
        return HeaderFooterBody(self.element, None)
