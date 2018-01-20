import os
import unittest

from core.inc import simens_dadm as smns
from core.inc import module_XX

# Data location in ROOT
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '\\Data\\Module_XX_test\\'


class ModuleXXTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Called once during test class initialization.
        Basically, you should place here your demo code (data loading). You should run your module in test methods.
        """
        pass

    def tearDown(self):
        """
        Called after each testing method.
        Might be necessary if your module modifies object in place.
        """
        pass


    def test_name_should_be_very_descriptive(self):
        """
        The actual test method. Your code should end with one of the following:

        self.assertTrue(expression)
        self.assertFalse(expression)

        self.assertEqual(value1, value2)
        self.assertNotEqual(value1, value2)

        If your module raises errors during execution:
        self.assertRaises(ErrorType, callable, arg1, arg2, ...)
        - where callable is a function, method or class constructor and arg1, arg2, ... are parameters passed to callable.

        If your module throws warnings during execution:
        self.assertWarns(WarningType, callable, arg1, arg2, ...)
        - syntax same as above
        """
        pass


if __name__ == '__main__':
    unittest.main()
