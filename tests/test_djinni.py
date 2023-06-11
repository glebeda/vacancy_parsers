from src.parsers.djinni.djinni_parser import DjinniParser
from src.utils import upload_results


def test_djinni_parser():
    results = DjinniParser().parse()
    upload_results(results)