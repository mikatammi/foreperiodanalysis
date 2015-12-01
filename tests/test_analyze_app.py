import unittest


class TestAnalyzeApp(unittest.TestCase):
    def test_import_app(self):
        """Compile and import code of application"""
        app_filename = 'bin/fpa'
        with open(app_filename) as f:
            code = compile(f.read(), app_filename, 'exec')
            exec(code)
