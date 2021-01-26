from config import agent_config

from opulence.common.base_collector import BaseCollector
from opulence.common.utils import load_classes_from_module
from opulence.common.exceptions import InvalidCollectorDefinition
from opulence.common.celery import create_app

def load_collectors():
    collector_modules = load_classes_from_module("opulence/agent/collectors", BaseCollector)
    collector_instances = {}
    for collector in collector_modules:
        collector_instance = collector()
        collector_name = collector_instance.config.name
        if collector_name in collector_instances:
            raise InvalidCollectorDefinition(f"Found collector with duplicate name `{collector_name}`.")
        collector_instances[collector_name] = {"instance": collector_instance, "active": False}   
    for collector_name in set(agent_config.collectors):
        if collector_name not in collector_instances:
            raise InvalidCollectorDefinition(f"Can't find `{collector_name}`, which is defined in the configuration file. Check your settings.yml file `collectors` section.")        
        collector_instances[collector_name]["active"] = True
    return collector_instances

COLLECTORS = load_collectors()

print(COLLECTORS)


celery_app = create_app()
celery_app.conf.update(
    {
        'collectors': {c_name: {"active": c_item["active"], "config": c_item["instance"].config.dict()} for c_name, c_item in COLLECTORS.items()},
        'task_routes': {
                'scan.*': { 'queue': 'scan', 'exchange': 'scan' }
        },
    }
)
celery_app.conf.update(agent_config.celery)

