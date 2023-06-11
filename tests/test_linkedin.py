from src.parsers.linkedin.linkedin_parser import LinkedinParser
from src.utils import upload_results


def test_linkedin_parser():
    results = LinkedinParser().parse()
    upload_results(results)
