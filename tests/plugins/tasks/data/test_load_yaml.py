import os
import sys


from brigade.plugins.tasks import data


from yaml.scanner import ScannerError


data_dir = "{}/test_data".format(os.path.dirname(os.path.realpath(__file__)))


class Test(object):

    def test_load_yaml(self, brigade):
        test_file = "{}/simple.yaml".format(data_dir)
        result = brigade.run(data.load_yaml, file=test_file)

        for h, r in result.items():
            d = r.result
            assert d["env"] == "test"
            assert d["services"] == ["dhcp", "dns"]

    def test_load_yaml_error_broken_file(self, brigade):
        test_file = "{}/broken.yaml".format(data_dir)
        results = brigade.run(data.load_yaml, file=test_file)
        processed = False
        for result in results.values():
            processed = True
            assert isinstance(result.exception, ScannerError)
        assert processed
        brigade.data.reset_failed_hosts()

    def test_load_yaml_error_missing_file(self, brigade):
        test_file = "{}/missing.yaml".format(data_dir)

        if sys.version_info.major == 2:
            not_found = IOError
        else:
            not_found = FileNotFoundError  # noqa

        results = brigade.run(data.load_yaml, file=test_file)
        processed = False
        for result in results.values():
            processed = True
            assert isinstance(result.exception, not_found)
        assert processed
        brigade.data.reset_failed_hosts()
