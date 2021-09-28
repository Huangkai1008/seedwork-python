import uuid
from dataclasses import dataclass, field
from typing import Any, Union

from typing_extensions import TypeAlias

EntityId: TypeAlias = Union[int, str]


__all__ = ['EntityId', 'Entity']


@dataclass
class Entity:
    """Entity base class.

    Attributes:
        id: Unique identifier of the entity.

    See Also:
        - https://enterprisecraftsmanship.com/posts/entity-base-class/

    """

    id: EntityId = field(init=False)

    def __post_init__(self) -> None:
        self.id = self.next_id()

    @classmethod
    def next_id(cls) -> EntityId:
        return str(uuid.uuid4())

    def __eq__(self, other: Any) -> bool:
        return other.__class__ is self.__class__ and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
