"""Minimal sideload helper with typed sideload interface."""

from __future__ import annotations

import importlib.util
import inspect
import os
from importlib.machinery import ModuleSpec
from importlib.util import spec_from_file_location
from types import ModuleType
from typing import Any, Protocol


# Legacy-compatible entry point
def _resolve_module_file(base_path: str, module: str) -> str:
    if not base_path:
        raise ValueError("base_path must be a non-empty string")

    if not os.path.isdir(base_path) and not os.path.isfile(base_path):
        raise FileNotFoundError(f"base_path does not exist: {base_path}")

    if os.path.isabs(module) and os.path.isfile(module):
        return module

    if module.endswith(".py"):
        candidate = os.path.join(base_path, module)
        if os.path.isfile(candidate):
            return candidate

    if "." in module:
        parts = module.split(".")
        *pkg, mod = parts
        candidate = os.path.join(base_path, *pkg, f"{mod}.py")
        if os.path.isfile(candidate):
            return candidate

    candidate = os.path.join(base_path, f"{module}.py")
    if os.path.isfile(candidate):
        return candidate

    init = os.path.join(base_path, module, "__init__.py")
    if os.path.isfile(init):
        return init

    msg = (
        "Cannot resolve module file for "
        f"module={module} under base_path={base_path}"
    )
    raise ImportError(msg)


def _create_spec(module_file: str) -> ModuleSpec:
    spec = spec_from_file_location(
        f"sideload_{abs(hash(module_file))}",
        module_file,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create module spec for {module_file}")
    return spec


def _load_module(base_path: str, module: str) -> ModuleType:
    module_file = _resolve_module_file(base_path, module)
    spec = _create_spec(module_file)
    module_obj = importlib.util.module_from_spec(spec)
    assert isinstance(module_obj, ModuleType)
    loader = spec.loader
    assert loader is not None
    loader.exec_module(module_obj)
    return module_obj


def _get_attribute(module_obj: ModuleType, attr_name: str) -> Any:
    if not hasattr(module_obj, attr_name):
        raise AttributeError(
            "Module loaded from "
            f"{getattr(module_obj, '__file__', '<unknown>')}"
            f" has no attribute {attr_name!r}"
        )

    attr = getattr(module_obj, attr_name)
    if inspect.isclass(attr):
        return attr()
    return attr


class ModuleLoader(Protocol):
    def load_module(self, base_path: str, module: str) -> ModuleType: ...

    def get_attribute(self, module_obj: ModuleType, attr_name: str) -> Any: ...


class DefaultModuleLoader:
    def load_module(self, base_path: str, module: str) -> ModuleType:
        return _load_module(base_path, module)

    def get_attribute(self, module_obj: ModuleType, attr_name: str) -> Any:
        return _get_attribute(module_obj, attr_name)


class PyModuleSideload:
    """Utility class that sideloads Python modules safely."""

    def __init__(self, module_loader: ModuleLoader | None = None) -> None:
        self._module_loader: ModuleLoader = module_loader or DefaultModuleLoader()

    def run(self, base_path: str, module: str, obj: str | None = None) -> Any:
        module_obj = self._module_loader.load_module(base_path, module)
        if obj is None:
            return module_obj
        return self._module_loader.get_attribute(module_obj, obj)


class x_cls_make_py_mod_sideload_x(PyModuleSideload):
    def run(self, base_path: str, module: str, obj: str | None = None) -> Any:
        """Load a module file under base_path and return module or attribute.

        base_path: directory containing modules or packages
        module: a filename (foo.py), a dotted name (pkg.mod) or a module name
        obj: optional attribute name to return from the module
        """
        return super().run(base_path, module, obj)


# Packaging-friendly alias
xclsmakepymodsideloadx = x_cls_make_py_mod_sideload_x

__all__ = ["PyModuleSideload", "x_cls_make_py_mod_sideload_x", "xclsmakepymodsideloadx"]
