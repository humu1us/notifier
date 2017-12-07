import os
from celery import Celery
from .config import Config


class NotifierApp(Celery):
    def __init__(self):
        config = Config()
        super().__init__("Notifier",
                         broker=config.key("broker_url"),
                         backend="rpc://")

        self.__namespace = "Notifier"
        self.__queue = config.key("queue_name")
        self.__plugin_path = config.key("plugin_path")
        self.__log_from = config.key("log_from")
        self.__log_path = config.key("log_path")
        self.__pid_path = config.key("pid_path")
        self.__hostname = config.key("hostname")
        self.__workers = config.key("num_workers")

    def plugin_path(self):
        return self.__plugin_path

    def queue(self):
        return self.__queue

    def function_name(self, name):
        return self.__namespace + "." + name

    def __load_args(self):
        log_path = os.path.join(self.__log_path, "%N.log")
        pid_path = os.path.join(self.__pid_path, "%N.pid")

        args = ["celery",
                "-A", "notifier.api.celery.endpoints",
                "-Q", self.__queue,
                "-l", self.__log_from,
                "--logfile=" + log_path,
                "--pidfile=" + pid_path,
                "multi", "start"]
        workers = self.__create_workers()
        return args + workers

    def __create_workers(self):
        workers = []
        worker_name = "worker{num}@{hostname}"

        for i in range(self.__workers):
            workers.append(worker_name.format(num=(i + 1),
                                              hostname=self.__hostname))

        return workers

    def start_app(self):
        self.start(self.__load_args())
