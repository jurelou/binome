from opulence.agent.collectors.base import BaseCollector
from opulence.agent.collectors.exceptions import InvalidCollectorDefinition
from opulence.common.utils import load_classes_from_module
from opulence.config import agent_config


def load_collectors():
    collector_modules = load_classes_from_module(
        root_path="opulence/agent/collectors",
        parent_class=BaseCollector,
        skip_first_level=True,
    )
    collector_instances = {}
    for collector in collector_modules:
        collector_instance = collector()
        collector_name = collector_instance.config.name
        if collector_name in collector_instances:
            raise InvalidCollectorDefinition(
                f"Found collector with duplicate name `{collector_name}`."
            )
        collector_instances[collector_name] = {
            "instance": collector_instance,
            "active": False,
        }
    for collector_name in set(agent_config.collectors or []):
        if collector_name not in collector_instances:
            raise InvalidCollectorDefinition(
                f"Can't find `{collector_name}`, which is defined in the configuration file. Check your settings.yml file `collectors` section."
            )
        collector_instances[collector_name]["active"] = True

    return collector_instances


all_collectors = load_collectors()
