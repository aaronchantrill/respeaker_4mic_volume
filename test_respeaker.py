# -*- coding: utf-8 -*-
import unittest
from naomi import testutils
from .respeaker import RespeakerVisualizationsPlugin


class TestRespeakerVisualizationsPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = testutils.get_plugin_instance(RespeakerVisualizationsPlugin)
