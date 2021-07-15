from dataclasses import FrozenInstanceError, dataclass
from typing import Optional, TypeVar, Union

import pytest

from seedwork.domain.value_object import ValueObject


@dataclass(frozen=True)
class ValueObjectA(ValueObject):
    field: int


@dataclass(frozen=True)
class ValueObjectB(ValueObject):
    field: int


VO = TypeVar('VO', bound=Union[ValueObjectA, ValueObjectB])


class TestValueObject:
    @pytest.mark.parametrize(
        'vo1,vo2',
        [
            pytest.param(
                None,
                None,
                id='both null',
            ),
            pytest.param(
                ValueObjectA(1),
                ValueObjectA(1),
                id='equal members',
            ),
        ],
    )
    def test_value_objects_are_equal(
        self, vo1: Optional[VO], vo2: Optional[VO]
    ) -> None:
        equality: bool = vo1 == vo2

        assert equality is True

    @pytest.mark.parametrize(
        'vo1,vo2',
        [
            pytest.param(
                ValueObjectA(1),
                ValueObjectA(2),
                id='different member values',
            ),
            pytest.param(
                ValueObjectA(1),
                ValueObjectB(1),
                id='different types',
            ),
        ],
    )
    def test_value_objects_are_not_equal(
        self,
        vo1: Optional[VO],
        vo2: Optional[VO],
    ) -> None:
        equality: bool = vo1 == vo2

        assert equality is False

    def test_value_objects_are_immutable(self) -> None:
        vo = ValueObjectA(1)

        with pytest.raises(FrozenInstanceError):
            vo.field = 2  # type: ignore  # noqa
