from abc import ABC, abstractmethod
from typing import Optional
from threecxapi.components.schemas.pbx import Group, User
from sync.logging import SyncLogger


class SyncSourceStrategy(ABC):
    @property
    @abstractmethod
    def mapping(self): ...

    def __init__(self, logger: SyncLogger):
        self.logger = logger

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def get_source_users(self) -> Optional[list[User]]: ...

    @abstractmethod
    def get_source_groups(self) -> Optional[list[Group]]: ...

    @abstractmethod
    def get_user_update_fields(self) -> list: ...
