class RegistryError[K, V](Exception):
    def __init__(self, key: K, registry: dict[K, V], message: str) -> None:
        self.key = key
        self.registry = registry
        self.message = message
        super().__init__(message)