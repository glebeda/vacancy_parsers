from src.parsers.epam.epam_parser import EpamParser
from src.utils import upload_results


def test_epam_parser():
    results = EpamParser().parse()
    upload_results(results)
