import importlib
import logging
import logging.config
import sys
import traceback
from multiprocessing.dummy import Pool

from brigade.core.configuration import Config
from brigade.core.task import AggregatedResult, Result, Task
from brigade.plugins.tasks import connections


if sys.version_info.major == 2:
    import copy_reg
    import types

    # multithreading requires objects passed around to be pickable
    # following methods allow py2 to know how to pickle methods
    def _pickle_method(method):
        func_name = method.im_func.__name__
        obj = method.im_self
        cls = method.im_class
        return _unpickle_method, (func_name, obj, cls)

    def _unpickle_method(func_name, obj, cls):
        for cls in cls.mro():
            try:
                func = cls.__dict__[func_name]
            except KeyError:
                pass
            else:
                break
        return func.__get__(obj, cls)

    copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)


class Data(object):
    """
    This class is just a placeholder to share data amongsts different
    versions of Brigade  after running ``filter`` multiple times.

    Attributes:
        failed_hosts (list): Hosts that have failed to run a task properly
    """

    def __init__(self):
        self.failed_hosts = set()


class Brigade(object):
    """
    This is the main object to work with. It contains the inventory and it serves
    as task dispatcher.

    Arguments:
        inventory (:obj:`brigade.core.inventory.Inventory`): Inventory to work with
        data(:obj:`brigade.core.Data`): shared data amongst different iterations of brigade
        dry_run(``bool``): Whether if we are testing the changes or not
        config (:obj:`brigade.core.configuration.Config`): Configuration object
        config_file (``str``): Path to Yaml configuration file
        available_connections (``dict``): dict of connection types that will be made available.
            Defaults to :obj:`brigade.plugins.tasks.connections.available_connections`

    Attributes:
        inventory (:obj:`brigade.core.inventory.Inventory`): Inventory to work with
        data(:obj:`brigade.core.Data`): shared data amongst different iterations of brigade
        dry_run(``bool``): Whether if we are testing the changes or not
        config (:obj:`brigade.core.configuration.Config`): Configuration parameters
        available_connections (``dict``): dict of connection types are available
    """

    def __init__(self, inventory, dry_run, config=None, config_file=None,
                 available_connections=None, logger=None, data=None):
        self.logger = logger or logging.getLogger("brigade")

        self.data = data or Data()
        self.inventory = inventory
        self.inventory.brigade = self

        self.dry_run = dry_run
        if config_file:
            self.config = Config(config_file=config_file)
        else:
            self.config = config or Config()

        self.configure_logging()

        if available_connections is not None:
            self.available_connections = available_connections
        else:
            self.available_connections = connections.available_connections

    def configure_logging(self):
        dictConfig = self.config.logging_dictConfig or {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {"format": self.config.logging_format}
            },
            "handlers": {},
            "loggers": {},
            "root": {
                "level": "CRITICAL" if self.config.logging_loggers else
                         self.config.logging_level.upper(),
                "handlers": [],
                "formatter": "simple",
            }
        }
        handlers_list = []
        if self.config.logging_file:
            dictConfig["root"]["handlers"].append('info_file_handler')
            handlers_list.append('info_file_handler')
            dictConfig["handlers"]["info_file_handler"] = {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "NOTSET",
                "formatter": "simple",
                "filename": self.config.logging_file,
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            }
        if self.config.logging_to_console:
            dictConfig["root"]["handlers"].append('info_console')
            handlers_list.append('info_console')
            dictConfig["handlers"]["info_console"] = {
                "class": "logging.StreamHandler",
                "level": "NOTSET",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            }

        for logger in self.config.logging_loggers:
            dictConfig["loggers"][logger] = {
                "level": self.config.logging_level.upper(),
                "handlers": handlers_list,
            }

        if dictConfig["root"]["handlers"]:
            logging.config.dictConfig(dictConfig)

    def filter(self, **kwargs):
        """
        See :py:meth:`brigade.core.inventory.Inventory.filter`

        Returns:
            :obj:`Brigade`: A new object with same configuration as ``self`` but filtered inventory.
        """
        b = Brigade(**self.__dict__)
        b.inventory = self.inventory.filter(**kwargs)
        return b

    def _run_serial(self, task, dry_run, **kwargs):
        result = AggregatedResult(kwargs.get("name") or task.__name__)
        for host in self.inventory.hosts.values():
            result[host.name] = run_task(host, self, dry_run, Task(task, **kwargs))
        return result

    def _run_parallel(self, task, num_workers, dry_run, **kwargs):
        result = AggregatedResult(kwargs.get("name") or task.__name__)

        pool = Pool(processes=num_workers)
        result_pool = [pool.apply_async(run_task,
                                        args=(h, self, dry_run, Task(task, **kwargs)))
                       for h in self.inventory.hosts.values()]
        pool.close()
        pool.join()

        for rp in result_pool:
            r = rp.get()
            result[r.host.name] = r
        return result

    def run(self, task, num_workers=None, dry_run=None, raise_on_error=None, **kwargs):
        """
        Run task over all the hosts in the inventory.

        Arguments:
            task (``callable``): function or callable that will be run against each device in
              the inventory
            num_workers(``int``): Override for how many hosts to run in paralell for this task
            dry_run(``bool``): Whether if we are testing the changes or not
            raise_on_error (``bool``): Override raise_on_error behavior
            **kwargs: additional argument to pass to ``task`` when calling it

        Raises:
            :obj:`brigade.core.exceptions.BrigadeExecutionError`: if at least a task fails
              and self.config.raise_on_error is set to ``True``

        Returns:
            :obj:`brigade.core.task.AggregatedResult`: results of each execution
        """
        num_workers = num_workers or self.config.num_workers

        self.logger.info("Running task '{}' with num_workers: {}, dry_run: {}".format(
            kwargs.get("name") or task.__name__, num_workers, dry_run))
        self.logger.debug(kwargs)

        if num_workers == 1:
            result = self._run_serial(task, dry_run, **kwargs)
        else:
            result = self._run_parallel(task, num_workers, dry_run, **kwargs)

        raise_on_error = raise_on_error if raise_on_error is not None else \
            self.config.raise_on_error
        if raise_on_error:
            result.raise_on_error()
        else:
            self.data.failed_hosts.update(result.failed_hosts.keys())
        return result


def run_task(host, brigade, dry_run, task):
    logger = logging.getLogger("brigade")
    try:
        logger.info("{}: {}: running task".format(host.name, task.name))
        r = task._start(host=host, brigade=brigade, dry_run=dry_run)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error("{}: {}".format(host, tb))
        r = Result(host, exception=e, result=tb, failed=True)
        task.results.append(r)
        r.name = task.name
    return task.results


def InitBrigade(config_file="", dry_run=False, **kwargs):
    """
    Arguments:
        config_file(str): Path to the configuration file (optional)
        dry_run(bool): Whether to simulate changes or not
        **kwargs: Extra information to pass to the
            :obj:`brigade.core.configuration.Config` object

    Returns:
        :obj:`brigade.core.Brigade`: fully instantiated and configured
    """
    conf = Config(config_file=config_file, **kwargs)

    module_path = ".".join(conf.inventory.split(".")[:-1])
    inv_class_name = conf.inventory.split(".")[-1]
    module = importlib.import_module(module_path)
    inv_class = getattr(module, inv_class_name)

    mapping = getattr(conf, inv_class_name, {})
    inv_class_args = mapping.update({'transform_function': conf.transform_function})
    inv = inv_class(**inv_class_args)

    return Brigade(
        inventory=inv,
        dry_run=dry_run,
        config=conf,
    )
