from configapi._internals.exceptions import RegistryError
from configapi._internals.typingtools import TranslateFn, is_builtin

from typing import Any, cast
from annotationlib import get_annotations


type Registry[I, O] = dict[type[O], TranslateFn[I, O]]


_REGISTRY: Registry[Any, Any] = {}


def register[O](fn: TranslateFn[Any, O]) -> None:
    rtn: type[O] = get_annotations(fn)["return"]

    if rtn in _REGISTRY:
        raise RegistryError(rtn, _REGISTRY, f"Deserializer for type {rtn.__name__} is already registered")

    _REGISTRY[rtn] = fn


def resolve[O](cls: type[O]) -> TranslateFn[Any, O]:
    drl: TranslateFn[Any, O] | None = _REGISTRY.get(cls)

    if drl is None:
        raise RegistryError(cls, _REGISTRY, f"No deserializer registered for type {cls.__name__}")

    return drl


def pop(cls: type) -> None:
    drl: TranslateFn[Any, Any] | None = _REGISTRY.pop(cls)

    if drl is None:
        raise RegistryError(cls, _REGISTRY, f"No deserializer registered for type {cls.__name__}")


def deserialize[O](Type: type[O], obj: object) -> O:
    if is_builtin(Type):
        return cast(O, obj)

    drl: TranslateFn[object, O] = resolve(Type)

    return drl(obj)