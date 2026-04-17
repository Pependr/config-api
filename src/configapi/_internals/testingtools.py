from typing import Callable, Any

def clear_registry(registry: dict[Any, Any]) -> Callable[[Callable[[], None]], Callable[[], None]]:
    def decorator(fn: Callable[[], None]) -> Callable[[], None]:
        def wrapper() -> None:
            registry.clear()
            fn()

        return wrapper
    
    return decorator