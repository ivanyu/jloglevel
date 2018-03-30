#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import unittest
from subprocess import call, check_output
from time import sleep
from click.testing import CliRunner
from jloglevel.cli import cli


class JLogLevelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        call(["docker", "build", "test/", "-t", "jloglevel-test-app"])
        cls._container_id = check_output([
              "docker", "run", "-d",
              "-p", "8778:8778",
              "jloglevel-test-app"
        ]).decode('utf-8').strip()
        sleep(3)

        cls._runner = CliRunner()

    @classmethod
    def tearDownClass(cls):
        call(["docker", "kill", cls._container_id])
        # call(["docker", "rmi", "jloglevel-test-app", "--force"])

    def test_list_loggers(self):
        result = self._runner.invoke(cli,
            ['list-loggers', '-h', 'localhost:8778'])
        self.assertEqual(result.exit_code, 0)
        lines = self._get_clean_lines_of_output(result.output)
        self.assertSequenceEqual(lines,
          ["http://localhost:8778/",
           "ROOT",
           "me",
           "me.ivanyu",
           "me.ivanyu.App"])

    def test_get_default(self):
        result = self._runner.invoke(cli,
            ['get', '-h', 'localhost:8778'])
        self.assertEqual(result.exit_code, 0)
        lines = self._get_clean_lines_of_output(result.output)
        self.assertSequenceEqual(lines,
          ["Logger ROOT",
           "http://localhost:8778/ DEBUG"])

    def test_get_root(self):
        result = self._runner.invoke(cli,
            ['get', '-h', 'localhost:8778', '--logger', 'ROOT'])
        self.assertEqual(result.exit_code, 0)
        lines = self._get_clean_lines_of_output(result.output)
        self.assertSequenceEqual(lines,
          ["Logger ROOT",
           "http://localhost:8778/ DEBUG"])

    def test_get_me_ivanyu_app(self):
        result = self._runner.invoke(cli,
            ['get', '-h', 'localhost:8778', '--logger', 'me.ivanyu.App'])
        self.assertEqual(result.exit_code, 0)
        lines = self._get_clean_lines_of_output(result.output)
        self.assertSequenceEqual(lines,
          ["Logger me.ivanyu.App",
           "http://localhost:8778/ --"])

    def test_set_default(self):
        result = self._runner.invoke(cli,
            ['set', 'ERROR', '-h', 'localhost:8778'])
        self.assertEqual(result.exit_code, 0)

        result = self._runner.invoke(cli,
            ['get', '-h', 'localhost:8778'])
        self.assertEqual(result.exit_code, 0)
        lines = self._get_clean_lines_of_output(result.output)
        self.assertSequenceEqual(lines,
          ["Logger ROOT",
           "http://localhost:8778/ ERROR"])

    def test_set_root(self):
        result = self._runner.invoke(cli,
            ['set', 'TRACE', '-h', 'localhost:8778', '--logger', 'ROOT'])
        self.assertEqual(result.exit_code, 0)

        result = self._runner.invoke(cli,
            ['get', '-h', 'localhost:8778', '--logger', 'ROOT'])
        self.assertEqual(result.exit_code, 0)
        lines = self._get_clean_lines_of_output(result.output)
        self.assertSequenceEqual(lines,
          ["Logger ROOT",
           "http://localhost:8778/ TRACE"])

    def test_set_me_ivanyu_app(self):
        result = self._runner.invoke(cli,
            ['set', 'WARN', '-h', 'localhost:8778',
             '--logger', 'me.ivanyu.App'])
        self.assertEqual(result.exit_code, 0)

        result = self._runner.invoke(cli,
            ['get', '-h', 'localhost:8778', '--logger', 'me.ivanyu.App'])
        self.assertEqual(result.exit_code, 0)
        lines = self._get_clean_lines_of_output(result.output)
        self.assertSequenceEqual(lines,
          ["Logger me.ivanyu.App",
           "http://localhost:8778/ WARN"])

    def _get_clean_lines_of_output(self, output):
        return [re.sub(r'\s+', ' ', l.strip()) for l in output.splitlines()]


if __name__ == '__main__':
    unittest.main()
