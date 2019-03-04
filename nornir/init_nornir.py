from typing import Any, Callable, Dict

from nornir.core import Nornir
from nornir.core.connections import Connections
from nornir.core.deserializer.configuration import Config
from nornir.core.state import GlobalState
from nornir.plugins.connections.napalm import Napalm
from nornir.plugins.connections.netmiko import Netmiko
from nornir.plugins.connections.paramiko import Paramiko


def register_default_connection_plugins() -> None:
    Connections.register("napalm", Napalm)
    Connections.register("netmiko", Netmiko)
    Connections.register("paramiko", Paramiko)


def cls_to_string(cls: Callable[..., Any]) -> str:
    return f"{cls.__module__}.{cls.__name__}"


def InitNornir(
    config_file: str = "",
    deep_merge: bool = False,
    dry_run: bool = False,
    configure_logging: bool = True,
    **kwargs: Dict[str, Any],
) -> Nornir:
    """
    Arguments:
        config_file(str): Path to the configuration file (optional)
        deep_merge(bool): Whether to merge config file settings and
            `kwarg` parameters (true) or replace config file with
            `kwarg` patameters (false, default)
        dry_run(bool): Whether to simulate changes or not
        **kwargs: Extra information to pass to the
            :obj:`nornir.core.configuration.Config` object

    Returns:
        :obj:`nornir.core.Nornir`: fully instantiated and configured
    """
    register_default_connection_plugins()

    if callable(kwargs.get("inventory", {}).get("plugin", "")):
        kwargs["inventory"]["plugin"] = cls_to_string(kwargs["inventory"]["plugin"])

    if callable(kwargs.get("inventory", {}).get("transform_function", "")):
        kwargs["inventory"]["transform_function"] = cls_to_string(
            kwargs["inventory"]["transform_function"]
        )

    conf = Config.load_from_file(config_file, deep_merge=deep_merge, **kwargs)

    data = GlobalState(dry_run=dry_run)

    if configure_logging:
        conf.logging.configure()

    inv = conf.inventory.plugin.deserialize(
        transform_function=conf.inventory.transform_function,
        transform_function_options=conf.inventory.transform_function_options,
        config=conf,
        **conf.inventory.options,
    )

    return Nornir(inventory=inv, config=conf, data=data)
