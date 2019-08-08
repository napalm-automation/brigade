import logging
import logging.config
from multiprocessing.dummy import Pool
from typing import List, Optional

from nornir.core.configuration import Config
from nornir.core.inventory import Host, Inventory
from nornir.core.processor import Processor, Processors
from nornir.core.state import GlobalState
from nornir.core.task import AggregatedResult, Task

logger = logging.getLogger(__name__)


class Nornir(object):
    """
    This is the main object to work with. It contains the inventory and it serves
    as task dispatcher.

    Arguments:
        inventory (:obj:`nornir.core.inventory.Inventory`): Inventory to work with
        data(GlobalState): shared data amongst different iterations of nornir
        dry_run(``bool``): Whether if we are testing the changes or not
        config (:obj:`nornir.core.configuration.Config`): Configuration object

    Attributes:
        inventory (:obj:`nornir.core.inventory.Inventory`): Inventory to work with
        data(:obj:`nornir.core.GlobalState`): shared data amongst different iterations of nornir
        dry_run(``bool``): Whether if we are testing the changes or not
        config (:obj:`nornir.core.configuration.Config`): Configuration parameters
    """

    def __init__(
        self,
        inventory: Inventory,
        config: Config = None,
        data: GlobalState = None,
        processors: Optional[Processors] = None,
    ) -> None:
        self.data = data if data is not None else GlobalState()
        self.inventory = inventory
        self.config = config or Config()
        self.processors = processors or Processors()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connections(on_good=True, on_failed=True)

    def with_processors(self, processors: List[Processor]) -> "Nornir":
        return Nornir(**{**self.__dict__, **{"processors": Processors(processors)}})

    def filter(self, *args, **kwargs):
        """
        See :py:meth:`nornir.core.inventory.Inventory.filter`

        Returns:
            :obj:`Nornir`: A new object with same configuration as ``self`` but filtered inventory.
        """
        b = Nornir(**self.__dict__)
        b.inventory = self.inventory.filter(*args, **kwargs)
        return b

    def _run_serial(self, task: Task, hosts, **kwargs):
        result = AggregatedResult(kwargs.get("name") or task.name)
        for host in hosts:
            result[host.name] = task_wrapper(task, host, self)
        return result

    def _run_parallel(self, task: Task, hosts, num_workers, **kwargs):
        result = AggregatedResult(kwargs.get("name") or task.name)

        pool = Pool(processes=num_workers)
        result_pool = [
            pool.apply_async(task_wrapper, args=(task, h, self)) for h in hosts
        ]
        pool.close()
        pool.join()

        for rp in result_pool:
            r = rp.get()
            result[r.host.name] = r
        return result

    def run(
        self,
        task,
        num_workers=None,
        raise_on_error=None,
        on_good=True,
        on_failed=False,
        **kwargs,
    ):
        """
        Run task over all the hosts in the inventory.

        Arguments:
            task (``callable``): function or callable that will be run against each device in
              the inventory
            num_workers(``int``): Override for how many hosts to run in parallel for this task
            raise_on_error (``bool``): Override raise_on_error behavior
            on_good(``bool``): Whether to run or not this task on hosts marked as good
            on_failed(``bool``): Whether to run or not this task on hosts marked as failed
            **kwargs: additional argument to pass to ``task`` when calling it

        Raises:
            :obj:`nornir.core.exceptions.NornirExecutionError`: if at least a task fails
              and self.config.core.raise_on_error is set to ``True``

        Returns:
            :obj:`nornir.core.task.AggregatedResult`: results of each execution
        """
        task = Task(task, **kwargs)
        self.processors.task_started(task)

        num_workers = num_workers or self.config.core.num_workers

        run_on = []
        if on_good:
            for name, host in self.inventory.hosts.items():
                if name not in self.data.failed_hosts:
                    run_on.append(host)
        if on_failed:
            for name, host in self.inventory.hosts.items():
                if name in self.data.failed_hosts:
                    run_on.append(host)

        num_hosts = len(self.inventory.hosts)
        task_name = kwargs.get("name") or task.name
        if num_hosts:
            logger.info(
                f"Running task %r with args %s on %d hosts",
                task_name,
                kwargs,
                num_hosts,
            )
        else:
            logger.warning("Task %r has not been run – 0 hosts selected", task_name)

        if num_workers == 1:
            result = self._run_serial(task, run_on, **kwargs)
        else:
            result = self._run_parallel(task, run_on, num_workers, **kwargs)

        raise_on_error = (
            raise_on_error
            if raise_on_error is not None
            else self.config.core.raise_on_error
        )  # noqa
        if raise_on_error:
            result.raise_on_error()
        else:
            self.data.failed_hosts.update(result.failed_hosts.keys())

        self.processors.task_completed(task, result)

        return result

    def dict(self):
        """ Return a dictionary representing the object. """
        return {"data": self.data.dict(), "inventory": self.inventory.dict()}

    def close_connections(self, on_good=True, on_failed=False):
        def close_connections_task(task):
            task.host.close_connections()

        self.run(task=close_connections_task, on_good=on_good, on_failed=on_failed)

    @classmethod
    def get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, cls):
            raise ValueError(f"Nornir: Nornir expected not {type(v)}")
        return v

    @property
    def state(self):
        return GlobalState


def task_wrapper(task: Task, host: Host, nr: Nornir) -> AggregatedResult:
    nr.processors.host_started(task, host)
    results = task.copy().start(host, nr)
    nr.processors.host_completed(task, host, results)
    return results
