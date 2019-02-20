#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from {{cookiecutter.repo_name}}.app import {{cookiecutter.project_name|replace(' ', '')}}App


class Test{{cookiecutter.project_name|replace(' ', '')}}App(unittest.TestCase):
    """TestCase for {{cookiecutter.project_name|replace(' ', '')}}App.
    """
    def setUp(self):
        self.app = {{cookiecutter.project_name|replace(' ', '')}}App()

    def test_name(self):
        self.assertEqual(self.app.name, '{{cookiecutter.repo_name}}')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
