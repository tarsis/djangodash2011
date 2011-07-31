import os
from django.conf import settings
from django.utils import unittest

from project.models import Project
from project.analyzer import BaseAnalyzer, CoverageAnalyzer, ClonneDiggerAnalyzer, PyLintAnalyzer, PEP8Analyzer

class BaseAnalyzerTestCase(unittest.TestCase):
    def setUp(self):
        self.project = Project.objects.create(url="media/sources/fake-github.tar.gz")
        self.analyzer = BaseAnalyzer(self.project)

    def tearDown(self):
        self.project.delete()

    def test_base_analyzer_get_project_modules_should_return_a_list_of_all_python_module_inside_its(self):
        python_modules = self.analyzer.get_project_modules()

        self.assertEquals(python_modules, ['apps', 'site_media', 'templates'])
        self.analyzer._remove_extracted_code()

    def test_base_analyzer_analyze_should_raises_not_implemented_error(self):
        self.assertRaises(NotImplementedError, self.analyzer.analyze)

class CoverageAnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.project = Project.objects.create(url="media/sources/fake-github.tar.gz")
        self.analyzer = CoverageAnalyzer(self.project)

    @unittest.skip
    def test_get_coverage_from_project(self):
        coverage = self.analyzer.analyze()
        self.assertEquals(17, coverage)

class ClonneDiggerTest(unittest.TestCase):
    def test_get_clonnedigger_report_from_project(self):
        project = Project.objects.create(url="media/sources/fake-github.tar.gz")
        analyzer = ClonneDiggerAnalyzer(project)

        self.assertAlmostEquals(19.24, analyzer.analyze())

class PyLintAnalyzerTestCase(unittest.TestCase):
    def setUp(self):
        self.project = Project.objects.create(url="media/sources/fake-github.tar.gz")
        self.pylint_analyzer = PyLintAnalyzer(self.project)

    def tearDown(self):
        self.project.delete()

    def test_py_lint_should_get_correct_config_file_when_instantiate(self):
        import ipdb;ipdb.set_trace()
        self.assertEquals(
            self.pylint_analyzer.config_file_path,
            os.path.join(settings.ANALYZERS_CONFIGURATION_DIR,'pylint.cfg')
        )

class PEP8Test(unittest.TestCase):
    def test_get_pep8_report_from_project(self):
        project = Project.objects.create(url="media/sources/fake-github.tar.gz")
        pep8_analyzer = PEP8Analyzer(project)

        self.assertTrue(0, pep8_analyzer.analyze())
