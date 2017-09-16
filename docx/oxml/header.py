from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from . import parse_xml
from .ns import nsdecls
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, OneOrMore, OptionalAttribute,
    RequiredAttribute, ZeroOrOne, ZeroOrMore
)

class CT_HeaderFooter(BaseOxmlElement):
    """
    ``<w:hdr>`` header element
    """
    p = OneOrMore('w:p')

    @classmethod
    def new(cls):
        """
        Return a new ``<w:hdr>`` element, containing an empty paragraph as the
        required EG_BlockLevelElt.
        """
        return parse_xml(
            '<w:hdr %s>\n'
            '  <w:p/>\n'
            '</w:hdr>' % nsdecls('w')
        )


