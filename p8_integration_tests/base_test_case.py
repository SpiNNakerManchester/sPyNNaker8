from lxml import etree
import os
import random
import sys
import unittest
from unittest import SkipTest
import spinn_utilities.conf_loader as conf_loader
from spalloc.job import JobDestroyedError
from spinn_front_end_common.utilities import globals_variables

p8_integration_factor = float(os.environ.get('P8_INTEGRATION_FACTOR', "1"))
random.seed(os.environ.get('P8_INTEGRATION_SEED', None))


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        # Remove random effect for testing
        # Set test_seed to None to allow random
        self._test_seed = 1

        factor = random.random()
        if factor > p8_integration_factor:
            raise SkipTest("Test skipped by random number {} above "
                           "P8_INTEGRATION_FACTOR {}".format(
                               factor, p8_integration_factor))

        globals_variables.unset_simulator()
        class_file = sys.modules[self.__module__].__file__
        path = os.path.dirname(os.path.abspath(class_file))
        os.chdir(path)

    def assert_logs_messages(
            self, log_records, sub_message, log_level='ERROR', count=1,
            allow_more=False):
        """ Tool to assert the log messages contain the sub-message

        :param log_records: list of log message
        :param sub_message: text to look for
        :param log_level: level to look for
        :param count: number of times this message should be found
        :param allow_more: If True, OK to have more than count repeats
        :return: None
        """
        seen = 0
        for record in log_records:
            if record.levelname == log_level and \
                    sub_message in str(record.msg):
                seen += 1
        if allow_more and seen > count:
            return
        if seen != count:
            raise self.failureException(
                "\"{}\" not found in any {} logs {} times, was found {} "
                "times".format(sub_message, log_level, count, seen))

    def assert_not_spin_three(self):
        config = conf_loader.load_config(
            filename="spynnaker.cfg", defaults=[])
        if config.has_option("Machine", "version"):
            version = config.get("Machine", "version")
            if version in ["2", "3"]:
                raise SkipTest(
                    "This test will not run on a spin {} board".format(
                        version))

    def report(self, message, file_name):
        if not message.endswith("\n"):
            message += "\n"
        p8_integration_tests_directory = os.path.dirname(__file__)
        test_dir = os.path.dirname(p8_integration_tests_directory)
        report_dir = os.path.join(test_dir, "reports")
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        report_path = os.path.join(report_dir, file_name)
        with open(report_path, "a") as report_file:
            report_file.write(message)

    def get_provenance(self, main_name, detail_name):
        provenance_file_path = globals_variables.get_simulator() \
            ._provenance_file_path
        xml_path = os.path.join(provenance_file_path, "pacman.xml")
        xml_root = etree.parse(xml_path)
        results = []
        for element in xml_root.findall("provenance_data_items"):
            if main_name in element.get('name'):
                for sub_element in element.findall("provenance_data_item"):
                    if detail_name in sub_element.get('name'):
                        results.append(sub_element.get('name'))
                        results.append(": ")
                        results.append(sub_element.text)
                        results.append("\n")
        return "".join(results)

    def get_provenance_files(self):
        provenance_file_path = globals_variables.get_simulator() \
            ._provenance_file_path
        return os.listdir(provenance_file_path)

    def get_run_time_of_BufferExtractor(self):
        return self.get_provenance("Execution", "BufferExtractor")

    def known_issue(self, issue):
        self.report(issue, "Skipped_due_to_issue")
        raise SkipTest(issue)

    def destory_path(self):
        p8_integration_tests_directory = os.path.dirname(__file__)
        test_dir = os.path.dirname(p8_integration_tests_directory)
        return os.path.join(test_dir, "JobDestroyedError.txt")

    def runsafe(self, method):
        retries = 0
        lastError = None
        while retries < 3:
            try:
                method()
                return
            except JobDestroyedError as ex:
                class_file = sys.modules[self.__module__].__file__
                with open(self.destory_path(), "a") as destroyed_file:
                    destroyed_file.write(class_file)
                    destroyed_file.write("\n")
                    destroyed_file.write(str(ex))
                    destroyed_file.write("\n")
                lastError = ex
                retries += 1
        raise lastError
