from importlib import import_module
import inspect
import os
import pkgutil
import sys


def load_classes_from_module(mod_path, base_mod):
    res = []
    def _discover_path(path):
        for (_, name, ispkg) in pkgutil.iter_modules([path]):
            pkg_path = os.path.join(path, name)
            if ispkg:
                yield from _discover_path(pkg_path)
                continue
            yield pkg_path.replace("/", ".")

    for mod_path in _discover_path(mod_path):
        if mod_path not in sys.modules:
            try:
                module = import_module(mod_path)
            except Exception as err:
                print(f"!!!IMPORT ERROR {err}")
        else:
            module = sys.modules[mod_path]
        for _, mod_cls in inspect.getmembers(module, inspect.isclass):
            if mod_cls.__module__.startswith(mod_path) and issubclass(
                mod_cls, base_mod
            ):
                res.append(mod_cls)
    return res

