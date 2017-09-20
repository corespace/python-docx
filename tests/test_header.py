# encoding: utf-8

"""
Test suite for the docx.header module
"""

from __future__ import (
    absolute_import, print_function, unicode_literals, division
)

import pytest

from docx.oxml.section import CT_SectPr
from docx.enum.header import WD_HEADER_FOOTER
from docx.header import _BaseHeaderFooter, Header, HeaderFooterBody, Footers, Footer
from docx.parts.document import DocumentPart
from docx.parts.header import HeaderPart

from .unitutil.cxml import element
from .unitutil.mock import call, instance_mock, method_mock, property_mock


class Describe_BaseHeaderFooter(object):

    def it_knows_whether_it_is_linked_to_previous(self, is_linked_fixture):
        header, expected_value = is_linked_fixture
        assert header.is_linked_to_previous is expected_value

    def it_provides_access_to_its_body(self, body_fixture):
        header, calls, expected_value = body_fixture
        body = header.body
        assert header.part.related_hdrftr_body.call_args_list == calls
        assert body == expected_value

    def it_provides_access_to_the_related_hdrftr_body(self, hdrftr_fixture):
        document_part, header_part_ = hdrftr_fixture
        rId = 'rId1'
        body = document_part.related_hdrftr_body(rId)
        assert body == header_part_.body

    def it_can_be_enumerated(self, footers_fixture):
        assert len(WD_HEADER_FOOTER.__members__) == len(footers_fixture)
        for footer in footers_fixture:
            assert isinstance(footer, Footer)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def footers_fixture(self, sect_pr_):
        return Footers(sect_pr_, None)

    @pytest.fixture
    def hdrftr_fixture(self, header_part_, body_, related_parts_prop_):
        header_part_.body = body_
        document_part = DocumentPart(None, None, None, None)
        related_parts_ = related_parts_prop_.return_value
        related_parts_.__getitem__.return_value.body = body_
        return document_part, header_part_

    @pytest.fixture
    def related_parts_prop_(self, request):
        return property_mock(request, DocumentPart, 'related_parts')

    @pytest.fixture(params=[
        ('w:sectPr',                                             None),
        ('w:sectPr/w:headerReference{w:type=even,r:id=rId6}',    None),
        ('w:sectPr/w:headerReference{w:type=default,r:id=rId8}', 'rId8'),
    ])
    def body_fixture(self, request, body_, part_prop_, document_part_):
        sectPr_cxml, rId = request.param
        sectPr = element(sectPr_cxml)
        if sectPr:
            header = Header(sectPr, None, sectPr.get_headerReference_of_type(WD_HEADER_FOOTER.PRIMARY))
        else:
            header = Header(sectPr, None, None)
        calls, expected_value = ([call(rId)], body_) if rId else ([], None)
        document_part_.related_hdrftr_body.return_value = body_
        return header, calls, expected_value

    @pytest.fixture(params=[
        ('w:sectPr',                                   True),
        ('w:sectPr/w:headerReference{w:type=default}', False),
        ('w:sectPr/w:headerReference{w:type=even}',    True),
    ])
    def is_linked_fixture(self, request):
        sectPr_cxml, expected_value = request.param
        sectPr = element(sectPr_cxml)
        if sectPr:
            header = Header(sectPr, None, sectPr.get_headerReference_of_type(WD_HEADER_FOOTER.PRIMARY))
        else:
            header = Header(sectPr, None, None)
        return header, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def sect_pr_(self, request):
        return instance_mock(request, CT_SectPr)

    @pytest.fixture
    def body_(self, request):
        return instance_mock(request, HeaderFooterBody)

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def header_part_(self, request):
        return instance_mock(request, HeaderPart)

    @pytest.fixture
    def part_prop_(self, request, document_part_):
        return property_mock(
            request, _BaseHeaderFooter, 'part', return_value=document_part_
        )
