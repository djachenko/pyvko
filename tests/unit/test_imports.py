import importlib
import pkgutil

import pytest

import pyvko

MODULES = [module.name for module in pkgutil.walk_packages(pyvko.__path__, "pyvko.")]


@pytest.mark.parametrize("module_name", MODULES)
def test_module_imports(module_name: str) -> None:
    importlib.import_module(module_name)
