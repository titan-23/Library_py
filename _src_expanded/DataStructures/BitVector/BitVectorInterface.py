from abc import ABC, abstractmethod

class BitVectorInterface(ABC):

  @abstractmethod
  def access(self, k: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def __getitem__(self, k: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def rank0(self, r: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def rank1(self, r: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def rank(self, r: int, v: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def select0(self, k: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def select1(self, k: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def select(self, k: int, v: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def __len__(self) -> int:
    raise NotImplementedError

  @abstractmethod
  def __str__(self) -> str:
    raise NotImplementedError

  @abstractmethod
  def __repr__(self) -> str:
    raise NotImplementedError


