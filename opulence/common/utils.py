from importlib import import_module
import inspect
import os
import pkgutil
import sys

def is_iterable(element):
    try:
        iter(element)
    except TypeError:
        return False
    else:
        return True


def is_list(element):
    return isinstance(element, (set, list, tuple))

def load_classes_from_module(root_path, parent_class, skip_first_level=False):

    def _discover_path(skip_first_level, path):
        for (_, name, ispkg) in pkgutil.iter_modules([path]):
            pkg_path = os.path.join(path, name)
            if ispkg:
                yield from _discover_path(False, pkg_path)
                continue
            if not skip_first_level:
                yield pkg_path.replace("/", ".")
         

    res = []
    for mod_path in _discover_path(skip_first_level, root_path):
        module = None
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

