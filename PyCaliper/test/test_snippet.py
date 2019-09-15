import unittest

from PyCaliper.uom.localizer import Localizer
import os

class TestPrefix(unittest.TestCase):

    def test_prefix(self):
        cwd = os.getcwd()
        TRANSLATION_ROOT = os.path.join(cwd, "locales")
        print(TRANSLATION_ROOT)
        print(Localizer.instance().langStr("m.name"))