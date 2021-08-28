from dataclasses import dataclass

from seedwork.application import BaseModel
from seedwork.domain import Entity


@dataclass
class Account(Entity):
    username: str
    password: str


class AccountReadModel(BaseModel):
    id: str
    username: str


class TestModel:
    def test_entity_to_model(self) -> None:
        account = Account(username='user', password='password')

        model = AccountReadModel.from_entity(account)

        assert model.username == 'user'
        assert not hasattr(model, 'password')
