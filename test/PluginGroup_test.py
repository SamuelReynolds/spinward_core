import unittest

from spinward.core.PluginGroup import PluginGroup


class PluginGroup1(metaclass=PluginGroup):
    """Single-level plugin group -- no intermediate virtual class(es)"""


class P1_1(PluginGroup1):
    _PLUGIN_NAME = 'P1_1'


class P1_2(PluginGroup1):
    _PLUGIN_NAME = 'P1_2'


class P1_3(PluginGroup1):
    _PLUGIN_NAME = 'P1_3'


class PluginGroup2(metaclass=PluginGroup):
    """Virtual-base PluginGroup"""
    _VIRTUAL_BASE = True

# class P2vb(PluginGroup2):
#     _PLUGIN_NAME = 'P2vb'


class P2_1v(PluginGroup2):
    _PLUGIN_NAME = 'P2_1v'


class P2_1(P2_1v):
    _PLUGIN_NAME = 'P2_1'
    _VIRTUAL_BASE = False


class P2_2(PluginGroup2):
    _PLUGIN_NAME = 'P2_2'
    _VIRTUAL_BASE = False


class P2_3(PluginGroup2):
    _PLUGIN_NAME = 'P2_3'
    _VIRTUAL_BASE = False


class PluginGroupTest(unittest.TestCase):

    def setUp(self):
        pass


    def test_get_plugin_names(self):
        group = PluginGroup1
        expected = 'P1_1 P1_2 P1_3'.split()
        actual = group.get_plugin_names()
        self.assertEquals(actual, expected)


    def test_get_plugin_names_vb(self):
        group = PluginGroup2
        expected = 'P2_1 P2_2 P2_3'.split()
        actual = group.get_plugin_names()
        self.assertEquals(actual, expected)


    def test_get_plugin_classes(self):
        group = PluginGroup1
        expected = [P1_1, P1_2, P1_3]
        actual = group.get_plugin_classes()
        self.assertEquals(actual, expected)


    def test_get_plugin_classes_vb(self):
        group = PluginGroup2
        expected = [P2_1, P2_2, P2_3]
        actual = group.get_plugin_classes()
        self.assertEquals(actual, expected)


    def test_get_plugins(self):
        group = PluginGroup1
        expected_classes = [P1_1, P1_2, P1_3]
        expected_names = [c._PLUGIN_NAME for c in expected_classes]
        actual = group.get_plugins()
        actual_names = [p._PLUGIN_NAME for p in actual]
        # print("expected_classes:", expected_classes)
        print("actual:", actual)
        # print("actual_classes:", actual_classes)
        print("expected_names:", expected_names)
        print("actual_names:", actual_names)
        self.assertEquals(actual_names, expected_names)


    def test_get_plugins_vb(self):
        group = PluginGroup2
        expected_classes = [P2_1, P2_2, P2_3]
        expected_names = [c._PLUGIN_NAME for c in expected_classes]
        actual = group.get_plugin_classes()
        actual_names = [p._PLUGIN_NAME for p in actual]
        # print("expected_classes:", expected_classes)
        print("actual:", actual)
        # print("actual_classes:", actual_classes)
        print("expected_names:", expected_names)
        print("actual_names:", actual_names)
        self.assertEquals(actual_names, expected_names)


    def test_get_plugin_by_name(self):
        group = PluginGroup1
        expected_class = P1_2
        expected_name = "P1_2"
        actual = group.get_plugin_by_name(expected_name)
        actual_name = actual._PLUGIN_NAME
        # print("expected_classes:", expected_classes)
        print("actual:", actual)
        # print("actual_classes:", actual_classes)
        print("expected_name:", expected_name)
        print("actual_name:", actual_name)
        self.assertEquals(actual.__class__, expected_class)
        self.assertEquals(actual_name, expected_name)


    def test_get_plugin_by_name_vb(self):
        group = PluginGroup2
        expected_class = P2_2
        expected_name = "P2_2"
        actual = group.get_plugin_by_name(expected_name)
        actual_name = actual._PLUGIN_NAME
        # print("expected_classes:", expected_classes)
        print("actual:", actual)
        # print("actual_classes:", actual_classes)
        print("expected_name:", expected_name)
        print("actual_name:", actual_name)
        self.assertEquals(actual.__class__, expected_class)
        self.assertEquals(actual_name, expected_name)


    def test_get_plugin_class_by_name(self):
        group = PluginGroup1
        expected = P1_2
        expected_name = "P1_2"
        actual = group.get_plugin_class_by_name(expected_name)
        # actual_name = actual._PLUGIN_NAME
        # print("expected_classes:", expected_classes)
        # print("actual:", actual)
        # print("actual_classes:", actual_classes)
        # print("expected_name:", expected_name)
        # print("actual_name:", actual_name)
        self.assertEquals(actual, expected)


if __name__ == '__main__':
    unittest.main()
