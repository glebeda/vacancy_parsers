from src.parsers.dou.dou_rss_parser import DouRssParser
from src.utils import upload_results


def test_dou_rss_parser():
    results = DouRssParser().parse()
    upload_results(results)
