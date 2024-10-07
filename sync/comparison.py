

from dataclasses import dataclass
from typing import Dict, Any, Optional
from sync.sync_strategy import SyncSourceStrategy
from tcx_api.components.schemas.pbx import User


@dataclass
class FieldChange():
    old: Any
    new: Any


@dataclass
class UserChangeDetail():

    field_changes: Dict[str, FieldChange]
    user_to_update: Optional[User] = None

    @property
    def Id(self):
        return self.user_to_update.Id

    @property
    def Number(self):
        return self.user_to_update.Number

    def __str__(self):
        changes = []
        for field_name, value in self.field_changes.items():
            changes.append(f"'{field_name}' from '{
                           value.old}' to '{value.new}'")
        return ', '.join(changes)


class UserComparer:
    def __init__(self, tcx_user_list: list[User], sync_source: SyncSourceStrategy):
        self.sync_source = sync_source
        self.tcx_user_list = tcx_user_list

        self.tcx_user_dict = self._index_users(users=tcx_user_list)
        self.tcx_user_keys = set(self.tcx_user_dict.keys())

        self.source_user_list = self.sync_source.get_source_users()
        self.source_user_dict = self._index_users(users=self.source_user_list)
        self.source_user_keys = set(self.source_user_dict.keys())

    def _index_users(self, users: list[User], key: str = "Number") -> dict[str, User]:
        return {getattr(user, key): user for user in users if user is not None and getattr(user, key) is not None}

    def get_user_change_details(self) -> list[UserChangeDetail]:
        user_change_details = []
        user_keys_to_compare = list(
            self.source_user_keys.intersection(self.tcx_user_keys))
        update_fields = self.sync_source.get_user_update_fields()

        for key in user_keys_to_compare:
            user_change_detail = self.compare_user(
                self.tcx_user_dict[key], self.source_user_dict[key], update_fields)
            if user_change_detail.field_changes:
                user_change_details.append(user_change_detail)

        return user_change_details

    def compare_user(self, tcx_user: User, source_user: User, update_fields: list) -> UserChangeDetail:
        updated_fields = {}
        field_changes = {}

        for field in update_fields:
            tcx_value = getattr(tcx_user, field, None)
            source_value = getattr(source_user, field, None)
            if tcx_value != source_value:
                updated_fields[field] = source_value
                field_changes[field] = FieldChange(
                    old=tcx_value, new=source_value)

        if not update_fields:
            return None

        return UserChangeDetail(user_to_update=User(**(tcx_user.model_dump() | updated_fields)), field_changes=field_changes)

    def get_users_to_create(self) -> list[User]:
        # Determine users to create
        user_keys_to_create = list(self.source_user_keys - self.tcx_user_keys)
        users_to_create = [self.source_user_dict[k] for k in list(
            set(self.source_user_dict).intersection(user_keys_to_create))]
        users_to_create.sort(key=lambda x: x.Number)
        return users_to_create
