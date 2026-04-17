# pyright: reportPrivateUsage=false
from configapi import srls
from configapi._internals.exceptions import RegistryError
from configapi._internals.testingtools import clear_registry as cr

from pytest import raises
from typing import Protocol, runtime_checkable


clear_registry = cr(srls._REGISTRY)


class Path:
    def __init__(self, path: str) -> None:
        self.path = path

    def as_posix(self) -> str:
        return self.path

class ImportPath(Path):
    def as_posix(self) -> str:
        return self.path.replace("/", ".")

@runtime_checkable
class PosixPath(Protocol):
    def as_posix(self) -> str: ...


def path_srl(path: Path) -> str:
    return path.as_posix()

def import_srl(path: ImportPath) -> str:
    return path.as_posix()

def posix_srl(path: PosixPath) -> str:
    return path.as_posix()


@clear_registry
def test_register() -> None:
    srls.register(path_srl)

    assert srls._REGISTRY.get(Path) is path_srl


@clear_registry
def test_register_error() -> None:
    srls.register(path_srl)

    with raises(RegistryError, match=f"Serializer for type {Path.__name__} is already registered"):
        srls.register(path_srl)


@clear_registry
def test_register_subclass_error() -> None:
    srls.register(path_srl)

    with raises(RegistryError, match=f"Serializer for type {Path.__name__} is already registered"):
        srls.register(import_srl)


@clear_registry
def test_register_protocol_error() -> None:
    srls.register(posix_srl)

    with raises(RegistryError, match=f"Serializer for type {PosixPath.__name__} is already registered"):
        srls.register(path_srl)

    with raises(RegistryError, match=f"Serializer for type {PosixPath.__name__} is already registered"):
        srls.register(import_srl)


@clear_registry
def test_resolve() -> None:
    srls._REGISTRY[Path] = path_srl

    assert srls.resolve(Path) is path_srl


@clear_registry
def test_resolve_subclass() -> None:
    srls._REGISTRY[Path] = path_srl

    assert srls.resolve(ImportPath) is path_srl


@clear_registry
def test_resolve_protocol() -> None:
    srls._REGISTRY[PosixPath] = posix_srl

    assert srls.resolve(Path) is posix_srl


@clear_registry
def test_resolve_error() -> None:
    with raises(RegistryError, match=f"No serializer registered for type {Path.__name__}"):
        srls.resolve(Path)


@clear_registry
def test_pop() -> None:
    srls._REGISTRY[Path] = path_srl

    srls.pop(Path)

    assert Path not in srls._REGISTRY


@clear_registry
def test_pop_subclass() -> None:
    srls._REGISTRY[Path] = path_srl

    srls.pop(ImportPath)

    assert Path not in srls._REGISTRY


@clear_registry
def test_pop_protocol() -> None:
    srls._REGISTRY[PosixPath] = posix_srl

    srls.pop(Path)

    assert PosixPath not in srls._REGISTRY

    srls._REGISTRY[PosixPath] = posix_srl

    srls.pop(ImportPath)

    assert PosixPath not in srls._REGISTRY


@clear_registry
def test_pop_error() -> None:
    with raises(RegistryError, match=f"No serializer registered for type {Path.__name__}"):
        srls.pop(Path)


@clear_registry
def test_serialize() -> None:
    srls.register(path_srl)

    p = Path("config.json")
    
    assert srls.serialize(p) == "config.json"