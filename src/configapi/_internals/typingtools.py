from typing import Callable, Protocol


type TranslateFn[I, O] = Callable[[I], O]


class Declared(Protocol):
    __module__: str

def is_builtin(cls: Declared) -> bool:
    return cls.__module__ == "builtins"