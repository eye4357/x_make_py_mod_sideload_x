"""Small sideloader utility.

Provides `x_cls_make_py_mod_sideload_x` which can load a python module from an
arbitrary path (for example a local site-packages directory), return the
module or a named attribute from it, and in the case of classes instantiate
them automatically (no-arg constructor).

API:
  x_cls_make_py_mod_sideload_x().run(base_path, module, obj=None) -> Any

Parameters:
  - base_path: directory that contains the package/module (required)
  - module: one of:
      * absolute path to a .py file
      * a filename ("mod.py") relative to base_path
      * a dotted name like "package.module" which resolves to
        base_path/package/module.py
      * a package name (will load package/__init__.py if present)
  - obj: optional attribute name inside the module to return

Behavior:
  - If obj is None the module object is returned.
  - If obj is provided the attribute is returned. If the attribute is a
    class, an instance will be constructed with no arguments and returned.

This module is implementation-light and deliberately permissive to make it
useful for ad-hoc sideloading during development or packaging workflows.

To get the module object:
mod = loader.run(r"C:\\path\\to\\site-packages", "x_make_yahw_x")
then call attribute/class manually:
inst = mod.x_cls_make_yahw_x() 
print(inst.run()) # -> "Hello world!"
To get an instantiated class directly:
inst2 = loader.run(r"C:\\path\\to\\site-packages", "x_make_yahw_x.x_cls_make_yahw_x", "x_cls_make_yahw_x") 
print(inst2.run()) # -> "Hello world!"

"""

import importlib.util
import inspect
import os
from typing import Any, Optional


class x_cls_make_py_mod_sideload_x:
    """Load a python module from a path and return the module or a named
    attribute from it. See module docstring for details.
    """

    def run(self, base_path: str, module: str, obj: Optional[str] = None) -> Any:
        """Load and return the requested object.

        base_path: directory where packages/modules live
        module: see module-level docstring for supported forms
        obj: attribute name inside the module (optional)
        """
        if not base_path:
            raise ValueError("base_path must be a non-empty string")

        if not os.path.isdir(base_path) and not os.path.isfile(base_path):
            raise FileNotFoundError(f"base_path does not exist: {base_path}")

        # Resolve module_file according to supported input shapes
        module_file = None

        # If module is an absolute path to a file, use it directly.
        if os.path.isabs(module) and os.path.isfile(module):
            module_file = module

        # If module looks like a filename (ends with .py) -> relative to base_path
        elif module.endswith(".py"):
            candidate = os.path.join(base_path, module)
            if os.path.isfile(candidate):
                module_file = candidate

        # If module is dotted (package.module) -> base_path/package/module.py
        elif "." in module:
            pkg_parts = module.split(".")
            *pkg_dirs, mod_name = pkg_parts
            candidate = os.path.join(base_path, *pkg_dirs, f"{mod_name}.py")
            if os.path.isfile(candidate):
                module_file = candidate

        else:
            # Try module.py inside base_path
            candidate = os.path.join(base_path, f"{module}.py")
            if os.path.isfile(candidate):
                module_file = candidate
            else:
                # Try package __init__.py
                pkg_init = os.path.join(base_path, module, "__init__.py")
                if os.path.isfile(pkg_init):
                    module_file = pkg_init

        if module_file is None or not os.path.isfile(module_file):
            raise ImportError(f"Cannot resolve module file for module={module} under base_path={base_path}")

        unique_name = f"sideload_{os.path.splitext(os.path.basename(module_file))[0]}_{abs(hash(module_file)) & 0xffffffff}"
        spec = importlib.util.spec_from_file_location(unique_name, module_file)
        if spec is None or spec.loader is None:
            raise ImportError(f"Failed to create module spec for {module_file}")

        mod = importlib.util.module_from_spec(spec)
        # Execute the module in its own namespace
        spec.loader.exec_module(mod)  # type: ignore[attr-defined]

        # Return module or requested attribute
        if obj is None:
            return mod

        if not hasattr(mod, obj):
            raise AttributeError(f"Module loaded from {module_file} has no attribute {obj!r}")

        attr = getattr(mod, obj)
        # If it's a class, instantiate it without args. Otherwise return as-is.
        if inspect.isclass(attr):
            try:
                return attr()
            except Exception as exc:  # pragma: no cover - surface runtime errors
                raise RuntimeError(f"Failed to instantiate class {obj!r}: {exc}") from exc

        return attr


if __name__ == "__main__":
    # Small CLI for manual testing: args -> base_path module [object]
    import sys

    if len(sys.argv) < 3:
        print("Usage: fo.py <base_path> <module> [object]")
        print("Examples:")
        print(r"  fo.py C:\\...\\site-packages x_make_yahw_x.x_cls_make_yahw_x x_cls_make_yahw_x")
        raise SystemExit(2)

    base_path = sys.argv[1]
    module = sys.argv[2]
    obj = sys.argv[3] if len(sys.argv) > 3 else None

    loader = x_cls_make_py_mod_sideload_x()
    res = loader.run(base_path, module, obj)
    print("Loaded:", repr(res))


# Backwards / packaging-friendly alias the user requested when publishing
# as `xmakepymodsideloadx` so consumers can `from xmakepymodsideloadx import
# xclsmakepymodsideloadx` (no underscores).
xclsmakepymodsideloadx = x_cls_make_py_mod_sideload_x

__all__ = ["x_cls_make_py_mod_sideload_x", "xclsmakepymodsideloadx"]

