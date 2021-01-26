from importlib import import_module
import inspect
import os
import pkgutil
import sys


def load_classes_from_module(root_path, parent_class, skip_first_level=False):
    skip_level = skip_first_level
    def _discover_path(path):

        for (_, name, ispkg) in pkgutil.iter_modules([path]):
            pkg_path = os.path.join(path, name)
            if ispkg:
                yield from _discover_path(pkg_path)
                continue
            if not skip_level:
                yield pkg_path.replace("/", ".")
            else:
                print("skipped", pkg_path)
        skip_level = False
         

    res = []
    for mod_path in _discover_path(root_path):
        if mod_path not in sys.modules:
            try:
                module = import_module(mod_path)
            except Exception as err:
                print(f"!!!IMPORT ERROR {err}")
        else:
            module = sys.modules[mod_path]
        for _, mod_cls in inspect.getmembers(module, inspect.isclass):
            if mod_cls.__module__.startswith(mod_path) and issubclass(
                mod_cls, parent_class
            ):
                res.append(mod_cls)
    return res

