"""Tests for the Python module sideload helper."""

from __future__ import annotations

from pathlib import Path

import pytest

from x_make_py_mod_sideload_x.x_cls_make_py_mod_sideload_x import (
    PyModuleSideload,
    x_cls_make_py_mod_sideload_x,
)


def write_module(base: Path, module: str, content: str) -> Path:
    path = base / f"{module}.py"
    path.write_text(content)
    return path


def test_run_returns_module(tmp_path: Path) -> None:
    module_dir = tmp_path / "modules"
    module_dir.mkdir()
    write_module(
        module_dir,
        "sample",
        """
VALUE = 42
""".strip(),
    )

    sideload = x_cls_make_py_mod_sideload_x()
    module_obj = sideload.run(str(module_dir), "sample")

    assert getattr(module_obj, "VALUE", None) == 42


def test_run_returns_attribute_instance(tmp_path: Path) -> None:
    module_dir = tmp_path / "modules"
    module_dir.mkdir()
    write_module(
        module_dir,
        "provider",
        """
class Thing:
    def __init__(self) -> None:
        self.value = "hello"
""".strip(),
    )

    module_sideload = PyModuleSideload()
    instance = module_sideload.run(str(module_dir), "provider", "Thing")

    assert getattr(instance, "value", None) == "hello"


def test_missing_attribute_raises(tmp_path: Path) -> None:
    module_dir = tmp_path / "modules"
    module_dir.mkdir()
    write_module(
        module_dir,
        "has_func",
        """
def ping() -> str:
    return "pong"
""".strip(),
    )

    sideload = PyModuleSideload()

    with pytest.raises(AttributeError):
        sideload.run(str(module_dir), "has_func", "Thing")
