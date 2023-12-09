"""Command-line interface for searching the PubMed database for abstracts"""
import argparse
import requests
import xml.etree.ElementTree as ET
import csv


class Config:
    """Configuration for search_pubmed commandline module"""

    def __init__(
        self,
        metadata_prefix: str,
        from_dt: str,
        until_dt: str,
        set_str: str,
        out_csv: str,
    ):
        """constructor"""
        self.metadata_prefix = metadata_prefix
        self.from_dt = from_dt
        self.until_dt = until_dt
        self.set_str = set_str
        self.out_csv = out_csv


def get_url(config) -> str:
    """given command-line arguments for metadata-prefix, from-dt, until-dt, set, generate query URL"""

    base_url = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=ListRecords"
    metadata_prefix = from_dt = until_dt = set_str = ""
    if config.metadata_prefix:
        metadata_prefix = f"&metadataPrefix={config.metadata_prefix}"
    if config.from_dt:
        from_dt = f"&from={config.from_dt}"
    if config.until_dt:
        until_dt = f"&until={config.until_dt}"
    if config.set_str:
        set_str = f"&set={config.set_str}"
    url = f"{base_url}{from_dt}{until_dt}{metadata_prefix}{set_str}"
    return url


def parse_xml(tree) -> list:
    """Parse PubMed XML file into a list"""

    csv_rows = []
    for article_meta in tree.iterfind(".//{*}article-meta"):
        title = pmid = abstract = article_url = ""

        title_element = article_meta.find("./{*}title-group/{*}article-title")
        if title_element != None:
            title = title_element.text.replace("\t", " ")

        article_ids = article_meta.findall("./{*}article-id")
        for aid in article_ids:
            if aid.attrib["pub-id-type"] == "pmid":
                pmid = aid.text

        abstract_element = article_meta.find("./{*}abstract")
        if abstract_element is not None:
            abstract = "".join(abstract_element.itertext())

        article_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/#abstract"

        csv_rows.append([title, pmid, article_url, abstract])

    return csv_rows


def write(csv_rows: list, field_names: list, config) -> None:
    """write extracted fields to file or stdout"""

    if config.out_csv:
        with open(config.out_csv, "w", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter="\t")
            csvwriter.writerow(field_names)
            for row in csv_rows:
                csvwriter.writerow(row[:3])
    else:
        for row in csv_rows:
            print("*" * 80)
            print(f"Title: {row[0]}")
            print(f"PMID: {row[1]}")
            print(f"Abstract: {row[3]}")


def run(config) -> None:
    """run main search_pubmed method"""

    url = get_url(config)
    response = requests.get(url, timeout=10)
    tree = ET.fromstring(response.text)
    field_names = ["title", "pmid", "url"]
    csv_rows = parse_xml(tree)
    write(csv_rows, field_names, config.out_csv)
    # tree = ET.parse('txt.xml')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="search_pubmed",
        description="Command-line interface for searching the PubMed database for abstracts",
    )
    parser.add_argument("-o", "--out_csv")  # store in CSV file
    parser.add_argument("-m", "--metadata_prefix")
    parser.add_argument("-f", "--from_dt")
    parser.add_argument("-u", "--until_dt")
    parser.add_argument("-s", "--set_str")
    args = parser.parse_args()

    cfg = Config(
        args.metadata_prefix, args.from_dt, args.until_dt, args.set_str, args.out_csv
    )
    run(cfg)
