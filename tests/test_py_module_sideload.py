"""Tests for the Python module sideload helper."""

from __future__ import annotations

from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, cast

from x_make_py_mod_sideload_x import (
    PyModuleSideload,
    x_cls_make_py_mod_sideload_x,
)

if TYPE_CHECKING:
    from pathlib import Path
    from types import TracebackType


class ExpectationError(AssertionError):
    """Raised when an expectation helper fails."""


class _ExpectRaises(AbstractContextManager[None]):
    def __init__(self, expected: type[BaseException]) -> None:
        self._expected = expected

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if exc_type is None:
            message = f"Expected {self._expected.__name__}"
            raise ExpectationError(message)
        if not issubclass(exc_type, self._expected):
            return False
        return exc is None or isinstance(exc, self._expected)


def expect_raises(exc_type: type[BaseException]) -> _ExpectRaises:
    return _ExpectRaises(exc_type)


def expect_equal(actual: object, expected: object, *, label: str | None = None) -> None:
    if actual == expected:
        return
    prefix = f"{label}: " if label else ""
    message = f"{prefix}Expected {expected!r}, got {actual!r}"
    raise ExpectationError(message)


def write_module(base: Path, module: str, content: str) -> Path:
    path = base / f"{module}.py"
    path.write_text(content)
    return path


def test_run_returns_module(tmp_path: Path) -> None:
    module_dir = tmp_path / "modules"
    module_dir.mkdir()
    expected_value = 42
    write_module(
        module_dir,
        "sample",
        """
VALUE = 42
""".strip(),
    )

    sideload = x_cls_make_py_mod_sideload_x()
    module_obj = sideload.run(str(module_dir), "sample")

    actual_value = cast("int | None", getattr(module_obj, "VALUE", None))
    expect_equal(actual_value, expected_value, label="module VALUE")


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

    actual_value = cast("str | None", getattr(instance, "value", None))
    expect_equal(actual_value, "hello", label="Thing.value")


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

    with expect_raises(AttributeError):
        sideload.run(str(module_dir), "has_func", "Thing")


def test_invalid_base_path_raises_file_not_found() -> None:
    sideload = PyModuleSideload()

    with expect_raises(FileNotFoundError):
        sideload.run("/does/not/exist", "some_module")


def test_missing_module_file_raises(tmp_path: Path) -> None:
    module_dir = tmp_path / "modules"
    module_dir.mkdir()

    sideload = PyModuleSideload()

    with expect_raises(ImportError):
        sideload.run(str(module_dir), "not_there")


def test_run_accepts_pathlike_base(tmp_path: Path) -> None:
    module_dir = tmp_path / "modules"
    module_dir.mkdir()
    write_module(
        module_dir,
        "pathish",
        """
VALUE = "pathlike"
""".strip(),
    )

    sideload = PyModuleSideload()
    module_obj = sideload.run(module_dir, "pathish")

    value = cast("str | None", getattr(module_obj, "VALUE", None))
    expect_equal(value, "pathlike", label="VALUE")


def test_run_supports_dotted_module_name(tmp_path: Path) -> None:
    module_dir = tmp_path / "modules"
    package_dir = module_dir / "pkg"
    package_dir.mkdir(parents=True)
    write_module(package_dir, "__init__", "\n# package marker\n".strip())
    write_module(
        package_dir,
        "inner",
        """
VALUE = "pkg.inner"
""".strip(),
    )

    sideload = PyModuleSideload()
    module_obj = sideload.run(str(module_dir), "pkg.inner")

    value = cast("str | None", getattr(module_obj, "VALUE", None))
    expect_equal(value, "pkg.inner", label="VALUE")
