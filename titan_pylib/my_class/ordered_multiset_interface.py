from titan_pylib.my_class.supports_less_than import SupportsLessThan
from abc import ABC, abstractmethod
from typing import Iterable, Optional, Iterator, TypeVar, Generic

T = TypeVar("T", bound=SupportsLessThan)


class OrderedMultisetInterface(ABC, Generic[T]):

    @abstractmethod
    def __init__(self, a: Iterable[T]) -> None:
        raise NotImplementedError

    @abstractmethod
    def add(self, key: T, cnt: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def discard(self, key: T, cnt: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def discard_all(self, key: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    def count(self, key: T) -> int:
        raise NotImplementedError

    @abstractmethod
    def remove(self, key: T, cnt: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def le(self, key: T) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def lt(self, key: T) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def ge(self, key: T) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def gt(self, key: T) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def get_max(self) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def get_min(self) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def pop_max(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def pop_min(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def tolist(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterator:
        raise NotImplementedError

    @abstractmethod
    def __next__(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, key: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __bool__(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError
