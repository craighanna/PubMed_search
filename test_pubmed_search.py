"""pytests for hello.py"""
import pubmed_search
import xml.etree.ElementTree as ET
import pytest

# import requests


@pytest.fixture(name="my_tree")
def fixture_my_tree():
    # url = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:156895&metadataPrefix=pmc"
    # response = requests.get(url, timeout=10)
    # with open('test.xml','w') as f:
    #    f.write(response.text)
    local_tree = ET.parse("test.xml")
    yield local_tree


class TestPubmedSearch:
    def test_parse_xml(self, my_tree):
        """test parse_xml"""
        output = pubmed_search.parse_xml(my_tree)
        assert len(output) == 1
        assert output[0][0].startswith("Wnt/Wingless signaling through")
        assert output[0][1] == "12729465"
        assert output[0][2] == "https://pubmed.ncbi.nlm.nih.gov/12729465/#abstract"
        assert output[0][3].startswith(
            "\n        \n          Background\n          Wnt/Wingless (Wg) signals are transduced"
        )
        assert output[0][3].endswith("genes through Dishevelled.\n        \n      ")

    def test_get_url(self):
        """test get_url method"""
        config = pubmed_search.Config("pmc", "2021-01-01", "2021-02-01", "bmj", None)
        out_url = pubmed_search.get_url(config)
        assert (
            out_url
            == "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=ListRecords&from=2021-01-01&until=2021-02-01&metadataPrefix=pmc&set=bmj"
        )
