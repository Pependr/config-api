# pyright: reportPrivateUsage=false
from configapi import drls
from configapi._internals.exceptions import RegistryError
from configapi._internals.testingtools import clear_registry as cr

from pytest import raises


clear_registry = cr(drls._REGISTRY)


class Path:
    def __init__(self, path: str) -> None:
        self.path = path

    def as_posix(self) -> str:
        return self.path

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Path):
            raise ValueError(f"Unsupported operand between types Path and {type(value).__name__}")

        return self.path == value.path

def to_path(string: str) -> Path:
    return Path(string)


@clear_registry
def test_register() -> None:
    drls.register(to_path)

    assert drls._REGISTRY.get(Path) is to_path


@clear_registry
def test_register_error() -> None:
    drls.register(to_path)

    with raises(RegistryError, match=f"Deserializer for type {Path.__name__} is already registered"):
        drls.register(to_path)


@clear_registry
def test_resolve() -> None:
    drls._REGISTRY[Path] = to_path

    assert drls.resolve(Path) is to_path


@clear_registry
def test_resolve_error() -> None:
    with raises(RegistryError, match=f"No deserializer registered for type {Path.__name__}"):
        drls.resolve(Path)


@clear_registry
def test_pop() -> None:
    drls._REGISTRY[Path] = to_path

    drls.pop(Path)

    assert Path not in drls._REGISTRY


@clear_registry
def test_pop_error() -> None:
    with raises(RegistryError, match=f"No deserializer registered for type {Path.__name__}"):
        drls.pop(Path)


@clear_registry
def test_deserialize() -> None:
    drls.register(to_path)

    assert drls.deserialize(Path, "config.json") == Path("config.json")