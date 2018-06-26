from unittest import TestCase
from micro.core.cli import CLI


class TestCLI(TestCase):
    def setUp(self):
        self.values = [
            "/path/to/plugins",
            "url://user:pass@1234//",
            "queue name",
            "/path/to/configfile",
            "example_hostname",
            5,
            "ERROR",
            "/path/to/logs",
            "INFO",
            "/path/to/celery/logs",
            "/path/to/celery/pids"
        ]
        self.cli = CLI()
        self.args = self.cli.parse_args([
            "-p", self.values[0],
            "-b", self.values[1],
            "-q", self.values[2],
            "-c", self.values[3],
            "-H", self.values[4],
            "-w", str(self.values[5]),
            "-ll", self.values[6],
            "-lp", self.values[7],
            "-cll", self.values[8],
            "-clp", self.values[9],
            "-cpp", self.values[10],
            "--default-params",
            "--version"
        ])

    def test_types(self):
        self.assertEqual(type(self.args.plugin_path), str)
        self.assertEqual(type(self.args.broker_url), str)
        self.assertEqual(type(self.args.queue_name), str)
        self.assertEqual(type(self.args.config_file), str)
        self.assertEqual(type(self.args.hostname), str)
        self.assertEqual(type(self.args.num_workers), int)
        self.assertEqual(type(self.args.log_level), str)
        self.assertEqual(type(self.args.log_path), str)
        self.assertEqual(type(self.args.celery_log_level), str)
        self.assertEqual(type(self.args.celery_log_path), str)
        self.assertEqual(type(self.args.celery_pid_path), str)
        self.assertEqual(type(self.args.default_params), bool)
        self.assertEqual(type(self.args.version), bool)

    def test_arguments(self):
        self.assertEqual(self.args.plugin_path, self.values[0])
        self.assertEqual(self.args.broker_url, self.values[1])
        self.assertEqual(self.args.queue_name, self.values[2])
        self.assertEqual(self.args.config_file, self.values[3])
        self.assertEqual(self.args.hostname, self.values[4])
        self.assertEqual(self.args.num_workers, self.values[5])
        self.assertEqual(self.args.log_level, self.values[6])
        self.assertEqual(self.args.log_path, self.values[7])
        self.assertEqual(self.args.celery_log_level, self.values[8])
        self.assertEqual(self.args.celery_log_path, self.values[9])
        self.assertEqual(self.args.celery_pid_path, self.values[10])
        self.assertTrue(self.args.default_params)
        self.assertTrue(self.args.version)

    def test_defaul_params_arg(self):
        args = self.cli.parse_args(["-w", "3"])
        self.assertFalse(args.default_params)
        self.assertFalse(args.version)
