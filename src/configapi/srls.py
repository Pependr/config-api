from configapi._internals.exceptions import RegistryError
from configapi._internals.typingtools import TranslateFn, is_builtin

from typing import Any
from annotationlib import get_annotations


type Registry[I, O] = dict[type[I], TranslateFn[I, O]]


_REGISTRY: Registry[Any, Any] = {}


def register(fn: TranslateFn[Any, Any]) -> None:
    inp, _ = get_annotations(fn).values()

    for key in _REGISTRY:
        if issubclass(inp, key):
            raise RegistryError(inp, _REGISTRY, f"Serializer for type {key.__name__} is already registered")

    _REGISTRY[inp] = fn


def resolve[I](cls: type[I]) -> TranslateFn[I, Any]:
    for key in _REGISTRY:
        if issubclass(cls, key):
            return _REGISTRY[key]
    else:
        raise RegistryError(cls, _REGISTRY, f"No serializer registered for type {cls.__name__}")


def pop(cls: type) -> None:
    for key in _REGISTRY:
        if issubclass(cls, key):
            _REGISTRY.pop(key)
            return
    else:
        raise RegistryError(cls, _REGISTRY, f"No serializer registered for type {cls.__name__}")


def serialize(obj: object) -> Any:
    Type: type = type(obj)
    
    if is_builtin(Type):
        return obj
    
    srl: TranslateFn[object, Any] = resolve(Type)

    return srl(obj)
