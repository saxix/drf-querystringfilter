import importlib
import pkgutil

import drf_querystringfilter as package


def test_imports():
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        current_module = '{}.{}'.format(package.__name__, modname)
        m = importlib.import_module(current_module)
        if hasattr(m, '__path__'):
            for _, sub_mod, __ in pkgutil.iter_modules(m.__path__):
                sub_module = '{}.{}'.format(current_module, sub_mod)
                sm = importlib.import_module(sub_module)
                if hasattr(sm, '__path__'):
                    for _, s_sub_mod, __ in pkgutil.iter_modules(sm.__path__):
                        s_sub_mod = '{}.{}.{}'.format(current_module, sub_mod, s_sub_mod)
                        try:
                            importlib.import_module(s_sub_mod)
                        except Exception as e:  # pragma: no cover
                            raise Exception(f"""Error importing '{s_sub_mod}'.
    {e}
    """)
